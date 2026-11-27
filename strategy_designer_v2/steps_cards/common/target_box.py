"""A run's target box (common/target_box.md): the rule that chooses it from the profile map, the run's file, and
whether an idea acts in it.

  python3 common/target_box.py            the rule on today's map: the twelve boxes' counts, shares and scores

Why this cannot leak: the choice reads finished records (the register, the box reader's shares) before a run starts;
the filter reads header lines of the idea and its brief. No bar of a run's data is read.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parent
sys.path.insert(0, str(HERE))
from lib import header_fields, profile_name, write_atomic, utc_now, PROFILES  # noqa: E402

SIDES = ("long", "short")
BOXES = [(p, s) for p in PROFILES for s in SIDES]          # the twelve boxes, in the map's order
BRIEF_SIDE = {"long only": ("long",), "short only": ("short",)}


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


# --- which ideas act in the box ---------------------------------------------------------------------------------

def shares_profile(idea_profile, box_profile):
    """Whether an idea's profile acts in the box's profile: the words of both are together still one of the six
    profiles ('rising' and 'rising agitated': yes; 'rising calm' and 'rising agitated': no). None: no profile, no."""
    if not idea_profile:
        return False
    words = dict.fromkeys(f"{idea_profile} {box_profile}".split())          # each word once ("rising" in both)
    return profile_name(" ".join(words)) is not None


def brief_side(brief_id, run, steps=STEPS):
    """The sides an idea's brief allows (its `side:` header line, as step 3 reads it): ('long',), ('short',) or both.
    The run's copy of the brief, else step 1's lists; a brief not found allows both (as step 3 adds no side)."""
    hits = [steps / "01_brief" / run / "briefs" / f"{brief_id}.md"] + sorted(steps.glob(f"01_brief/*/briefs/{brief_id}.md"))
    f = next((h for h in hits if h.exists()), None)
    side = header_fields(f.read_text()).get("side", "").strip().lower() if f else ""
    return BRIEF_SIDE.get(side, SIDES)


def idea_profile_side(text, run, steps=STEPS):
    """(the idea's profile or None, the sides it may take), from the idea file's header and its brief's."""
    h = header_fields(text)
    return profile_name(h.get("profile")), brief_side(h.get("brief", ""), run, steps)


def in_box(text, run, box, steps=STEPS):
    """Whether an idea (its file's text) acts in the box {profile, side} (common/target_box.md). The box's side may be
    'both' (a reading of an older run's header): any side then shares it."""
    prof, sides = idea_profile_side(text, run, steps)
    box_sides = SIDES if box["side"] == "both" else (box["side"],)
    return shares_profile(prof, box["profile"]) and any(s in sides for s in box_sides)


# --- the rule that chooses it -----------------------------------------------------------------------------------

def map_strategies(steps=STEPS):
    """The profile map's strategies: the register's paying books, each with the profile its idea names and its side."""
    sys.path.insert(0, str(steps / "orchestration" / "ideas_similarities_check" / "helper"))
    import ideas_similarities_check as isc
    reg = steps / "orchestration" / "ideas_similarities_check" / "register"
    return [{**r, "named": isc.book_profile(r, steps)} for r in isc.books(reg) if r["kind"] == "paying"]


def market_shares(strategies, steps=STEPS):
    """The market's share of each profile on the map's strategies (each strategy's coins and dates, as the combination
    step's box reader reads them), each strategy counted once: ({profile: share}, strategies read)."""
    import pandas as pd
    boxes_csv = steps / "orchestration" / "combine" / "boxes.csv"
    rows = pd.read_csv(boxes_csv) if boxes_csv.exists() else pd.DataFrame(columns=["key", "profile", "box_side", "market"])
    rows = rows[rows.box_side == "long"]
    kept = {k: g.set_index("profile").market.to_dict() for k, g in rows.groupby("key")}
    per = []
    for r in strategies:
        m = kept.get(r["key"])
        if m is None:
            sys.path.insert(0, str(steps / "orchestration" / "combine" / "helper"))
            import boxes
            res = boxes.read_book(steps / "04_backtest" / r["run"] / "backtests" / r["id"])
            m = {p: res["cells"][(p, "long")]["market"] for p in PROFILES} if res else None
        if m is not None and all(p in m and m[p] == m[p] for p in PROFILES):
            per.append(m)
    return {p: (sum(m[p] for m in per) / len(per) if per else 0.0) for p in PROFILES}, len(per)


def choose(steps=STEPS, strategies=None, shares=None):
    """The rule (common/target_box.md): {'box': (profile, side), 'table': [one row per box, the winner first],
    'strategies': n, 'read': n}."""
    strategies = map_strategies(steps) if strategies is None else strategies
    read = None
    if shares is None:
        shares, read = market_shares(strategies, steps)
    table = []
    for p, s in BOXES:
        n = sum(1 for r in strategies if r.get("named") == p and r.get("side") in (s, "both"))
        table.append({"profile": p, "side": s, "named_exactly": n, "share": round(shares[p], 4),
                      "score": round(shares[p] / (1 + n), 4)})
    order = sorted(range(len(table)), key=lambda i: (-table[i]["score"], -table[i]["share"], i))
    table = [table[i] for i in order]
    return {"box": (table[0]["profile"], table[0]["side"]), "table": table, "strategies": len(strategies), "read": read}


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
               "strategies_in_map": c["strategies"], "strategies_read_for_shares": c["read"], "table": c["table"]}
    else:
        p, s = parse_box(value)
        box = {"profile": p, "side": s, "chosen_by": "the operator"}
    box = {**box, "at": utc_now()}
    f = box_file(run, steps)
    f.parent.mkdir(parents=True, exist_ok=True)
    write_atomic(f, json.dumps(box, indent=1) + "\n")
    return box


def table_md(c):
    lines = [f"The map's strategies: {c['strategies']}; their market shares read: {c['read']}.", "",
             "| Rank | Box | Strategies naming it exactly | Share of market days | Score = share / (1 + count) |",
             "|---|---|---|---|---|"]
    lines += [f"| {i} | {r['profile']}, {r['side']} | {r['named_exactly']} | {100 * r['share']:.1f} % | {r['score']:.4f} |"
              for i, r in enumerate(c["table"], 1)]
    return "\n".join(lines)


if __name__ == "__main__":
    c = choose()
    print(f"The box chosen: {c['box'][0]}, {c['box'][1]}\n")
    print(table_md(c))
