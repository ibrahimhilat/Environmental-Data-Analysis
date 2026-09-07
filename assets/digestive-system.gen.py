# -*- coding: utf-8 -*-
"""Build the digestive-system illustration and its drop-in web component.

One source of geometry, four outputs:

    assets/digestive-system.svg              standalone file (works in <img>)
    web/digestive-system/digestive-system.css   themeable stylesheet
    web/digestive-system/digestive-system.js    <digestive-system> element
    web/digestive-system/demo.html              usage + integration reference

Run:  python3 assets/digestive-system.gen.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web", "digestive-system")

W, H = 1070, 1440

# ===================================================================== paths
ESOPHAGUS = "M 611,-10 C 611,90 604,190 606,250 C 608,302 626,330 664,346"

STOMACH = (
    "M 656,336 "                                    # cardia
    "C 690,306 744,286 800,290 "                    # fundus
    "C 872,296 924,348 928,424 "                    # greater curvature, shoulder
    "C 932,498 898,562 838,592 "                    # greater curvature, descending
    "C 790,616 736,614 692,592 "                    # lower body
    "C 650,572 606,550 568,538 "                    # antrum, outer edge
    "C 542,530 516,520 500,508 "                    # pylorus
    "C 494,494 498,482 510,474 "                    # pylorus, rounded tip
    "C 556,488 606,506 644,522 "                    # antrum, inner edge
    "C 676,534 704,526 718,500 "                    # incisura angularis
    "C 730,472 726,428 706,390 "                    # lesser curvature
    "C 692,364 674,346 656,336 Z"
)

DUODENUM = (
    "M 504,492 C 456,480 420,506 410,554 "
    "C 397,614 424,660 476,678 "
    "C 532,698 600,688 648,704"
)

SMALL_BOWEL = (
    "M 651,700 "
    "C 578,724 500,690 452,738 "
    "C 400,790 424,856 494,856 "
    "C 558,856 602,818 656,838 "
    "C 722,862 762,908 746,962 "
    "C 730,1016 660,1024 616,988 "
    "C 566,948 588,884 532,868 "
    "C 472,851 420,902 442,958 "
    "C 462,1008 524,1018 548,1064 "
    "C 574,1112 532,1156 482,1146 "
    "C 428,1135 418,1076 470,1046 "
    "C 522,1016 596,1042 640,1082 "
    "C 676,1114 668,1178 616,1196 "
    "C 560,1214 502,1180 470,1140"
)

SMALL_EXTRA = [
    "M 700,760 C 766,778 800,840 770,890 C 744,928 692,934 664,910",
    "M 396,898 C 342,924 338,992 390,1014 C 432,1032 478,1010 486,974",
    "M 556,1162 C 620,1198 702,1176 730,1124 C 750,1086 732,1044 702,1030",
    "M 468,782 C 414,808 404,866 446,894",
    "M 592,910 C 644,896 692,920 702,960",
    "M 522,1094 C 470,1084 428,1110 426,1148",
    "M 612,616 C 668,634 706,624 736,640 C 772,660 776,706 748,724",
    "M 786,690 C 830,708 846,764 812,800 C 782,832 736,826 716,796",
    "M 358,986 C 318,1014 320,1074 362,1096 C 396,1114 436,1100 450,1072",
    "M 640,1128 C 594,1150 548,1136 522,1104",
    "M 754,996 C 800,1020 812,1084 774,1116 C 742,1144 698,1136 680,1108",
    "M 434,724 C 386,748 372,802 398,838",
    "M 386,1128 C 424,1166 486,1176 524,1152",
    "M 664,1044 C 620,1060 578,1046 560,1010",
    "M 480,932 C 528,908 586,928 604,972",
    "M 728,860 C 692,832 686,788 712,764",
    "M 340,1046 C 306,1074 306,1122 340,1146",
    "M 596,1204 C 654,1228 716,1212 742,1170",
]

COLON = (
    "M 306,1216 "                                   # caecum
    "C 234,1204 198,1156 196,1086 "                 # ascending colon
    "C 192,978 190,848 200,762 "
    "C 208,690 254,648 328,644 "                    # hepatic flexure
    "C 412,640 462,684 508,744 "                    # transverse colon, sagging
    "C 566,820 640,832 706,776 "
    "C 764,726 796,650 862,622 "                    # splenic flexure
    "C 918,598 950,638 950,706 "                    # descending colon
    "C 958,802 960,1002 950,1096 "
    "C 946,1182 892,1242 808,1252 "                 # sigmoid
    "C 744,1260 692,1232 654,1262"
)

TAENIA = (
    "M 318,1190 C 262,1178 236,1140 234,1084 "
    "C 230,978 228,850 238,772 "
    "C 244,712 280,682 336,678 "
    "C 404,674 446,712 488,766 "
    "C 552,844 640,858 712,798 "
    "C 770,748 802,678 862,654 "
    "C 900,638 918,662 918,712 "
    "C 918,806 920,1002 912,1092 "
    "C 906,1162 862,1210 796,1218 "
    "C 742,1224 700,1204 668,1228"
)

RECTUM = "M 654,1262 C 620,1288 602,1318 600,1356 C 598,1396 599,1424 600,1452"
APPENDIX = "M 322,1222 C 342,1262 352,1290 348,1310"

# ================================================================== organs
# id, English name, Arabic name, label anchor as a % of the viewBox
ORGANS = [
    ("oesophagus",      "Oesophagus",       "المريء",                    44.0, 12.0),
    ("stomach",         "Stomach",          "المعدة",                    82.0, 24.0),
    ("duodenum",        "Duodenum",         "الاثنا عشر",                26.0, 39.0),
    ("small-intestine", "Small intestine",  "الأمعاء الدقيقة",           58.0, 68.0),
    ("large-intestine", "Large intestine",  "الأمعاء الغليظة (القولون)", 21.0, 55.0),
    ("appendix",        "Appendix",         "الزائدة الدودية",           27.0, 93.0),
    ("rectum",          "Rectum",           "المستقيم",                  74.0, 90.0),
]

# ================================================================== tokens
TOKENS = [
    ("--ds-glow",      "#8FE0FA"),
    ("--ds-halo",      "#7FD4F6"),
    ("--ds-edge",      "#F2FDFF"),
    ("--ds-mid",       "#8CDCF9"),
    ("--ds-core",      "#D6F4FE"),
    ("--ds-sheen",     "#FFFFFF"),
    ("--ds-seam",      "#7C97E4"),
    ("--ds-taenia",    "#EAFBFF"),
    ("--ds-rim-1",     "#8ED9F8"),
    ("--ds-rim-2",     "#5F6BDA"),
    ("--ds-colon-1",   "#84D6F8"),
    ("--ds-colon-2",   "#5A66D7"),
    ("--ds-glow-o",    ".42"),
    ("--ds-edge-o",    ".95"),
    ("--ds-core-o",    ".92"),
    ("--ds-sheen-o",   ".80"),
    ("--ds-seam-o",    ".40"),
    ("--ds-taenia-o",  ".65"),
    ("--ds-halo-o",    ".22"),
]

# class -> declarations, shared by the standalone <style> and the stylesheet
ART_RULES = [
    ("ds-glow",   "fill:none; stroke:var(--ds-glow,#8FE0FA); "
                  "stroke-opacity:var(--ds-glow-o,.42); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    ("ds-edge",   "fill:none; stroke:var(--ds-edge,#F2FDFF); "
                  "stroke-opacity:var(--ds-edge-o,.95); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    # .ds-sb / .ds-lb get their paint from a stroke="url(#ds-g-*)" attribute in
    # the markup, not from CSS: the ids are rewritten per instance, and a static
    # stylesheet cannot follow that.
    ("ds-sb",     "fill:none; stroke-linecap:round; stroke-linejoin:round"),
    ("ds-lb",     "fill:none; stroke-linecap:round; stroke-linejoin:round"),
    ("ds-mid",    "fill:none; stroke:var(--ds-mid,#8CDCF9); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    ("ds-core",   "fill:none; stroke:var(--ds-core,#D6F4FE); "
                  "stroke-opacity:var(--ds-core-o,.92); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    ("ds-sheen",  "fill:none; stroke:var(--ds-sheen,#FFFFFF); "
                  "stroke-opacity:var(--ds-sheen-o,.80); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    ("ds-seam",   "fill:none; stroke:var(--ds-seam,#7C97E4); "
                  "stroke-opacity:var(--ds-seam-o,.40); stroke-linecap:butt"),
    ("ds-taenia", "fill:none; stroke:var(--ds-taenia,#EAFBFF); "
                  "stroke-opacity:var(--ds-taenia-o,.65); stroke-linecap:round; "
                  "stroke-linejoin:round"),
    ("ds-hit",    "fill:none; stroke:transparent; stroke-linecap:round; "
                  "stroke-linejoin:round; pointer-events:stroke"),
    ("ds-halo",   "fill:none; stroke:var(--ds-halo,#7FD4F6); stroke-linecap:round; "
                  "stroke-linejoin:round; opacity:var(--ds-halo-o,.22)"),
]

# ================================================================== helpers
PAINT = {"ds-sb": "url(#ds-g-tube)", "ds-lb": "url(#ds-g-colon)"}


_glows = {}
_hits = {}


def tube(organ, d, w, dash_beads=None, cls="ds-sb", indent=6):
    """Layer stack for one tube.

    Shading runs ACROSS the tube, not along the path: a wide rim stroke in the
    deep periwinkle, then progressively narrower and lighter strokes, then an
    offset white sheen. That is what gives each loop its glassy, cylindrical
    read, the way the reference illustration is lit.
    """
    p = " " * indent
    _glows.setdefault(organ, []).append(
        f'      <path d="{d}" stroke-width="{w + 12}"/>')
    # A transparent, deliberately fat stroke so thin loops are still an easy
    # pointer/touch target (the painted tube alone is well under 44px).
    _hits.setdefault(organ, []).append(
        f'{p}<path d="{d}" stroke-width="{max(w + 14, 40)}"/>')
    o = [f'{p}<path class="ds-edge" d="{d}" stroke-width="{w + 5:.1f}"/>']
    if dash_beads:                       # haustra: a chain of round-capped dots
        bw, gap = dash_beads
        o += [
            f'{p}<path class="ds-edge" d="{d}" stroke-width="{bw + 5}" '
            f'stroke-dasharray="1 {gap}" stroke-linecap="round"/>',
            f'{p}<path class="{cls}" stroke="{PAINT[cls]}" d="{d}" '
            f'stroke-width="{bw}" stroke-dasharray="1 {gap}" '
            f'stroke-linecap="round"/>',
            f'{p}<path class="ds-mid" d="{d}" stroke-width="{bw * 0.66:.1f}" '
            f'stroke-dasharray="1 {gap}" stroke-linecap="round"/>',
        ]
    o += [
        f'{p}<path class="{cls}" stroke="{PAINT[cls]}" d="{d}" '
        f'stroke-width="{w}"/>',
        f'{p}<path class="ds-mid" d="{d}" stroke-width="{w * 0.70:.1f}"/>',
        f'{p}<path class="ds-core" d="{d}" stroke-width="{w * 0.38:.1f}"/>',
        f'{p}<path class="ds-sheen" filter="url(#ds-f-soft)" d="{d}" '
        f'stroke-width="{w * 0.17:.1f}" '
        f'transform="translate(-{w * 0.20:.1f},-{w * 0.20:.1f})"/>',
    ]
    if dash_beads:
        bw, gap = dash_beads
        o.append(
            f'{p}<path class="ds-seam" d="{d}" stroke-width="{bw}" '
            f'stroke-dasharray="2.5 {gap}" stroke-dashoffset="{gap / 2 + 1:.1f}"/>'
        )
    return "\n".join(o)


def organ_group(organ, body):
    name = next(o[1] for o in ORGANS if o[0] == organ)
    hits = "\n".join(_hits.get(organ, []))
    hit = f'\n      <g class="ds-hit">\n{hits}\n      </g>' if hits else ""
    return (f'    <g class="ds-organ" data-organ="{organ}" '
            f'aria-label="{name}">\n{body}{hit}\n    </g>')


# ================================================================== defs
# Every stop is a (themed, literal) pair: the component keeps custom properties
# and color-mix() so overriding --ds-rim-1/--ds-rim-2 recolours the whole
# illustration, while the standalone .svg gets plain hex for rasterisers that
# implement neither.
def _mix(a, b, pct, lit):
    return (f"color-mix(in oklab, var({a}) {pct}%, var({b}))", lit)  # noqa


def _var(name, lit):
    return (f"var({name},{lit})", lit)


R1, R2 = "--ds-rim-1", "--ds-rim-2"
C1, C2 = "--ds-colon-1", "--ds-colon-2"

GRADIENTS = [
    ("ds-g-tube", "linearGradient", 'x1="0" y1="0" x2="1" y2="1"', [
        ("0",    _var(R1, "#8ED9F8")),
        ("0.35", _mix(R1, R2, 62, "#72C4F4")),
        ("0.72", _mix(R1, R2, 26, "#6E8CE8")),
        ("1",    _var(R2, "#5F6BDA")),
    ]),
    ("ds-g-colon", "linearGradient", 'x1="0.1" y1="0" x2="0.9" y2="1"', [
        ("0",    _var(C1, "#84D6F8")),
        ("0.32", _mix(C1, C2, 66, "#71BEF3")),
        ("0.68", _mix(C1, C2, 28, "#6C86E6")),
        ("1",    _var(C2, "#5A66D7")),
    ]),
    ("ds-g-stomach", "radialGradient", 'cx="0.34" cy="0.28" r="0.86"', [
        ("0",    _var("--ds-core", "#E4F8FE")),
        ("0.30", _mix("--ds-core", R1, 46, "#A9E4FB")),
        ("0.66", _mix(R1, R2, 72, "#79CDF4")),
        ("1",    _var(R2, "#6C86E6")),
    ]),
]

FILTERS = (
    '    <filter id="ds-f-glow" x="-25%" y="-25%" width="150%" height="150%">\n'
    '      <feGaussianBlur stdDeviation="11"/>\n'
    '    </filter>\n'
    '    <filter id="ds-f-soft" x="-25%" y="-25%" width="150%" height="150%">\n'
    '      <feGaussianBlur stdDeviation="2.6"/>\n'
    '    </filter>\n'
    '    <filter id="ds-f-halo" x="-30%" y="-30%" width="160%" height="160%">\n'
    '      <feGaussianBlur stdDeviation="18"/>\n'
    '    </filter>'
)


def build_defs(themed=True):
    out = []
    for gid, tag, geom, stops in GRADIENTS:
        out.append(f'    <{tag} id="{gid}" {geom}>')
        for offset, (themed_v, literal_v) in stops:
            out.append(f'      <stop offset="{offset}" '
                       f'stop-color="{themed_v if themed else literal_v}"/>')
        out.append(f'    </{tag}>')
    out.append(FILTERS)
    return "\n".join(out)


DEFS = build_defs(themed=True)

# ================================================================== artwork
bodies = []

bodies.append(organ_group("large-intestine", "\n".join([
    tube("large-intestine", COLON, 40, dash_beads=(70, 36), cls="ds-lb"),
    f'      <path class="ds-taenia" d="{TAENIA}" stroke-width="3.6"/>',
])))
bodies.append(organ_group("appendix",
                          tube("appendix", APPENDIX, 16, cls="ds-lb")))
bodies.append(organ_group("rectum", tube("rectum", RECTUM, 46, cls="ds-lb")))

si = [tube("small-intestine", d, 42) for d in SMALL_EXTRA]
si.append(tube("small-intestine", SMALL_BOWEL, 46))
bodies.append(organ_group("small-intestine", "\n".join(si)))

bodies.append(organ_group("duodenum", tube("duodenum", DUODENUM, 44)))
bodies.append(organ_group("oesophagus", tube("oesophagus", ESOPHAGUS, 20)))

STOMACH_BODY = f'''      <path d="{STOMACH}" fill="none" stroke="var(--ds-glow,#8FE0FA)"
            stroke-opacity=".45" stroke-width="18" stroke-linejoin="round"
            filter="url(#ds-f-glow)"/>
      <path d="{STOMACH}" fill="url(#ds-g-stomach)" stroke="var(--ds-edge,#E8FAFF)"
            stroke-opacity=".9" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M 690,336 C 740,308 800,296 856,320" fill="none" stroke="#FFFFFF"
            stroke-opacity=".55" stroke-width="16" stroke-linecap="round"
            filter="url(#ds-f-soft)"/>
      <path d="M 896,388 C 916,424 918,468 906,506" fill="none" stroke="#FFFFFF"
            stroke-opacity=".85" stroke-width="9" stroke-linecap="round"
            filter="url(#ds-f-soft)"/>
      <path d="M 700,470 C 690,506 660,522 626,512" fill="none" stroke="#EAFBFF"
            stroke-opacity=".55" stroke-width="4" stroke-linecap="round"/>
      <path d="M 556,514 C 620,536 690,578 760,590" fill="none" stroke="var(--ds-seam,#6F8FDE)"
            stroke-opacity=".35" stroke-width="4" stroke-linecap="round"/>
      <g fill="none" stroke="var(--ds-seam,#79A0E8)" stroke-opacity=".30" stroke-width="3.2"
         stroke-linecap="round">
        <path d="M 706,330 C 692,372 686,420 694,462"/>
        <path d="M 776,294 C 768,346 770,400 786,448"/>
        <path d="M 848,300 C 852,352 858,404 872,450"/>
      </g>'''
bodies.append(organ_group("stomach", STOMACH_BODY))

halo = ['  <g class="ds-halo" aria-hidden="true" filter="url(#ds-f-halo)">']
for d, w in ((COLON, 70), (SMALL_BOWEL, 56), (STOMACH, 40), (ESOPHAGUS, 30)):
    halo.append(f'    <path d="{d}" stroke-width="{w}"/>')
halo.append('  </g>')

glow_layer = ['  <g class="ds-glows ds-glow" aria-hidden="true" '
              'filter="url(#ds-f-glow)">']
for organ, paths in _glows.items():
    glow_layer.append(f'    <g class="ds-organ-glow" data-organ="{organ}">')
    glow_layer += paths
    glow_layer.append('    </g>')
glow_layer.append('  </g>')

ART = "\n".join(halo + glow_layer + ['  <g class="ds-art">'] + bodies + ['  </g>'])

TITLE = '  <title id="ds-title">Human digestive system</title>'
DESC = ('  <desc id="ds-desc">Vector illustration of the human digestive tract — '
        'oesophagus, stomach, duodenum, small intestine, colon and rectum — '
        'rendered as glowing cyan-to-periwinkle translucent tubes.</desc>')

# ---------------------------------------------------------- standalone .svg
_VAR = re.compile(r"var\(\s*--[\w-]+\s*,\s*([^()]*?)\s*\)")


def literal(text):
    """Resolve var(--x, fallback) down to the fallback.

    The component keeps the custom properties so host pages can theme it, but
    the standalone .svg is also consumed by <img> and by rasterisers (librsvg,
    cairosvg, Inkscape) that do not implement CSS custom properties.
    """
    return _VAR.sub(r"\1", text)


inline_style = "  <style>\n" + "".join(
    f"    .{c} {{ {literal(decl)}; }}\n" for c, decl in ART_RULES) + "  </style>"

standalone = "\n".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
    f'height="{H}" role="img" aria-labelledby="ds-title ds-desc">',
    TITLE, DESC,
    "  <defs>\n" + build_defs(themed=False) + "\n  </defs>",
    inline_style,
    literal(ART),
    "</svg>",
]) + "\n"

with open(os.path.join(ROOT, "assets", "digestive-system.svg"), "w",
          encoding="utf-8") as f:
    f.write(standalone)

# ============================================================ stylesheet
css = """/* digestive-system — themeable stylesheet for the <digestive-system> element.
   Generated by assets/digestive-system.gen.py — edit that, not this file.

   Theming: override any --ds-* custom property on the element or an ancestor.
     digestive-system { --ds-rim-2: #7a4fd8; --ds-mid: #c9a6f5; }
*/

digestive-system {
  --ds-dim: 0.28;            /* opacity of the organs that are not active   */
  --ds-duration: 240ms;      /* hover/select transition                     */
  --ds-focus: #1d4ed8;       /* focus ring                                  */
  --ds-label-bg: rgba(255, 255, 255, 0.92);
  --ds-label-fg: #123a52;
  --ds-label-bd: rgba(94, 160, 214, 0.45);
%TOKENS%
  display: block;
  position: relative;
  inline-size: 100%;
  max-inline-size: 640px;
  aspect-ratio: %W% / %H%;
  container-type: inline-size;
}

digestive-system .ds-svg {
  display: block;
  inline-size: 100%;
  block-size: 100%;
}

%ART%

/* ------------------------------------------------------------- interaction */
digestive-system .ds-halo,
digestive-system .ds-glows { pointer-events: none; }

digestive-system .ds-organ,
digestive-system .ds-organ-glow {
  transition: opacity var(--ds-duration) ease;
}

digestive-system[interactive] .ds-organ { cursor: pointer; }

/* Dim everything except the active organ. JS toggles the classes so no
   per-organ CSS rule is needed. */
digestive-system .ds-organ.is-dimmed,
digestive-system .ds-organ-glow.is-dimmed { opacity: var(--ds-dim); }

digestive-system .ds-organ.is-active {
  filter: drop-shadow(0 0 14px var(--ds-glow, #8fe0fa));
}

digestive-system .ds-organ:focus { outline: none; }

/* Focus ring: a real rect drawn around the focused group's bounding box,
   because outlines on SVG groups are unreliable across browsers. */
digestive-system .ds-focus-ring {
  fill: none;
  stroke: var(--ds-focus, #1d4ed8);
  stroke-width: 3;
  stroke-dasharray: 8 6;
  rx: 12;
  pointer-events: none;
}
digestive-system .ds-focus-ring[hidden] { display: none; }

/* ------------------------------------------------------------------ labels */
digestive-system .ds-label {
  position: absolute;
  transform: translate(-50%, -50%);
  display: inline-flex;
  align-items: center;
  gap: 0.4em;
  padding: 0.35em 0.7em;
  border: 1px solid var(--ds-label-bd);
  border-radius: 999px;
  background: var(--ds-label-bg);
  color: var(--ds-label-fg);
  font: 500 clamp(11px, 2.6cqi, 14px)/1.2 system-ui, -apple-system,
        "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  white-space: nowrap;
  backdrop-filter: blur(2px);
  transition: opacity var(--ds-duration) ease;
}
digestive-system .ds-label::before {
  content: "";
  inline-size: 0.5em;
  block-size: 0.5em;
  border-radius: 50%;
  background: var(--ds-rim-2, #5f6bda);
}
digestive-system .ds-label.is-dimmed { opacity: var(--ds-dim); }
digestive-system:not([labels]) .ds-labels { display: none; }

/* ----------------------------------------------------------------- caption */
digestive-system .ds-caption {
  position: absolute;
  inset-inline: 0;
  inset-block-end: 0;
  margin: 0;
  padding: 0.5em 0.8em;
  border-radius: 10px;
  background: var(--ds-label-bg);
  color: var(--ds-label-fg);
  font: 500 clamp(12px, 3cqi, 15px)/1.4 system-ui, sans-serif;
  text-align: center;
}
digestive-system:not([caption]) .ds-caption { display: none; }

/* ---------------------------------------------------------------- a11y/pref */
@media (prefers-reduced-motion: reduce) {
  digestive-system * { transition-duration: 1ms !important; }
}

@media (prefers-color-scheme: dark) {
  digestive-system {
    --ds-halo-o: .34;
    --ds-seam-o: .5;
    --ds-label-bg: rgba(12, 24, 40, 0.86);
    --ds-label-fg: #dbf3ff;
    --ds-label-bd: rgba(120, 190, 240, 0.35);
    --ds-focus: #7dd3fc;
  }
}

@media print {
  digestive-system .ds-organ.is-dimmed,
  digestive-system .ds-organ-glow.is-dimmed,
  digestive-system .ds-label.is-dimmed { opacity: 1; }
}
"""
css = (css.replace("%W%", str(W)).replace("%H%", str(H))
          .replace("%TOKENS%", "".join(f"  {k}: {v};\n" for k, v in TOKENS))
          .replace("%ART%", "\n".join(
              f"digestive-system .{c} {{ {decl}; }}" for c, decl in ART_RULES)))

os.makedirs(WEB, exist_ok=True)
with open(os.path.join(WEB, "digestive-system.css"), "w", encoding="utf-8") as f:
    f.write(css)

# ================================================================ component
def js_str(s):
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


organs_js = ",\n".join(
    f'  {{ id: "{i}", en: "{en}", ar: "{ar}", x: {x}, y: {y} }}'
    for i, en, ar, x, y in ORGANS
)

js = """/* <digestive-system> — a dependency-free custom element wrapping the
   digestive-tract illustration. Generated by assets/digestive-system.gen.py.

   Usage:
     <link rel="stylesheet" href="digestive-system.css">
     <script type="module" src="digestive-system.js"></script>
     <digestive-system interactive labels caption lang="ar"></digestive-system>

   Attributes
     interactive   hover / focus / click highlighting
     labels        static name chips positioned over each organ
     caption       caption line naming the active organ
     lang="ar"     Arabic organ names (any other value = English)
     selected      organ id; reflected, settable from outside

   Events (bubbling, composed)
     organ-hover   detail: { id, name } | { id: null }
     organ-select  detail: { id, name }

   The element renders in the light DOM on purpose, so host pages can theme it
   with plain CSS. Each instance carries its own <defs> with id-scoped
   gradients, so several differently themed instances can coexist.
*/

export const VIEWBOX = { width: %W%, height: %H% };

export const ORGANS = [
%ORGANS%
];

export const DEFS = `%DEFS%`;

/** Gradient + filter definitions, and the artwork that references them.
 *  Exported for hand-rolled integrations: inline `<svg><defs>${DEFS}</defs>
 *  ${ART}</svg>` and the illustration renders without the custom element. */
export const ART = `%ART%`;

let uid = 0;

/** Scope every gradient/filter id to one instance.
 *  The defs live INSIDE each element so that per-instance CSS custom
 *  properties (--ds-rim-1 and friends) actually reach the gradient stops —
 *  a shared sprite in <body> cannot inherit them. */
function scope(markup, n) {
  return markup.replace(/ds-(g|f)-([a-z-]+)/g, `ds-$1-$2-${n}`);
}

const nameOf = (organ, lang) => (lang === "ar" ? organ.ar : organ.en);

export class DigestiveSystem extends HTMLElement {
  static observedAttributes = ["selected", "lang", "interactive", "caption"];

  #svg = null;
  #ring = null;
  #caption = null;
  #hovered = null;

  connectedCallback() {
    if (this.#svg) return;
    this.#render();
  }

  attributeChangedCallback() {
    if (!this.#svg) return;
    this.#syncLabels();
    this.#paint();
  }

  /** Currently selected organ id, or null. */
  get selected() { return this.getAttribute("selected"); }
  set selected(id) {
    if (id) this.setAttribute("selected", id);
    else this.removeAttribute("selected");
  }

  get organs() { return ORGANS.slice(); }

  /** Select an organ programmatically; fires organ-select. */
  select(id) {
    const organ = ORGANS.find((o) => o.id === id);
    if (!organ) return false;
    this.selected = id;
    this.#emit("organ-select", { id, name: nameOf(organ, this.lang) });
    return true;
  }

  /** Clear selection and hover state. */
  clear() {
    this.selected = null;
    this.#hovered = null;
    this.#paint();
  }

  get lang() { return this.getAttribute("lang") === "ar" ? "ar" : "en"; }

  // ------------------------------------------------------------- internals
  #render() {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("class", "ds-svg");
    svg.setAttribute("viewBox", `0 0 ${VIEWBOX.width} ${VIEWBOX.height}`);
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", this.getAttribute("aria-label") ||
      "Human digestive system");
    const n = ++uid;
    svg.innerHTML = `<defs>${scope(DEFS, n)}</defs>${scope(ART, n)}`;

    const ring = document.createElementNS(ns, "rect");
    ring.setAttribute("class", "ds-focus-ring");
    ring.hidden = true;
    svg.append(ring);

    this.#svg = svg;
    this.#ring = ring;
    this.append(svg);

    const labels = document.createElement("div");
    labels.className = "ds-labels";
    for (const organ of ORGANS) {
      const el = document.createElement("span");
      el.className = "ds-label";
      el.dataset.organ = organ.id;
      el.style.left = `${organ.x}%`;   // physical, not logical: the anchors
      el.style.top = `${organ.y}%`;     // are viewBox coordinates, never RTL

      labels.append(el);
    }
    this.append(labels);

    const caption = document.createElement("p");
    caption.className = "ds-caption";
    caption.setAttribute("aria-live", "polite");
    this.#caption = caption;
    this.append(caption);

    this.#syncLabels();
    this.#wire();
    this.#paint();
  }

  #groups(selector = ".ds-organ, .ds-organ-glow") {
    return this.#svg.querySelectorAll(selector);
  }

  #wire() {
    for (const g of this.#svg.querySelectorAll(".ds-organ")) {
      const id = g.dataset.organ;
      g.addEventListener("pointerenter", () => this.#hover(id));
      g.addEventListener("pointerleave", () => this.#hover(null));
      g.addEventListener("click", () => this.#activate(id));
      g.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          this.#activate(id);
        } else if (e.key === "Escape") {
          this.clear();
        }
      });
      // :focus-visible so the ring answers the keyboard, not every mouse click
      g.addEventListener("focus", () => {
        this.#hover(id);
        this.#ringTo(g.matches(":focus-visible") ? g : null);
      });
      g.addEventListener("blur", () => { this.#hover(null); this.#ringTo(null); });
    }
  }

  #interactive() { return this.hasAttribute("interactive"); }

  #hover(id) {
    if (!this.#interactive()) return;
    this.#hovered = id;
    this.#emit("organ-hover", id
      ? { id, name: nameOf(ORGANS.find((o) => o.id === id), this.lang) }
      : { id: null, name: null });
    this.#paint();
  }

  #activate(id) {
    if (!this.#interactive()) return;
    if (this.selected === id) this.clear();
    else this.select(id);
  }

  #ringTo(g) {
    if (!g || !this.#interactive()) { this.#ring.hidden = true; return; }
    const box = g.getBBox();
    const pad = 10;
    this.#ring.setAttribute("x", box.x - pad);
    this.#ring.setAttribute("y", box.y - pad);
    this.#ring.setAttribute("width", box.width + pad * 2);
    this.#ring.setAttribute("height", box.height + pad * 2);
    this.#ring.hidden = false;
  }

  #syncLabels() {
    const lang = this.lang;
    this.dataset.lang = lang;
    for (const el of this.querySelectorAll(".ds-label")) {
      const organ = ORGANS.find((o) => o.id === el.dataset.organ);
      el.textContent = nameOf(organ, lang);
    }
    for (const g of this.#svg.querySelectorAll(".ds-organ")) {
      const organ = ORGANS.find((o) => o.id === g.dataset.organ);
      g.setAttribute("aria-label", nameOf(organ, lang));
    }
  }

  /** Apply active/dimmed classes; the single place that touches the DOM state. */
  #paint() {
    const on = this.#interactive();
    const active = this.#hovered || this.selected;

    for (const g of this.#svg.querySelectorAll(".ds-organ")) {
      if (on) {
        g.setAttribute("role", "button");
        g.setAttribute("tabindex", "0");
      } else {
        g.removeAttribute("role");
        g.removeAttribute("tabindex");
      }
      g.setAttribute("aria-pressed", String(this.selected === g.dataset.organ));
    }

    for (const g of this.#groups()) {
      const isActive = Boolean(active) && g.dataset.organ === active;
      g.classList.toggle("is-active", isActive && g.classList.contains("ds-organ"));
      g.classList.toggle("is-dimmed", Boolean(active) && !isActive);
    }
    for (const el of this.querySelectorAll(".ds-label")) {
      el.classList.toggle("is-dimmed",
        Boolean(active) && el.dataset.organ !== active);
    }

    if (this.#caption) {
      const organ = ORGANS.find((o) => o.id === active);
      this.#caption.textContent = organ
        ? nameOf(organ, this.lang)
        : (this.lang === "ar" ? "الجهاز الهضمي" : "Digestive system");
    }
  }

  #emit(type, detail) {
    this.dispatchEvent(new CustomEvent(type, {
      detail, bubbles: true, composed: true,
    }));
  }
}

if (!customElements.get("digestive-system")) {
  customElements.define("digestive-system", DigestiveSystem);
}

export default DigestiveSystem;
"""
js = (js.replace("%W%", str(W)).replace("%H%", str(H))
        .replace("%ORGANS%", organs_js)
        .replace("%DEFS%", js_str(DEFS))
        .replace("%ART%", js_str(ART)))

with open(os.path.join(WEB, "digestive-system.js"), "w", encoding="utf-8") as f:
    f.write(js)

# ===================================================================== demo
demo = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>&lt;digestive-system&gt; — usage</title>
<link rel="stylesheet" href="digestive-system.css">
<style>
  :root { color-scheme: light dark; }
  body {
    margin: 0; padding: clamp(16px, 4vw, 48px);
    font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    color: #0f2733; background: #f6fbfe;
    display: grid; gap: 32px;
    grid-template-columns: minmax(280px, 460px) minmax(300px, 1fr);
    align-items: start;
  }
  @media (max-width: 760px) { body { grid-template-columns: 1fr; } }
  h1 { font-size: clamp(20px, 4vw, 28px); margin: 0 0 4px; }
  h2 { font-size: 15px; text-transform: uppercase; letter-spacing: .08em;
       color: #4a7691; margin: 28px 0 8px; }
  p.lede { margin: 0 0 20px; color: #46687c; }
  fieldset { border: 1px solid #cfe3ef; border-radius: 12px; margin: 0 0 16px;
             padding: 12px 14px; }
  legend { padding: 0 6px; font-size: 13px; color: #4a7691; }
  label { display: inline-flex; align-items: center; gap: 6px; margin: 4px 12px 4px 0;
          min-height: 32px; }
  button { min-height: 44px; padding: 0 14px; border-radius: 10px; cursor: pointer;
           border: 1px solid #bcd9e9; background: #fff; font: inherit; }
  button:hover { background: #eaf6fc; }
  pre { margin: 0 0 16px; padding: 14px; border-radius: 12px; overflow-x: auto;
        background: #0e2231; color: #d7ecf7; font-size: 13px; line-height: 1.55; }
  code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
  #log { margin: 0; padding: 10px 14px; border-radius: 10px; background: #fff;
         border: 1px solid #cfe3ef; min-height: 44px; font-size: 14px; }
  .stage { padding: 12px; background: #fff; border: 1px solid #dceaf3;
           border-radius: 16px; }
  @media (prefers-color-scheme: dark) {
    body { color: #dceefa; background: #0a1620; }
    .stage { background: #0f2231; border-color: #1e3b50; }
    fieldset, #log, button { border-color: #1e3b50; background: #0f2231; color: inherit; }
    p.lede, legend, h2 { color: #8fb6cd; }
  }
</style>
</head>
<body>

<div>
  <h1>&lt;digestive-system&gt;</h1>
  <p class="lede">One custom element, no dependencies. Hover, click or tab
     through the organs.</p>

  <div class="stage">
    <digestive-system id="demo" interactive caption></digestive-system>
  </div>

  <fieldset>
    <legend>Attributes</legend>
    <label><input type="checkbox" id="t-interactive" checked> interactive</label>
    <label><input type="checkbox" id="t-labels"> labels</label>
    <label><input type="checkbox" id="t-caption" checked> caption</label>
    <label><input type="checkbox" id="t-ar"> lang="ar"</label>
  </fieldset>

  <fieldset>
    <legend>Theme (CSS custom properties)</legend>
    <button data-theme="">Default</button>
    <button data-theme="violet">Violet</button>
    <button data-theme="emerald">Emerald</button>
    <button data-theme="amber">Amber</button>
  </fieldset>

  <fieldset>
    <legend>API</legend>
    <button id="pick">select('stomach')</button>
    <button id="clear">clear()</button>
  </fieldset>

  <p id="log">events appear here</p>
</div>

<div>
  <h2>1. Plain HTML</h2>
<pre><code>&lt;link rel="stylesheet" href="digestive-system.css"&gt;
&lt;script type="module" src="digestive-system.js"&gt;&lt;/script&gt;

&lt;digestive-system interactive labels caption lang="ar"&gt;&lt;/digestive-system&gt;

&lt;script type="module"&gt;
  document.querySelector('digestive-system')
    .addEventListener('organ-select', e =&gt; console.log(e.detail.id));
&lt;/script&gt;</code></pre>

  <h2>2. React / Next.js</h2>
<pre><code>import { useEffect, useRef } from 'react';
import 'digestive-system/digestive-system.css';

export function DigestiveSystem({ onSelect, lang = 'en' }) {
  const ref = useRef(null);
  useEffect(() =&gt; { import('digestive-system/digestive-system.js'); }, []);
  useEffect(() =&gt; {
    const el = ref.current;
    const h = e =&gt; onSelect?.(e.detail);
    el.addEventListener('organ-select', h);
    return () =&gt; el.removeEventListener('organ-select', h);
  }, [onSelect]);
  return &lt;digestive-system ref={ref} interactive caption lang={lang} /&gt;;
}</code></pre>
  <p class="lede">In Next.js load it from a client component
     (<code>'use client'</code>); custom elements need the DOM.</p>

  <h2>3. Just the picture</h2>
<pre><code>&lt;img src="digestive-system.svg" alt="Human digestive system" width="535"&gt;

&lt;!-- or inline, to style it with CSS: --&gt;
&lt;div class="illustration"&gt;&lt;!-- paste assets/digestive-system.svg --&gt;&lt;/div&gt;</code></pre>

  <h2>4. Theming</h2>
<pre><code>digestive-system {
  --ds-rim-1: #c9a6f5;   /* light rim          */
  --ds-rim-2: #7a4fd8;   /* deep rim / shadow  */
  --ds-mid:   #d9c2fb;   /* mid tone           */
  --ds-core:  #f3ebff;   /* bright core        */
  --ds-glow:  #b98cf5;   /* outer glow         */
  --ds-dim:   0.2;       /* inactive organs    */
  max-inline-size: 420px;
}</code></pre>

  <h2>5. Events &amp; API</h2>
<pre><code>el.select('large-intestine');   // programmatic selection
el.clear();                     // drop hover + selection
el.selected;                    // 'large-intestine' | null
el.organs;                      // [{ id, en, ar, x, y }, ...]

el.addEventListener('organ-hover',  e =&gt; e.detail.id);
el.addEventListener('organ-select', e =&gt; e.detail.name);</code></pre>
  <p class="lede">Organ ids: %IDS%.</p>
</div>

<script type="module" src="digestive-system.js"></script>
<script type="module">
  const el = document.getElementById('demo');
  const log = document.getElementById('log');

  const bind = (id, attr) =>
    document.getElementById(id).addEventListener('change', (e) => {
      if (attr === 'lang') {
        el.setAttribute('lang', e.target.checked ? 'ar' : 'en');
      } else {
        e.target.checked ? el.setAttribute(attr, '') : el.removeAttribute(attr);
      }
    });
  bind('t-interactive', 'interactive');
  bind('t-labels', 'labels');
  bind('t-caption', 'caption');
  bind('t-ar', 'lang');

  const THEMES = {
    '': {},
    violet:  { '--ds-rim-1': '#c9a6f5', '--ds-rim-2': '#7a4fd8',
               '--ds-mid': '#d9c2fb', '--ds-core': '#f3ebff',
               '--ds-glow': '#b98cf5', '--ds-colon-1': '#c3a2f3',
               '--ds-halo': '#b98cf5', '--ds-halo': '#6fe6bb', '--ds-halo': '#ffc46b', '--ds-colon-2': '#6c42cf' },
    emerald: { '--ds-rim-1': '#8ef0c8', '--ds-rim-2': '#12876a',
               '--ds-mid': '#9ff0d3', '--ds-core': '#e6fff5',
               '--ds-glow': '#6fe6bb', '--ds-colon-1': '#87ecc4',
               '--ds-colon-2': '#0f7d62' },
    amber:   { '--ds-rim-1': '#ffd58a', '--ds-rim-2': '#c2691a',
               '--ds-mid': '#ffe0a6', '--ds-core': '#fff6e4',
               '--ds-glow': '#ffc46b', '--ds-colon-1': '#ffcf85',
               '--ds-colon-2': '#b45c12' },
  };
  for (const b of document.querySelectorAll('[data-theme]')) {
    b.addEventListener('click', () => {
      for (const k of Object.keys(THEMES.violet)) el.style.removeProperty(k);
      for (const [k, v] of Object.entries(THEMES[b.dataset.theme] || {}))
        el.style.setProperty(k, v);
    });
  }

  document.getElementById('pick').onclick = () => el.select('stomach');
  document.getElementById('clear').onclick = () => el.clear();

  el.addEventListener('organ-select', (e) => {
    log.textContent = `organ-select → ${e.detail.id} (${e.detail.name})`;
  });
  el.addEventListener('organ-hover', (e) => {
    if (!el.selected) log.textContent = e.detail.id
      ? `organ-hover → ${e.detail.id}` : 'events appear here';
  });
</script>
</body>
</html>
"""
demo = demo.replace("%IDS%", ", ".join(f"<code>{o[0]}</code>" for o in ORGANS))

with open(os.path.join(WEB, "demo.html"), "w", encoding="utf-8") as f:
    f.write(demo)

print("wrote web/digestive-system/demo.html")


print("wrote assets/digestive-system.svg")
print("wrote web/digestive-system/digestive-system.css")
print("wrote web/digestive-system/digestive-system.js")
