"""unseen_test: one idea's plan, unchanged, on every unseen period (common/unseen_dates.md): step 4 on the period's
windows, step 5 with the idea's own measure.py (no model call), step 6; then whether the idea holds there.

  python3 unseen_test.py PLAN --run NAME_run --python VENV_PYTHON

PLAN is the idea's plan in 03_test_plan/<run>/plans/; its in-sample verdict (result.json and measure.py) is read from
05_verification/<run>/verdicts/<plan id>/. Per period P (a windows file 04_backtest/windows/P.json), the steps'
files go in their usual folders under the run: 04_backtest/<run>/P/backtests/, 05_verification/<run>/P/verdicts/,
06_profitability/<run>/P/checks/. The idea's result: orchestration/unseen_test/<run>/<plan id>.json and one line in
orchestration/unseen_test/<run>/INDEX.md. A step whose output already exists is not called again.
Prints one last line: the result as JSON.
"""
import argparse, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import write_atomic  # noqa: E402

WINDOWS = STEPS / "04_backtest" / "windows"


def periods():
    """The unseen periods: one windows file each (common/unseen_dates.md)."""
    return sorted(p.stem for p in WINDOWS.glob("unseen_*.json"))


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def measure(check, key):
    return next((m["value"] for m in (check or {}).get("measures", []) if m["measure"] == key), None)


def main_values(result):
    """(main measure value, its statistic) of a step 5 result, or (None, None)."""
    mm = (result or {}).get("main_measure") or {}
    st = mm.get("statistic")
    return mm.get("value"), (st.get("value") if isinstance(st, dict) else None)


def reading(in_sample, verdict, check):
    """One period's reading: step 5 and 6 as they say, and whether the idea holds (common/unseen_dates.md: the main
    measure has its in-sample sign AND the book's Sharpe after costs is above 0)."""
    ins, _ = main_values(in_sample)
    value, stat = main_values(verdict)
    sharpe, vs_hold = measure(check, "sharpe_min"), measure(check, "sharpe_vs_hold_min")
    holds = (value is not None and ins is not None and sharpe is not None
             and (value > 0) == (ins > 0) and value != 0 and sharpe > 0)
    return {"step5": (verdict or {}).get("status", "no verdict"), "main": value, "statistic": stat,
            "sharpe": sharpe, "holding_sharpe": None if sharpe is None or vs_hold is None else sharpe - vs_hold,
            "step6": (check or {}).get("status", "not checked"), "holds": holds}


def call(cmd, period):
    """One step's helper. Its whole output is printed, headed by the period and the step, so the caller's log keeps
    it (run_idea: logs/<backtest>/unseen_test.txt); a step that fails leaves its message there and no result file."""
    r = subprocess.run([sys.executable] + [str(c) for c in cmd], capture_output=True, text=True)
    print(f"--- {period}: {Path(str(cmd[0])).name} (exit {r.returncode})\n{(r.stdout + r.stderr).strip()}", flush=True)
    return r.returncode


def main():
    a = argparse.ArgumentParser()
    a.add_argument("plan", type=Path)
    a.add_argument("--run", required=True)
    a.add_argument("--python", required=True)
    args = a.parse_args()
    plan, run = args.plan.resolve(), args.run
    rid = plan.stem
    verdict_dir = STEPS / "05_verification" / run / "verdicts" / rid
    in_sample, measure_py = load(verdict_dir / "result.json"), verdict_dir / "measure.py"
    if not in_sample or not measure_py.exists():
        sys.exit(f"no in-sample verdict with its measure.py for {rid} in {run}")
    out = {"idea": rid, "run": run, "in_sample": dict(zip(("main", "statistic"), main_values(in_sample))), "periods": {}}
    for p in periods():
        bt = STEPS / "04_backtest" / run / p / "backtests"
        vd = STEPS / "05_verification" / run / p / "verdicts"
        ck = STEPS / "06_profitability" / run / p / "checks"
        if not (bt / rid / "run.md").exists():
            call([STEPS / "04_backtest/helper/run_backtest.py", plan, "--python", args.python, "--out-root", bt,
                  "--windows", WINDOWS / f"{p}.json"], p)
        if not (vd / rid / "result.json").exists():
            call([STEPS / "05_verification/helper/make_verdict.py", plan, "--python", args.python, "--records-root", bt,
                  "--verdicts-dir", vd, "--measure", measure_py], p)
        if (bt / rid).exists() and not (ck / rid / "result.json").exists():
            call([STEPS / "06_profitability/helper/check_profitability.py", bt / rid, "--checks-dir", ck], p)
        out["periods"][p] = reading(in_sample, load(vd / rid / "result.json"), load(ck / rid / "result.json"))
    d = HERE.parent / run
    d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / f"{rid}.json", json.dumps(out, indent=2) + "\n")
    line = "; ".join(f"{p}: {'holds' if r['holds'] else 'does not hold'}" for p, r in out["periods"].items())
    index = d / "INDEX.md"
    lines = [l for l in (index.read_text(encoding="utf-8").splitlines() if index.exists() else [])
             if not l.startswith(rid + ":")]
    write_atomic(index, "".join(l + "\n" for l in sorted(lines + [f"{rid}: {line}"])))
    print(json.dumps({"unseen": line}))


if __name__ == "__main__":
    main()
