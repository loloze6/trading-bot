"""unseen_test: one idea's plan, unchanged, on unseen data: every unseen period (common/unseen_dates.md), or with
--coins its unseen coins (common/unseen_coins.md). Step 4 on the period's windows (or on the unseen coins over the
plan's own folds), step 5 with the idea's own measure.py (no model call), step 6; then whether the idea holds there.

  python3 unseen_test.py PLAN --run NAME_run --python VENV_PYTHON [--coins]

PLAN is the idea's plan in 03_test_plan/<run>/plans/; its in-sample verdict (result.json and measure.py) is read from
05_verification/<run>/verdicts/<plan id>/. Per period P (a windows file 04_backtest/windows/P.json), the steps'
files go in their usual folders under the run: 04_backtest/<run>/P/backtests/, 05_verification/<run>/P/verdicts/,
06_profitability/<run>/P/checks/. The idea's result: orchestration/unseen_test/<run>/<plan id>.json and one line in
orchestration/unseen_test/<run>/INDEX.md; each kind of unseen data is one entry of its "periods" (unseen_2016_2017,
unseen_2026, unseen_coins), a call keeping the entries it did not run. With --coins, the steps' files go under
unseen_coins in place of P. A step whose output already exists is not called again (step 4's: a
record where at least one window ran). After step 4, the record's chart files under their committed names (step 4's
chart_files.py), so an unseen record is read on any machine, not only where its bars were made.
Prints one last line: the result as JSON.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import write_atomic  # noqa: E402

WINDOWS = STEPS / "04_backtest" / "windows"
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
COINS = "unseen_coins"   # the name of the unseen coins' entry and folders


def periods():
    """The unseen periods: one windows file each (common/unseen_dates.md)."""
    return sorted(p.stem for p in WINDOWS.glob("unseen_*.json"))


def data_coins():
    """The coins of the data: the Kraken files the data tool recorded in local_data/coverage.yaml (kraken_<COIN>USD_*),
    the venue step 4 runs on. Reads the file names only, no price."""
    import re
    text = (DATA / "coverage.yaml").read_text(encoding="utf-8") if (DATA / "coverage.yaml").exists() else ""
    return sorted(set(re.findall(r"^\s*kraken_([A-Z0-9]+)USD_\w+\.csv:", text, re.M)))


def plan_coins(plan_text):
    """The coins the plan tested: its header's data-instruments, as step 4 reads them ("BTC, ETH" or "BTC/USDT")."""
    import re
    m = re.search(r"^data-instruments:(.*)$", plan_text, re.M)
    out = []
    for part in (m.group(1) if m else "").split(","):
        base = re.sub(r"(USDT|USD)$", "", re.split(r"[/\s-]", part.strip())[0].upper())
        if base and base not in out:
            out.append(base)
    return out


def unseen_coins(plan_text):
    """The plan's unseen coins (common/unseen_coins.md): the data's coins it did not test. Step 4 runs each where it
    has data in the plan's folds; a coin with none runs no window and is not counted."""
    tested = set(plan_coins(plan_text))
    return [c for c in data_coins() if c not in tested]


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


def coverage(record):
    """The coins that ran at least one window in a record, and how many (coin, window) pairs ran."""
    ran = sorted(d.name for d in record.iterdir() if d.is_dir() and any(d.glob("w*/metrics.json"))) \
        if record.is_dir() else []
    return ran, sum(len(list((record / c).glob("w*/metrics.json"))) for c in ran)


def reading(in_sample, verdict, check):
    """One period's reading: step 5 and 6 as they say, and whether the idea holds (common/unseen_dates.md: the main
    measure has its in-sample sign AND the book's Sharpe after costs is above 0). holds is None when the period could
    not be judged at all (no verdict and no check: no data for these dates, e.g. hourly bars not fetched)."""
    ins, _ = main_values(in_sample)
    value, stat = main_values(verdict)
    sharpe, vs_hold = measure(check, "sharpe_min"), measure(check, "sharpe_vs_hold_min")
    holds = (value is not None and ins is not None and sharpe is not None
             and (value > 0) == (ins > 0) and value != 0 and sharpe > 0)
    if verdict is None and check is None:
        holds = None
    return {"step5": (verdict or {}).get("status", "no verdict"), "main": value, "statistic": stat,
            "sharpe": sharpe, "holding_sharpe": None if sharpe is None or vs_hold is None else sharpe - vs_hold,
            "step6": (check or {}).get("status", "not checked"), "holds": holds}


def backtest_ran(record):
    """Step 4's output exists: its run.md, and at least one window run (a coin's w*/metrics.json). A record where no
    window ran (the dates not fetched, for example) is not an output: step 4 is called again on the next call."""
    return (record / "run.md").exists() and any(record.glob("*/w*/metrics.json"))


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
    a.add_argument("--coins", action="store_true", help="the plan's unseen coins over its own folds, in place of the "
                   "unseen periods (common/unseen_coins.md)")
    args = a.parse_args()
    plan, run = args.plan.resolve(), args.run
    rid = plan.stem
    verdict_dir = STEPS / "05_verification" / run / "verdicts" / rid
    in_sample, measure_py = load(verdict_dir / "result.json"), verdict_dir / "measure.py"
    if not in_sample or not measure_py.exists():
        sys.exit(f"no in-sample verdict with its measure.py for {rid} in {run}")
    d = HERE.parent / run
    old = load(d / f"{rid}.json") or {}
    out = {"idea": rid, "run": run, "in_sample": dict(zip(("main", "statistic"), main_values(in_sample))),
           "periods": dict(old.get("periods") or {})}     # the entries this call does not run are kept
    others = unseen_coins(plan.read_text(encoding="utf-8")) if args.coins else None
    for p in ([COINS] if args.coins else periods()):
        if args.coins and not others:                     # the plan tested every coin of the data
            out["periods"][p] = {"coins": [], "step5": "no verdict", "step6": "not checked", "holds": None,
                                 "coins_asked": [],
                                 "why": "no unseen coin: the plan tested every coin of the data"}
            continue
        where = (["--coins", ", ".join(others)] if args.coins else ["--windows", WINDOWS / f"{p}.json"])
        bt = STEPS / "04_backtest" / run / p / "backtests"
        vd = STEPS / "05_verification" / run / p / "verdicts"
        ck = STEPS / "06_profitability" / run / p / "checks"
        if not backtest_ran(bt / rid):
            if (bt / rid).exists():                # a record where no window ran (e.g. the dates were not fetched)
                shutil.rmtree(bt / rid)            # holds no result: step 4 is called again
            call([STEPS / "04_backtest/helper/run_backtest.py", plan, "--python", args.python, "--out-root", bt]
                 + where, p)
        if backtest_ran(bt / rid) and not (bt / rid / "chart_bars.csv.gz").exists():
            call([STEPS / "04_backtest/helper/chart_files.py", bt / rid], p)   # readable on any machine (committed)
        if not (vd / rid / "result.json").exists():
            call([STEPS / "05_verification/helper/make_verdict.py", plan, "--python", args.python, "--records-root", bt,
                  "--verdicts-dir", vd, "--measure", measure_py], p)
        if (bt / rid).exists() and not (ck / rid / "result.json").exists():
            call([STEPS / "06_profitability/helper/check_profitability.py", bt / rid, "--checks-dir", ck], p)
        ran, coin_windows = coverage(bt / rid)
        check = load(ck / rid / "result.json")
        out["periods"][p] = {**({"coins_asked": others} if args.coins else {}), "coins": ran, "coin_windows": coin_windows,
                             "years": ((check or {}).get("informative") or {}).get("years"),
                             **reading(in_sample, load(vd / rid / "result.json"), check)}
    d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / f"{rid}.json", json.dumps(out, indent=2) + "\n")
    said = {True: "holds", False: "does not hold", None: "no data"}
    def say(p, r):
        if p != COINS:
            return f"{p}: {said[r['holds']]}"
        if not r.get("coins_asked"):
            return f"{p}: none (the plan tested every coin of the data)"
        return f"{p}: {said[r['holds']]} ({len(r.get('coins') or [])} of {len(r['coins_asked'])} coins ran)"
    line = "; ".join(say(p, r) for p, r in sorted(out["periods"].items(), key=lambda kv: (kv[0] == COINS, kv[0])))
    index = d / "INDEX.md"
    lines = [l for l in (index.read_text(encoding="utf-8").splitlines() if index.exists() else [])
             if not l.startswith(rid + ":")]
    write_atomic(index, "".join(l + "\n" for l in sorted(lines + [f"{rid}: {line}"])))
    print(json.dumps({"unseen": line}))


if __name__ == "__main__":
    main()
