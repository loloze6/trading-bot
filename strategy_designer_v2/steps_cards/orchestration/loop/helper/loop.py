"""loop: from a starting idea, run_idea on the idea select_next ranks first, turn after turn, until stopped.

  python3 orchestration/loop/helper/loop.py --run NAME_run --python VENV_PYTHON [IDEA_FILE [--brief BRIEF]] [--budget USD] [--model M]

It has no limit of its own: it stops when the operator stops it (it resumes from the run's files), when the optional
budget is reached (an idea already started is finished), or when no candidate is left. It decides only which idea comes
next (select_next's ranking); the steps judge. Between two ideas it calls the components step (components/card.md) on
the run's open wishes: every 10 turns since its last call, and before stopping for "no candidate left"; what it builds
unblocks ideas, which select_next counts as candidates again. Before each turn it turns every new discovery a line
wrote in the run (an idea off its brief's theme: common/theme.md) into a brief, by run_brief's steps 1 and 2: the
brief's ideas are first ideas, ranked like any brief's. Visibility only: loop.jsonl (one line per turn, per call
of the components step, per stop), queue.md and queue.json (every idea written in the run and what happened to it, a
reached goal marked).
"""
import argparse, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORCH = HERE.parents[1]
STEPS = ORCH.parent
sys.path.insert(0, str(STEPS / "common"))
sys.path.insert(0, str(ORCH / "select_next" / "helper"))
from lib import write_atomic, utc_now, SERVICE_REFUSED  # noqa: E402
import select_next  # noqa: E402
sys.path.insert(0, str(STEPS / "components" / "helper"))
import wishes  # noqa: E402
sys.path.insert(0, str(ORCH / "run_brief" / "helper"))
import run_brief  # noqa: E402

RUN_IDEA = ORCH / "run_idea" / "helper" / "run_idea.py"
BUILDER = STEPS / "components" / "helper" / "build_component.py"
COMPONENTS_EVERY = 10      # turns between two calls of the components step (operator, 2026-11-17)


def table_rows(run, root=ORCH):
    p = root / "run_idea" / run / "table.json"
    return json.loads(p.read_text()) if p.exists() else []


def spent(run, root=ORCH):
    """The run's USD so far: the ideas' costs in run_idea's table (from its journal), the components step's calls for
    the run (from its journal), and run_brief's steps 1 and 2 (from its journal: the run's brief, its discoveries)."""
    p = root.parent / "components" / "journal.jsonl"
    built = sum(e.get("usd", 0.0) for e in map(json.loads, p.read_text().splitlines()) if e.get("run") == run) if p.exists() else 0.0
    return round(sum(r.get("cost", 0.0) for r in table_rows(run, root)) + built + run_brief.spent(root / "run_brief" / run), 4)


def turns(run, root=ORCH):
    p = root / "loop" / run / "loop.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def next_turn(run, root=ORCH):
    """The number of the next turn: the turns logged so far, not the stop or failure lines, plus one."""
    return sum("turn" in t for t in turns(run, root)) + 1


def turns_since_components(run, root=ORCH):
    """The turns logged since the components step was last called in the run (all the run's turns if never)."""
    n = 0
    for t in turns(run, root):
        if "components" in t:
            n = 0
        elif "turn" in t:
            n += 1
    return n


def call_components(args):
    """The components step on the run's open wishes; its summary line."""
    cmd = [sys.executable, str(BUILDER), "--runs", args.run, "--python", args.python] + (["--model", args.model] if args.model else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout.strip().splitlines() or p.stderr.strip().splitlines()      # its summary is its last line on stdout
    return p.returncode, (out[-1:] or [""])[0]


def components_due(args, why_stop):
    """Call the components step now? When the run has open wishes, and either 10 turns have passed since its last call,
    or the loop would stop for no candidate left. Never twice without a turn between (a call that failed before
    answering is not repeated in a row)."""
    if not wishes.open_wishes([args.run], STEPS):
        return False
    n = turns_since_components(args.run, ORCH)
    return n >= COMPONENTS_EVERY or (why_stop == "no candidate left" and n > 0)


def failed(run, root=ORCH):
    """Ideas whose run_idea call failed: not picked again (they are not retried). An idea's latest outcome line counts:
    a later line that is not a failure (a "retry" line, written with its reason when the failure was not the idea's,
    such as the model service refusing every call; 2026-11-21) makes it a candidate again."""
    latest = {}
    for t in turns(run, root):
        if "idea" in t and "outcome" in t:
            latest[t["idea"]] = t["outcome"]
    return {i for i, o in latest.items() if o.startswith("failed")}


def unfinished(run, root=ORCH):
    """Ideas whose latest turn did not finish: no row in run_idea's table written after that turn started, and not
    marked failed. The loop was stopped mid-idea (the operator, a restart). Their plan exists, so select_next counts them
    as tested; they are finished first when the loop resumes (run_idea skips the steps already done). An idea turned
    again after a row (a refusal the components step unblocked) is unfinished until run_idea writes its row again
    (2026-11-19: 017-02 was read as finished from its old refusal row). A row written before rows carried their end
    time (`finished_at`) counts as finished, as before."""
    ended = {r["idea"]: r.get("finished_at", "") for r in table_rows(run, root)}
    latest = {}
    for t in turns(run, root):
        if "turn" in t:
            latest[t.get("idea")] = t.get("at", "")
    out = [i for i, at in latest.items() if i not in ended or (ended[i] and ended[i] < at)]
    return [i for i in out if i not in failed(run, root)]


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
    entry = {"at": utc_now(), "run": run, **entry}
    with open(d / "loop.jsonl", "a") as fh:
        fh.write(json.dumps(entry) + "\n")


def discoveries(run, root=STEPS):
    """The discoveries the run's lines wrote (topic 50): `07?_*/<run>/<backtest>/discoveries/<id>.md`."""
    return sorted(root.glob(f"07?_*/{run}/*/discoveries/*.md"))


def briefed(run, root=ORCH):
    """The discoveries already turned into a brief (or found not researchable) in the run: logged in loop.jsonl."""
    return {t["discovery"] for t in turns(run, root) if "discovery" in t and "outcome" in t}


def brief_discoveries(args, steps=STEPS, root=ORCH):
    """Each new discovery becomes a brief (step 1, with the discovery as its source) and its first ideas (step 2), once;
    logged in loop.jsonl. False when the model service refused a call (the loop stops, to resume later)."""
    done = briefed(args.run, root)
    for f in discoveries(args.run, steps):
        rel = str(f.relative_to(steps))
        if rel in done or stop_reason(args.budget, spent(args.run, root), [rel]):
            continue
        used = spent(args.run, root)
        try:
            brief, why = run_brief.write_brief(args.run, source=f, model=args.model)
            ideas, why = run_brief.write_ideas(args.run, brief, args.model) if brief else ([], why)
        except SystemExit as e:
            if e.code != SERVICE_REFUSED:
                raise
            log_turn(args.run, {"stop": f"{REFUSED} (a discovery's brief; resume the loop later)", "spent": used}, root)
            print(f"{args.run}: stopped: {REFUSED} (a discovery's brief)")
            return False
        log_turn(args.run, {"discovery": rel, "brief": brief.stem if brief else None, "ideas": len(ideas),
                            "outcome": why or "ok", "spent_before": used}, root)
        print(f"{args.run}: discovery {f.stem}: " + (f"brief {brief.stem}, {len(ideas)} ideas" if brief and ideas else why))
    return True


def call_run_idea(idea_path, args, brief=None):
    cmd = [sys.executable, str(RUN_IDEA), str(idea_path), "--run", args.run, "--python", args.python]
    if brief:
        cmd += ["--brief", str(brief)]
    if args.model:
        cmd += ["--model", args.model]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]


REFUSED = "not run: the model service refused a call"


def refused(run, iid, code, last, root=ORCH):
    """A turn the model service refused (exit SERVICE_REFUSED: a usage limit, an outage): not the idea's fault. Nothing
    is marked failed; the loop stops, and the idea is picked again when the loop is resumed (2026-11-21, night 3: the
    account's usage limit marked 138 untested ideas failed in minutes, and turned one idea about 4,000 times)."""
    if code != SERVICE_REFUSED:
        return False
    log_turn(run, {"idea": iid, "outcome": f"{REFUSED}: {last[0][:300]}"}, root)
    log_turn(run, {"stop": f"{REFUSED} (resume the loop later)", "spent": spent(run, root)}, root)
    print(f"{run}: stopped: {REFUSED}: {last[0][:200]}")
    return True


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path, nargs="?", help="the starting idea (a new run); without it, the run's own ideas are used")
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
    if args.idea is None and not table_rows(args.run) and not select_next.written_in(args.run):
        sys.exit("a new run needs a starting idea, or ideas already written in it (run_brief's step 2)")

    if args.idea is not None and args.idea.stem not in {r["idea"] for r in table_rows(args.run)}:
        used = spent(args.run)
        log_turn(args.run, {"turn": next_turn(args.run), "idea": args.idea.stem, "why": "the starting idea", "spent_before": used})
        code, last = call_run_idea(args.idea, args, args.brief)
        if refused(args.run, args.idea.stem, code, last):
            return
        if code:
            log_turn(args.run, {"idea": args.idea.stem, "outcome": f"failed: {last[0][:300]}"})
    paths = {f.stem: f for f in select_next.written_in(args.run)}
    for iid in unfinished(args.run):
        if iid not in paths:
            continue
        why = stop_reason(args.budget, spent(args.run), [iid])          # the budget holds for a resumed idea too
        if why:                                                        # (2026-11-21: 29 resumed ideas ran past it)
            log_turn(args.run, {"stop": why, "spent": spent(args.run)})
            print(f"{args.run}: stopped: {why}")
            return
        log_turn(args.run, {"idea": iid, "resumed": "its run was stopped before it finished", "spent_before": spent(args.run)})
        code, last = call_run_idea(paths[iid], args)
        if refused(args.run, iid, code, last):
            return
        if code:
            log_turn(args.run, {"idea": iid, "outcome": f"failed: {last[0][:300]}"})
    while True:
        if not brief_discoveries(args):
            return
        ranking = select_next.rank(args.run, exclude=failed(args.run))
        cands = [r for r in ranking if r["status"] == "candidate"]
        used = spent(args.run)
        why = stop_reason(args.budget, used, cands)
        if not (why or "").startswith("budget") and components_due(args, why):
            code, last = call_components(args)
            log_turn(args.run, {"components": last[:300], "outcome": "ok" if code == 0 else f"failed (exit {code})",
                                "spent_before": used})
            print(f"{args.run}: components: {last[:200]}")
            if code == SERVICE_REFUSED:
                log_turn(args.run, {"stop": f"{REFUSED} (the components step; resume the loop later)", "spent": used})
                print(f"{args.run}: stopped: {REFUSED} (the components step)")
                return
            continue
        write_queue(args.run, ranking)
        if why:
            log_turn(args.run, {"stop": why, "spent": used})
            print(f"{args.run}: stopped: {why}")
            return
        top = cands[0]
        log_turn(args.run, {"turn": next_turn(args.run), "idea": top["idea"],
                            "why": f"select_next rank 1: score {top['score']} = record {top['record']} ({top['line']}) / (1 + generation {top['generation']})",
                            "spent_before": used})
        code, last = call_run_idea(Path(top["path"]), args)
        if refused(args.run, top["idea"], code, last):
            return
        if code:
            log_turn(args.run, {"idea": top["idea"], "outcome": f"failed: {last[0][:300]}"})
        print(f"{args.run}: {top['idea']}: {last[0][:200]}")


if __name__ == "__main__":
    main()
