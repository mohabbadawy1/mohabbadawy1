"""Builds the static boarding-pass assets. Run: python3 scripts/build.py"""
import os

from bp import *  # noqa: F401,F403

os.makedirs(ASSETS, exist_ok=True)


def write(name, content):
    with open(os.path.join(ASSETS, name), "w") as f:
        f.write(content)


# ═══════════════════════════════════════════════════════════════════ HERO PASS
def hero():
    W, H = 1200, 548
    X, Y, TW, TH, SX = 40, 40, 1120, 456, 880
    b = backdrop(W, H)
    d = ticket_shape(X, Y, TW, TH, SX, cid="hero")
    b += f'<defs><clipPath id="tk"><path d="{d}"/></clipPath></defs>'

    body = ""
    body += f'<path d="{d}" fill="{PAPER}"/>'
    body += f'<g clip-path="url(#tk)"><rect x="{X}" y="{Y}" width="{TW}" height="{TH}" filter="url(#paper)"/>'
    # header band
    body += f'<rect x="{X}" y="{Y}" width="{TW}" height="62" fill="{INK}"/>'
    body += f'<rect x="{SX}" y="{Y}" width="{X+TW-SX}" height="62" fill="{ORANGE}"/>'
    body += f'</g>'
    body += f'<path d="M{X+44} {Y+31}" /><g transform="translate({X+52} {Y+31}) scale(0.95)"><path d="{PLANE}" fill="{ORANGE}"/></g>'
    body += t(X + 82, Y + 38, "BOARDING PASS", size=19, fill=CREAM, font=SANS, weight=700, ls=5)
    body += t(SX - 30, Y + 37, "FIRST CLASS  ·  FOUNDER", size=12, fill=ORANGE, ls=3, anchor="end", weight=600)
    body += t(SX + 26, Y + 37, "BOARDING PASS", size=12.5, fill=INK, ls=3.5, weight=600)

    # route
    ry = 214
    for x, code, l1, l2, col in [(76, "ENG", "ENGINEERING", "ECE @ AUC '28", INK),
                                 (362, "AUT", "AUTOMATION", "AI AGENTS · N8N · APIS", INK),
                                 (648, "CLD", "NEXT STOP", "CLOUD · AWS · AZURE · IaC", ORANGE)]:
        body += t(x - 4, ry, code, size=94, fill=col, font=SANS, weight=700, ls=-1)
        body += t(x, ry + 28, l1, size=11, fill=col, ls=2.4, weight=600)
        body += t(x, ry + 45, l2, size=10.5, fill=INK_DIM, ls=1.8)
    # leg 1 (flown)
    body += f'<path d="M268 178 H352" stroke="{INK}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
    body += f'<g transform="translate(312 178)"><path d="{PLANE}" fill="{INK}"/></g>'
    # leg 2 (in flight)
    body += f'<path id="leg2" d="M556 178 H638" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
    body += (f'<g><path d="{PLANE}" fill="{ORANGE}"/>'
             f'<animateMotion dur="3.2s" repeatCount="indefinite" path="M556 178 H638" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines="0.45 0 0.55 1"/></g>')

    # tagline
    body += (f'<text x="74" y="318" font-family="{DISPLAY}" font-size="34" font-weight="700" fill="{INK}" letter-spacing="-0.6">'
             f'Engineering solutions with a <tspan fill="{ORANGE}">business brain.</tspan></text>')
    body += f'<path d="M76 340 H{SX-36}" stroke="{INK}" stroke-opacity="0.25" stroke-dasharray="3 4"/>'

    # fields
    body += field(76, 372, "PASSENGER", "MOHAB BADAWY")
    body += field(330, 372, "FLIGHT", "AUC · ECE '28")
    body += field(560, 372, "CLASS", "FOUNDER × ENGINEER")
    body += field(76, 430, "GATE", "SOLVEN")
    body += field(230, 430, "SEAT", "CO-FOUNDER &amp; GM")
    body += field(470, 430, "BOARDING", "NOW", vfill=ORANGE)
    body += field(640, 430, "STATUS", "ON TIME", vfill="#1f7a4a")
    body += t(76, 484, "ISSUED IN CAIRO  ·  VALID FOR ALL DESTINATIONS  ·  GITHUB.COM/MOHABBADAWY1", size=9.5, fill=INK_DIM, ls=2)

    # perforation
    body += f'<path d="M{SX} {Y+62} V{Y+TH-14}" stroke="{INK}" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="1 7" stroke-linecap="round"/>'

    # stub
    sx = SX + 28
    body += field(sx, 132, "PASSENGER", "BADAWY / MOHAB", size=17)
    body += field(sx, 190, "FROM", "ENG", size=26)
    body += field(sx + 92, 190, "VIA", "AUT", size=26)
    body += field(sx + 184, 190, "TO", "CLD", size=26, vfill=ORANGE)
    body += field(sx, 258, "SEAT", "GM", size=17)
    body += field(sx + 92, 258, "GATE", "SV", size=17)
    body += field(sx + 184, 258, "ZONE", "1", size=17)
    body += pdf417(sx, 318, 222, 66, seed=7)
    # now boarding pill
    py = 418
    body += f'<rect x="{sx}" y="{py}" width="222" height="40" rx="20" fill="{INK}"/>'
    body += (f'<circle cx="{sx+24}" cy="{py+20}" r="5" fill="{ORANGE}" filter="url(#glow)">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="1.3s" repeatCount="indefinite"/></circle>')
    body += t(sx + 42, py + 25, "NOW BOARDING", size=13, fill=CREAM, ls=3.2, weight=600)

    # sheen sweep
    body += (f'<g clip-path="url(#tk)"><rect x="-260" y="{Y}" width="220" height="{TH}" fill="url(#sheen)" transform="skewX(-18)">'
             f'<animate attributeName="x" values="-260;1500;1500" keyTimes="0;0.35;1" dur="8s" begin="1.2s" repeatCount="indefinite"/></rect></g>')

    b += rise(f'<g filter="url(#shadow)">{body}</g>', dy=30, dur=1.1)

    # runway lights
    for i, x in enumerate(range(60, 1150, 36)):
        b += (f'<circle cx="{x}" cy="526" r="2.4" fill="{FLAP}" opacity="0.25">'
              f'<animate attributeName="opacity" values="0.15;1;0.15" dur="2.4s" begin="{i*0.06:.2f}s" repeatCount="indefinite"/></circle>')
    return svg(W, H, b, "Boarding pass: Mohab Badawy. Engineering to automation and AI agents, next stop cloud.",
               ("sg700", "plex400", "plex600", "brico"))


# ═══════════════════════════════════════════════════════════ DEPARTURES BOARD
ROWS = [
    ("SV001", "SOLVEN", "GCC", "LIVE"),
    ("ND002", "NUDGE", "AUC", "BETA"),
    ("CL003", "DRALAAHUSSIEN.COM", "CAIRO", "LIVE"),
    ("OP004", "OPS CONTROL DEMO", "WEB", "ONLINE"),
    ("AZ900", "AZURE FUNDAMENTALS", "CLOUD", "LANDED"),
    ("AWS01", "AWS SOLUTIONS ARCH", "CLOUD", "BOARDING"),
    ("TF002", "TERRAFORM ASSOCIATE", "CLOUD", "SCHEDULED"),
    ("MB028", "AUC · ECE DEGREE", "CAIRO", "EN ROUTE"),
]
STATUS_COL = {"LIVE": GREEN, "ONLINE": GREEN, "LANDED": GREEN, "BETA": FLAP,
              "BOARDING": FLAP, "EN ROUTE": FLAP, "SCHEDULED": MUTED}


def departures():
    W = 1200
    pitch, cw, chh = 26, 24, 34
    cols = [(5, "FLIGHT"), (19, "DESTINATION"), (5, "GATE"), (9, "STATUS")]
    gap = 28
    x0, top, rh = 64, 150, 46
    H = top + rh * len(ROWS) + 56
    b = backdrop(W, H)
    b += f'<rect x="24" y="24" width="{W-48}" height="{H-48}" rx="14" fill="#08080a" stroke="#26262b"/>'
    b += f'<g transform="translate(78 72) rotate(-20)"><path d="{PLANE}" fill="{FLAP}"/></g>'
    b += t(106, 84, "DEPARTURES", size=32, fill=FLAP, font=SANS, weight=700, ls=5)
    b += t(W - 64, 72, "CAIRO INTL · TERMINAL MB", size=12, fill=MUTED, ls=2.6, anchor="end")
    b += t(W - 64, 92, "PROJECTS · CERTIFICATIONS · DEGREE", size=12, fill=CREAM, ls=2.6, anchor="end")
    # column heads
    cx = x0
    for n, head in cols:
        b += t(cx, top - 18, head, size=11, fill=MUTED, ls=2.4)
        cx += n * pitch + gap
    for r, row in enumerate(ROWS):
        y = top + r * rh
        cx = x0
        for c, ((n, _), val) in enumerate(zip(cols, row)):
            col = STATUS_COL.get(row[3], FLAP) if c == 3 else (CREAM if c == 1 else FLAP)
            for i in range(n):
                ch = val[i] if i < len(val) else " "
                x = cx + i * pitch
                b += f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="3" fill="#1c1c20"/>'
                if ch.strip():
                    blink = ""
                    if c == 3 and row[3] == "BOARDING":
                        blink = '<animate attributeName="opacity" values="1;1;0.25;1" keyTimes="0;0.6;0.8;1" dur="1.2s" repeatCount="indefinite"/>'
                    b += (f'<text x="{x + cw/2}" y="{y + 24.5}" font-family="{MONO}" font-size="20" font-weight="600" '
                          f'fill="{col}" text-anchor="middle">{ch}{blink}</text>')
                b += f'<rect x="{x}" y="{y + chh/2 - 0.6}" width="{cw}" height="1.2" fill="#000" opacity="0.85"/>'
                # flap: starts open (height 0), drops once on load, then status column flickers
                begin = 0.25 + r * 0.12 + (cx - x0 + i * pitch) * 0.0018
                anim = (f'<animate attributeName="height" values="{chh};{chh/2};0" keyTimes="0;0.5;1" begin="{begin:.2f}s" dur="0.32s" fill="freeze"/>')
                if c == 3:
                    anim += (f'<animate attributeName="height" values="0;{chh};0;0" keyTimes="0;0.02;0.045;1" '
                             f'begin="{4 + r*0.35 + i*0.03:.2f}s" dur="10s" repeatCount="indefinite"/>')
                b += f'<rect x="{x}" y="{y}" width="{cw}" height="0" rx="3" fill="#2a2a30">{anim}</rect>'
            cx += n * pitch + gap
    b += t(64, H - 42, "ALL TIMES LOCAL · CAIRO (UTC+2)  ·  BOARDING CLOSES WHEN IT SHIPS", size=10.5, fill=MUTED, ls=2.2)
    return svg(W, H, b, "Departures board listing Mohab's projects, certifications and degree",
               ("sg700", "plex400", "plex600"))


# ═════════════════════════════════════════════════════════════ PROJECT TICKETS
def ticket(fname, flight, route, name, desc, fields, gate, seat, status, scol, link, seed):
    W, H = 590, 290
    X, Y, TW, TH, SX = 14, 14, 562, 258, 418
    d = ticket_shape(X, Y, TW, TH, SX, r=14, notch=11)
    b = f'<defs><clipPath id="c{seed}"><path d="{d}"/></clipPath></defs>'
    body = f'<path d="{d}" fill="{PAPER}"/>'
    body += f'<g clip-path="url(#c{seed})"><rect x="{X}" y="{Y}" width="{TW}" height="{TH}" filter="url(#paper)"/>'
    body += f'<rect x="{X}" y="{Y}" width="{TW}" height="44" fill="{INK}"/><rect x="{SX}" y="{Y}" width="{X+TW-SX}" height="44" fill="{ORANGE}"/></g>'
    body += t(X + 22, Y + 28, f"FLIGHT {flight}", size=12, fill=CREAM, ls=3, weight=600)
    body += t(SX - 22, Y + 28, route, size=12, fill=ORANGE, ls=2.4, anchor="end", weight=600)
    body += t(SX + 20, Y + 28, "BOARDING", size=11.5, fill=INK, ls=3, weight=600)
    body += t(X + 20, Y + 100, name, size=36, fill=INK, font=SANS, weight=700, ls=-0.5)
    body += t(X + 22, Y + 128, desc[0], size=14, fill=INK_DIM, font=SANS, weight=500)
    body += t(X + 22, Y + 148, desc[1], size=14, fill=INK_DIM, font=SANS, weight=500)
    body += f'<path d="M{X+22} {Y+168} H{SX-22}" stroke="{INK}" stroke-opacity="0.22" stroke-dasharray="3 4"/>'
    for i, (k, v) in enumerate(fields):
        body += field(X + 22 + i * 190, Y + 192, k, v, size=14)
    body += f'<path d="M{SX} {Y+44} V{Y+TH-10}" stroke="{INK}" stroke-opacity="0.35" stroke-width="1.4" stroke-dasharray="1 6" stroke-linecap="round"/>'
    sx = SX + 20
    body += field(sx, Y + 72, "GATE", gate, size=17)
    body += field(sx + 70, Y + 72, "SEAT", seat, size=17)
    body += t(sx, Y + 128, "STATUS", size=10.5, fill=INK_DIM, ls=2.2)
    body += (f'<circle cx="{sx+5}" cy="{Y+143}" r="4.5" fill="{scol}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    body += t(sx + 16, Y + 149, status, size=16, fill=INK, font=SANS, weight=700, ls=1)
    body += barcode(sx, Y + 166, 118, 38, seed=seed)
    body += t(sx, Y + 232, f"{link} ↗", size=11, fill=INK, ls=0.6, weight=600)
    b += f'<g filter="url(#shadow)">{body}</g>'
    write(fname, svg(W, H, b, f"{name}: {desc[0]} {desc[1]}", ("sg700", "sg500", "plex400", "plex600")))
    return b


# ═════════════════════════════════════════════════════════════════ PASSPORT
def _arc_text(r, txt, size, color, top=True, sid="a"):
    if top:
        path = f"M{-r} 0 A{r} {r} 0 0 1 {r} 0"
    else:
        path = f"M{-r} 0 A{r} {r} 0 0 0 {r} 0"
    return (f'<defs><path id="{sid}" d="{path}"/></defs>'
            f'<text font-family="{MONO}" font-size="{size}" font-weight="600" fill="{color}" letter-spacing="2.4">'
            f'<textPath href="#{sid}" startOffset="50%" text-anchor="middle">{txt}</textPath></text>')


_sid = [0]


def stamp(kind, cx, cy, rot, color, lines, begin, size=None, dashed=False, w=None, h=None, r=None):
    _sid[0] += 1
    sid = f"s{_sid[0]}"
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    g = ""
    if kind == "circle":
        g += f'<circle r="{r}" fill="none" stroke="{color}" stroke-width="3.2"{dash}/>'
        g += f'<circle r="{r-7}" fill="none" stroke="{color}" stroke-width="1.4"/>'
        g += f'<circle r="{r*0.52:.1f}" fill="none" stroke="{color}" stroke-width="1.2"/>'
        g += _arc_text(r - 19, lines[0], 10.5, color, True, sid + "t")
        g += _arc_text(r - 10, lines[2], 10.5, color, False, sid + "b")
        g += t(0, (size or 24) * 0.36, lines[1], size=size or 24, fill=color, font=SANS, weight=700, anchor="middle", ls=0.5)
        g += f'<path d="M{-r+14} 0 h6 M{r-20} 0 h6" stroke="{color}" stroke-width="2"/>'
    elif kind == "rect":
        g += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="5" fill="none" stroke="{color}" stroke-width="3"{dash}/>'
        g += f'<rect x="{-w/2+6}" y="{-h/2+6}" width="{w-12}" height="{h-12}" rx="3" fill="none" stroke="{color}" stroke-width="1.2"/>'
        n = len(lines)
        for i, ln in enumerate(lines):
            big = i == 0
            y = -((n - 1) * 20) / 2 + i * 20 + (7 if big else 4)
            g += t(0, y, ln, size=(size or 19) if big else 11, fill=color, font=SANS if big else MONO,
                   weight=700 if big else 600, anchor="middle", ls=0.8 if big else 1.8)
    else:  # oval
        g += f'<ellipse rx="{w/2}" ry="{h/2}" fill="none" stroke="{color}" stroke-width="3"{dash}/>'
        g += f'<ellipse rx="{w/2-7}" ry="{h/2-7}" fill="none" stroke="{color}" stroke-width="1.2"/>'
        g += t(0, 2, lines[0], size=size or 20, fill=color, font=SANS, weight=700, anchor="middle", ls=0.5)
        g += t(0, 22, lines[1], size=10.5, fill=color, font=MONO, weight=600, anchor="middle", ls=1.8)
    anim = (f'<animateTransform attributeName="transform" type="scale" values="1;1.35;0.96;1" keyTimes="0;0.01;0.6;1" '
            f'begin="{begin:.2f}s" dur="0.45s" fill="freeze"/>')
    return (f'<g transform="translate({cx} {cy}) rotate({rot})"><g opacity="0.88" filter="url(#ink)">{anim}{g}</g></g>')


def passport():
    W, H = 1200, 590
    b = ""
    px, py, pw, ph = 46, 46, 554, 498
    # booklet cover edge
    b += f'<g filter="url(#shadow)"><rect x="{px-10}" y="{py-10}" width="{2*pw+20}" height="{ph+20}" rx="18" fill="#1d2a3a"/></g>'
    guil = "".join(f'<path d="M0 {i*9} Q 60 {i*9-7} 120 {i*9} T 240 {i*9}" fill="none" stroke="#9fb3c8" stroke-opacity="0.22"/>' for i in range(4))
    b += f'<defs><pattern id="gl" width="240" height="36" patternUnits="userSpaceOnUse">{guil}</pattern></defs>'
    for i in range(2):
        x = px + i * pw
        b += f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="{8}" fill="#ece8de"/>'
        b += f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="url(#gl)"/>'
        b += f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="8" filter="url(#paper)"/>'
    b += f'<rect x="{px+pw-14}" y="{py}" width="28" height="{ph}" fill="#000" opacity="0.10"/>'
    b += f'<path d="M{px+pw} {py} V{py+ph}" stroke="#000" stroke-opacity="0.25"/>'

    b += t(px + 28, py + 38, "VISAS · SKILLS", size=12, fill="#2c3e57", ls=3.4, weight=600)
    b += t(px + pw - 28, py + 38, "MOHAB BADAWY", size=12, fill="#2c3e57", ls=3, anchor="end")
    b += t(px + pw + 28, py + 38, "ENTRY STAMPS · CERTS &amp; EXPERIENCE", size=12, fill="#2c3e57", ls=3.4, weight=600)
    b += t(px + 2 * pw - 28, py + 38, "P. 07", size=12, fill="#2c3e57", ls=3, anchor="end")

    RED, BLUE, GRN, PUR, ORG, NAVY = "#b8322a", "#2a4a96", "#2c6b4d", "#5a3d8a", "#d9541e", "#1f2f4a"
    L = px
    s = ""
    s += stamp("circle", L + 120, py + 150, -12, RED, ["LANGUAGES", "PYTHON", "C · C++ · TS"], 0.3, size=24, r=70)
    s += stamp("rect", L + 340, py + 128, 6, BLUE, ["FULL-STACK", "NEXT.JS · REACT", "FASTAPI · REST APIS"], 0.5, w=230, h=96)
    s += stamp("oval", L + 400, py + 262, -8, GRN, ["AUTOMATION", "N8N · AI AGENTS · APIS"], 0.7, w=250, h=96)
    s += stamp("circle", L + 130, py + 350, 10, PUR, ["CLOUD", "AWS", "AZURE · VERCEL"], 0.9, size=28, r=66)
    s += stamp("rect", L + 380, py + 392, -4, ORG, ["INFRA &amp; SECURITY", "LINUX · GIT · NETWORKING", "FORTIGATE · CROWDSTRIKE"], 1.1, size=17, w=262, h=84)
    s += stamp("rect", L + 225, py + 250, 12, NAVY, ["HUBSPOT", "CRM · SALES OPS"], 1.3, size=15, w=112, h=58)

    R = px + pw
    s += stamp("circle", R + 110, py + 150, 8, RED, ["MICROSOFT", "AZ-900", "CLEARED"], 0.4, size=26, r=72)
    s += stamp("rect", R + 372, py + 128, -5, BLUE, ["DUBIZZLE · IT", "ADMITTED · JUL 2026", "SECURITY · NETWORK · TELEPHONY"], 0.6, size=20, w=270, h=100)
    s += stamp("oval", R + 372, py + 266, 7, GRN, ["AUC · ECE '28", "GPA 3.72 · 50% MERIT AWARD"], 0.8, w=284, h=100)
    s += stamp("rect", R + 118, py + 254, -8, NAVY, ["QNB · SIAC", "PRIOR ENTRIES"], 1.5, size=15, w=128, h=52)
    s += stamp("circle", R + 108, py + 360, -14, PUR, ["IELTS", "8.0", "ACADEMIC"], 1.0, size=32, r=58)
    s += stamp("rect", R + 290, py + 392, 4, ORG, ["AWS SAA", "VISA PENDING"], 1.2, w=158, h=68, dashed=True)
    s += stamp("rect", R + 458, py + 386, -9, ORG, ["TERRAFORM", "VISA PENDING"], 1.35, size=17, w=146, h=68, dashed=True)
    b += s

    # MRZ
    mrz1 = "P&lt;MBXBADAWY&lt;&lt;MOHAB&lt;AYMAN&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;"
    mrz2 = "MB2028&lt;&lt;ECE&lt;AUC&lt;&lt;FOUNDER&lt;GM&lt;SOLVEN&lt;&lt;&lt;&lt;&lt;&lt;"
    b += t(L + 28, py + ph - 44, mrz1, size=15, fill="#2c3e57", ls=3.2)
    b += t(L + 28, py + ph - 20, mrz2, size=15, fill="#2c3e57", ls=3.2)
    return b


# ═══════════════════════════════════════════════════════════════════ DIVIDER
def divider():
    W, H = 1200, 44
    b = f'<path d="M20 22 H1180" stroke="{MUTED}" stroke-opacity="0.5" stroke-width="1.5" stroke-dasharray="2 9" stroke-linecap="round"/>'
    b += (f'<g><path d="{PLANE}" fill="{ORANGE}"/>'
          f'<animateMotion dur="9s" repeatCount="indefinite" path="M20 22 H1180"/></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{b}</svg>'


# ═══════════════════════════════════════════════════════════════ ITINERARY
LEGS = [
    ("2026 → NOW", "SLV", "Solven · Cairo", "Co-founder &amp; General Manager",
     ["Software, automation &amp; AI agents for SMEs in Egypt and the GCC.", "Leads sales, proposals, product and delivery."], "IN FLIGHT"),
    ("2026 → NOW", "NDG", "Nudge", "Co-founder",
     ["Study-planning app for university students.", "Web beta, pitching at AUC's startup competition."], "IN FLIGHT"),
    ("JUL 2026", "DBZ", "Dubizzle", "IT Intern",
     ["CrowdStrike · FortiGate · FortiAnalyzer · networking · telephony.", "Presented a telephony comparison brief to the IT team."], "LANDED"),
    ("EARLIER", "QNB", "QNB Alahli · SIAC Construction", "Intern",
     ["Internships in banking and construction."], "LANDED"),
    ("AT AUC", "AQC", "Al Quds Club", "Co-head of Events",
     ["Runs the club's events alongside a fellow co-head."], "IN FLIGHT"),
    ("PART-TIME", "MTH", "A-Level Mathematics", "Teaching Assistant",
     ["Supporting A-Level maths students."], "LOGGED"),
    ("2024 → 2028", "AUC", "American University in Cairo", "B.Sc. Electrical &amp; Computer Engineering",
     ["GPA 3.72 · 50% first-year merit award."], "EN ROUTE"),
]
LEG_COL = {"IN FLIGHT": ORANGE, "EN ROUTE": FLAP, "LANDED": GREEN, "LOGGED": MUTED}


def itinerary():
    W = 1200
    top = 132
    heights = [56 + 22 * len(l[4]) for l in LEGS]
    H = top + sum(heights) + 44
    b = backdrop(W, H)
    b += f'<g transform="translate(64 64) rotate(-20) scale(0.85)"><path d="{PLANE}" fill="{FLAP}"/></g>'
    b += t(92, 74, "ITINERARY", size=30, fill=CREAM, font=SANS, weight=700, ls=5)
    b += t(W - 56, 62, "PASSENGER · MOHAB BADAWY", size=11.5, fill=MUTED, ls=2.4, anchor="end")
    b += t(W - 56, 82, "EXPERIENCE · LEADERSHIP · EDUCATION", size=11.5, fill=CREAM, ls=2.4, anchor="end")
    b += f'<path d="M56 104 H{W-56}" stroke="{CREAM}" stroke-opacity="0.25"/>'
    lx = 236
    ys = []
    y = top
    for h in heights:
        ys.append(y)
        y += h
    route = f"M{lx} {ys[0]+18} V{ys[-1]+18}"
    b += f'<path d="{route}" stroke="{MUTED}" stroke-opacity="0.5" stroke-width="1.6" stroke-dasharray="2 7" stroke-linecap="round"/>'
    b += (f'<g><g transform="rotate(90)"><path d="{PLANE}" fill="{ORANGE}" transform="scale(0.8)"/></g>'
          f'<animateMotion dur="9s" repeatCount="indefinite" path="{route}"/></g>')
    for i, ((when, code, title, role, lines, status), y0) in enumerate(zip(LEGS, ys)):
        col = LEG_COL[status]
        row = ""
        row += t(56, y0 + 24, when, size=13, fill=FLAP, ls=2, weight=600)
        row += f'<circle cx="{lx}" cy="{y0+18}" r="7" fill="#0f1013" stroke="{col}" stroke-width="2.5"/>'
        if status == "IN FLIGHT":
            row += (f'<circle cx="{lx}" cy="{y0+18}" r="7" fill="none" stroke="{col}" stroke-width="2">'
                    f'<animate attributeName="r" values="7;18" dur="1.8s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0.9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
        row += f'<rect x="268" y="{y0}" width="62" height="30" rx="6" fill="{PAPER}"/>'
        row += t(299, y0 + 20, code, size=14, fill=INK, ls=2, weight=600, anchor="middle")
        row += (f'<text x="352" y="{y0+23}" font-family="{SANS}" font-size="22" font-weight="700" fill="{CREAM}">{title}'
                f'<tspan font-size="16" font-weight="500" fill="{ORANGE}">   {role}</tspan></text>')
        for j, ln in enumerate(lines):
            row += t(352, y0 + 50 + j * 22, ln, size=15, fill=MUTED, font=SANS, weight=500)
        pw = len(status) * 9 + 40
        row += f'<rect x="{W-56-pw}" y="{y0+2}" width="{pw}" height="28" rx="14" fill="none" stroke="{col}" stroke-opacity="0.7"/>'
        row += f'<circle cx="{W-56-pw+16}" cy="{y0+16}" r="4" fill="{col}"/>'
        row += t(W - 56 - pw + 28, y0 + 21, status, size=11.5, fill=CREAM, ls=2)
        if i < len(LEGS) - 1:
            row += f'<path d="M268 {y0 + heights[i] - 14} H{W-56}" stroke="{CREAM}" stroke-opacity="0.07"/>'
        b += rise(row, dy=18, begin=0.15 + i * 0.1, dur=0.8)
    b += t(56, H - 22, "ALL LEGS CONFIRMED · ISSUED IN CAIRO", size=10.5, fill=MUTED, ls=2.2)
    return svg(W, H, b, "Itinerary: Solven co-founder and GM, Nudge co-founder, Dubizzle IT intern, QNB and SIAC internships, Al Quds club events co-head, A-Level maths assistant, AUC ECE 2024-2028",
               ("sg700", "sg500", "plex400", "plex600"))


# ═══════════════════════════════════════════════════════════ SECTION HEADERS
def header(title, r1, r2):
    W, H = 1200, 132
    b = backdrop(W, H)
    b += f'<rect x="24" y="24" width="{W-48}" height="{H-48}" rx="14" fill="#08080a" stroke="#26262b"/>'
    b += f'<g transform="translate(78 66) rotate(-20)"><path d="{PLANE}" fill="{FLAP}"/></g>'
    b += t(106, 78, title, size=32, fill=FLAP, font=SANS, weight=700, ls=5)
    b += t(W - 64, 62, r1, size=12, fill=MUTED, ls=2.6, anchor="end")
    b += t(W - 64, 84, r2, size=12, fill=CREAM, ls=2.6, anchor="end")
    return svg(W, H, b, title.title(), ("sg700", "plex400"))


def contact_tile(label, value):
    W, H = 290, 104
    b = f'<rect width="{W}" height="{H}" rx="16" fill="url(#lamp)"/><rect width="{W}" height="{H}" rx="16" filter="url(#grain)"/>'
    b += f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="10" fill="#08080a" stroke="#26262b"/>'
    b += f'<rect x="10" y="10" width="6" height="{H-20}" rx="3" fill="{ORANGE}"/>'
    b += t(32, 44, label, size=11, fill=FLAP, ls=2.6, weight=600)
    b += t(32, 72, value, size=17, fill=CREAM, font=SANS, weight=700)
    b += t(W - 28, 72, "↗", size=18, fill=ORANGE, anchor="end", weight=600)
    return svg(W, H, b, f"{label}: {value}", ("sg700", "plex400", "plex600"))



# ═══════════════════════════════════════════════ CONNECTED SECTIONS (header + content in one panel)
def header_body(title, r1, r2, W=1200):
    b = f'<rect x="24" y="24" width="{W-48}" height="84" rx="14" fill="#08080a" stroke="#26262b"/>'
    b += f'<g transform="translate(78 66) rotate(-20)"><path d="{PLANE}" fill="{FLAP}"/></g>'
    b += t(106, 78, title, size=32, fill=FLAP, font=SANS, weight=700, ls=5)
    b += t(W - 64, 62, r1, size=12, fill=MUTED, ls=2.6, anchor="end")
    b += t(W - 64, 84, r2, size=12, fill=CREAM, ls=2.6, anchor="end")
    return b


def section(title, r1, r2, content, content_h, label, faces, top=108):
    W, H = 1200, top + content_h + 18
    b = backdrop(W, H) + header_body(title, r1, r2) + f'<g transform="translate(0 {top})">{content}</g>'
    return svg(W, H, b, label, faces)


def tile_body(label, value, w=282):
    b = f'<rect x="0" y="0" width="{w}" height="84" rx="10" fill="#08080a" stroke="#26262b"/>'
    b += f'<rect x="0" y="0" width="6" height="84" rx="3" fill="{ORANGE}"/>'
    b += t(24, 34, label, size=11, fill=FLAP, ls=2.6, weight=600)
    b += t(24, 62, value, size=17 if len(value) < 20 else 14.5, fill=CREAM, font=SANS, weight=700)
    b += t(w - 20, 62, "↗", size=18, fill=ORANGE, anchor="end", weight=600)
    return b

write("bp-pass4.svg", hero())
write("bp-itinerary.svg", itinerary())
write("bp-departures.svg", departures())
write("bp-route.svg", divider())
tk_solven = ticket("bp-solven.svg", "SV001", "CAI → GCC", "Solven",
       ("Software, automation &amp; AI agents for", "SMEs across Egypt and the GCC."),
       [("ROLE", "Co-founder &amp; GM"), ("STACK", "Next.js · FastAPI · n8n")],
       "SV", "GM", "LIVE", "#1f9a58", "solvenhq.com", 11)
tk_nudge = ticket("bp-nudge.svg", "ND002", "CAI → APP STORE", "Nudge",
       ("A cozy study world that plans your", "study time. Built for uni students."),
       [("ROLE", "Co-founder"), ("STAGE", "Web beta · AUC pitch")],
       "ND", "CO-F", "BETA", "#e0a01a", "studynudge.app", 12)
tk_clinic = ticket("bp-clinic.svg", "CL003", "CAI → LIVE", "Clinic Platform",
       ("A pediatric &amp; lactation practice,", "online end to end, for a real client."),
       [("SHIPS", "Site · booking · staff app"), ("INFRA", "Render · custom domain")],
       "CL", "BUILD", "LIVE", "#1f9a58", "dralaahussien.com", 13)
tk_ops = ticket("bp-ops.svg", "OP004", "WEB → YOU", "Ops Control Engine",
       ("A real-time operations command center", "on simulated data. Try it live."),
       [("BY", "Solven"), ("FOR", "SME operations teams")],
       "OP", "DEMO", "ONLINE", "#1f9a58", "demo.solvenhq.com", 14)
print("built")

# connected sections
tickets_content = (f'<g transform="translate(10 6)">{tk_solven}</g><g transform="translate(600 6)">{tk_nudge}</g>'
                   f'<g transform="translate(10 290)">{tk_clinic}</g><g transform="translate(600 290)">{tk_ops}</g>')
write("bp-sec-tickets.svg", section("YOUR TICKETS", "PROJECTS · LIVE BUILDS", "FOUR FLIGHTS IN SERVICE",
      tickets_content, 572, "Your tickets: Solven, Nudge, Clinic Platform, Ops Control Engine",
      ("sg700", "sg500", "plex400", "plex600")))
write("bp-sec-passport.svg", section("PASSPORT", "SKILLS · CERTIFICATIONS", "EXPERIENCE STAMPS",
      f'<g transform="translate(0 -24)">{passport()}</g>', 548,
      "Passport: skills, certifications and experience as stamps", ("sg700", "plex400", "plex600")))
tiles = "".join(f'<g transform="translate({24 + i*(279+12)} 16)">{tile_body(l, v, w=279)}</g>' for i, (l, v) in enumerate(
    [("LINKEDIN", "mohab-badawy-auc"), ("EMAIL", "mohab.badawy12@gmail.com"), ("COMPANY", "solvenhq.com"), ("PRODUCT", "studynudge.app")]))
write("bp-sec-contact2.svg", section("CONTACT", "ARRIVALS · GET IN TOUCH", "MOHAB BADAWY", tiles, 108,
      "Contact: LinkedIn mohab-badawy-auc, email mohab.badawy12@gmail.com, solvenhq.com, studynudge.app",
      ("sg700", "plex400", "plex600")))
