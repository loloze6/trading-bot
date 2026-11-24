"""select_next: which idea of a run to test next.

  python3 orchestration/select_next/helper/select_next.py --run NAME_run [--top N]

Candidates: the ideas written in the run (by step 2, or the run's starting idea, in 02_ideation/<run>/ideas/; by a step 7
line in 07x_<line>/<run>/<backtest>/ideas/), not yet tested in the run (no plan for them in 03_test_plan/<run>/plans/,
or a missing-components refusal the components step has unblocked: components/card.md), not duplicates (same Idea text
and same data as an idea tested or listed before them).

Order (operator, 2026-11-17 and 2026-11-22), three groups, each ranked by its priority:
  1. a brief's own ideas (generation 0), by score: every idea of a theory is tested once before the workflow goes deep;
  2. ideas written from a confirmed idea whose book is more different from the held books than no evidence (w > 0.5):
     real ideas unlike what we hold, by priority;
  3. the others, by priority (an idea written from a confirmed idea we already hold, w < 0.5, after the unproven ones).
score = record of the line that wrote the idea / (1 + the idea's generation); priority = score x w
w = the parent's difference = 1 - the share of the parent's book its nearest held book explains (the paying books and
the portfolio's books, register/held.json, 2026-11-24; the similarity
register, orchestration/ideas_similarities_check/: common/measures.md), when the parent is confirmed and in the
register; 0.5 (no evidence) otherwise, as a line with no record has 0.5.
record = (s + 1) / (n + 2) over every analysis of that line with a tested idea, in every named run (the same idea
read by a line in two runs is two analyses); s the analyses with a
success (at least one tested idea with a profitable book: step 6's "profitable enough"; operator, 2026-11-19). Words and id convention:
common/idea_created_from.md. It writes nothing; it returns (and prints) the ranking.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import header_fields, idea_code  # noqa: E402  (shared helpers, common/lib.py)
sys.path.insert(0, str(STEPS / "components" / "helper"))
import wishes  # noqa: E402  (the components step: which refusals are unblocked)

SEG = re.compile(r"\.([a-g])(\d+)(?=[._])")          # one analysis in an id: .<line letter><number>, then _ or .
BRIEF_IDEA = re.compile(r"^(\d{3})-(\d{2})_")          # an idea created from a brief: NNN-KK_
BAR = re.compile(r"_\d+[mhdw]$")                       # a plan's id ends with its bar size


def id_parts(idea_id):
    """(line, created_from, number, generation) read from an id; line 'step 2' for a brief's idea, None if the id does
    not follow the convention (ideas renamed by hand). created_from is the parent's lineage code (`idea_code`), the
    same for an id written in either convention (topic 46)."""
    segs = list(SEG.finditer(idea_id))
    if segs:
        last = segs[-1]
        return "7." + last.group(1), idea_code(idea_id[:last.start()]), int(last.group(2)), len(segs)
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
        if not v.exists():
            continue                     # not tested: no plan could be built (step 3), or no backtest; no evidence about the line
        # a success is a book that pays (step 6), not a confirmation: on finer bars a small effect is confirmed
        # easily and never pays (topic 30, 2026-11-19)
        ok = c.exists() and json.loads(c.read_text()).get("status") == "profitable enough"
        key = (run, line, created_from)                    # each run's reading is its own analysis
        analyses[key] = analyses.get(key, False) or bool(ok)
    out = {}
    for (_, line, _), ok in analyses.items():
        s, n = out.get(line, (0, 0))[:2]
        out[line] = (s + ok, n + 1)
    return {line: (s, n, (s + 1) / (n + 2)) for line, (s, n) in out.items()}


REGISTER = STEPS / "orchestration" / "ideas_similarities_check" / "register"


def parent_evidence(root=STEPS):
    """{(run, parent idea id or its lineage code): (kind, difference)} for every book of the similarity register: its kind (paying or
    confirmed) and 1 - the share its nearest held book explains (the paying books and the portfolio's, register/held.json;
    a comparison made before 2026-11-24 has its nearest paying book only); None if none is comparable."""
    reg = root / "orchestration" / "ideas_similarities_check" / "register"
    f = reg / "books.json"
    out = {}
    for r in (json.loads(f.read_text()) if f.exists() else []):
        c = reg / "comparisons" / f"{r['key']}.json"
        cj = json.loads(c.read_text()) if c.exists() else {}
        n = cj["nearest_held"] if "nearest_held" in cj else cj.get("nearest_relative")
        v = (r.get("kind", "paying"), 1 - n["share_explained"] if n else None)
        out[(r["run"], BAR.sub("", r["id"]))] = v                  # by the parent's id (an idea file's source-idea)
        out.setdefault((r["run"], idea_code(BAR.sub("", r["id"]))), v)   # and by its lineage code (an id alone, topic 46)
    return out


def parent_confirmed(run, created_from, root=STEPS):
    """Whether the idea a candidate was written from (its id, or its lineage code) was confirmed by step 5 in the run
    (any of its plans)."""
    for v in (root / "05_verification" / run / "verdicts").glob(f"{created_from.split('.')[0].split('_')[0]}*/result.json"):
        idea = BAR.sub("", v.parent.name)
        if created_from in (idea, idea_code(idea)) and json.loads(v.read_text()).get("status") == "confirmed":
            return True
    return False


NAME_MAX = 255          # the longest file name the system writes, in bytes (Linux)
def longest_name(idea_id, run):
    """The longest file name an idea's test writes (topic 46): step 3's config (`<id>_<bar>_config.json`) or the
    similarity register's returns (`<run>__<id>_<bar>.csv.gz`), with the longest bar."""
    return max(len(f"{idea_id}_4h_config.json".encode()), len(f"{run}__{idea_id}_4h.csv.gz".encode()))


def too_long(idea_id, run=""):
    """Whether some file of this idea's test cannot be written: its longest name over the file name limit (topic 46: an
    id grows with every generation; step 3, or the similarity register after step 6, then fails "File name too long")."""
    return longest_name(idea_id, run) > NAME_MAX


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
    """The ids of the ideas tested in the run: those with a plan in it, but a missing-components refusal the components
    step has unblocked (every wish answered built or exists, the catalogue changed since): that idea is a candidate
    again."""
    out = set()
    for plan in (root / "03_test_plan" / run / "plans").glob("*.md"):
        if plan.name in ("INDEX.md", "COMPONENT_WISHLIST.md"):
            continue
        if wishes.unblocked(plan, root):
            continue
        out.add(header_fields(plan.read_text()).get("idea") or BAR.sub("", plan.stem))
    return out


def rank(run, root=STEPS, exclude=()):
    """The run's ideas: candidates ranked by score, then the others (tested, duplicate, unreadable, excluded)."""
    recs, tested = records(root), tested_in(run, root)
    evidence = parent_evidence(root)
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
        # the idea it was written from, as its file names it (the id holds only its lineage code since topic 46)
        created_from = header_fields(text).get("source-idea") or created_from
        rec = record_of(line, recs)
        row = {"idea": iid, "path": str(f), "line": line or "?", "generation": gen, "number": number,
               "record": round(rec, 4), "score": round(rec / (1 + gen), 4)}
        # the group and the priority (operator, 2026-11-22): a brief's idea; an idea written from a confirmed idea,
        # weighted by how different that idea's book is from the paying books; the others
        if gen == 0:
            row["group"], row["priority"] = 1, row["score"]
        else:
            d = evidence.get((run, created_from), (None, None))[1] if created_from and parent_confirmed(run, created_from, root) else None
            row["difference"] = round(d, 4) if d is not None else None
            w = d if d is not None else 0.5
            row["group"], row["priority"] = (2 if w > 0.5 else 3), round(row["score"] * w, 4)
        if iid in seen.values() and iid in tested:
            continue                                       # the same file found twice (a copy in the run)
        if iid in tested:
            row["status"] = "tested"
        elif key[0] and key in seen:
            row["status"] = f"duplicate of {seen[key]}"
        elif iid in exclude:
            row["status"] = "excluded"
        elif too_long(iid, run):
            row["status"] = "not testable: its id is too long for a file name (topic 46)"
        else:
            row["status"] = "candidate"
        if key[0]:
            seen.setdefault(key, iid)
        rows.append(row)
    # a brief's own ideas first (operator, 2026-11-17); then the real ideas unlike what we earn; then the others
    # (operator, 2026-11-22); within a group, by priority; ties: the lower number first
    cands = sorted((r for r in rows if r["status"] == "candidate"),
                   key=lambda r: (r["group"], -r["priority"], r["number"], r["idea"]))
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
    print(f"\n| Rank | Idea | Line | Generation | Record | Score | Group | Parent's difference | Priority | Status |\n|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows[: args.top], 1):
        print(f"| {i if r['status'] == 'candidate' else '-'} | {r['idea']} | {r.get('line', '?')} | {r.get('generation', '')} | "
              f"{r.get('record', '')} | {r.get('score', '')} | {r.get('group', '')} | {r.get('difference', '')} | {r.get('priority', '')} | {r['status']} |")


if __name__ == "__main__":
    main()
