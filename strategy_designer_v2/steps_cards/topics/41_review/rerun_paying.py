"""Topic 41, plan step 3: every paying book (step 5 confirmed, step 6 profitable enough, any run; an idea's latest record
counts once) rerun on today's engine and costs: steps 4, 5 (its own measure.py, no model call) and 6, into the run
`paying_rerun_run`; then the before and after table (rerun_before_after.md, next to this script). Resumes: a step whose
output exists is not called again.

  python3 topics/41_review/rerun_paying.py --python VENV_PYTHON [--table-only]
"""
import argparse, json, subprocess, sys
from pathlib import Path

ST = Path(__file__).resolve().parents[2]
RUN = "paying_rerun_run"
LABELS = ["Sharpe", "Sharpe minus holding's Sharpe", "Mean daily return", "Lowest Sharpe, one window left out", "Calmar", "Trades per day"]


def paying_records():
    out = {}
    for v in sorted((ST / "05_verification").glob("*_run/verdicts/*/result.json")):
        run, rid = v.parts[-4], v.parent.name
        if run == RUN or json.loads(v.read_text()).get("status") != "confirmed":
            continue
        c = ST / "06_profitability" / run / "checks" / rid / "result.json"
        if not (c.exists() and json.loads(c.read_text()).get("status", "").startswith("profitable")):
            continue
        m = next((ST / "04_backtest" / run / "backtests" / rid).glob("*/w*/manifest.json"), None)
        made = json.loads(m.read_text()).get("created_utc", "") if m else ""
        if rid not in out or made > out[rid]["made"]:
            out[rid] = {"run": run, "id": rid, "made": made}
    return sorted(out.values(), key=lambda r: r["id"])


def rerun(r, py):
    plan = ST / "03_test_plan" / r["run"] / "plans" / f"{r['id']}.md"
    bt, vd, ck = (ST / "04_backtest" / RUN / "backtests", ST / "05_verification" / RUN / "verdicts", ST / "06_profitability" / RUN / "checks")
    for d in (bt, vd, ck):
        d.mkdir(parents=True, exist_ok=True)
    log = []
    if not (bt / r["id"] / "run.md").exists():
        p = subprocess.run([sys.executable, ST / "04_backtest/helper/run_backtest.py", plan, "--python", py, "--out-root", bt], capture_output=True, text=True)
        log.append(f"step 4 exit {p.returncode}: {(p.stdout + p.stderr).strip().splitlines()[-1:]}")
    measure = ST / "05_verification" / r["run"] / "verdicts" / r["id"] / "measure.py"
    if not (vd / r["id"] / "result.json").exists():
        p = subprocess.run([sys.executable, ST / "05_verification/helper/make_verdict.py", plan, "--python", py, "--records-root", bt,
                            "--verdicts-dir", vd, "--measure", measure], capture_output=True, text=True)
        log.append(f"step 5 exit {p.returncode}: {(p.stdout + p.stderr).strip().splitlines()[-1:]}")
    if not (ck / r["id"] / "result.json").exists() and (bt / r["id"] / "run.md").exists():
        p = subprocess.run([sys.executable, ST / "06_profitability/helper/check_profitability.py", bt / r["id"], "--checks-dir", ck], capture_output=True, text=True)
        log.append(f"step 6 exit {p.returncode}: {(p.stdout + p.stderr).strip().splitlines()[-1:]}")
    return log


def status(run, rid):
    v = ST / "05_verification" / run / "verdicts" / rid / "result.json"
    c = ST / "06_profitability" / run / "checks" / rid / "result.json"
    rv = json.loads(v.read_text()) if v.exists() else {}
    rc = json.loads(c.read_text()) if c.exists() else {}
    stat = rv.get("main_measure", {}).get("statistic", {}).get("value")
    return {"step5": rv.get("status", "no verdict"), "t": stat, "step6": rc.get("status", "not checked"),
            "measures": {m["label"]: m["value"] for m in rc.get("measures", [])}}


def table(rows):
    lines = ["# Paying books rerun on today's engine: before and after (topic 41, plan step 3)", "",
             f"Every paying book (step 5 confirmed, step 6 profitable enough; an idea's latest record counts once), rerun in `{RUN}`:",
             "steps 4, 5 (its own measure.py, no model call) and 6 on today's engine and costs. Before: as recorded. After: rerun.", "",
             "| Book | Run | Made | Step 5 before → after (t) | Step 6 before → after | Sharpe | Minus holding's | Calmar | Mean daily return |",
             "|---|---|---|---|---|---|---|---|---|"]
    f = lambda x, p=2: "-" if x is None else f"{x:.{p}f}"
    for r in rows:
        b, a = status(r["run"], r["id"]), status(RUN, r["id"])
        mb, ma = b["measures"], a["measures"]
        pair = lambda k, p=2: f"{f(mb.get(k), p)} → {f(ma.get(k), p)}"
        lines.append(f"| {r['id']} | {r['run']} | {r['made'][:10]} | {b['step5']} ({f(b['t'])}) → {a['step5']} ({f(a['t'])}) | "
                     f"{b['step6'].split(' (')[0]} → {a['step6'].split(' (')[0]} | {pair('Sharpe')} | {pair(LABELS[1])} | {pair('Calmar')} | "
                     f"{pair('Mean daily return', 5)} |")
    still = sum(status(RUN, r["id"])["step5"] == "confirmed" and status(RUN, r["id"])["step6"].startswith("profitable") for r in rows)
    lines += ["", f"Still paying after the rerun: {still} of {len(rows)}."]
    (Path(__file__).parent / "rerun_before_after.md").write_text("\n".join(lines) + "\n")
    print(f"table: {still} of {len(rows)} still paying")


def main():
    a = argparse.ArgumentParser(); a.add_argument("--python", required=True); a.add_argument("--table-only", action="store_true")
    args = a.parse_args()
    rows = paying_records()
    print(f"{len(rows)} paying books (distinct ideas)", flush=True)
    if not args.table_only:
        for i, r in enumerate(rows, 1):
            for line in rerun(r, args.python):
                print(f"{i}/{len(rows)} {r['id'][-60:]}: {line}", flush=True)
            print(f"DONE {i}/{len(rows)} {r['id'][-60:]}", flush=True)
    table(rows)


if __name__ == "__main__":
    main()
