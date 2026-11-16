"""loop: from a starting idea, run_idea on the idea select_next ranks first, turn after turn, until stopped.

  python3 orchestration/loop/helper/loop.py --run NAME_run --python VENV_PYTHON [IDEA_FILE [--brief BRIEF]] [--budget USD] [--model M]

It has no limit of its own: it stops when the operator stops it (it resumes from the run's files), when the optional
budget is reached (an idea already started is finished), or when no candidate is left. It decides only which idea comes
next (select_next's ranking); the steps judge. Visibility only: loop.jsonl (one line per turn), queue.md and queue.json
(every idea written in the run and what happened to it, a reached goal marked).
"""
import argparse, datetime, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORCH = HERE.parents[1]
STEPS = ORCH.parent
sys.path.insert(0, str(STEPS / "common"))
sys.path.insert(0, str(ORCH / "select_next" / "helper"))
from lib import write_atomic  # noqa: E402
import select_next  # noqa: E402

RUN_IDEA = ORCH / "run_idea" / "helper" / "run_idea.py"


def table_rows(run, root=ORCH):
    p = root / "run_idea" / run / "table.json"
    return json.loads(p.read_text()) if p.exists() else []


def spent(run, root=ORCH):
    """The run's USD so far: the ideas' costs in run_idea's table (from its journal)."""
    return round(sum(r.get("cost", 0.0) for r in table_rows(run, root)), 4)


def turns(run, root=ORCH):
    p = root / "loop" / run / "loop.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def failed(run, root=ORCH):
    """Ideas whose run_idea call failed: not picked again (they are not retried)."""
    return {t["idea"] for t in turns(run, root) if t.get("outcome", "").startswith("failed")}


def stop_reason(budget, used, candidates):
    if budget is not None and used >= budget:
        return f"budget reached ({used:.2f} of {budget:.2f} USD)"
    if not candidates:
        return "no candidate left"
    return None


def goal(row):
    return bool(row) and str(row.get("step5", "")).startswith("confirmed") and str(row.get("step6", "")).startswith("profitable")


def write_queue(run, ranking, root=ORCH):
    rows = {r["idea"]: r for r in table_rows(run, root)}
    d = root / "loop" / run
    d.mkdir(parents=True, exist_ok=True)
    out = []
    for r in ranking:
        t = rows.get(r["idea"])
        what = r["status"]
        if r["status"] == "tested" and t:
            what = f"tested: step 5 {t.get('step5', '-')}; step 6 {t.get('step6', '-')}" + ("  GOAL REACHED" if goal(t) else "")
        out.append({**{k: r.get(k) for k in ("idea", "line", "generation", "record", "score")}, "status": what})
    write_atomic(d / "queue.json", json.dumps(out, indent=2) + "\n")
    lines = ["# Queue (loop)\n", f"Every idea written in the run; candidates first, in select_next's order. Spent: {spent(run, root):.2f} USD.\n",
             "| Rank | Idea | Line | Generation | Record | Score | Status |", "|---|---|---|---|---|---|---|"]
    rank = 0
    for r in out:
        rank += r["status"] == "candidate"
        lines.append(f"| {rank if r['status'] == 'candidate' else '-'} | {r['idea']} | {r.get('line') or '?'} | {r.get('generation', '')} | "
                     f"{r.get('record', '')} | {r.get('score', '')} | {r['status']} |")
    write_atomic(d / "queue.md", "\n".join(lines) + "\n")


def log_turn(run, entry, root=ORCH):
    d = root / "loop" / run
    d.mkdir(parents=True, exist_ok=True)
    entry = {"at": datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S UTC"), "run": run, **entry}
    with open(d / "loop.jsonl", "a") as fh:
        fh.write(json.dumps(entry) + "\n")


def call_run_idea(idea_path, args, brief=None):
    cmd = [sys.executable, str(RUN_IDEA), str(idea_path), "--run", args.run, "--python", args.python]
    if brief:
        cmd += ["--brief", str(brief)]
    if args.model:
        cmd += ["--model", args.model]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path, nargs="?", help="the starting idea (a new run); without it, the run is resumed")
    a.add_argument("--run", required=True)
    a.add_argument("--python", required=True)
    a.add_argument("--brief", type=Path)
    a.add_argument("--budget", type=float, help="stop once the run's USD reaches this (optional; no limit otherwise)")
    a.add_argument("--model")
    args = a.parse_args()
    if not args.run.endswith("_run"):
        sys.exit("a run name ends in _run")
    if args.budget is not None and args.budget <= 0:
        sys.exit("a budget is a positive number of USD")
    if args.idea is None and not table_rows(args.run):
        sys.exit("a new run needs a starting idea")

    if args.idea is not None and args.idea.stem not in {r["idea"] for r in table_rows(args.run)}:
        used = spent(args.run)
        log_turn(args.run, {"turn": len(turns(args.run)) + 1, "idea": args.idea.stem, "why": "the starting idea", "spent_before": used})
        code, last = call_run_idea(args.idea, args, args.brief)
        if code:
            log_turn(args.run, {"idea": args.idea.stem, "outcome": f"failed: {last[0][:300]}"})
    while True:
        ranking = select_next.rank(args.run, exclude=failed(args.run))
        write_queue(args.run, ranking)
        cands = [r for r in ranking if r["status"] == "candidate"]
        used = spent(args.run)
        why = stop_reason(args.budget, used, cands)
        if why:
            log_turn(args.run, {"stop": why, "spent": used})
            print(f"{args.run}: stopped: {why}")
            return
        top = cands[0]
        log_turn(args.run, {"turn": len(turns(args.run)) + 1, "idea": top["idea"],
                            "why": f"select_next rank 1: score {top['score']} = record {top['record']} ({top['line']}) / (1 + generation {top['generation']})",
                            "spent_before": used})
        code, last = call_run_idea(Path(top["path"]), args)
        if code:
            log_turn(args.run, {"idea": top["idea"], "outcome": f"failed: {last[0][:300]}"})
        print(f"{args.run}: {top['idea']}: {last[0][:200]}")


if __name__ == "__main__":
    main()
