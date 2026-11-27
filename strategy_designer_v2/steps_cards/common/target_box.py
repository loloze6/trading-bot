"""A run's target box (common/target_box.md): the rule that chooses it, the run's file, the theme note that carries it
into the prompts, the check of a boxed run's brief, and whether an idea acts in it (visibility only).

  python3 common/target_box.py            the rule on today's map: the twelve boxes' counts, shares and scores

Why this cannot leak: the choice reads finished records (the register, the last portfolio's box reading) before a run
starts; the note, the brief's check and the field read header lines. No bar of a run's data is read.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parent
sys.path.insert(0, str(HERE))
from lib import header_fields, profile_name, write_atomic, utc_now, PROFILES  # noqa: E402

SIDES = ("long", "short")
BOXES = [(p, s) for p in PROFILES for s in SIDES]          # the twelve boxes, in the map's order
BRIEF_SIDE = {"long only": ("long",), "short only": ("short",), "long and short": SIDES}


def box_file(run, steps=STEPS):
    return steps / "orchestration" / "loop" / run / "target_box.json"


def run_box(run, steps=STEPS):
    """The run's target box {profile, side, ...}, or None (a run without one)."""
    p = box_file(run, steps)
    return json.loads(p.read_text()) if p.exists() else None


def parse_box(text):
    """'rising agitated, long' -> ('rising agitated', 'long'); None when it is not one of the twelve boxes."""
    words = re.findall(r"[a-z]+", (text or "").lower())
    sides = [w for w in words if w in SIDES]
    prof = profile_name(" ".join(w for w in words if w not in SIDES))
    return (prof, sides[0]) if len(sides) == 1 and prof in PROFILES else None


def box_name(box):
    return f"{box['profile']}, {box['side']}"


def holds(profile, box_profile):
    """Whether a named profile holds the box's profile: it is that profile or a wider one ('rising' and 'agitated' hold
    'rising agitated'; 'rising calm' does not). No profile: no."""
    return bool(profile) and all(w in box_profile.split() for w in profile.split())


# --- the theme note: the box in every prompt that writes ideas --------------------------------------------------

def theme_note(run, steps=STEPS):
    """The run's box as part of the brief's theme (common/theme.md), pasted after the brief wherever a prompt is given
    one (step 2, every step 7 line). Empty for a run without a box: the prompt as before."""
    box = run_box(run, steps)
    if not box:
        return ""
    p, s = box["profile"], box["side"]
    return (f"\n[THE MARKET AND SIDE OF THIS RESEARCH: PART OF THE BRIEF'S THEME]\n"
            f"This research is about one market profile and one side: {p} markets, {s} positions. They are part of the "
            f"brief's theme. Every idea you write keeps to them: its situation is in a {p} market, and it says so in a "
            f"`profile: {p}` line; its position is {s} only. A pattern off the brief's theme is looked for in {p} markets, "
            f"for {s} positions, only.\n")


# --- the check of a boxed run's brief ---------------------------------------------------------------------------

def brief_sides(text):
    """The sides a brief names (its `side:` header line): ('long',), ('short',), both, or () when it names none."""
    return BRIEF_SIDE.get(header_fields(text).get("side", "").strip().lower(), ())


def brief_refusal(text, box):
    """Why a boxed run cannot start from this brief (common/target_box.md), or None: its header must name a profile
    (`profile:`) holding the box's, and a side (`side:`) including the box's."""
    prof, sides = profile_name(header_fields(text).get("profile")), brief_sides(text)
    why = []
    if not holds(prof, box["profile"]):
        why.append(f"its profile line names {prof or 'no profile'}, which does not hold {box['profile']}")
    if box["side"] not in sides:
        why.append(f"its side line names {' and '.join(sides) or 'no side'}, not {box['side']}")
    return "; ".join(why) or None


# --- visibility: whether an idea acts in the box ----------------------------------------------------------------

def brief_side(brief_id, run, steps=STEPS):
    """The sides an idea's brief allows, as step 3 reads them (`make_test_plan.py`, `brief_side`): the run's copy of the
    brief, else step 1's lists; no side line (or no brief found) allows both."""
    hits = [steps / "01_brief" / run / "briefs" / f"{brief_id}.md"] + sorted(steps.glob(f"01_brief/*/briefs/{brief_id}.md"))
    f = next((h for h in hits if h.exists()), None)
    return (brief_sides(f.read_text()) if f else ()) or SIDES


def in_box(text, run, box, steps=STEPS):
    """Whether an idea (its file's text) acts in the box: its `profile:` line holds the box's profile, and its brief's
    side includes the box's side. Recorded, never used to refuse or filter (the operator, 2026-11-27)."""
    h = header_fields(text)
    return holds(profile_name(h.get("profile")), box["profile"]) and box["side"] in brief_side(h.get("brief", ""), run, steps)


# --- the rule that chooses it -----------------------------------------------------------------------------------

def map_strategies(steps=STEPS):
    """The profile map's strategies: the register's paying books, each with the profile its idea names and its side."""
    sys.path.insert(0, str(steps / "orchestration" / "ideas_similarities_check" / "helper"))
    import ideas_similarities_check as isc
    reg = steps / "orchestration" / "ideas_similarities_check" / "register"
    return [{**r, "named": isc.book_profile(r, steps)} for r in isc.books(reg) if r["kind"] == "paying"]


def market_shares(steps=STEPS):
    """The market's share of each profile on the portfolio's coins and days: the last portfolio version built on the
    common records (common/data_use.md, steps 9 and 10: the 25 portfolio coins, 2016-2026), its `boxes.csv` (the box
    reader on each candidate's common record), each candidate counted once. ({profile: share}, version, candidates)."""
    import pandas as pd
    sys.path.insert(0, str(steps / "orchestration" / "combine" / "helper"))
    import update
    v, _ = update.last_list()
    if v is None:
        sys.exit("no portfolio version built on the common records: the rule has no share of market days")
    rows = pd.read_csv(update.PORTFOLIOS / v / "boxes.csv")
    rows = rows[(rows.box_side == "long") & rows.market.notna()]
    per = rows.groupby("profile").market.mean()
    return {p: float(per.get(p, 0.0)) for p in PROFILES}, v, rows.key.nunique()


def choose(steps=STEPS, strategies=None, shares=None):
    """The rule (common/target_box.md): {'box': (profile, side), 'table': [one row per box, the winner first], ...}."""
    strategies = map_strategies(steps) if strategies is None else strategies
    version = read = None
    if shares is None:
        shares, version, read = market_shares(steps)
    table = []
    for p, s in BOXES:
        on = [r for r in strategies if r.get("side") in (s, "both")]
        n = sum(1 for r in on if r.get("named") == p)
        table.append({"profile": p, "side": s, "named_exactly": n, "in_map": sum(1 for r in on if holds(r.get("named"), p)),
                      "share": round(shares[p], 4), "score": round(shares[p] / (1 + n), 4)})
    table.sort(key=lambda r: (-r["score"], -r["share"], r["in_map"]))
    return {"box": (table[0]["profile"], table[0]["side"]), "table": table, "strategies": len(strategies),
            "shares_from": version, "candidates_read": read}


def start(run, value, steps=STEPS):
    """run_brief's --target-box: the run's box written once (auto: the rule; else the operator's box), kept when
    resumed; refused when the run already has another box. Returns the run's box, or None (no option, no file)."""
    have = run_box(run, steps)
    if value is None:
        return have
    if value.strip().lower() != "auto" and parse_box(value) is None:
        sys.exit(f"--target-box: '{value}' is not one of the twelve boxes ('auto', or a profile then a side: "
                 f"'rising agitated, long')")
    if have is not None:
        want = parse_box(value)
        if want and want != (have["profile"], have["side"]):
            sys.exit(f"{run}: the run's box is {box_name(have)}, not {want[0]}, {want[1]}")
        return have
    if value.strip().lower() == "auto":
        c = choose(steps)
        box = {"profile": c["box"][0], "side": c["box"][1], "chosen_by": "the rule (common/target_box.md)",
               "strategies_in_map": c["strategies"], "shares_from": f"portfolio {c['shares_from']}, "
               f"{c['candidates_read']} common records", "table": c["table"]}
    else:
        p, s = parse_box(value)
        box = {"profile": p, "side": s, "chosen_by": "the operator"}
    box = {**box, "at": utc_now()}
    f = box_file(run, steps)
    f.parent.mkdir(parents=True, exist_ok=True)
    write_atomic(f, json.dumps(box, indent=1) + "\n")
    return box


def table_md(c):
    lines = [f"The map's strategies: {c['strategies']}; the shares from portfolio {c['shares_from']} "
             f"({c['candidates_read']} common records: the 25 portfolio coins, 2016-2026).", "",
             "| Rank | Box | Strategies naming it exactly | Strategies acting in it (the map) | Share of market days | Score = share / (1 + exact) |",
             "|---|---|---|---|---|---|"]
    lines += [f"| {i} | {r['profile']}, {r['side']} | {r['named_exactly']} | {r['in_map']} | {100 * r['share']:.1f} % | {r['score']:.4f} |"
              for i, r in enumerate(c["table"], 1)]
    return "\n".join(lines)


if __name__ == "__main__":
    c = choose()
    print(f"The box chosen: {c['box'][0]}, {c['box'][1]}\n")
    print(table_md(c))
