"""U7 · Activity matrix: renders the last year of GitHub contributions as an LED matrix.

Runs daily from .github/workflows/activity.yml. Needs a token in GH_PAT or GITHUB_TOKEN.
Without a token it renders sample data (clearly labelled) so the layout can be previewed.
"""
import datetime as dt
import json
import os
import random
import urllib.request

from mb import *  # noqa: F401,F403

LOGIN = os.environ.get("GH_LOGIN", "mohabbadawy1")
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{contributionCount contributionLevel date weekday}}}}}}"""


def fetch():
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GitHub API error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["weekday"], LEVEL[d["contributionLevel"]]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def sample():
    rng = random.Random(3)
    weeks = []
    for w in range(53):
        heat = 0.35 + 0.5 * (w / 52)
        weeks.append([(d, min(4, int(rng.random() ** (1.6 - heat) * 5)) if rng.random() < heat else 0) for d in range(7)])
    return None, weeks


def render(total, weeks, is_sample):
    W, H = 1200, 290
    b = board(W, H, holes=False, r=20)
    b += text(40, 46, "U7 · ACTIVITY MATRIX · 53 × 7 LED", size=11.5, ls=2.6)
    right = "SAMPLE DATA · SYNCS ON FIRST ACTION RUN" if is_sample else f"{total:,} CONTRIBUTIONS · LAST 12 MONTHS"
    b += text(W - 40, 46, right, size=11.5, fill=CREAM, anchor="end", ls=2.2)

    pitch, r = 19.4, 6.2
    cols = len(weeks)
    gx = (W - (cols - 1) * pitch) / 2
    gy = 84
    # module housing
    b += f'<g filter="url(#shadow)"><rect x="{gx-22}" y="{gy-22}" width="{(cols-1)*pitch+44}" height="{6*pitch+44}" rx="8" fill="#0d0d0f"/></g>'
    b += f'<rect x="{gx-22}" y="{gy-22}" width="{(cols-1)*pitch+44}" height="{6*pitch+44}" rx="8" fill="none" stroke="url(#gold)" stroke-opacity="0.35"/>'
    fills = {1: "#5a2410", 2: "#a53a12", 3: "#e64d17", 4: ORANGE_HOT}
    for c, week in enumerate(weeks):
        t_on = 0.3 + c * 0.03
        for day, lvl in week:
            x, y = gx + c * pitch, gy + day * pitch
            b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#17110d" stroke="#000" stroke-width="1"/>'
            if lvl:
                glow = ' filter="url(#glow)"' if lvl >= 3 else ""
                b += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r-0.6}" fill="{fills[lvl]}" opacity="0"{glow}>'
                      f'<animate attributeName="opacity" values="0;1;0.85;1" keyTimes="0;0.25;0.5;1" begin="{t_on:.2f}s" dur="0.5s" fill="freeze"/></circle>')
    # scanning column
    b += (f'<rect x="{gx - r - 2:.1f}" y="{gy - r - 4:.1f}" width="{2*r+4:.1f}" height="{6*pitch + 2*r + 8:.1f}" rx="{r+2}" '
          f'fill="{ORANGE}" opacity="0.10"><animate attributeName="x" from="{gx - r - 2:.1f}" to="{gx + (cols-1)*pitch - r - 2:.1f}" '
          f'dur="6s" begin="2s" repeatCount="indefinite"/></rect>')
    # legend + stamp
    ly = H - 30
    b += text(40, ly + 4, "LESS", size=10, ls=2)
    for i, lvl in enumerate([0, 1, 2, 3, 4]):
        cx = 90 + i * 20
        b += f'<circle cx="{cx}" cy="{ly}" r="6" fill="{fills.get(lvl, "#17110d")}" stroke="#000"/>'
    b += text(196, ly + 4, "MORE", size=10, ls=2)
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=2))).strftime("%Y-%m-%d %H:%M")
    b += text(W - 40, ly + 4, f"LAST SYNC {stamp} CAIRO · github.com/{LOGIN}", size=10, anchor="end", ls=2)
    return svg(W, H, b, "GitHub contribution activity as an LED matrix", fonts=("plex400",))


if __name__ == "__main__":
    got = fetch()
    total, weeks = got if got else sample()
    with open(os.path.join(ASSETS, "activity.svg"), "w") as f:
        f.write(render(total, weeks, got is None))
    print("activity:", "sample" if got is None else f"{total} contributions")
