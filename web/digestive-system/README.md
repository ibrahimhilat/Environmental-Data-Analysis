# `<digestive-system>`

An interactive, themeable digestive-tract illustration. No dependencies, no
build step — one CSS file and one ES module.

```
web/digestive-system/
  digestive-system.css   themeable stylesheet (custom properties)
  digestive-system.js    the <digestive-system> custom element
  demo.html              live demo + integration snippets
assets/
  digestive-system.svg   the same artwork as a plain file, for <img>
  digestive-system.gen.py  generator — the source of truth for all of the above
```

Everything above is generated. Edit `assets/digestive-system.gen.py`, then:

```bash
python3 assets/digestive-system.gen.py
```

## Use it

```html
<link rel="stylesheet" href="digestive-system.css">
<script type="module" src="digestive-system.js"></script>

<digestive-system interactive labels caption lang="ar"></digestive-system>
```

ES modules need a real origin — open `demo.html` through a server
(`python3 -m http.server`), not as a `file://` path.

Just want the picture? `<img src="assets/digestive-system.svg" alt="…">`.
That file carries its own styles and plain hex colours, so it also survives
rasterisers that do not implement CSS custom properties.

## Attributes

| Attribute     | Effect                                              |
| ------------- | --------------------------------------------------- |
| `interactive` | hover / focus / click highlighting, keyboard support |
| `labels`      | name chips positioned over each organ                |
| `caption`     | caption line naming the active organ                 |
| `lang="ar"`   | Arabic organ names (any other value → English)       |
| `selected`    | organ id; reflected, settable from outside           |

## API

```js
el.select('large-intestine');   // programmatic selection
el.clear();                     // drop hover + selection
el.selected;                    // 'large-intestine' | null
el.organs;                      // [{ id, en, ar, x, y }, ...]

el.addEventListener('organ-hover',  e => e.detail.id);
el.addEventListener('organ-select', e => e.detail.name);
```

Organ ids: `oesophagus`, `stomach`, `duodenum`, `small-intestine`,
`large-intestine`, `appendix`, `rectum`.

## Theming

Override any `--ds-*` property on the element or an ancestor. The two rim
colours drive the whole palette — the mid-tones are `color-mix()`ed from them,
so a two-line override recolours every organ, stomach included.

```css
digestive-system {
  --ds-rim-1: #c9a6f5;   /* light rim  */
  --ds-rim-2: #7a4fd8;   /* deep rim   */
  --ds-glow:  #b98cf5;   /* outer glow */
  --ds-dim:   0.2;       /* inactive organs */
  max-inline-size: 420px;
}
```

Each instance carries its own id-scoped `<defs>`, so two elements on one page
can use different palettes.

## Notes

- Renders in the **light DOM** on purpose, so host pages can style it with
  ordinary CSS. Inside a shadow root, import the stylesheet into that root.
- Every organ is a `role="button"`, tab-reachable, with an `aria-label` in the
  active language and a visible focus ring; `aria-pressed` tracks selection.
- Thin loops carry a transparent, wider hit stroke so they remain a usable
  pointer and touch target.
- Honours `prefers-reduced-motion` and `prefers-color-scheme`; in print,
  dimming is disabled so the whole tract stays legible.
