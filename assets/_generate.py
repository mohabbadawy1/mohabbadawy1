"""Generates the circuit-board SVG assets for Mohab's GitHub profile README."""
import os, random

random.seed(7)
OUT = "/home/claude/profile/assets"
os.makedirs(OUT, exist_ok=True)

BOARD = "#0a1712"
BOARD2 = "#0e2019"
COPPER = "#b9853a"
COPPER_DIM = "#5e4520"
PULSE = "#ffd98a"
SILK = "#e8efe9"
SILK_DIM = "#8fa89a"
CHIP = "#121614"
LED_G = "#3dff8f"
LED_A = "#ffb547"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

DEFS = f"""
<defs>
  <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="#173528"/>
  </pattern>
  <radialGradient id="vign" cx="50%" cy="45%" r="75%">
    <stop offset="0%" stop-color="{BOARD2}"/>
    <stop offset="100%" stop-color="{BOARD}"/>
  </radialGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="chipg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#1b201d"/>
    <stop offset="100%" stop-color="#0d100e"/>
  </linearGradient>
</defs>
"""


def board_bg(w, h, holes=True):
    s = f'<rect width="{w}" height="{h}" rx="22" fill="url(#vign)"/>'
    s += f'<rect width="{w}" height="{h}" rx="22" fill="url(#dots)"/>'
    s += f'<rect x="8" y="8" width="{w-16}" height="{h-16}" rx="16" fill="none" stroke="#1f4434" stroke-width="1.5"/>'
    if holes:
        for x, y in [(30, 30), (w - 30, 30), (30, h - 30), (w - 30, h - 30)]:
            s += f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{COPPER}" stroke-width="3"/>'
            s += f'<circle cx="{x}" cy="{y}" r="6" fill="#050a07"/>'
    return s


def trace(d, w=3, pulse=True, dur=None, begin=None):
    """Copper trace plus an animated signal pulse travelling along it."""
    s = f'<path d="{d}" fill="none" stroke="{COPPER_DIM}" stroke-width="{w+3}" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" fill="none" stroke="{COPPER}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    if pulse:
        dur = dur or round(random.uniform(2.2, 4.2), 2)
        begin = begin if begin is not None else round(random.uniform(0, 3), 2)
        s += (f'<path d="{d}" pathLength="100" fill="none" stroke="{PULSE}" stroke-width="{w}" '
              f'stroke-linecap="round" stroke-dasharray="6 94" stroke-dashoffset="100" filter="url(#glow)">'
              f'<animate attributeName="stroke-dashoffset" values="100;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')
    return s


def via(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="6" fill="{COPPER}"/>'
            f'<circle cx="{x}" cy="{y}" r="2.5" fill="#050a07"/>')


def pins(x, y, w, h, step=14, plen=9, sides="lrtb"):
    s = ""
    if "l" in sides or "r" in sides:
        for py in range(int(y + 14), int(y + h - 8), step):
            if "l" in sides:
                s += f'<rect x="{x-plen}" y="{py-2.5}" width="{plen}" height="5" fill="#c9ccc9"/>'
            if "r" in sides:
                s += f'<rect x="{x+w}" y="{py-2.5}" width="{plen}" height="5" fill="#c9ccc9"/>'
    if "t" in sides or "b" in sides:
        for px in range(int(x + 14), int(x + w - 8), step):
            if "t" in sides:
                s += f'<rect x="{px-2.5}" y="{y-plen}" width="5" height="{plen}" fill="#c9ccc9"/>'
            if "b" in sides:
                s += f'<rect x="{px-2.5}" y="{y+h}" width="5" height="{plen}" fill="#c9ccc9"/>'
    return s


def chip(x, y, w, h, ref, name, sub, sides="lr", name_size=22):
    s = pins(x, y, w, h, sides=sides)
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#chipg)" stroke="#2a302c" stroke-width="1.5"/>'
    s += f'<circle cx="{x+12}" cy="{y+12}" r="3.5" fill="#2c332f"/>'
    s += f'<text x="{x+w/2}" y="{y+h/2+2}" text-anchor="middle" font-family="{MONO}" font-size="{name_size}" font-weight="700" fill="{SILK}" letter-spacing="2">{name}</text>'
    s += f'<text x="{x+w/2}" y="{y+h/2+22}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{SILK_DIM}" letter-spacing="1.5">{sub}</text>'
    s += f'<text x="{x}" y="{y-14}" font-family="{MONO}" font-size="12" fill="{SILK_DIM}" letter-spacing="1">{ref}</text>'
    return s


def led(x, y, color, label, dur, begin):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="{color}" opacity="0.18"/>'
            f'<circle cx="{x}" cy="{y}" r="5" fill="{color}" filter="url(#glow)">'
            f'<animate attributeName="opacity" values="1;1;0.25;1" keyTimes="0;0.6;0.8;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>'
            f'<text x="{x+16}" y="{y+4}" font-family="{MONO}" font-size="12" fill="{SILK}" letter-spacing="1.5">{label}</text>')


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<title>{label}</title>{DEFS}{body}</svg>')


# ---------------------------------------------------------------- HERO BOARD
def hero():
    W, H = 1200, 540
    b = board_bg(W, H)

    # Silkscreen title block
    b += f'<text x="60" y="88" font-family="{MONO}" font-size="13" fill="{SILK_DIM}" letter-spacing="3">MB-01 // PERSONAL MAINBOARD</text>'
    b += f'<text x="58" y="132" font-family="{MONO}" font-size="40" font-weight="800" fill="{SILK}" letter-spacing="4">MOHAB BADAWY</text>'
    b += f'<text x="60" y="160" font-family="{MONO}" font-size="13" fill="{SILK_DIM}" letter-spacing="2">ECE @ AUC · FOUNDER · CLOUD &amp; AUTOMATION</text>'

    # Status LEDs, top right
    b += f'<text x="860" y="88" font-family="{MONO}" font-size="12" fill="{SILK_DIM}" letter-spacing="3">STATUS</text>'
    b += led(868, 114, LED_G, "SOLVEN · LIVE", 2.6, 0)
    b += led(868, 140, LED_G, "NUDGE · BETA", 3.1, 0.7)
    b += led(1022, 114, LED_G, "CLINIC · LIVE", 2.8, 1.3)
    b += led(1022, 140, LED_A, "AWS · LOADING", 1.4, 0.2)

    # Central MCU
    cx, cy, cw, ch = 470, 225, 260, 150
    # traces first (under chips)
    # left side -> U1 (Solven) and U2 (Nudge)
    t = ""
    t += trace("M470 245 H400 V232 H270")
    t += trace("M470 265 H385 V252 H270")
    t += trace("M470 335 H385 V382 H270")
    t += trace("M470 355 H400 V402 H270")
    # right side -> U3 (Clinic) and U4 (Cloud)
    t += trace("M730 245 H800 V232 H930")
    t += trace("M730 265 H815 V252 H930")
    t += trace("M730 335 H815 V382 H930")
    t += trace("M730 355 H800 V402 H930")
    # top -> status block
    t += trace("M660 225 V196 H830 V114 H852", w=2.5)
    t += trace("M690 225 V206 H840 V140 H852", w=2.5)
    # bottom -> connector J1
    for i, x in enumerate(range(512, 700, 36)):
        t += trace(f"M{x} 375 V{430 + (i % 2) * 8} H{x + (600 - x) * 0.0} V462", w=2.5)
    b += t
    for v in [(400, 232), (385, 252), (385, 382), (400, 402), (800, 232), (815, 252), (815, 382), (800, 402), (830, 196), (840, 206)]:
        b += via(*v)

    b += chip(cx, cy, cw, ch, "U0 · CORE", "MOHAB.B", "ECE '28 · CAIRO, EG", sides="lrtb", name_size=30)
    b += chip(70, 202, 200, 80, "U1", "SOLVEN", "SOFTWARE · AI AGENTS")
    b += chip(70, 352, 200, 80, "U2", "NUDGE", "STUDY PLANNER")
    b += chip(930, 202, 200, 80, "U3", "CLINIC", "BOOKING PLATFORM")
    b += chip(930, 352, 200, 80, "U4", "CLOUD", "AWS · AZURE · IaC")

    # Connector header J1
    b += f'<rect x="490" y="462" width="220" height="34" rx="4" fill="#111" stroke="#2a302c"/>'
    for i, x in enumerate(range(512, 700, 36)):
        b += f'<rect x="{x-8}" y="471" width="16" height="16" fill="{COPPER}"/><circle cx="{x}" cy="479" r="3.5" fill="#050a07"/>'
    b += f'<text x="490" y="455" font-family="{MONO}" font-size="12" fill="{SILK_DIM}" letter-spacing="1">J1 · I/O</text>'

    # little passives scattered
    for (x, y, lab) in [(330, 300, "R1"), (850, 300, "R2"), (790, 470, "C2"), (360, 470, "R3")]:
        b += f'<rect x="{x}" y="{y}" width="26" height="12" rx="2" fill="#3a2a17" stroke="{COPPER}" stroke-width="1"/>'
        b += f'<text x="{x}" y="{y-6}" font-family="{MONO}" font-size="10" fill="{SILK_DIM}">{lab}</text>'

    # bottom silkscreen
    b += f'<text x="60" y="505" font-family="{MONO}" font-size="11" fill="{SILK_DIM}" letter-spacing="2">REV 2026.11 · ASSEMBLED IN CAIRO</text>'
    b += f'<text x="1140" y="505" text-anchor="end" font-family="{MONO}" font-size="11" fill="{SILK_DIM}" letter-spacing="2">FW: hoba v3.0 · DO NOT POWER DOWN</text>'
    return svg(W, H, b, "Mohab Badawy - personal mainboard")


# ---------------------------------------------------------------- SERIAL MONITOR
def terminal():
    W = 1200
    lines = [
        ("> ", "booting MB-01 ...", None, None),
        ("[ OK ] ", "ece.auc ............... ", "junior, class of 2028", LED_G),
        ("[ OK ] ", "solven ................ ", "co-founder &amp; GM · online", LED_G),
        ("[ OK ] ", "nudge ................. ", "studynudge.app · beta", LED_G),
        ("[ OK ] ", "dralaahussien.com ..... ", "deployed · render", LED_G),
        ("[ OK ] ", "cert.az-900 ........... ", "verified", LED_G),
        ("[ .. ] ", "aws-saa + terraform ... ", "compiling", LED_A),
    ]
    lh, top = 30, 92
    H = top + lh * (len(lines) + 1) + 6
    fs = 17
    cw = fs * 0.602
    b = f'<rect width="{W}" height="{H}" rx="18" fill="#070d0a"/>'
    b += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="#1f4434" stroke-width="1.5"/>'
    b += f'<rect x="1" y="1" width="{W-2}" height="50" rx="17" fill="#0c1913"/><rect x="1" y="34" width="{W-2}" height="17" fill="#0c1913"/>'
    b += f'<circle cx="32" cy="26" r="6" fill="{LED_G}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>'
    b += f'<text x="50" y="31" font-family="{MONO}" font-size="13" fill="{SILK_DIM}" letter-spacing="3">SERIAL MONITOR · /dev/tty.mb01 · 115200 baud</text>'
    b += f'<text x="{W-32}" y="31" text-anchor="end" font-family="{MONO}" font-size="13" fill="{SILK_DIM}" letter-spacing="2">hoba@cairo</text>'

    t0, step = 0.4, 0.75
    clips = ""
    for i, (tag, key, val, col) in enumerate(lines):
        y = top + i * lh
        n = len(tag) + len(key.replace("&amp;", "&")) + (len(val.replace("&amp;", "&")) if val else 0)
        wfull = n * cw + 10
        begin = t0 + i * step
        clips += (f'<clipPath id="c{i}"><rect x="40" y="{y-22}" height="{lh}" width="0">'
                  f'<animate attributeName="width" from="0" to="{wfull:.0f}" begin="{begin}s" dur="0.55s" fill="freeze"/></rect></clipPath>')
        tagcol = col if col else SILK_DIM
        txt = (f'<text x="44" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
               f'<tspan fill="{tagcol}">{tag}</tspan><tspan fill="{SILK}">{key}</tspan>')
        if val:
            txt += f'<tspan fill="{PULSE}">{val}</tspan>'
        txt += '</text>'
        b += f'<g clip-path="url(#c{i})">{txt}</g>'
    # prompt + blinking cursor
    y = top + len(lines) * lh
    pb = t0 + len(lines) * step + 0.3
    prompt = "hoba@cairo:~$ "
    b += (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{pb}s" dur="0.01s" fill="freeze"/>'
          f'<text x="44" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve"><tspan fill="{LED_G}">hoba@cairo</tspan><tspan fill="{SILK}">:~$ </tspan></text>'
          f'<rect x="{44 + len(prompt)*cw:.1f}" y="{y-15}" width="10" height="19" fill="{SILK}">'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect></g>')
    return svg(W, H, f"<defs>{clips}</defs>" + b, "Serial monitor boot log")


# ---------------------------------------------------------------- PROJECT CARDS
def card(fname, ref, name, tagline, lines, status, status_col, link):
    W, H = 590, 250
    b = board_bg(W, H, holes=False)
    # trace entering from left with pulse
    b += trace("M0 125 H40 V95 H70", w=2.5, dur=2.6)
    b += trace("M0 160 H52 V175 H70", w=2.5, dur=3.4, begin=1)
    b += via(40, 95) + via(52, 175)
    # chip
    x, y, w, h = 70, 54, 490, 160
    b += pins(x, y, w, h, step=16, plen=8, sides="tb")
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="url(#chipg)" stroke="#2a302c" stroke-width="1.5"/>'
    b += f'<circle cx="{x+14}" cy="{y+14}" r="4" fill="#2c332f"/>'
    b += f'<text x="{x}" y="34" font-family="{MONO}" font-size="12" fill="{SILK_DIM}" letter-spacing="2">{ref}</text>'
    b += f'<text x="{x+w}" y="34" text-anchor="end" font-family="{MONO}" font-size="12" fill="{SILK_DIM}" letter-spacing="1">{link} ↗</text>'
    b += f'<text x="{x+30}" y="{y+48}" font-family="{MONO}" font-size="26" font-weight="800" fill="{SILK}" letter-spacing="3">{name}</text>'
    b += f'<text x="{x+30}" y="{y+72}" font-family="{MONO}" font-size="13" fill="{PULSE}" letter-spacing="0.5">{tagline}</text>'
    for i, ln in enumerate(lines):
        b += f'<text x="{x+30}" y="{y+100+i*20}" font-family="{MONO}" font-size="12.5" fill="{SILK_DIM}">› {ln}</text>'
    # status LED
    b += (f'<circle cx="{x+w-92}" cy="{y+h-24}" r="5" fill="{status_col}" filter="url(#glow)">'
          f'<animate attributeName="opacity" values="1;1;0.3;1" keyTimes="0;0.6;0.8;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    b += f'<text x="{x+w-80}" y="{y+h-20}" font-family="{MONO}" font-size="12" fill="{SILK}" letter-spacing="2">{status}</text>'
    open(f"{OUT}/{fname}.svg", "w").write(svg(W, H, b, f"{name} - {tagline}"))


# ---------------------------------------------------------------- DIVIDER
def divider():
    W, H = 1200, 34
    b = trace("M10 17 H560 V10 H640 V24 H1190", w=2.5, dur=3.5, begin=0)
    b += via(560, 10) + via(640, 24)
    return svg(W, H, b, "divider")


open(f"{OUT}/board.svg", "w").write(hero())
open(f"{OUT}/serial.svg", "w").write(terminal())
open(f"{OUT}/trace.svg", "w").write(divider())

card("u1-solven", "U1 · CO-FOUNDER &amp; GM", "SOLVEN", "Software, automation &amp; AI agents for SMEs",
     ["Egypt + GCC clients · websites, apps, workflows", "Multi-agent systems on one shared brain",
      "Next.js · FastAPI · n8n · HubSpot"], "LIVE", LED_G, "solvenhq.com")
card("u2-nudge", "U2 · CO-FOUNDER", "NUDGE", "A cozy study world for university students",
     ["Plans your study time so you don't have to", "Day-desk / night-desk themes",
      "Started at AUC · built to scale beyond it"], "BETA", LED_G, "studynudge.app")
card("u3-clinic", "U3 · CLIENT BUILD", "CLINIC PLATFORM", "Pediatric &amp; lactation practice, end to end",
     ["Public site + online booking", "Private staff dashboard on its own subdomain",
      "Custom domain · deployed on Render"], "LIVE", LED_G, "dralaahussien.com")
card("u4-ops", "U4 · LIVE DEMO", "OPS CONTROL ENGINE", "Operations command center, running on sim data",
     ["Real-time ops view built for SMEs", "Shows what Solven ships before clients commit",
      "Try it in the browser"], "DEMO", LED_A, "demo.solvenhq.com")
print("ok")
