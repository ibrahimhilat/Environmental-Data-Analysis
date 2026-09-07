# -*- coding: utf-8 -*-
"""Generator for assets/digestive-system.svg — layered tube rendering."""

W, H = 1070, 1440

# ---------------------------------------------------------------- paths
ESOPHAGUS = ("M 611,-10 C 611,90 604,190 606,250 C 608,302 626,330 664,346")

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

# duodenum: pylorus -> C-loop -> jejunum
DUODENUM = (
    "M 504,492 C 456,480 420,506 410,554 "
    "C 397,614 424,660 476,678 "
    "C 532,698 600,688 648,704"
)

# jejunum + ileum: one long meander, ends at the caecum
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

# large intestine: caecum -> ascending -> transverse -> descending -> sigmoid
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

RECTUM = "M 654,1262 C 620,1288 602,1318 600,1356 C 598,1396 599,1424 600,1452"
APPENDIX = "M 322,1222 C 342,1262 352,1290 348,1310"

# ---------------------------------------------------------------- helpers
GLOWS = []


def tube(d, w, key, dash_beads=None, cls="sb"):
    """Layer stack for one tube.

    Shading runs ACROSS the tube, not along the path: a wide rim stroke in the
    deep periwinkle, then progressively narrower and lighter strokes, then an
    offset white sheen. That is what gives each loop its glassy, cylindrical
    read, the way the reference illustration is lit.
    """
    GLOWS.append(f'    <path d="{d}" stroke-width="{w + 12}"/>')
    o = [f'    <path class="edge" d="{d}" stroke-width="{w + 5:.1f}"/>']
    if dash_beads:
        bw, gap = dash_beads
        o += [
            f'    <path class="edge" d="{d}" stroke-width="{bw + 5}" '
            f'stroke-dasharray="1 {gap}" stroke-linecap="round"/>',
            f'    <path class="{cls}" d="{d}" stroke-width="{bw}" '
            f'stroke-dasharray="1 {gap}" stroke-linecap="round"/>',
            f'    <path class="mid" d="{d}" stroke-width="{bw * 0.66:.1f}" '
            f'stroke-dasharray="1 {gap}" stroke-linecap="round"/>',
        ]
    o += [
        f'    <path class="{cls}" d="{d}" stroke-width="{w}"/>',
        f'    <path class="mid"  d="{d}" stroke-width="{w * 0.70:.1f}"/>',
        f'    <path class="core" d="{d}" stroke-width="{w * 0.38:.1f}"/>',
        f'    <path class="sheen" d="{d}" stroke-width="{w * 0.17:.1f}" '
        f'transform="translate(-{w * 0.20:.1f},-{w * 0.20:.1f})"/>',
    ]
    if dash_beads:
        bw, gap = dash_beads
        o.append(
            f'    <path class="seam" d="{d}" stroke-width="{bw}" '
            f'stroke-dasharray="2.5 {gap}" stroke-dashoffset="{gap / 2 + 1:.1f}"/>'
        )
    return "\n".join(o)


# ---------------------------------------------------------------- document
defs = '''  <defs>
    <linearGradient id="gTube" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0"    stop-color="#8ED9F8"/>
      <stop offset="0.35" stop-color="#72C4F4"/>
      <stop offset="0.72" stop-color="#6E8CE8"/>
      <stop offset="1"    stop-color="#5F6BDA"/>
    </linearGradient>
    <linearGradient id="gColon" x1="0.1" y1="0" x2="0.9" y2="1">
      <stop offset="0"    stop-color="#84D6F8"/>
      <stop offset="0.32" stop-color="#71BEF3"/>
      <stop offset="0.68" stop-color="#6C86E6"/>
      <stop offset="1"    stop-color="#5A66D7"/>
    </linearGradient>
    <radialGradient id="gStomach" cx="0.34" cy="0.28" r="0.86">
      <stop offset="0"    stop-color="#E4F8FE"/>
      <stop offset="0.30" stop-color="#A9E4FB"/>
      <stop offset="0.66" stop-color="#79CDF4"/>
      <stop offset="1"    stop-color="#6C86E6"/>
    </radialGradient>
    <radialGradient id="gBead" cx="0.36" cy="0.30" r="0.78">
      <stop offset="0"    stop-color="#D8F5FE"/>
      <stop offset="0.42" stop-color="#8FDCF9"/>
      <stop offset="0.78" stop-color="#7690EA"/>
      <stop offset="1"    stop-color="#5A63D6"/>
    </radialGradient>

    <filter id="fGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="11"/>
    </filter>
    <filter id="fSoft" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="2.6"/>
    </filter>
    <filter id="fHalo" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>'''

style = '''  <style>
    .glow   { fill:none; stroke:#8FE0FA; stroke-opacity:.42; stroke-linecap:round;
              stroke-linejoin:round; }
    .edge   { fill:none; stroke:#F2FDFF; stroke-opacity:.95; stroke-linecap:round;
              stroke-linejoin:round; }
    .sb     { fill:none; stroke:url(#gTube);  stroke-linecap:round; stroke-linejoin:round; }
    .lb     { fill:none; stroke:url(#gColon); stroke-linecap:round; stroke-linejoin:round; }
    .mid    { fill:none; stroke:#8CDCF9; stroke-linecap:round; stroke-linejoin:round; }
    .core   { fill:none; stroke:#D6F4FE; stroke-opacity:.92; stroke-linecap:round;
              stroke-linejoin:round; }
    .sheen  { fill:none; stroke:#FFFFFF; stroke-opacity:.80; stroke-linecap:round;
              stroke-linejoin:round; filter:url(#fSoft); }
    .seam   { fill:none; stroke:#7C97E4; stroke-opacity:.40; stroke-linecap:butt; }
    .taenia { fill:none; stroke:#EAFBFF; stroke-opacity:.65; stroke-linecap:round;
              stroke-linejoin:round; }
  </style>'''

# rim mask: keep only the outer edge of each stroke (thin bright outline)
parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" role="img" '
             f'aria-labelledby="ttl desc">')
parts.append('  <title id="ttl">Human digestive system</title>')
parts.append('  <desc id="desc">Vector illustration of the human digestive tract — '
             'oesophagus, stomach, duodenum, small intestine, colon and rectum — '
             'rendered as glowing cyan-to-periwinkle translucent tubes.</desc>')
parts.append(defs)
parts.append(style)

# ambient halo behind everything
parts.append('  <g filter="url(#fHalo)" opacity=".22" fill="none" stroke="#7FD4F6" '
             'stroke-linecap="round" stroke-linejoin="round">')
for d, w in ((COLON, 70), (SMALL_BOWEL, 56), (STOMACH, 40), (ESOPHAGUS, 30)):
    parts.append(f'    <path d="{d}" stroke-width="{w}"/>')
parts.append('  </g>')

# ---- large intestine (behind the small bowel)
BODY = []
parts.append("@@GLOWS@@")
parts.append('  <g id="large-intestine">')
parts.append(tube(COLON, 40, "colon", dash_beads=(70, 36), cls="lb"))
parts.append(tube(APPENDIX, 16, "appendix", cls="lb"))
parts.append('''    <path class="taenia"
          d="M 318,1190 C 262,1178 236,1140 234,1084
             C 230,978 228,850 238,772
             C 244,712 280,682 336,678
             C 404,674 446,712 488,766
             C 552,844 640,858 712,798
             C 770,748 802,678 862,654
             C 900,638 918,662 918,712
             C 918,806 920,1002 912,1092
             C 906,1162 862,1210 796,1218
             C 742,1224 700,1204 668,1228"
          stroke-width="3.6"/>''')
parts.append('  </g>')

# ---- small intestine
parts.append('  <g id="small-intestine">')
for d in SMALL_EXTRA:
    parts.append(tube(d, 42, "loop"))
parts.append(tube(SMALL_BOWEL, 46, "jejunum-ileum"))
parts.append(tube(DUODENUM, 44, "duodenum"))
parts.append('  </g>')

# ---- rectum / anal canal
parts.append('  <g id="rectum">')
parts.append(tube(RECTUM, 46, "rectum", cls="lb"))
parts.append('  </g>')

# ---- oesophagus + stomach (front)
parts.append('  <g id="upper-tract">')
parts.append(tube(ESOPHAGUS, 20, "oesophagus"))
parts.append(f'''    <path d="{STOMACH}" fill="none" stroke="#8FE0FA" stroke-opacity=".45"
          stroke-width="18" stroke-linejoin="round" filter="url(#fGlow)"/>
    <path d="{STOMACH}" fill="url(#gStomach)" stroke="#E8FAFF" stroke-opacity=".9"
          stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M 690,336 C 740,308 800,296 856,320" fill="none" stroke="#FFFFFF"
          stroke-opacity=".55" stroke-width="16" stroke-linecap="round" filter="url(#fSoft)"/>
    <path d="M 896,388 C 916,424 918,468 906,506" fill="none" stroke="#FFFFFF"
          stroke-opacity=".85" stroke-width="9" stroke-linecap="round" filter="url(#fSoft)"/>
    <path d="M 700,470 C 690,506 660,522 626,512" fill="none" stroke="#EAFBFF"
          stroke-opacity=".55" stroke-width="4" stroke-linecap="round"/>
    <path d="M 556,514 C 620,536 690,578 760,590" fill="none" stroke="#6F8FDE"
          stroke-opacity=".35" stroke-width="4" stroke-linecap="round"/>
    <g fill="none" stroke="#79A0E8" stroke-opacity=".30" stroke-width="3.2"
       stroke-linecap="round">
      <path d="M 706,330 C 692,372 686,420 694,462"/>
      <path d="M 776,294 C 768,346 770,400 786,448"/>
      <path d="M 848,300 C 852,352 858,404 872,450"/>
    </g>''')
parts.append('  </g>')
parts.append('</svg>')

glow_group = ('  <g class="glow" filter="url(#fGlow)">\n'
              + "\n".join(GLOWS) + "\n  </g>")
doc = "\n".join(parts).replace("@@GLOWS@@", glow_group)
open("/home/user/Environmental-Data-Analysis/assets/digestive-system.svg", "w",
     encoding="utf-8").write(doc + "\n")
print("written")
