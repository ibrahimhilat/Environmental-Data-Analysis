# Dr. Ahmad Al-Wahidi Clinic — Surgical Hero

Reworked Elementor hero section, designed against the `ui-ux-pro-max` skill's
verified data (`--design-system` for medical clinic, `--domain landing`,
`--domain ux`, `--domain color`, `--domain typography`).

## Files

| File | Where it goes |
|---|---|
| `hero-section.html` | Elementor **HTML widget** |
| `doctor-portrait.html` | A second Elementor **HTML widget** — style and markup in one block |
| `hero-section.css` | The widget's **Advanced ▸ Custom CSS** panel |
| `hero-section.preview.html` | Standalone build for local checking — not for WordPress |

`hero-section.preview.html` is generated, not hand-edited. Regenerate it after changing either part:

```sh
{ echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}';
  sed -E 's/(^|[[:space:]])selector([[:space:]*{])/\1.elw-scope\2/g' hero-section.css;
  echo '</style><div class="elw-scope">'; cat hero-section.html; echo '</div>'; } > hero-section.preview.html
```

## Before going live

Three `[[REPLACE]]` markers in `hero-section.html`:

- `tel:+96265000000` — the clinic's real number
- `JMC Reg. 00000` — Jordan Medical Council registration number
- Optionally set `--elw-hero-photo` in the CSS to a real operating-theatre photograph

## The brand palette

The brand blue is **`#2E9CC5`**. Measured, it is **3.14:1 on white** — below the 4.5:1
floor — so it cannot carry small text, and a white-on-brand button fails at the same
3.14:1. Using it directly for the CTA would have reintroduced the defect this rework
removed.

So the whole blue family is derived from **the brand's own hue (196.3°)** at different
lightness steps. Every token below is visibly the same blue as `#2E9CC5`, and each one
passes where it is used:

| Token | Value | Contrast | Used for |
|---|---|---|---|
| `--elw-primary` | `#2E9CC5` | 3.14:1 on white | Fills, rules, the specialty bar, large marks — **never small text** |
| `--elw-primary-deep` | `#1F6984` | 6.15:1 on white | Icons, index numbers, tick rule, tertiary link |
| `--elw-cta` | `#19556B` | 8.23:1 with white | Primary button, focus ring |
| `--elw-cta-hover` | `#103846` | 12.53:1 with white | Primary button hover |
| `--elw-soft-blue` | `#83C8E2` | tint | Title highlight bar only |
| `--elw-accent` | `#F59327` | 6.29:1 on ink | The primary action's hover icon, nothing else |

To rebrand later, change `--elw-primary` and re-derive the rest at the same hue —
lightness 32% / 26% / 17% / 70%.

## What changed and why

### Accessibility (the blocking defects)

- **`--elw-neutral: #969696` failed WCAG.** It was 2.85:1 on white — the skill's
  contrast rule names `#999 on white (2.8:1)` as its bad example verbatim. It carried
  the `__row-label` and `__clinical-line` text. Replaced with a three-step ink scale:
  `--elw-ink #0A2C3F` (14.5:1), `--elw-body #3C5666` (7.7:1), `--elw-meta #55707F` (5.2:1).
- Measured result: **0 contrast failures across 44 text nodes; lowest ratio 5.24:1.**
- Smallest type raised from 10px to 11px, and body/footnote to a 12px floor.
- Added `prefers-reduced-transparency` (the liquid-glass checklist calls for it) and
  `prefers-contrast: more` — both drop the glass to solid white with a steel border.
- Added `@media (hover: none)` so coarse pointers get no hover-only affordances.
- Every interactive element now shares one 3px focus ring; all targets are ≥52px tall.

### Visual direction — from wellness-spa to surgical practice

The `trust-authority-conversion` pattern specifies *"Navy/Grey corporate. Trust blue.
**Accent for CTA only.**"* The original inverted this:

- **The primary CTA was the palest element on the page** — `#68B7EE` with black text,
  weaker than the secondary button beside it. It is now `--elw-cta #19556B` with white
  text (8.23:1), carrying the only shadow in the composition.
- **The orange accent was spent on a decorative eyebrow dot.** It is now reserved
  entirely for the primary action's hover state, and the warm radial was removed from
  the ambient wash — that warmth was reading as spa, not theatre.
- **Title dropped from 800/4.15rem to 700/3rem** and split into a name line plus a
  subordinate positioning line. A consultant surgeon reads as restraint, not a
  product launch. `Al‑Wahidi` uses a non-breaking hyphen so the name never splits.
- Radius tightened 14px → 8px (4px on controls); monospace tabular figures on the
  index numbers, training years and registration number; the eyebrow rule is a
  measured tick scale. Precision instead of softness.

### Information architecture

- **Credentials were buried in prose and in card 02's icon rows.** Facharzt / FEBS /
  FACS / DGEM are now a scannable chip row directly under the description in card 01 —
  proof above the fold, which is what the trust pattern asks for.
- **There was no phone number anywhere.** For a clinic, calling *is* a conversion path.
  Added a `tel:` secondary action, and demoted "Review surgical services" to a text
  link so three actions do not compete at equal weight.
- **Practice locations moved from card 01 to card 02.** Card 01 was overloaded while
  card 02 ended in dead space; card 01 is now the offer and the action, card 02 the
  record and the locations.
- Card 02's credential list became a dated ledger (year column + entry) rather than
  three icon rows, which reads as a surgical CV.
- Added a registration-number slot on the clinical line — the strongest single trust
  signal a clinic hero can carry.

### Correctness and performance

- **`font-family: Inter` was declared but never loaded**, so the page fell back to an
  arbitrary system sans. Now loads **Figtree + Noto Sans** (the skill's "Medical Clean"
  pairing) via `<link>` in the HTML widget — Elementor's Custom CSS panel cannot host
  an `@import`, which must be first in a stylesheet.
- `backdrop-filter: blur(32px)` → `22px`. Visually identical at this scale, cheaper to
  composite, and there are three blurred surfaces on screen at once.
- **The reveal script could leave the hero permanently invisible** if the
  IntersectionObserver never fired (Elementor preview re-parenting, an already-scrolled
  load). Added a 1200 ms failsafe that shows the section regardless. A hero that starts
  at `opacity: 0` must never depend on a single observer.
- Figures are a `<ul>` with a label instead of anonymous `<div>`s; the arrow glyph
  `↗` is now an SVG, per the skill's no-glyph-icons rule.
- Removed the dead `.elw-hero-figures__surface` rules left over from the old markup.

## Verified

- 1440 / 900 / 390 px: no horizontal overflow, no console errors
- Contrast audit: 0 failures, lowest 5.24:1
- Touch targets: 54, 54, 52, 80 px tall
- `prefers-contrast: more` and `prefers-reduced-motion` render correctly


---

## `doctor-portrait.html` — the caption that would not show

The overlay caption rendered at `display: none` and `0×0`.

`display` was the one property the CSS never set. Themes commonly ship
`figcaption { display: none }`, and with nothing to oppose it that rule won
outright — every *other* property carried `!important`, which is why the symptom
looked like a z-index or positioning fault when it was neither.

The fix states `display` / `visibility` / `opacity` explicitly and scopes every
selector to `.custom-doctor-image-wrap`, so the rules outrank even a bare
`figcaption { ... !important }` coming from the theme.

Verified against nine theme rules that break overlay captions — `display:none`
(plain and `!important`), `position:static!important`, `visibility:hidden`,
`opacity:0`, `clip-path:inset(50%)`, and an `img` lifted to `z-index:99` —
asserting on **painted pixels**, not computed style: 9/9 pass, with the photo
never bleeding through the text.

Text contrast was measured end-to-end against a **pure-white photograph**, the
worst case for a dark gradient: name **8.04:1**, subtitle **8.72:1**.

Also aligned to the hero's system: brand family (`#2E9CC5` hue), Figtree/Noto
Sans instead of the unloaded `Inter`, 8px radius instead of 22px, weight 700
instead of 800, and the same brand tick rule as the hero eyebrow.
`pointer-events: none` was dropped — it blocked text selection for no benefit.


---

## `elementor/contact-hero.html` + `.css` — status instead of duplicate CTAs

The hero's WhatsApp and phone buttons duplicated card 01 of
`contact-section.html` a few hundred pixels below, which already lists
**Main Line +962 79 555 6563** and **WhatsApp 079 555 6563** as tappable rows.

**A number mismatch was found while removing them.** The hero's buttons pointed
at `962791080910` in both `href`s while *displaying* `+962795556563` — so the
call button dialled a different number than the one it showed, and its WhatsApp
link went somewhere other than the card below. Removing the buttons removes the
mismatch; the card's `962795556563` is now the single source.

In their place the hero carries the one thing the cards cannot show at a glance:
**whether the clinic is open right now**, computed in `Asia/Amman` from the same
hours card 03 publishes, plus a quiet anchor down to `#elw-contact-details`.
Colour is never the only cue — the wording itself says open or closed.

**If the opening hours change, update BOTH `contact-section.html` (card 03) and
the `HOURS` table in `contact-hero.html`.**

Verified: twelve boundary times across a full week (including Thursday 15:00
correctly rolling to Saturday over the Friday closure), no JS errors, no
horizontal overflow at 1100/390 px. Contrast 0 failures; the status pill
measures 4.84:1 open and 5.35:1 closed on its own tinted plate.

Also fixed while in the file: the title highlight used an absolutely positioned
`::after`, which stretched into one edge-to-edge bar once the line wrapped on
mobile. It is now a per-line background with `box-decoration-break: clone`.
Palette and type were brought onto the `#2E9CC5` family and Figtree/Noto Sans,
and `--elwc-neutral: #969696` (2.85:1) was retired.

---

# Health Calculator — BMI / BMR / TDEE

Arabic, RTL, two-step assessment widget. Step 01 takes height and weight and
records the BMI; step 02 adds age, biological sex and activity level, then a
modal shows BMI, BMR (Mifflin-St Jeor), TDEE and two deficit targets, with a
prefilled WhatsApp handoff.

## Files

| File | Where it goes |
|---|---|
| `health-calculator.html` | Elementor **HTML widget** (markup + script in one block) |
| `health-calculator.css` | The widget's **Advanced ▸ Custom CSS** panel |
| `health-calculator.preview.html` | Standalone build for local checking — not for WordPress |

Regenerate the preview after touching either part:

```sh
{ echo '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Al-Wahidi Health Calculator — Preview</title><style>body{margin:0;background:#fff}';
  sed -E 's/(^|[[:space:]])selector([[:space:]*{,])/\1.elw-scope\2/g' health-calculator.css;
  echo '</style></head><body><div class="elw-scope">'; cat health-calculator.html; echo '</div></body></html>'; } > health-calculator.preview.html
```

## What was broken

**The WhatsApp button did not exist.** Its opening `<a` tag was missing, so the
browser parsed `class="…" href="…" >` as *text* and printed the raw attributes
inside the modal. `[data-role="whatsapp-link"]` then resolved to `null`, and
`renderResults()` threw on `whatsappLink.href` — which also killed the BMI
gauge marker and left the results half-rendered. The tag is back, and the
message build is its own function with the number and clinic name hoisted to
`WHATSAPP_NUMBER` / `CLINIC_NAME` at the top of the script.

**The slider fill ran backwards.** The widget is RTL, so the range thumb starts
at the *right* edge and travels left as the value grows, but the track gradient
was `90deg` — painted left to right. The colour therefore drained away from the
thumb instead of trailing it. The gradient is now `to left`, with an explicit
`direction: rtl` on the input so the two agree in every browser.

**`[hidden]` lost every argument it had.** The `selector [hidden]{display:none}`
rule sat near the top of the file while `!important` declarations of
`display: inline-flex / grid / flex` came later, so later-wins source order beat
it. Three elements JS "hid" stayed on screen: the **عرض نتائجي** submit button
was visible before any choice was made, the recorded-BMI card showed its `—`
placeholders on step 01, and the modal only stayed away because of its
`visibility: hidden`. The `[hidden]` block is now the last rule in the file.

Also fixed:

- Typing in a number box clamped on every keystroke, so `1` on the way to `175`
  jumped straight to the `120` minimum. Live typing now only syncs values that
  are already in range; the clamp waits for `change`/`blur`/`Enter`, and
  `commitAll()` runs before any calculation so an uncommitted box can't leak a
  stale number into the results.
- **بدء تقييم جديد** reset the choices but left height, weight, age and the
  recorded BMI from the previous run.
- The page behind the modal scrolled freely; `body` overflow is now locked while
  it's open and restored on close.
- `closeModal()` was re-entrant — a second call restored focus to whatever the
  first had already focused.
- Sliders that were still `hidden` at init never painted their fill, so step 02's
  age track started blank until first touch.
- Firefox drew a 14 px thumb against Chrome's 22 px.
- Keyboard focus was invisible on the choice cards, the sliders and the buttons.

## Before going live

`WHATSAPP_NUMBER` at the top of the script is `962795556563` — the same number
card 03 and the hero publish. Change it in one place if the clinic's number
changes.

Verified in headless Chromium: fill tracks the thumb (value 210/220 paints blue
from the right edge to the 10 % mark, grey beyond it), the results button stays
hidden until sex and activity are chosen, BMI 26.3 / BMR 1,983 / TDEE 3,074 for
190 cm · 95 kg · 32 y · male · moderate, the WhatsApp `href` carries the full
encoded message, restart clears everything, and no console or page errors fire.
