"""select_next: which idea of a run to test next.

  python3 orchestration/select_next/helper/select_next.py --run NAME_run [--top N]

Candidates: the ideas written in the run (by step 2, or the run's starting idea, in 02_ideation/<run>/ideas/; by a step 7
line in 07x_<line>/<run>/<backtest>/ideas/), not yet tested in the run (no plan for them in 03_test_plan/<run>/plans/),
not duplicates (same Idea text and same data as an idea tested or listed before them).

score = record of the line that wrote the idea / (1 + the idea's generation)
record = (s + 1) / (n + 2) over every analysis of that line with a tested idea, in every named run; s the analyses with a
success (at least one tested idea confirmed, or with a profitable book). Words and id convention:
common/idea_created_from.md. It writes nothing; it returns (and prints) the ranking.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import header_fields  # noqa: E402  (shared helpers, common/lib.py)

SEG = re.compile(r"\.([a-g])(\d+)_")                 # one analysis in an id: .<line letter><number>_
BRIEF_IDEA = re.compile(r"^(\d{3})-(\d{2})_")          # an idea created from a brief: NNN-KK_
BAR = re.compile(r"_\d+[mhdw]$")                       # a plan's id ends with its bar size


def id_parts(idea_id):
    """(line, created_from, number, generation) read from an id; line 'step 2' for a brief's idea, None if the id does
    not follow the convention (ideas renamed by hand)."""
    segs = list(SEG.finditer(idea_id))
    if segs:
        last = segs[-1]
        return "7." + last.group(1), idea_id[:last.start()], int(last.group(2)), len(segs)
    m = BRIEF_IDEA.match(idea_id)
    if m:
        return "step 2", m.group(1), int(m.group(2)), 0
    return None, None, 0, 0


def records(root=STEPS):
    """Every line's record, from every named run: {line: (successes, analyses, record)}."""
    analyses = {}
    for plan in sorted(root.glob("03_test_plan/*_run/plans/*.md")):
        if plan.name in ("INDEX.md", "COMPONENT_WISHLIST.md"):
            continue
        run, rid = plan.parents[1].name, plan.stem
        idea = header_fields(plan.read_text()).get("idea") or BAR.sub("", rid)
        line, created_from, _, _ = id_parts(idea)
        if line is None:
            continue
        v = root / "05_verification" / run / "verdicts" / rid / "result.json"
        c = root / "06_profitability" / run / "checks" / rid / "result.json"
        ok = (v.exists() and json.loads(v.read_text()).get("status") == "confirmed") or \
             (c.exists() and json.loads(c.read_text()).get("status") == "profitable enough")
        key = (line, created_from)
        analyses[key] = analyses.get(key, False) or bool(ok)
    out = {}
    for (line, _), ok in analyses.items():
        s, n = out.get(line, (0, 0))[:2]
        out[line] = (s + ok, n + 1)
    return {line: (s, n, (s + 1) / (n + 2)) for line, (s, n) in out.items()}


def record_of(line, recs):
    return recs.get(line, (0, 0, 0.5))[2]                # a line with no analysis yet: (0 + 1) / (0 + 2)


def idea_key(text):
    """What makes two ideas the same: the Idea sentence and the data, whitespace and case aside."""
    h = header_fields(text)
    m = re.search(r"^Idea:\s*(.+)$", text, re.M)
    data = tuple((h.get(k) or "").strip().lower() for k in ("instruments", "bar", "period"))
    return (re.sub(r"\s+", " ", m.group(1).strip().lower()) if m else None), data


def written_in(run, root=STEPS):
    """Every idea file written in the run: the run's own ideas (step 2, the starting idea), then each line's."""
    files = sorted((root / "02_ideation" / run / "ideas").glob("*.md"))
    files += sorted(root.glob(f"07?_*/{run}/*/ideas/*.md"))
    return [f for f in files if f.name != "INDEX.md"]


def tested_in(run, root=STEPS):
    """The ids of the ideas tested in the run: those with a plan in it."""
    out = set()
    for plan in (root / "03_test_plan" / run / "plans").glob("*.md"):
        if plan.name in ("INDEX.md", "COMPONENT_WISHLIST.md"):
            continue
        out.add(header_fields(plan.read_text()).get("idea") or BAR.sub("", plan.stem))
    return out


def rank(run, root=STEPS, exclude=()):
    """The run's ideas: candidates ranked by score, then the others (tested, duplicate, unreadable, excluded)."""
    recs, tested = records(root), tested_in(run, root)
    seen, rows = {}, []
    files = written_in(run, root)
    # an idea tested in the run is seen first, so a later idea with the same text and data is its duplicate
    files.sort(key=lambda f: (f.stem not in tested, id_parts(f.stem)[3], f.stem))
    for f in files:
        iid = f.stem
        try:
            text = f.read_text()
            key = idea_key(text)
        except OSError:
            rows.append({"idea": iid, "path": str(f), "status": "unreadable"})
            continue
        line, created_from, number, gen = id_parts(iid)
        rec = record_of(line, recs)
        row = {"idea": iid, "path": str(f), "line": line or "?", "generation": gen, "number": number,
               "record": round(rec, 4), "score": round(rec / (1 + gen), 4)}
        if iid in seen.values() and iid in tested:
            continue                                       # the same file found twice (a copy in the run)
        if iid in tested:
            row["status"] = "tested"
        elif key[0] and key in seen:
            row["status"] = f"duplicate of {seen[key]}"
        elif iid in exclude:
            row["status"] = "excluded"
        else:
            row["status"] = "candidate"
        if key[0]:
            seen.setdefault(key, iid)
        rows.append(row)
    cands = sorted((r for r in rows if r["status"] == "candidate"), key=lambda r: (-r["score"], r["number"], r["idea"]))
    return cands + [r for r in rows if r["status"] != "candidate"]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--run", required=True)
    a.add_argument("--top", type=int, default=20)
    args = a.parse_args()
    if not args.run.endswith("_run"):
        sys.exit("a run name ends in _run")
    recs = records()
    print("Records: " + ", ".join(f"{l} {r[2]:.2f} ({r[0]} of {r[1]})" for l, r in sorted(recs.items(), key=lambda x: -x[1][2])))
    rows = rank(args.run)
    print(f"\n| Rank | Idea | Line | Generation | Record | Score | Status |\n|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows[: args.top], 1):
        print(f"| {i if r['status'] == 'candidate' else '-'} | {r['idea']} | {r.get('line', '?')} | {r.get('generation', '')} | "
              f"{r.get('record', '')} | {r.get('score', '')} | {r['status']} |")


if __name__ == "__main__":
    main()
