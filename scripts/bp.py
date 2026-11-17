"""Boarding-pass kit: fonts, palette and shared parts for Mohab's profile SVGs.
SMIL animation only (runs inside GitHub's <img>). Nothing starts hidden, so every
graphic still reads correctly as a still frame.
"""
import base64
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

NIGHT = "#0f1013"       # terminal at night
NIGHT2 = "#17181c"
PAPER = "#f3ecdc"       # ticket stock
PAPER2 = "#e9dfc9"
INK = "#1a1917"
INK_DIM = "#6f6758"
ORANGE = "#ff5a1f"
FLAP = "#ffc23d"        # split-flap amber
GREEN = "#3ddc84"
CREAM = "#efe7d6"
MUTED = "#8b8579"

SANS = "'SG', 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif"
MONO = "'PX', 'IBM Plex Mono', ui-monospace, Menlo, monospace"
DISPLAY = "'BG', 'Bricolage Grotesque', 'Helvetica Neue', Arial, sans-serif"
SERIF = "'IS', 'Instrument Serif', Georgia, serif"

_FACES = {
    "sg700": ("SG", 700, "normal"), "sg500": ("SG", 500, "normal"),
    "plex400": ("PX", 400, "normal"), "plex600": ("PX", 600, "normal"),
    "serifi": ("IS", 400, "italic"), "brico": ("BG", 700, "normal"), "serif": ("IS", 400, "normal"),
}

PLANE = ("M13 0 L-3 -3.2 L-8 -12 L-11.5 -12 L-8 -2.6 L-14.5 -2.6 L-17.5 -7 L-20 -7 L-18 0 "
         "L-20 7 L-17.5 7 L-14.5 2.6 L-8 2.6 L-11.5 12 L-8 12 L-3 3.2 Z")


def _b64(n):
    with open(os.path.join(HERE, "fonts", n + ".woff2"), "rb") as f:
        return base64.b64encode(f.read()).decode()


def fonts(*which):
    css = "".join(
        f"@font-face{{font-family:'{_FACES[w][0]}';font-weight:{_FACES[w][1]};font-style:{_FACES[w][2]};"
        f"src:url(data:font/woff2;base64,{_b64(w)}) format('woff2');}}" for w in which)
    return f"<style>{css}</style>"


DEFS = f"""<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
  </filter>
  <filter id="paper" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3" seed="8" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.28  0 0 0 0 0.15  0 0 0 0.10 0"/>
  </filter>
  <filter id="ink" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="2" seed="2" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="2.2" result="d"/>
    <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="5" result="s"/>
    <feColorMatrix in="s" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.55" result="mask"/>
    <feComposite in="d" in2="mask" operator="in"/>
  </filter>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="140%">
    <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity="0.55"/>
  </filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
    <stop offset="50%" stop-color="#fff" stop-opacity="0.38"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="lamp" cx="50%" cy="0%" r="90%">
    <stop offset="0%" stop-color="#2a2620"/><stop offset="70%" stop-color="{NIGHT}"/>
  </radialGradient>
</defs>"""


def svg(w, h, body, label, faces):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}"><title>{label}</title>{fonts(*faces)}{DEFS}{body}</svg>')


def backdrop(w, h, r=24):
    return (f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#lamp)"/>'
            f'<rect width="{w}" height="{h}" rx="{r}" filter="url(#grain)"/>')


def t(x, y, s, size=12, fill=INK, font=MONO, weight=400, anchor="start", ls=0, style="normal", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{s}</text>')


def field(x, y, label, value, size=19, vfill=INK, lfill=INK_DIM):
    return t(x, y, label, size=10.5, fill=lfill, ls=2.2) + t(x, y + size + 7, value, size=size, fill=vfill, font=SANS, weight=700, ls=0.3)


def ticket_shape(x, y, w, h, stub_x, r=18, notch=13, cid="tk"):
    """Ticket outline with semicircle notches at the perforation, as a clipPath + fill."""
    d = (f"M{x+r} {y} H{stub_x-notch} A{notch} {notch} 0 0 0 {stub_x+notch} {y} H{x+w-r} "
         f"Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{stub_x+notch} "
         f"A{notch} {notch} 0 0 0 {stub_x-notch} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z")
    return d


def barcode(x, y, w, h, seed=1, color=INK):
    rng = random.Random(seed)
    s, cx = "", x
    while cx < x + w:
        bw = rng.choice([1, 1, 1.5, 2, 3])
        s += f'<rect x="{cx:.1f}" y="{y}" width="{bw}" height="{h}" fill="{color}"/>'
        cx += bw + rng.choice([1, 1.5, 2, 2.5])
    return s


def pdf417(x, y, w, h, seed=2, color=INK):
    rng = random.Random(seed)
    s, rows = "", int(h // 6)
    for r in range(rows):
        cx = x
        while cx < x + w:
            bw = rng.choice([1, 2, 2, 3, 4])
            if rng.random() < 0.55:
                s += f'<rect x="{cx}" y="{y + r*6}" width="{bw}" height="5" fill="{color}"/>'
            cx += bw + 1
    return s


def rise(inner, dy=24, begin=0.0, dur=0.9):
    return (f'<g><animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
            f'begin="{begin}s" dur="{dur}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="0.16 1 0.3 1"/>{inner}</g>')
