"""Generate the profile's SVG graphics (header, stats panel, project banners, rank chart).

Run from the repo root:  python scripts/build_assets.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = 'ui-sans-serif,-apple-system,&quot;Segoe UI&quot;,Roboto,Helvetica,Arial,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Consolas,&quot;Liberation Mono&quot;,monospace'

THEMES = {
    "dark": dict(bg1="#070a12", bg2="#111933", grid="#ffffff", grid_op="0.045", fg="#eef2fb",
                 sub="#c9d4ea", dim="#7f8aa6", a="#7cf5c9", b="#8ab4ff", c="#d59bff",
                 card="#0f1629", card_stroke="#24304f"),
    "light": dict(bg1="#f7f9fc", bg2="#e8eefb", grid="#0b0f19", grid_op="0.05", fg="#0b0f19",
                  sub="#2b3550", dim="#5b6682", a="#0f9d6e", b="#3b6fe0", c="#9b4dde",
                  card="#ffffff", card_stroke="#d5dcec"),
}


def write(name, svg):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg.strip() + "\n", encoding="utf-8")


def defs(t, w, h):
    return f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['a']}"><animate attributeName="stop-color" values="{t['a']};{t['b']};{t['c']};{t['a']}" dur="9s" repeatCount="indefinite"/></stop>
      <stop offset="1" stop-color="{t['b']}"><animate attributeName="stop-color" values="{t['b']};{t['c']};{t['a']};{t['b']}" dur="9s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}"/>
    </pattern>
    <radialGradient id="glowA" cx="0.85" cy="0.25" r="0.55">
      <stop offset="0" stop-color="{t['b']}" stop-opacity="0.25"/><stop offset="1" stop-color="{t['b']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.1" cy="1" r="0.5">
      <stop offset="0" stop-color="{t['c']}" stop-opacity="0.16"/><stop offset="1" stop-color="{t['c']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" rx="20" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" rx="20" fill="url(#glowA)"/>
  <rect width="{w}" height="{h}" rx="20" fill="url(#glowB)"/>"""


def header(mode):
    t = THEMES[mode]
    w, h = 1000, 330
    # constellation: nodes + edges, animated
    nodes = [(700, 70, 5), (790, 120, 8), (880, 62, 5), (760, 210, 6), (900, 190, 7), (835, 270, 5), (950, 120, 4)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 4), (4, 5), (3, 5), (2, 6), (6, 4)]
    e = "\n".join(
        f'<line class="edge" x1="{nodes[i][0]}" y1="{nodes[i][1]}" x2="{nodes[j][0]}" y2="{nodes[j][1]}"/>'
        for i, j in edges)
    n = "\n".join(
        f'<circle class="node" style="animation-delay:{k * 0.45:.2f}s" cx="{x}" cy="{y}" r="{r}"/>'
        for k, (x, y, r) in enumerate(nodes))
    chips = ["AWS AI Practitioner", "SAP Certified", "Citi Bridge Top 5%", "#27 / 1,983 HackerRank"]
    cx, chip_svg = 60, []
    for label in chips:
        cw = 16 + len(label) * 7.6
        chip_svg.append(
            f'<g transform="translate({cx:.0f},262)"><rect width="{cw:.0f}" height="30" rx="15" fill="{t["card"]}" '
            f'fill-opacity="0.75" stroke="{t["card_stroke"]}"/><text x="{cw / 2:.0f}" y="20" text-anchor="middle" '
            f'font-family="{MONO}" font-size="12.5" fill="{t["sub"]}">{label}</text></g>')
        cx += cw + 10
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Aira K. Salish: I build AI that's right more often.">
  <style>
    .node{{fill:{t['a']};animation:pulse 3.2s ease-in-out infinite}}
    @keyframes pulse{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
    .edge{{stroke:{t['b']};stroke-opacity:.45;stroke-width:1.4;stroke-dasharray:4 6;animation:flow 2.6s linear infinite}}
    @keyframes flow{{to{{stroke-dashoffset:-20}}}}
    .cursor{{animation:blink 1.1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .rise{{animation:rise .9s ease-out both}}
    .d2{{animation-delay:.15s}}.d3{{animation-delay:.3s}}.d4{{animation-delay:.45s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
  </style>{defs(t, w, h)}
  <g>{e}{n}</g>
  <text class="rise" x="62" y="66" font-family="{MONO}" font-size="14" fill="{t['a']}" letter-spacing="2">~/airasalish $ whoami</text>
  <text class="rise d2" x="58" y="138" font-family="{SANS}" font-size="64" font-weight="800" fill="url(#ink)">Aira K. Salish</text>
  <text class="rise d3" x="62" y="184" font-family="{SANS}" font-size="24" font-weight="600" fill="{t['fg']}">I build AI that's right more often, and prove it with tests.</text>
  <text class="rise d4" x="62" y="222" font-family="{MONO}" font-size="14" fill="{t['dim']}">AI/ML @ SRM Chennai · Class of 2027 · agents · evals · fintech<tspan class="cursor" fill="{t['a']}"> ▍</tspan></text>
  {''.join(chip_svg)}
</svg>"""


STATS = [
    ("#27", "of 1,983", "HackerRank Orchestrate, Aug 2026"),
    ("−35%", "wrong answers", "in a live AI product (BeSuperhuman)"),
    ("20M", "views", "on one AI short (BabyBillion)"),
    ("0", "wrong committed calls", "Warrant, on a sealed held-out set"),
    ("Top 5%", "of 1,200+", "Citi Bridge 2026"),
    ("3", "live products", "Drift · Receipts · AIRA"),
]


def stats(mode):
    t = THEMES[mode]
    w, h = 1000, 250
    cols, cw, ch, gx, gy, x0, y0 = 3, 296, 92, 18, 18, 36, 24
    cards = []
    for i, (big, unit, note) in enumerate(STATS):
        x = x0 + (i % cols) * (cw + gx)
        y = y0 + (i // cols) * (ch + gy)
        cards.append(f"""
  <g class="card" style="animation-delay:{i * 0.12:.2f}s" transform="translate({x},{y})">
    <rect width="{cw}" height="{ch}" rx="14" fill="{t['card']}" fill-opacity="0.8" stroke="{t['card_stroke']}"/>
    <rect x="0" y="18" width="4" height="56" rx="2" fill="url(#ink)"/>
    <text x="24" y="50" font-family="{SANS}"><tspan font-size="34" font-weight="800" fill="url(#ink)">{big}</tspan><tspan dx="10" font-size="15" font-weight="600" fill="{t['fg']}">{unit}</tspan></text>
    <text x="24" y="74" font-family="{MONO}" font-size="12" fill="{t['dim']}">{note}</text>
  </g>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="By the numbers: #27 of 1,983 at HackerRank Orchestrate; 35% fewer wrong answers in a live AI product; 20M views on one AI short; zero wrong committed calls on Warrant; top 5% at Citi Bridge; 3 live products.">
  <style>
    .card{{animation:pop .7s ease-out both}}
    @keyframes pop{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1}}}}
  </style>{defs(t, w, h)}{''.join(cards)}
</svg>"""


PROJECTS = {
    "warrant": dict(title="WARRANT", tag="Because a hunch isn't evidence", event="RAZORPAY AI BUILDATHON 2026",
                    a="#5b8cff", b="#1b2a6b", metric="0 FP · 0 FN · 100% attack defence", motif="shield"),
    "receipts": dict(title="RECEIPTS", tag="A track record for every stock tip", event="SERPAPI INDIA HACKATHON 2026",
                     a="#ffd166", b="#5a3d00", metric="6 search engines · real SEBI case", motif="receipt"),
    "drift": dict(title="DRIFT", tag="Know what changed since you last looked", event="CODE, BY GROWW 2026",
                  a="#2ee6a6", b="#003d2c", metric="121 tests · 191 commits · live", motif="chart"),
    "traverse": dict(title="TRAVERSE", tag="Survey-grade area &amp; length from any shapefile", event="GEOSPATIAL API",
                     a="#ff8a5b", b="#4d1a00", metric="error ≈ 1 part in 10⁹", motif="polygon"),
    "aira": dict(title="AIRA", tag="One prompt. Full campaign. Under 30 s.", event="XENO INTERNSHIP CHALLENGE 2026",
                 a="#d59bff", b="#35105a", metric="Llama 3.3 70B · live analytics", motif="pulse"),
    "buyorwait": dict(title="BUY OR WAIT?", tag="Can you afford it, 90 days ahead?", event="HACKERRANK ORCHESTRATE · SEP 2026",
                      a="#7cf5c9", b="#0b3d33", metric="Top 2.7% · fails closed", motif="bars"),
}


def motif(kind, a):
    if kind == "shield":
        return (f'<path d="M520 40 L590 66 V122 C590 162 558 186 520 200 C482 186 450 162 450 122 V66 Z" fill="none" '
                f'stroke="{a}" stroke-width="3"/><path class="draw" d="M490 120 L512 142 L554 98" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"/>')
    if kind == "receipt":
        lines = "".join(f'<rect class="bar" style="animation-delay:{i * .15}s" x="476" y="{70 + i * 22}" width="{88 - (i % 2) * 30}" height="6" rx="3" fill="{a}" fill-opacity=".7"/>' for i in range(5))
        return (f'<path d="M462 44 H578 V196 L566 186 L554 196 L542 186 L530 196 L518 186 L506 196 L494 186 L482 196 L470 186 L462 196 Z" '
                f'fill="none" stroke="{a}" stroke-width="3"/>{lines}<text x="540" y="186" font-family="{MONO}" font-size="22" fill="{a}">✓</text>')
    if kind == "chart":
        return (f'<path class="draw" d="M440 180 L478 150 L506 160 L536 110 L560 124 L600 60" fill="none" stroke="{a}" stroke-width="4" stroke-linejoin="round"/>'
                f'<circle cx="600" cy="60" r="7" fill="{a}"><animate attributeName="r" values="6;11;6" dur="2s" repeatCount="indefinite"/></circle>'
                f'<line x1="440" y1="196" x2="606" y2="196" stroke="{a}" stroke-opacity=".35" stroke-width="2"/>')
    if kind == "polygon":
        pts = [(460, 150), (500, 60), (580, 74), (606, 160), (530, 194)]
        poly = " ".join(f"{x},{y}" for x, y in pts)
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{a}"/>' for x, y in pts)
        return f'<polygon class="draw" points="{poly}" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-width="3"/>{dots}'
    if kind == "pulse":
        rings = "".join(
            f'<circle cx="526" cy="124" r="20" fill="none" stroke="{a}" stroke-width="2"><animate attributeName="r" values="18;78" dur="3s" begin="{i}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".9;0" dur="3s" begin="{i}s" repeatCount="indefinite"/></circle>' for i in range(3))
        return f'{rings}<circle cx="526" cy="124" r="14" fill="{a}"/>'
    if kind == "bars":
        hs = [60, 90, 70, 120, 100, 140]
        return "".join(
            f'<rect class="bar" style="animation-delay:{i * .12}s" x="{452 + i * 26}" y="{196 - hv}" width="16" height="{hv}" rx="4" fill="{a}" fill-opacity="{.35 + i * .1:.2f}"/>'
            for i, hv in enumerate(hs))
    return ""


def banner(key, p):
    w, h = 640, 240
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{p['title']}: {p['tag']}">
  <style>
    .draw{{stroke-dasharray:600;stroke-dashoffset:600;animation:draw 2.2s ease-out .2s forwards}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    .bar{{transform-box:fill-box;transform-origin:bottom;animation:grow .9s ease-out both}}
    @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
  </style>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070a12"/><stop offset="1" stop-color="{p['b']}"/></linearGradient>
    <pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".07"/></pattern>
  </defs>
  <rect width="{w}" height="{h}" rx="16" fill="url(#g)"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#d)"/>
  <text x="32" y="46" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{p['a']}">{p['event']}</text>
  <text x="30" y="104" font-family="{SANS}" font-size="44" font-weight="900" fill="#ffffff">{p['title']}</text>
  <text x="32" y="138" font-family="{SANS}" font-size="16" fill="#dfe6f5">{p['tag']}</text>
  <rect x="32" y="166" width="{24 + len(p['metric']) * 7.4:.0f}" height="30" rx="15" fill="{p['a']}" fill-opacity=".14" stroke="{p['a']}" stroke-opacity=".6"/>
  <text x="44" y="186" font-family="{MONO}" font-size="12.5" fill="{p['a']}">{p['metric']}</text>
  {motif(p['motif'], p['a'])}
</svg>"""


def orchestrate(mode):
    """Rank progression across the three HackerRank Orchestrate rounds (lower rank = higher on chart)."""
    t = THEMES[mode]
    w, h = 1000, 230
    rounds = [("June", 206, "Top 11.6%", "Damage-claim photo checker"),
              ("August", 27, "Top 1.4%", "WhatsApp notification router"),
              ("September", 84, "Top 2.7%", "Buy or Wait? money agent")]
    xs = [200, 500, 800]
    def y(rank):  # map rank 1..220 to 92..160
        return 92 + (rank / 220) * 68
    pts = [(x, y(r)) for x, (_, r, _, _) in zip(xs, rounds)]
    path = "M" + " L".join(f"{x:.0f} {yy:.0f}" for x, yy in pts)
    marks = []
    for (x, yy), (month, rank, pct, what) in zip(pts, rounds):
        best = rank == 27
        marks.append(f"""
  <circle cx="{x}" cy="{yy:.0f}" r="{11 if best else 8}" fill="{t['a'] if best else t['b']}"/>
  {'<circle cx="%d" cy="%.0f" r="11" fill="none" stroke="%s" stroke-width="2"><animate attributeName="r" values="11;24" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle>' % (x, yy, t['a']) if best else ''}
  <text x="{x}" y="{yy - 22:.0f}" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="{t['fg']}">#{rank}</text>
  <text x="{x}" y="196" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{t['sub']}">{month} · {pct}</text>
  <text x="{x}" y="215" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{t['dim']}">{what}</text>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="HackerRank Orchestrate 2026 ranks: June #206 (top 11.6%), August #27 (top 1.4%), September #84 (top 2.7%).">
  <style>
    .draw{{stroke-dasharray:900;stroke-dashoffset:900;animation:draw 2s ease-out forwards}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
  </style>{defs(t, w, h)}
  <text x="36" y="36" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{t['a']}">HACKERRANK ORCHESTRATE 2026 · 24-HOUR AI AGENT HACKATHON · 15,295 SIGNED UP</text>
  <path class="draw" d="{path}" fill="none" stroke="url(#ink)" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
  {''.join(marks)}
</svg>"""


def main():
    for mode in THEMES:
        write(f"header-{mode}.svg", header(mode))
        write(f"stats-{mode}.svg", stats(mode))
        write(f"orchestrate-{mode}.svg", orchestrate(mode))
    for key, p in PROJECTS.items():
        write(f"projects/{key}.svg", banner(key, p))
    print("assets written to", OUT)


if __name__ == "__main__":
    main()
