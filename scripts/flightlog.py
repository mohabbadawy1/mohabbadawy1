"""Flight log: the last 12 months of GitHub contributions as a flight-altitude chart.

Runs daily from .github/workflows/flightlog.yml (token in GH_PAT or GITHUB_TOKEN).
Without a token it renders clearly labelled sample data. Writes assets/bp-flightlog.svg.
"""
import datetime as dt
import json
import os
import random
import urllib.request
from collections import OrderedDict

from bp import *  # noqa: F401,F403

LOGIN = os.environ.get("GH_LOGIN", "mohabbadawy1")
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{contributionCount date}}}}}}"""


def fetch():
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GitHub API error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    return cal["totalContributions"], days


def sample():
    rng = random.Random(5)
    end = dt.date.today()
    days = [((end - dt.timedelta(days=i)).isoformat(), int(rng.random() ** 2 * 8 * (1 + (365 - i) / 300)))
            for i in range(364, -1, -1)]
    return sum(c for _, c in days), days


def months_of(days):
    m = OrderedDict()
    for date, c in days:
        m[date[:7]] = m.get(date[:7], 0) + c
    return list(m.items())[-12:]


def render(total, months, is_sample):
    W, H = 1200, 400
    b = backdrop(W, H)
    b += f'<g transform="translate(58 58) rotate(-20) scale(0.8)"><path d="{PLANE}" fill="{FLAP}"/></g>'
    b += t(82, 63, "FLIGHT LOG · LAST 12 MONTHS", size=12.5, fill=FLAP, ls=3.2, weight=600)
    b += t(W - 48, 63, "SAMPLE DATA · LIVE AFTER FIRST SYNC" if is_sample else "LIVE FROM GITHUB · UPDATED DAILY",
           size=11, fill=MUTED, ls=2.4, anchor="end")
    b += (f'<text x="46" y="122" font-family="{SANS}" font-size="40" font-weight="700" fill="{CREAM}" letter-spacing="-0.5">'
          f'<tspan fill="{ORANGE}">{total:,}</tspan> contributions logged.</text>')

    x0, x1, top, base = 70, 1130, 170, 320
    peak = max(c for _, c in months) or 1
    n = len(months)
    pts = [(x0 + i * (x1 - x0) / (n - 1), base - (base - top) * c / peak) for i, (_, c) in enumerate(months)]
    for gy in (top, (top + base) / 2, base):
        b += f'<path d="M{x0} {gy} H{x1}" stroke="{MUTED}" stroke-opacity="0.25" stroke-dasharray="2 6"/>'
    # smooth path
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mx = (ax + bx) / 2
        d += f" C{mx:.1f} {ay:.1f} {mx:.1f} {by:.1f} {bx:.1f} {by:.1f}"
    area = d + f" L{x1} {base} L{x0} {base} Z"
    b += f'<defs><linearGradient id="alt" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{ORANGE}" stop-opacity="0.35"/><stop offset="100%" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient></defs>'
    b += f'<path d="{area}" fill="url(#alt)"/>'
    b += (f'<path d="{d}" pathLength="100" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="0">'
          f'<animate attributeName="stroke-dashoffset" values="100;0" begin="0.2s" dur="2.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/></path>')
    best = max(range(n), key=lambda i: months[i][1])
    for i, ((key, c), (px, py)) in enumerate(zip(months, pts)):
        b += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{5 if i == best else 3.2}" fill="{ORANGE if i == best else CREAM}"/>'
        lab = dt.date(int(key[:4]), int(key[5:]), 1).strftime("%b").upper()
        b += t(px, base + 26, lab, size=11, fill=CREAM if i == best else MUTED, anchor="middle", ls=1.8)
        if i == best:
            b += t(px, py - 14, f"PEAK · {c:,}", size=11.5, fill=ORANGE, anchor="middle", ls=1.4, weight=600)
    # plane cruising along the route
    b += (f'<g><path d="{PLANE}" fill="{CREAM}"/>'
          f'<animateMotion dur="11s" begin="2.4s" repeatCount="indefinite" rotate="auto" path="{d}"/></g>')
    b += f'<path d="M{x0} {base} H{x1}" stroke="{CREAM}" stroke-opacity="0.5"/>'
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=2))).strftime("%d %b %Y").upper()
    b += t(46, H - 22, f"SOURCE: GITHUB · @{LOGIN.upper()} · LAST SYNC {stamp}", size=10.5, fill=MUTED, ls=2.2)
    return svg(W, H, b, f"{total} GitHub contributions in the last 12 months", ("sg700", "plex400", "plex600"))


if __name__ == "__main__":
    got = fetch()
    total, days = got if got else sample()
    with open(os.path.join(ASSETS, "bp-flightlog.svg"), "w") as f:
        f.write(render(total, months_of(days), got is None))
    print("flightlog:", "sample" if got is None else total)
