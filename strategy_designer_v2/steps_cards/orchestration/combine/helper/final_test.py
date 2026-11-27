"""combine, step 12 of common/data_use.md (card: ../card.md, "The final test"): a ready version's strategies,
unchanged, on the final coins, once; go or no-go for live.

  python3 orchestration/combine/helper/final_test.py VERSION --python VENV_PYTHON

Refuses unless the version is ready (its measures.json, step 11) and no final test was made for the current final
group (`common/coins.py`, FINAL). Then, in this order:
1. The record, written before any run: `../final_tests/<group>.json` (the group, the version, the version's commit,
   this commit, the measures expected and the bar, the start time, status "started"). Its existence marks the group
   used: a second call is refused, whatever happened to the first (a run that fails does not give the group back).
2. Each of the version's strategies, its plan unchanged (`03_test_plan/<run>/plans/<plan id>.md`), on each final coin,
   over the windows of `04_backtest/windows/research_2016.json` whose start is past the coin's first 90 days (the same
   windows and rule as step 9's common record; the designer, 2026-11-26): one call to step 9's runner,
   `common_record.backtest(..., coin_list=coins.FINAL)` (joined 2026-11-27: one runner for steps 9 and 12), then step
   4's chart files. The record: `04_backtest/<run>/<group>/backtests/<plan id>/` (per coin, as step 9's).
3. The portfolio at the version's weights, coin by coin (combine.py's rule 6), against holding the same coins (equal
   weight, the same days); go when its Sharpe after costs is above 0 and above holding's. Written in the record
   (status "done"), in the version's measures.json (`final_test`) and in its INDEX line.
Why this cannot leak: the version, its strategies and its weights are fixed before the run and written in the record;
nothing read here changes them; each bar's decision is the engine's, on data up to that bar's close.
"""
import argparse, json, subprocess, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import combine as cb  # noqa: E402
import update as up  # noqa: E402
sys.path.insert(0, str(cb.STEPS / "common"))
import coins  # noqa: E402
sys.path.insert(0, str(cb.STEPS / "orchestration" / "common_record" / "helper"))
import common_record as cr  # noqa: E402  (step 9's runner, used unchanged for step 12)

MARKS = cb.FUNC / "final_tests"


def group():
    """The current final group's name: its coins, in coins.py's order."""
    return "final_" + "-".join(coins.FINAL)


def mark():
    return MARKS / f"{group()}.json"


def refusal(version):
    """Why the final test cannot be made for this version now, or None."""
    m = cb.FUNC / "portfolios" / version / "measures.json"
    if not m.exists():
        return f"{version} has no measures.json: not a version built by update.py"
    if json.loads(m.read_text()).get("ready") is not True:
        return f"{version} is not ready for the final test (step 11)"
    if mark().exists():
        return f"a final test was already made for the final group {group()} ({mark().name}): one test per group"
    return None


def run_book(r, python, data=coins.DATA):
    """One strategy, its plan unchanged, on every final coin over step 9's windows (common_record.backtest, the same
    runner and the same 90-day rule as the common record), then its chart file. Returns the coins that gave bars."""
    plan = cb.STEPS / "03_test_plan" / r["run"] / "plans" / f"{r['id']}.md"
    dest = up.record_dir(r, group())
    windows = json.loads(Path(coins.WINDOWS).read_text())
    cr.backtest(plan, python, dest, windows, coins.FINAL, usable=lambda c, start: coins.usable(c, start, data=data))
    subprocess.run([sys.executable, cb.STEPS / "04_backtest/helper/chart_files.py", dest])
    chart = dest / "chart_bars.csv.gz"
    return sorted(pd.read_csv(chart).coin.unique()) if chart.exists() else []


def go(m):
    v, h = m["this version"], m[up.HOLDING]
    return bool(v and h and v["sharpe"] > 0 and v["sharpe"] > h["sharpe"])


def final_test(version, python, run_book=run_book):
    why = refusal(version)
    if why:
        sys.exit(f"final test refused: {why}")
    folder = cb.FUNC / "portfolios" / version
    port = json.loads((folder / "portfolio.json").read_text())
    measures = json.loads((folder / "measures.json").read_text())
    weights = {b["key"]: b["weight"] for b in port["books"]}
    rows = {r["key"]: r for r in json.loads((cb.REG / "books.json").read_text())}
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=cb.STEPS).stdout.strip()
    rec = {"group": group(), "coins": list(coins.FINAL), "version": version, "version_commit": port.get("commit"),
           "commit": sha, "started_utc": cb.utc_now(), "status": "started",
           "books": weights,
           "measures_expected": {"what": f"the version's daily Sharpe after costs on the final coins, against {up.HOLDING}",
                                 "days": "the windows of research_2016.json past each coin's first 90 days (as step 9)",
                                 "go_if": "Sharpe above 0 and above holding's (common/data_use.md, section 4)",
                                 "step 11 on the portfolio coins": measures.get("portfolio_coins")}}
    MARKS.mkdir(parents=True, exist_ok=True)
    cb.write_atomic(mark(), json.dumps(rec, indent=1))           # before any run: the group is used from here
    ran = {k: run_book(rows[k], python) for k in weights}
    m = up.measure(weights, rows, group()) if any(ran.values()) else {"this version": None, up.HOLDING: None}
    m.pop("ready", None)
    rec.update({"status": "done", "finished_utc": cb.utc_now(), "coins_with_bars": ran, "result": m,
                "go": go(m)})
    cb.write_atomic(mark(), json.dumps(rec, indent=1))
    measures["final_test"] = {"record": str(mark().relative_to(cb.STEPS)), "go": rec["go"], **m}
    cb.write_atomic(folder / "measures.json", json.dumps(measures, indent=1))
    idx = up.PORTFOLIOS / "INDEX.md"
    v = m["this version"]
    said = (f"{'go' if rec['go'] else 'no-go'}: Sharpe {v['sharpe']} (holding {m[up.HOLDING]['sharpe']})" if v
            else "no-go: no bars on the final coins")
    lines = [l.rsplit("|", 2)[0] + f"| {group()}: {said} |" if l.startswith(f"| {version} |") else l
             for l in idx.read_text().splitlines()]
    cb.write_atomic(idx, "\n".join(lines) + "\n")
    return rec


def main():
    a = argparse.ArgumentParser()
    a.add_argument("version")
    a.add_argument("--python", required=True, help="a venv with trading-bot/requirements.txt (step 4)")
    args = a.parse_args()
    rec = final_test(args.version, args.python)
    print(f"final test of {args.version} on {rec['group']}: {'go' if rec['go'] else 'no-go'}")


if __name__ == "__main__":
    main()
