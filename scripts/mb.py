"""MB-01 drawing kit: shared materials, fonts and parts for Mohab's profile SVGs.

Matte-black solder mask, orange copper, ENIG gold pads, brushed-metal lids.
All animation is SMIL so it runs inside GitHub's <img> rendering (no JS).
"""
import base64
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ── palette ────────────────────────────────────────────────────────────────
MASK = "#0b0b0c"          # matte black solder mask
MASK_HI = "#141416"
COPPER_OFF = "#2b1a10"    # copper seen through the mask, unpowered
ORANGE = "#ff5a1f"        # powered trace
ORANGE_HOT = "#ffc08a"    # signal pulse
AMBER = "#ffa23a"
CREAM = "#f1e8d8"         # silkscreen
CREAM_DIM = "#8d8473"
INK = "#3f4044"           # laser etch on metal

SANS = "'SG', 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif"
MONO = "'PX', 'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace"

POWER_ON = 0.25           # seconds before the board starts lighting up


def _font(name):
    with open(os.path.join(HERE, "fonts", name + ".woff2"), "rb") as f:
        return base64.b64encode(f.read()).decode()


def fonts_css(*which):
    faces = {
        "sg700": ("SG", 700), "sg500": ("SG", 500),
        "plex400": ("PX", 400), "plex600": ("PX", 600),
    }
    css = ""
    for w in which:
        fam, wt = faces[w]
        css += (f"@font-face{{font-family:'{fam}';font-weight:{wt};"
                f"src:url(data:font/woff2;base64,{_font(w)}) format('woff2');}}")
    return f"<style>{css}</style>"


DEFS = f"""
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.055 0"/>
  </filter>
  <radialGradient id="sheen" cx="30%" cy="0%" r="110%">
    <stop offset="0%" stop-color="#1d1d20"/>
    <stop offset="55%" stop-color="{MASK}"/>
    <stop offset="100%" stop-color="#060607"/>
  </radialGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softglow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="7"/>
  </filter>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
    <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity="0.75"/>
  </filter>
  <linearGradient id="pkg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#232326"/>
    <stop offset="100%" stop-color="#0f0f11"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f6dc98"/>
    <stop offset="50%" stop-color="#c99a3e"/>
    <stop offset="100%" stop-color="#e9c574"/>
  </linearGradient>
  <linearGradient id="tin" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#eeeeef"/>
    <stop offset="100%" stop-color="#8e8f93"/>
  </linearGradient>
  <linearGradient id="lid" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f2f2f3"/>
    <stop offset="35%" stop-color="#b9babd"/>
    <stop offset="60%" stop-color="#dcdde0"/>
    <stop offset="100%" stop-color="#9c9da1"/>
  </linearGradient>
  <pattern id="brushed" width="400" height="3" patternUnits="userSpaceOnUse">
    <rect width="400" height="1" fill="#ffffff" opacity="0.10"/>
    <rect y="2" width="400" height="1" fill="#000000" opacity="0.06"/>
  </pattern>
  <linearGradient id="cap" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#d9d9db"/><stop offset="18%" stop-color="#9a9a9e"/>
    <stop offset="19%" stop-color="#6b4a2b"/><stop offset="81%" stop-color="#4f3520"/>
    <stop offset="82%" stop-color="#9a9a9e"/><stop offset="100%" stop-color="#d9d9db"/>
  </linearGradient>
</defs>
"""


def svg(w, h, body, label, fonts=("sg700", "sg500", "plex400", "plex600"), extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label}</title>'
            f'{fonts_css(*fonts)}{DEFS}{extra_defs}{body}</svg>')


# ── board ──────────────────────────────────────────────────────────────────
def board(w, h, holes=True, r=24):
    s = f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#sheen)"/>'
    s += f'<rect width="{w}" height="{h}" rx="{r}" filter="url(#grain)"/>'
    # gold edge plating + inner keep-out line
    s += f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="{r-1}" fill="none" stroke="url(#gold)" stroke-width="1.5" opacity="0.55"/>'
    s += f'<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="{r-8}" fill="none" stroke="{CREAM}" stroke-opacity="0.07" stroke-dasharray="2 6"/>'
    if holes:
        for x, y in [(34, 34), (w - 34, 34), (34, h - 34), (w - 34, h - 34)]:
            s += f'<circle cx="{x}" cy="{y}" r="13" fill="url(#gold)"/>'
            s += f'<circle cx="{x}" cy="{y}" r="7.5" fill="#030303"/>'
            for a in range(8):
                import math
                vx, vy = x + 19 * math.cos(a * math.pi / 4), y + 19 * math.sin(a * math.pi / 4)
                s += f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="1.6" fill="url(#gold)" opacity="0.8"/>'
    return s


def text(x, y, t, size=12, fill=CREAM_DIM, font=MONO, weight=400, anchor="start", ls=1.5, opacity=1):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{opacity}">{t}</text>')


# ── traces ─────────────────────────────────────────────────────────────────
def trace(d, t_on, w=2.6, pulse=True, rng=random, layer="top", pulse_dur=None):
    """A copper trace: dark under the mask, lights up orange at t_on, then carries pulses."""
    if layer == "bottom":
        return (f'<path d="{d}" fill="none" stroke="{COPPER_OFF}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 0" opacity="0.9"/>'
                f'<path d="{d}" pathLength="100" fill="none" stroke="{ORANGE}" stroke-opacity="0.35" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100">'
                f'<animate attributeName="stroke-dashoffset" from="100" to="0" begin="{t_on}s" dur="1.6s" fill="freeze"/></path>')
    s = f'<path d="{d}" fill="none" stroke="{COPPER_OFF}" stroke-width="{w+2.4}" stroke-linecap="round" stroke-linejoin="round"/>'
    s += (f'<path d="{d}" pathLength="100" fill="none" stroke="{ORANGE}" stroke-width="{w}" stroke-linecap="round" '
          f'stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100">'
          f'<animate attributeName="stroke-dashoffset" from="100" to="0" begin="{t_on}s" dur="0.7s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/></path>')
    if pulse:
        dur = pulse_dur or round(rng.uniform(2.4, 4.6), 2)
        begin = round(t_on + 0.8 + rng.uniform(0, 2.5), 2)
        s += (f'<path d="{d}" pathLength="100" fill="none" stroke="{ORANGE_HOT}" stroke-width="{w}" stroke-linecap="round" '
              f'stroke-dasharray="5 95" stroke-dashoffset="100" opacity="0" filter="url(#glow)">'
              f'<set attributeName="opacity" to="1" begin="{begin}s"/>'
              f'<animate attributeName="stroke-dashoffset" values="100;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')
    return s


def via(x, y, r=5.5):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.42:.2f}" fill="#050505"/>')


def bus(x0, ys0, x1, ys1, t_on, rng, w=2.4):
    """Parallel traces with 45-degree bends, PCB-router style."""
    s, vias = "", []
    n = len(ys0)
    sign = 1 if x1 > x0 else -1
    mid = (x0 + x1) / 2
    for i, (a, b) in enumerate(zip(ys0, ys1)):
        dy = b - a
        # stagger bend points so diagonals stay parallel
        k = (i - (n - 1) / 2) * 10 * (1 if dy > 0 else -1) * sign
        bx = mid - sign * abs(dy) / 2 + k
        ex = bx + sign * abs(dy)
        d = f"M{x0} {a} H{bx:.1f} L{ex:.1f} {b} H{x1}"
        s += trace(d, t_on + i * 0.08, w=w, rng=rng)
    return s


# ── parts ──────────────────────────────────────────────────────────────────
def qfp(x, y, w, h, ref, name, sub, sides="lr", name_size=24, accent=False, pitch=13):
    """Quad-flat package chip with tinned leads on gold pads."""
    s = ""
    pl = 10
    if "l" in sides or "r" in sides:
        for py in range(int(y + 14), int(y + h - 9), pitch):
            for side in "lr":
                if side not in sides:
                    continue
                px = x - pl - 2 if side == "l" else x + w + 2
                s += f'<rect x="{px-1}" y="{py-3.5}" width="{pl+2}" height="7" rx="1" fill="url(#gold)" opacity="0.85"/>'
                s += f'<rect x="{px + (2 if side=="l" else 0)}" y="{py-2}" width="{pl}" height="4" fill="url(#tin)"/>'
    if "t" in sides or "b" in sides:
        for px in range(int(x + 14), int(x + w - 9), pitch):
            for side in "tb":
                if side not in sides:
                    continue
                py = y - pl - 2 if side == "t" else y + h + 2
                s += f'<rect x="{px-3.5}" y="{py-1}" width="7" height="{pl+2}" rx="1" fill="url(#gold)" opacity="0.85"/>'
                s += f'<rect x="{px-2}" y="{py + (2 if side=="t" else 0)}" width="4" height="{pl}" fill="url(#tin)"/>'
    s += f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#pkg)"/></g>'
    s += f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="4.5" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" filter="url(#grain)" opacity="0.6"/>'
    s += f'<circle cx="{x+13}" cy="{y+13}" r="4" fill="#09090a" stroke="#ffffff" stroke-opacity="0.06"/>'
    if accent:
        s += f'<rect x="{x+w-34}" y="{y+10}" width="22" height="4" rx="2" fill="{ORANGE}"/>'
    s += text(x + w / 2, y + h / 2 + 4, name, size=name_size, fill=CREAM, font=SANS, weight=700, anchor="middle", ls=2.5)
    s += text(x + w / 2, y + h / 2 + 24, sub, size=10, fill=CREAM_DIM, anchor="middle", ls=1.8)
    s += text(x, y - 18, ref, size=11, ls=2)
    return s


def led(x, y, t_on, label, color=ORANGE, blink=None, size=12):
    s = f'<rect x="{x-7}" y="{y-4.5}" width="14" height="9" rx="1.5" fill="#1a1a1c" stroke="url(#gold)" stroke-width="0.8"/>'
    s += (f'<circle cx="{x}" cy="{y}" r="11" fill="{color}" opacity="0" filter="url(#softglow)">'
          f'<set attributeName="opacity" to="0.55" begin="{t_on}s"/></circle>')
    anim = f'<set attributeName="fill" to="{color}" begin="{t_on}s"/>'
    if blink:
        anim += f'<animate attributeName="opacity" values="1;1;0.15;1" keyTimes="0;0.55;0.75;1" dur="{blink}s" begin="{t_on}s" repeatCount="indefinite"/>'
    s += f'<rect x="{x-4.5}" y="{y-3}" width="9" height="6" rx="1" fill="#3a2418">{anim}</rect>'
    s += text(x + 16, y + 4, label, size=size, fill=CREAM, ls=1.6)
    return s


def smd(x, y, ref=None, w=22, h=11, rot=0):
    s = f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="url(#cap)"/></g>'
    if ref:
        s += text(x, y - 6, ref, size=9, ls=1)
    return s


def silk_box(x, y, w, h, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{CREAM}" stroke-opacity="0.35" stroke-width="1"{d}/>'
