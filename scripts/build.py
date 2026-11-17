"""Builds the static MB-01 assets: hero board, serial monitor, divider, project cards.
Run:  python3 scripts/build.py
"""
import math
import os
import random

from mb import *  # noqa: F401,F403

rng = random.Random(11)
os.makedirs(ASSETS, exist_ok=True)


def write(name, content):
    with open(os.path.join(ASSETS, name), "w") as f:
        f.write(content)


# ═══════════════════════════════════════════════════════════════ HERO BOARD
def gamepad_icon(x, y):
    """Generic gamepad silkscreen outline (easter egg)."""
    c = f'stroke="{CREAM}" stroke-opacity="0.55" stroke-width="1.3" fill="none"'
    s = f'<path d="M{x} {y+8} q2 -10 14 -10 h20 q12 0 14 10 l3 12 q1 8 -6 8 q-5 0 -9 -7 h-24 q-4 7 -9 7 q-7 0 -6 -8 z" {c}/>'
    s += f'<path d="M{x+10} {y+7} h8 M{x+14} {y+3} v8" {c}/>'
    s += f'<circle cx="{x+37}" cy="{y+4}" r="1.6" fill="{CREAM}" fill-opacity="0.55"/><circle cx="{x+41}" cy="{y+8}" r="1.6" fill="{CREAM}" fill-opacity="0.55"/>'
    return s


def football_icon(cx, cy, r=11):
    c = f'stroke="{CREAM}" stroke-opacity="0.55" stroke-width="1.2" fill="none"'
    pts = " ".join(f"{cx + r*0.42*math.cos(math.radians(-90 + 72*i)):.1f},{cy + r*0.42*math.sin(math.radians(-90 + 72*i)):.1f}" for i in range(5))
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" {c}/><polygon points="{pts}" fill="{CREAM}" fill-opacity="0.45"/>'
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        s += f'<line x1="{cx + r*0.42*math.cos(a):.1f}" y1="{cy + r*0.42*math.sin(a):.1f}" x2="{cx + r*math.cos(a):.1f}" y2="{cy + r*math.sin(a):.1f}" {c}/>'
    return s


def pyramids_icon(x, y):
    c = f'stroke="{CREAM}" stroke-opacity="0.6" stroke-width="1.2" fill="none" stroke-linejoin="round"'
    return (f'<path d="M{x} {y} l12 -14 l12 14 z" {c}/><path d="M{x+16} {y} l9 -10 l9 10" {c}/>'
            f'<path d="M{x+12} {y-14} l-3 14" stroke="{CREAM}" stroke-opacity="0.3" stroke-width="1.2" fill="none"/>')


def hero():
    W, H = 1200, 700
    b = board(W, H)
    T = POWER_ON

    # ── bottom layer easter egg: Kuwait → Cairo (drawn first, under everything)
    kw = (150, 566)
    eg = (1050, 566)
    d_kw = f"M{kw[0]} {kw[1]} H330 L350 546 H850 L870 566 H{eg[0]}"
    b += trace(d_kw, T + 0.1, w=2, pulse=False, layer="bottom")
    b += (f'<path d="{d_kw}" pathLength="100" fill="none" stroke="{AMBER}" stroke-width="2" stroke-linecap="round" '
          f'stroke-dasharray="3 97" stroke-dashoffset="100" opacity="0" filter="url(#glow)">'
          f'<set attributeName="opacity" to="0.9" begin="{T+2.2}s"/>'
          f'<animate attributeName="stroke-dashoffset" values="100;0" dur="7s" begin="{T+2.2}s" repeatCount="indefinite"/></path>')
    for (x, y), lab in [(kw, "TP1 · KUWAIT"), (eg, "TP2 · CAIRO")]:
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="url(#gold)"/><circle cx="{x}" cy="{y}" r="2.5" fill="#050505"/>'
        b += text(x, y + 26, lab, size=10.5, anchor="middle", ls=2)
    b += text(360, 534, "NET KWT→CAI · BOTTOM LAYER", size=9.5, ls=2, opacity=0.75)

    # ── title block
    b += text(64, 92, "MB-01  ·  PERSONAL MAINBOARD  ·  REV 3", size=12, ls=3.2)
    b += text(60, 152, "MOHAB BADAWY", size=58, fill=CREAM, font=SANS, weight=700, ls=1)
    b += text(63, 186, "Think like a founder. Build like an engineer.", size=19, fill=ORANGE, font=SANS, weight=500, ls=0.2)
    b += text(64, 214, "CO-FOUNDER &amp; GM @ SOLVEN  ·  ECE @ AUC '28  ·  CAIRO, EG", size=11.5, ls=2.2)

    # ── status bank
    bx, by = 840, 64
    b += silk_box(bx, by, 300, 150)
    b += text(bx + 18, by + 28, "D1–D4 · SYSTEM STATUS", size=10.5, ls=2.4)
    b += led(bx + 30, by + 58, T + 2.3, "SOLVEN ········ LIVE")
    b += led(bx + 30, by + 84, T + 2.45, "NUDGE ········· BETA", color=AMBER)
    b += led(bx + 30, by + 110, T + 2.6, "CLINIC ········ LIVE")
    b += led(bx + 30, by + 136, T + 2.75, "AWS · TF ···· LOADING", color=AMBER, blink=1.1)

    # ── traces (under parts)
    core = (488, 262, 224, 206)             # substrate x,y,w,h
    cx0, cy0, cw, ch = core
    b += bus(cx0, [300, 313, 326], 296, [282, 295, 308], T + 0.5, rng)               # → U1
    b += bus(cx0, [400, 413, 426], 296, [432, 445, 458], T + 0.65, rng)              # → U2
    b += bus(cx0 + cw, [300, 313, 326], 904, [282, 295, 308], T + 0.8, rng)          # → U3
    b += bus(cx0 + cw, [400, 413, 426], 904, [432, 445, 458], T + 0.95, rng)         # → U4
    # core → status bank
    b += trace("M660 262 V238 L684 214 H804 L826 192 H840", T + 1.1, w=2.2, rng=rng)
    b += trace("M676 262 V246 L692 230 H812 L836 206 H840", T + 1.15, w=2.2, rng=rng)
    b += via(804, 214) + via(812, 230)
    # core → USB-C
    for i, x in enumerate([566, 586, 614, 634]):
        b += trace(f"M{x} {cy0+ch} V{600 + (i in (1, 2)) * 6} V626", T + 1.25 + i * 0.05, w=2.2, rng=rng)
    # core → crystal
    b += trace(f"M{cx0+cw} 446 H752 L772 466 H800", T + 1.3, w=2, pulse=False)
    b += trace(f"M{cx0+cw} 456 H744 L768 480 H800", T + 1.32, w=2, pulse=False)
    # core → title (decorative)

    # ── core: substrate + brushed IHS lid
    b += f'<g filter="url(#shadow)"><rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="8" fill="#17110c"/></g>'
    b += f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="8" fill="none" stroke="url(#gold)" stroke-opacity="0.35"/>'
    for i in range(10):  # die-side caps
        b += f'<rect x="{cx0 + 14 + i*20}" y="{cy0 + 7}" width="9" height="5" rx="1" fill="url(#gold)" opacity="0.8"/>'
        b += f'<rect x="{cx0 + 14 + i*20}" y="{cy0 + ch - 12}" width="9" height="5" rx="1" fill="url(#gold)" opacity="0.8"/>'
    lx, ly, lw, lh = cx0 + 16, cy0 + 20, cw - 32, ch - 40
    b += f'<g filter="url(#shadow)"><rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="7" fill="url(#lid)"/></g>'
    b += f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="7" fill="url(#brushed)"/>'
    b += f'<rect x="{lx+0.5}" y="{ly+0.5}" width="{lw-1}" height="{lh-1}" rx="6.5" fill="none" stroke="#ffffff" stroke-opacity="0.6"/>'
    # orange halo when powered
    b += (f'<rect x="{lx-6}" y="{ly-6}" width="{lw+12}" height="{lh+12}" rx="12" fill="none" stroke="{ORANGE}" stroke-width="3" opacity="0" filter="url(#softglow)">'
          f'<animate attributeName="opacity" values="0;0.9;0.45" keyTimes="0;0.3;1" begin="{T+0.3}s" dur="1.8s" fill="freeze"/></rect>')
    b += text(lx + 18, ly + 30, "MB-01 · CORE", size=10, fill=INK, ls=2.4)
    b += text(lx + 18, ly + 74, "MOHAB", size=40, fill=INK, font=SANS, weight=700, ls=3)
    b += text(lx + 18, ly + 96, "FOUNDER × ENGINEER", size=10.5, fill=INK, weight=600, ls=2.2)
    b += text(lx + 18, ly + 140, "CAIRO EG · 2026", size=9.5, fill=INK, ls=2)
    b += f'<path d="M{lx+lw-30} {ly+lh-20} l10 -14 l10 14 z" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    b += text(cx0, cy0 - 14, "U0 · MOHAB.CORE", size=11, ls=2)

    # ── peripheral chips
    b += qfp(76, 254, 210, 86, "U1 · SOLVEN", "SOLVEN", "SOFTWARE · AI AGENTS", accent=True)
    b += qfp(76, 404, 210, 86, "U2 · NUDGE", "NUDGE", "STUDY PLANNER")
    b += qfp(914, 254, 210, 86, "U3 · CLINIC", "CLINIC", "BOOKING PLATFORM")
    b += qfp(914, 404, 210, 86, "U4 · CLOUD", "CLOUD", "AWS · AZURE · IaC")

    # ── crystal oscillator
    b += f'<g filter="url(#shadow)"><rect x="800" y="458" width="64" height="30" rx="15" fill="url(#lid)"/></g>'
    b += f'<rect x="800" y="458" width="64" height="30" rx="15" fill="url(#brushed)"/>'
    b += text(832, 477, "24.000", size=9, fill=INK, anchor="middle", weight=600, ls=1)
    b += text(800, 450, "Y1", size=9.5, ls=1.5)

    # ── passives
    for x, y, ref in [(330, 360, "C1"), (360, 360, "C2"), (850, 360, "C3"), (420, 470, "R1"), (330, 470, "R2"), (440, 600, "C4"), (740, 600, "C5")]:
        b += smd(x, y, ref)

    # ── USB-C
    ux, uy = 560, 626
    b += f'<g filter="url(#shadow)"><rect x="{ux}" y="{uy}" width="80" height="50" rx="10" fill="url(#lid)"/></g>'
    b += f'<rect x="{ux}" y="{uy}" width="80" height="50" rx="10" fill="url(#brushed)"/>'
    b += f'<rect x="{ux+14}" y="{uy+30}" width="52" height="14" rx="7" fill="#111"/>'
    b += f'<rect x="{ux+22}" y="{uy+35}" width="36" height="4" rx="2" fill="#2a2a2c"/>'
    b += text(ux - 12, uy + 30, "J1 · USB-C", size=10, anchor="end", ls=2)

    # ── easter eggs on silkscreen
    b += gamepad_icon(200, 612)
    b += text(262, 624, "SW1 · IDLE MODE", size=9.5, ls=2)
    b += football_icon(896, 618)
    b += text(916, 622, "INT0 · MATCHDAY", size=9.5, ls=2)

    # ── footer silkscreen
    b += pyramids_icon(66, 668)
    b += text(110, 666, "ASSEMBLED IN CAIRO, EGYPT", size=10.5, ls=2.4)
    b += text(1134, 666, "FW mohab.os 3.0 · DO NOT POWER DOWN", size=10.5, anchor="end", ls=2.4)

    # ── PWR LED (first thing to light)
    b += led(bx + 236, by + 24, T, "PWR", size=10)

    # ── power-on flash veil
    b += (f'<rect width="{W}" height="{H}" rx="24" fill="#000" opacity="0.55">'
          f'<animate attributeName="opacity" values="0.55;0.55;0" keyTimes="0;0.2;1" dur="{T+0.9}s" fill="freeze"/></rect>')
    return svg(W, H, b, "MB-01: Mohab Badawy's personal mainboard")


# ═══════════════════════════════════════════════════════════ SERIAL MONITOR
def serial():
    W = 1200
    rows = [
        ("> ", "powering on MB-01 ...", "", CREAM_DIM),
        ("[ OK ] ", "mohab.core .......... ", "founder mode + engineer mode", ORANGE),
        ("[ OK ] ", "solven .............. ", "co-founder &amp; GM · clients in EG + GCC", ORANGE),
        ("[ OK ] ", "nudge ............... ", "studynudge.app · beta", ORANGE),
        ("[ OK ] ", "dralaahussien.com ... ", "live · booking + staff dashboard", ORANGE),
        ("[ OK ] ", "cert.az-900 ......... ", "verified", ORANGE),
        ("[ .. ] ", "aws-saa · terraform . ", "compiling", AMBER),
    ]
    fs, lh, top = 16.5, 30, 96
    cw = fs * 0.6
    H = top + lh * len(rows) + 46
    b = f'<rect width="{W}" height="{H}" rx="20" fill="#08080a"/>'
    b += f'<rect width="{W}" height="{H}" rx="20" filter="url(#grain)"/>'
    b += f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="19.5" fill="none" stroke="url(#gold)" stroke-opacity="0.45" stroke-width="1.5"/>'
    b += f'<path d="M1 54 H{W-1}" stroke="{CREAM}" stroke-opacity="0.08"/>'
    b += (f'<circle cx="34" cy="28" r="5" fill="{ORANGE}" filter="url(#glow)">'
          f'<animate attributeName="opacity" values="1;0.25;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    b += text(52, 32, "SERIAL MONITOR  ·  /dev/tty.mb01  ·  115200 baud", size=12, ls=2.6)
    b += text(W - 32, 32, "mohab@cairo", size=12, anchor="end", ls=2)

    clips = ""
    t0, step = 0.5, 0.7
    for i, (tag, key, val, col) in enumerate(rows):
        y = top + i * lh
        n = len(tag) + len(key) + len(val.replace("&amp;", "&"))
        begin = t0 + i * step
        clips += (f'<clipPath id="r{i}"><rect x="40" y="{y-22}" height="{lh}" width="0">'
                  f'<animate attributeName="width" from="0" to="{n*cw+12:.0f}" begin="{begin}s" dur="0.5s" fill="freeze"/></rect></clipPath>')
        b += (f'<g clip-path="url(#r{i})"><text x="44" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
              f'<tspan fill="{col}" font-weight="600">{tag}</tspan><tspan fill="{CREAM}">{key}</tspan>'
              f'<tspan fill="{CREAM_DIM}">{val}</tspan></text></g>')
    y = top + len(rows) * lh
    pb = t0 + len(rows) * step + 0.2
    b += (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{pb}s"/>'
          f'<text x="44" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
          f'<tspan fill="{ORANGE}" font-weight="600">mohab@cairo</tspan><tspan fill="{CREAM}">:~$ </tspan></text>'
          f'<rect x="{44 + 15*cw:.1f}" y="{y-14}" width="9" height="18" fill="{ORANGE}">'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect></g>')
    return svg(W, H, b, "Serial monitor boot log", fonts=("plex400", "plex600"), extra_defs=f"<defs>{clips}</defs>")


# ═══════════════════════════════════════════════════════════════ DIVIDER
def divider():
    W, H = 1200, 30
    b = trace("M8 15 H540 L552 7 H648 L660 15 H1192", 0.2, w=2, rng=rng, pulse_dur=4)
    b += via(552, 7, 4) + via(648, 7, 4)
    return svg(W, H, b, "", fonts=())


# ═══════════════════════════════════════════════════════════ PROJECT CARDS
def card(fname, ref, name, pitch, rows, status, scol, link, name_size=30):
    W, H = 590, 300
    b = board(W, H, holes=False, r=20)
    b += trace("M0 150 H26 L44 132 H60", 0.3, w=2.2, rng=rng)
    b += trace("M0 172 H34 L48 186 H60", 0.4, w=2.2, rng=rng)
    b += via(26, 150, 4.5) + via(34, 172, 4.5)
    x, y, w, h = 70, 58, 492, 214
    # leads top & bottom
    for px in range(x + 18, x + w - 10, 15):
        for py in (y - 11, y + h + 1):
            b += f'<rect x="{px-3}" y="{py}" width="6" height="10" rx="1" fill="url(#gold)" opacity="0.8"/>'
            b += f'<rect x="{px-1.8}" y="{py+1}" width="3.6" height="8" fill="url(#tin)"/>'
    b += f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="url(#pkg)"/></g>'
    b += f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="6.5" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>'
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" filter="url(#grain)" opacity="0.6"/>'
    b += f'<circle cx="{x+15}" cy="{y+15}" r="4.5" fill="#09090a" stroke="#ffffff" stroke-opacity="0.06"/>'
    b += text(x, 36, ref, size=11, ls=2.4)
    b += text(x + w, 36, f"{link} ↗", size=11, anchor="end", fill=CREAM, ls=1.4)
    b += text(x + 30, y + 52, name, size=name_size, fill=CREAM, font=SANS, weight=700, ls=1.2)
    b += text(x + 30, y + 78, pitch, size=14.5, fill=ORANGE, font=SANS, weight=500, ls=0.2)
    b += f'<path d="M{x+30} {y+96} H{x+w-30}" stroke="{CREAM}" stroke-opacity="0.09"/>'
    for i, (k, v) in enumerate(rows):
        yy = y + 122 + i * 24
        b += text(x + 30, yy, k, size=10.5, ls=2)
        b += text(x + 118, yy, v, size=12.5, fill=CREAM, ls=0.2)
    b += led(x + w - 98, y + 30, 0.6, status, color=scol, blink=2.6 if status == "BETA" else None, size=11)
    write(fname + ".svg", svg(W, H, b, f"{name}: {pitch}"))


write("board.svg", hero())
write("serial.svg", serial())
write("trace.svg", divider())

card("u1-solven", "U1 · CO-FOUNDER &amp; GM", "Solven", "Software, automation &amp; AI agents for SMEs",
     [("PROBLEM", "Manual work quietly eating time &amp; money"),
      ("SHIPS", "Websites · apps · workflows · AI agents"),
      ("MARKET", "SMEs across Egypt + the GCC"),
      ("STACK", "Next.js · FastAPI · n8n · HubSpot")], "LIVE", ORANGE, "solvenhq.com")
card("u2-nudge", "U2 · CO-FOUNDER", "Nudge", "A cozy study world for university students",
     [("FOR", "Students who'd rather plan than cram"),
      ("SHIPS", "Study planner · day / night desk themes"),
      ("STAGE", "Web beta · pitching at AUC"),
      ("NEXT", "App Store + Google Play")], "BETA", AMBER, "studynudge.app")
card("u3-clinic", "U3 · CLIENT BUILD", "Clinic Platform", "A pediatric &amp; lactation practice, end to end",
     [("FOR", "Dr. Alaa Hussien's practice"),
      ("SHIPS", "Public site · online booking"),
      ("OPS", "Private staff dashboard"),
      ("INFRA", "Custom domain · live on Render")], "LIVE", ORANGE, "dralaahussien.com", name_size=28)
card("u4-ops", "U4 · LIVE DEMO", "Ops Control Engine", "An operations command center for SMEs",
     [("WHAT", "Real-time ops view on simulated data"),
      ("WHY", "Clients see it working before they buy"),
      ("BY", "Solven"),
      ("TRY", "Open it in your browser")], "DEMO", AMBER, "demo.solvenhq.com", name_size=28)
print("built")
