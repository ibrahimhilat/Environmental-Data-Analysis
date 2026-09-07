"""Browser checks for <digestive-system>.

    pip install playwright && playwright install chromium
    python3 -m http.server 8731 &
    python3 web/digestive-system/test-browser.py

Set DS_URL / DS_CHROME to point elsewhere.
"""
import os, sys, tempfile
from playwright.sync_api import sync_playwright

SP = os.environ.get("DS_SHOTS", tempfile.mkdtemp(prefix="ds-shots-"))
url = os.environ.get("DS_URL", "http://127.0.0.1:8731/web/digestive-system/demo.html")
CHROME = os.environ.get("DS_CHROME")
fails = []

with sync_playwright() as pw:
    b = pw.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
    page = b.new_page(viewport={"width": 1280, "height": 1000})
    errs = []
    page.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(url)
    page.wait_for_timeout(600)

    el = page.locator("digestive-system")
    # 1. renders
    n = page.evaluate("document.querySelectorAll('digestive-system .ds-organ').length")
    print("organ groups:", n)
    if n != 7: fails.append(f"expected 7 organ groups, got {n}")
    # 2. shared defs injected once
    defs = page.evaluate("document.querySelectorAll('digestive-system defs').length")
    print("per-instance defs:", defs)
    if defs != 1: fails.append("instance should carry exactly one <defs>")
    # 3. gradients actually resolve (stroke references a live paint server)
    ok = page.evaluate("""() => {
      const p = document.querySelector('.ds-organ[data-organ=stomach] path:nth-child(2)');
      return getComputedStyle(p).fill.includes('url');
    }""")
    if not ok: fails.append("stomach gradient fill did not resolve")

    page.screenshot(path=f"{SP}/browser-default.png", full_page=False)

    # Hover/click by viewBox coordinate: the bbox centre of a hollow organ is
    # not painted, so aim at a point that actually sits on the artwork.
    def point(vx, vy):
        return page.evaluate("""([vx, vy]) => {
          const svg = document.querySelector('.ds-svg');
          const p = svg.createSVGPoint(); p.x = vx; p.y = vy;
          const q = p.matrixTransform(svg.getScreenCTM());
          return { x: q.x, y: q.y };
        }""", [vx, vy])

    # 4. hover dims the others  (830,430 = middle of the stomach body)
    pt = point(830, 430)
    page.mouse.move(pt["x"], pt["y"])
    page.wait_for_timeout(350)
    dim = page.evaluate("document.querySelectorAll('.ds-organ.is-dimmed').length")
    print("dimmed on hover:", dim)
    if dim != 6: fails.append(f"hover should dim 6 organs, dimmed {dim}")
    page.screenshot(path=f"{SP}/browser-hover.png")

    # 5. click selects + fires event
    page.evaluate("""() => { window.__ev = null;
      document.querySelector('digestive-system')
        .addEventListener('organ-select', e => window.__ev = e.detail); }""")
    pt = point(196, 1000)          # ascending colon
    page.mouse.move(pt["x"], pt["y"])
    page.mouse.click(pt["x"], pt["y"])
    page.wait_for_timeout(250)
    ev = page.evaluate("window.__ev")
    print("organ-select:", ev)
    if not ev or ev["id"] != "large-intestine": fails.append("organ-select did not fire")
    sel = el.get_attribute("selected")
    if sel != "large-intestine": fails.append(f"selected attr = {sel}")

    # 6. focus ring: keyboard yes, mouse no
    ring_mouse = page.evaluate("!document.querySelector('.ds-focus-ring').hidden")
    if ring_mouse: fails.append("focus ring shown after a mouse click")
    page.keyboard.press("Tab"); page.keyboard.press("Tab")
    page.wait_for_timeout(250)
    ring = page.evaluate("!document.querySelector('.ds-focus-ring').hidden")
    print("focus ring — mouse:", ring_mouse, "| keyboard:", ring)
    if not ring: fails.append("focus ring not shown on keyboard focus")

    # 7. labels + Arabic
    page.check("#t-labels"); page.check("#t-ar")
    page.wait_for_timeout(350)
    txt = page.evaluate("document.querySelector('.ds-label[data-organ=stomach]').textContent")
    print("arabic label:", txt)
    if txt.strip() != "المعدة": fails.append(f"arabic label wrong: {txt!r}")
    vis = page.locator('.ds-label[data-organ="stomach"]').is_visible()
    if not vis: fails.append("labels not visible with [labels]")
    page.screenshot(path=f"{SP}/browser-labels-ar.png")

    # 8. theming via custom property
    page.evaluate("""() => document.querySelector('[data-theme=violet]').click()""")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{SP}/browser-violet.png")

    # 9. API
    page.evaluate("document.querySelector('digestive-system').clear()")
    page.wait_for_timeout(150)
    if el.get_attribute("selected") is not None: fails.append("clear() left a selection")
    okd = page.evaluate("document.querySelector('digestive-system').select('duodenum')")
    if not okd or el.get_attribute("selected") != "duodenum":
        fails.append("select() failed")

    # 10. two instances share one defs sprite
    page.evaluate("""() => { const b = document.createElement('digestive-system');
      b.setAttribute('interactive', ''); document.body.append(b); }""")
    page.wait_for_timeout(300)
    ids = page.evaluate("""() => [...document.querySelectorAll('linearGradient')]
        .map(g => g.id)""")
    print("gradient ids:", ids)
    if len(set(ids)) != len(ids):
        fails.append(f"gradient ids collide across instances: {ids}")

    # 11. theming reaches the gradient stops (the whole point of per-instance defs)
    page.evaluate("""() => { const el = document.querySelector('digestive-system');
      el.style.setProperty('--ds-rim-1', '#c9a6f5');
      el.style.setProperty('--ds-rim-2', '#7a4fd8'); }""")
    page.wait_for_timeout(200)
    stop = page.evaluate("""() => getComputedStyle(
      document.querySelector('digestive-system [id^=ds-g-tube] stop')).stopColor""")
    print("themed first stop:", stop)
    if "201, 166, 245" not in stop.replace(" ", ", ").replace(",,", ","):
        if stop.replace(" ", "") not in ("rgb(201,166,245)",):
            fails.append(f"theme did not reach gradient stop: {stop}")
    black = page.evaluate("""() => getComputedStyle(
      document.querySelector('digestive-system [id^=ds-g-stomach] stop:nth-child(3)')
      ).stopColor""")
    print("stomach mid stop:", black)
    if black.replace(" ", "") in ("rgb(0,0,0)", "rgba(0,0,0,0)"):
        fails.append("stomach gradient resolved to black")

    if errs: fails.append("console errors: " + " | ".join(errs[:5]))
    b.close()

print()
print("FAILURES:", *fails, sep="\n  ") if fails else print("ALL CHECKS PASSED")
sys.exit(1 if fails else 0)
