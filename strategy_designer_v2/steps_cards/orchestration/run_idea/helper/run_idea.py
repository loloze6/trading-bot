"""run_idea: one idea through steps 3 to 7, each step called as validated, recorded under one run name.

  python3 orchestration/run_idea/helper/run_idea.py IDEA_FILE --run NAME_run --python VENV_PYTHON [--brief BRIEF] [--model M]

It calls the steps' own helpers in order (step 3's plan, step 4's backtest, step 5's verdict, step 6's check, every
active step 7 line), skips a step whose output for the idea already exists in the run, stops where a step stops (a
plan that is not testable), and writes the idea's row in orchestration/run_idea/<run>/table.md and table.json.
It decides nothing: each step's own rules, entry conditions included, are the steps'.
"""
import argparse, json, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import header_fields, write_atomic, utc_now  # noqa: E402  (shared helpers, common/lib.py)
sys.path.insert(0, str(STEPS / "components" / "helper"))
import wishes  # noqa: E402  (the components step: which refusals are unblocked)
sys.path.insert(0, str(STEPS / "04_backtest" / "helper"))
import chart_files  # noqa: E402  (step 4's chart files, for the run viewer)

import yaml  # noqa: E402

DEFAULT_BAR = "1d"   # step 3's default bar size, when the idea's header names none
COST = re.compile(r"cost:?\s*([0-9]+\.[0-9]+)\s*USD")
CALL = re.compile(r"^model call: ([0-9.]+) s; .*?; ([0-9.]+) USD", re.M)          # one line per call (common/lib.py)
KILLED = re.compile(r"^model call: killed after ([0-9]+) s", re.M)


def folders(run):
    """The run's folder in each step, the usual named-run layout."""
    return {"briefs": STEPS / "01_brief" / run / "briefs", "ideas": STEPS / "02_ideation" / run / "ideas",
            "plans": STEPS / "03_test_plan" / run / "plans", "backtests": STEPS / "04_backtest" / run / "backtests",
            "verdicts": STEPS / "05_verification" / run / "verdicts", "checks": STEPS / "06_profitability" / run / "checks",
            "table": HERE.parent / run}


def active_lines():
    """The step 7 lines to run: every line folder whose line.yaml does not say active: false."""
    out = []
    for y in sorted(STEPS.glob("07?_*/helper/line.yaml")):
        line = yaml.safe_load(y.read_text())
        if line.get("active", True):
            out.append((line["id"], y.parents[1]))
    return out


def find_brief(brief_id):
    hits = sorted(STEPS.glob(f"01_brief/*/briefs/{brief_id}.md"))
    if not hits:
        sys.exit(f"the brief {brief_id} is not in any of step 1's brief folders; give it with --brief")
    return hits[0]


def check_idea(text):
    h = header_fields(text)
    missing = [k for k in ("brief",) if not h.get(k)] + [k for k in ("Idea", "Consequence") if not re.search(rf"^{k}:\s*\S", text, re.M)]
    if missing:
        sys.exit(f"the idea file has no {', '.join(missing)}")
    return h


def model_calls(out):
    """The model calls a helper's output reports (common/lib.py prints one line each): [{seconds, usd}], a killed
    call with usd None."""
    calls = [{"seconds": float(s), "usd": float(u)} for s, u in CALL.findall(out)]
    return calls + [{"seconds": float(s), "usd": None} for s in KILLED.findall(out)]


def call(cmd):
    """One step's helper; returns (stdout, its cost): the sum of its model calls' USD, so the calls made before a
    helper stops are counted too (the helper's own "cost: X USD" line if it reports no call line)."""
    p = subprocess.run([sys.executable] + [str(c) for c in cmd], capture_output=True, text=True)
    out = p.stdout + p.stderr
    calls = model_calls(out)
    if calls:
        return out, sum(c["usd"] or 0.0 for c in calls)
    return out, sum(float(c) for c in COST.findall(out))


class Journal:
    """Visibility only: one line per step call in <run>/journal.jsonl, the helper's output in <run>/logs/<rid>/<step>.txt,
    and the consumption of each step (USD, seconds) for the idea's row. It controls nothing."""

    def __init__(self, table_dir, run, rid):
        self.dir, self.run, self.rid, self.use = table_dir, run, rid, {}
        (table_dir / "logs" / rid).mkdir(parents=True, exist_ok=True)

    def step(self, name, cmd, outputs, done=None, said=None):
        """Call a step unless `done` says its output exists; record what happened either way. `said`, if given, reads
        what the step said of itself after the call (a line's "not run: entry condition not met")."""
        t0, out, cost = time.time(), "", 0.0
        action = "skipped: its output exists" if done else "called"
        if not done:
            out, cost = call(cmd)
            (self.dir / "logs" / self.rid / f"{name}.txt").write_text(out)
        secs = round(time.time() - t0, 1)
        calls = model_calls(out)
        killed = sum(c["usd"] is None for c in calls)
        if killed:
            action += f": {killed} model call(s) killed after the timeout, cost unknown"
        if said:
            what = said()
            if what and what.startswith("not run"):
                action += f": {what}"
        u = self.use.setdefault(name, {"usd": 0.0, "seconds": 0.0})
        u["usd"] += cost; u["seconds"] += secs
        rel = lambda x: str(Path(x).resolve().relative_to(STEPS)) if Path(x).exists() else f"{Path(x).name} (not written)"
        entry = {"at": utc_now(), "run": self.run,
                 "backtest": self.rid, "step": name, "action": action, "usd": round(cost, 4), "seconds": secs,
                 "model_calls": len(calls), "longest_call_seconds": max((c["seconds"] for c in calls), default=0.0),
                 "outputs": [rel(o) for o in outputs],
                 "log": str((self.dir / "logs" / self.rid / f"{name}.txt").relative_to(STEPS)) if not done else None}
        with open(self.dir / "journal.jsonl", "a") as fh:
            fh.write(json.dumps(entry) + "\n")
        return out, cost


def copy_into(src, dst):
    """Copy a file into the run, unless it is already that file (a resumed run finds its own copies)."""
    if Path(src).resolve() != Path(dst).resolve():
        shutil.copy(src, dst)


def result(path):
    return json.loads(path.read_text()) if path.exists() else None


def verdict_label(rv):
    """Step 5's status and its statistic, for the row: "confirmed (+2.93)". A verdict without a main measure (a mismatch
    or a not-observable: the criterion was not applied, recorded as null) is its status alone."""
    if not rv:
        return "no verdict"
    st = (rv.get("main_measure") or {}).get("statistic") or {}
    return f"{rv['status']}" + (f" ({st.get('value'):+.2f})" if isinstance(st.get("value"), (int, float)) else "")


def index_says(index, rid):
    for l in (index.read_text().splitlines() if index.exists() else []):
        if l.startswith(rid + ":"):
            return l[len(rid) + 1:].strip()
    return None


def render(rows):
    head = ("| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |\n"
            "|---|---|---|---|---|---|---|---|\n")
    mins = lambda r: sum(u["seconds"] for u in r.get("consumption", {}).values()) / 60
    body = "".join(f"| {r['idea']} | {r.get('parent') or '-'} | {r['step3']} | {r.get('step5') or '-'} | {r.get('step6') or '-'} | "
                   f"{'; '.join(f'{k}: {v}' for k, v in r.get('step7', {}).items()) or '-'} | {r['cost']:.2f} | {mins(r):.1f} |\n" for r in rows)
    steps = {}
    for r in rows:
        for k, u in r.get("consumption", {}).items():
            s = steps.setdefault(k, {"usd": 0.0, "seconds": 0.0}); s["usd"] += u["usd"]; s["seconds"] += u["seconds"]
    use = "".join(f"| {k} | {v['usd']:.2f} | {v['seconds'] / 60:.1f} |\n" for k, v in steps.items())
    total = (f"\n## Consumption\n{len(rows)} ideas, {sum(r['cost'] for r in rows):.2f} USD, "
             f"{sum(mins(r) for r in rows):.1f} minutes in all.\n\n| Step | USD | Minutes |\n|---|---|---|\n" + use)
    return ("# Run table (run_idea)\n\nOne row per idea run; every status is read from the step's own result file. "
            "Each step call: `journal.jsonl`; each helper's output: `logs/`.\n\n" + head + body + total)


def consumption(table_dir, rid):
    """What the idea has cost in the run, every call included (a resumed run adds nothing): from the journal."""
    use = {}
    jp = table_dir / "journal.jsonl"
    for l in (jp.read_text().splitlines() if jp.exists() else []):
        e = json.loads(l)
        if e["backtest"] == rid:
            u = use.setdefault(e["step"], {"usd": 0.0, "seconds": 0.0})
            u["usd"] += e["usd"]; u["seconds"] += e["seconds"]
    return use


def write_row(table_dir, row):
    table_dir.mkdir(parents=True, exist_ok=True)
    if row.get("backtest"):
        row["consumption"] = consumption(table_dir, row["backtest"])
        row["cost"] = round(sum(u["usd"] for u in row["consumption"].values()), 4)
    jp = table_dir / "table.json"
    rows = [r for r in (json.loads(jp.read_text()) if jp.exists() else []) if r["idea"] != row["idea"]] + [row]
    write_atomic(jp, json.dumps(rows, indent=2) + "\n")
    write_atomic(table_dir / "table.md", render(rows))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path)
    a.add_argument("--run", required=True, help="the run's name, ending in _run")
    a.add_argument("--python", required=True, help="the interpreter of a venv with trading-bot/requirements.txt")
    a.add_argument("--brief", type=Path, help="the brief file (default: the one the idea's header names)")
    a.add_argument("--model", help="the model for steps 3, 5 and 7 (default: each helper's own)")
    args = a.parse_args()
    if not args.run.endswith("_run"):
        sys.exit("a run name ends in _run")
    text = args.idea.read_text()
    h = check_idea(text)
    brief = args.brief or find_brief(h["brief"])
    f = folders(args.run)
    for k in ("briefs", "ideas"):
        f[k].mkdir(parents=True, exist_ok=True)
    idea_id = args.idea.stem
    copy_into(brief, f["briefs"] / brief.name)
    idea_file = f["ideas"] / f"{idea_id}.md"
    copy_into(args.idea, idea_file)
    model = ["--model", args.model] if args.model else []
    rid = f"{idea_id}_{h.get('bar') or DEFAULT_BAR}"
    row = {"idea": idea_id, "backtest": rid, "parent": h.get("source-idea"), "cost": 0.0}
    j = Journal(f["table"], args.run, rid)

    # Step 3: the plan (called again for a missing-components refusal the components step has unblocked)
    plan = f["plans"] / f"{rid}.md"
    done = plan.exists() and not wishes.unblocked(plan)
    out, c = j.step("step3_plan", [STEPS / "03_test_plan/helper/make_test_plan.py", idea_file, "--briefs-dir", f["briefs"],
                                   "--plans-dir", f["plans"]] + model, [plan, plan.with_name(plan.stem + "_config.json")], done=done)
    row["cost"] += c
    if not plan.exists():
        sys.exit(f"step 3 wrote no plan for {rid}:\n{out[-800:]}")
    outcome = header_fields(plan.read_text()).get("outcome", "?")
    row["step3"] = outcome
    if outcome != "plan":
        write_row(f["table"], row)
        print(f"{rid}: step 3: {outcome}; the run of this idea stops here")
        return

    # Step 4: the backtest (it skips a record it already holds)
    record = f["backtests"] / rid
    out, _ = j.step("step4_backtest", [STEPS / "04_backtest/helper/run_backtest.py", plan, "--python", args.python,
                                       "--out-root", f["backtests"]], [record / "run.md"], done=(record / "run.md").exists())
    if not (record / "run.md").exists():
        sys.exit(f"step 4 wrote no record for {rid}:\n{out[-800:]}")

    # Step 5: the verdict
    v = f["verdicts"] / rid / "result.json"
    _, c = j.step("step5_verdict", [STEPS / "05_verification/helper/make_verdict.py", plan, "--python", args.python,
                                    "--records-root", f["backtests"], "--verdicts-dir", f["verdicts"]] + model,
                  [v.with_name("verdict.md")], done=v.exists())
    row["cost"] += c
    row["step5"] = verdict_label(result(v))

    # Step 6: the check (code only)
    j.step("step6_check", [STEPS / "06_profitability/helper/check_profitability.py", record, "--checks-dir", f["checks"]],
           [f["checks"] / rid / "check.md"])
    rc = result(f["checks"] / rid / "result.json")
    # The chart files (the run viewer's data), for every backtest (code only): committed names for a backtest worth a
    # chart (confirmed or profitable enough), local names, which git ignores, for any other
    local = not chart_files.worth_a_chart(v, f["checks"] / rid / "result.json")
    j.step("chart_files", [STEPS / "04_backtest/helper/chart_files.py", record] + (["--local"] if local else []),
           [record / chart_files.NAMES[local][0]])
    if rc:
        failed = [m["label"] for m in rc["measures"] if not m["passed"]]
        row["step6"] = rc["status"] + (f" (failed: {', '.join(failed)})" if failed else "")
    else:
        row["step6"] = "not checked"

    # Step 7: every active line, in parallel; each line's own entry condition decides whether it runs
    def run_line(line):
        lid, ldir = line
        out_dir = ldir / args.run
        _, c = j.step(f"step7_{lid}", [STEPS / "07_common/helper/analyse.py", ldir, record, "--plan", plan,
                                       "--briefs-dir", f["briefs"], "--verdicts-dir", f["verdicts"], "--checks-dir", f["checks"],
                                       "--python", args.python, "--out-dir", out_dir, "--idea", idea_file] + model,
                      [out_dir / rid / "analysis.md"], done=index_says(out_dir / "INDEX.md", rid) is not None,
                      said=lambda: index_says(out_dir / "INDEX.md", rid))
        said = index_says(out_dir / "INDEX.md", rid) or "no answer"
        r = result(out_dir / rid / "result.json")
        if said.startswith("not run"):
            return lid, None, c
        return lid, (", ".join(r["idea_ids"]) if r and r.get("idea_ids") else said), c

    with ThreadPoolExecutor() as ex:
        done = list(ex.map(run_line, active_lines()))
    row["step7"] = {lid: what for lid, what, _ in done if what is not None}
    row["cost"] += sum(c for _, _, c in done)
    write_row(f["table"], row)
    print(f"{rid}: step 3 {row['step3']}; step 5 {row['step5']}; step 6 {row['step6']}; "
          f"step 7: {', '.join(row['step7']) or 'no line ran'}; cost in this run {row['cost']:.2f} USD")


if __name__ == "__main__":
    main()
