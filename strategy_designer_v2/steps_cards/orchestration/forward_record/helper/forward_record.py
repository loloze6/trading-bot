"""forward_record (card: ../card.md): the forward record of one portfolio version. The version's strategies, frozen,
run on the days after the version was built; the portfolio's daily return at the version's weights and holding's on the
same coins, appended to one file.

  python3 orchestration/forward_record/helper/forward_record.py VERSION --python VENV_PYTHON [--update-data]

The files, in orchestration/forward_record/<version>/:
  frozen.json   written once: the start day (the date of the version's made_utc), each strategy's weight, plan and the
                SHA-256 of its plan and config
  days.csv      one line per forward day (day, portfolio, holding, coins, strategies, added_utc, commit); appended only;
                the window's last day waits for the next update
  record.md     rewritten at each update: since the start, the days, both returns, Sharpe (from 60 days), worst fall
The engine's files of the last update: 04_backtest/<run>/forward_<version>/backtests/<plan id>/ (step 9's runner).

What it depends on, by name: common_record.backtest (the runner) and common_record.commit; step 4's chart_files.py
and its chart_bars.csv.gz (coin, window, timestamp, close, position, value); common/coins.py portfolio_group() and
usable(); trading-bot/backtest/holdout_policy.py (check_windows_before, holdout_start_of, load_policy), called in the
venv; trading-bot/tools/extend_kraken_daily.py --coins. It reads the portfolio's and holding's returns with its own
functions (day_returns, portfolio_and_holding), not combine's.

Why this cannot leak: the version is frozen before its first forward day (frozen.json's fingerprints are checked at
every update); each bar's decision is the engine's, on data up to that bar's close; only days strictly after the start
day are kept (keep_forward) and append() refuses any other. The coins come from portfolio_group(), which leaves the
last test's coins out; this file never names them.
"""
import argparse, csv, datetime as dt, hashlib, json, math, os, subprocess, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
FUNC = HERE.parent
STEPS = FUNC.parents[1]
REPO = STEPS.parents[1]
sys.path.insert(0, str(STEPS / "common"))
sys.path.insert(0, str(STEPS / "orchestration" / "common_record" / "helper"))
from lib import write_atomic, utc_now  # noqa: E402
import coins  # noqa: E402  (the portfolio coins and the 90-day rule)
import common_record as cr  # noqa: E402  (step 9's runner, used unchanged)

PORTFOLIOS = STEPS / "orchestration" / "combine" / "portfolios"
COLUMNS = ["day", "portfolio", "holding", "coins", "strategies", "added_utc", "commit"]
SHARPE_DAYS = 60            # the card: Sharpe once at least 60 days exist
SAME = 1e-9                 # two computations of one day's return are equal within this


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def config_of(plan):
    plan = Path(plan)
    return plan.with_name(plan.stem + "_config.json")


def freeze(version, portfolios=PORTFOLIOS, steps=STEPS):
    """What the record runs at every update, read once from the version: its start day, and each strategy's weight,
    plan (the one its common record ran) and the fingerprints of its plan and config."""
    port = json.loads((Path(portfolios) / version / "portfolio.json").read_text(encoding="utf-8"))
    books = []
    for b in port["books"]:
        run, rid = b["key"].split("__", 1)
        common = json.loads((steps / "orchestration" / "common_record" / run / f"{rid}.json").read_text(encoding="utf-8"))
        plan = steps / common["plan"]
        books.append({"key": b["key"], "weight": b["weight"], "run": run, "id": rid, "plan": common["plan"],
                      "plan_sha256": sha(plan), "config_sha256": sha(config_of(plan))})
    return {"version": version, "made_utc": port["made_utc"], "version_commit": port.get("commit"),
            "start_day": port["made_utc"][:10], "frozen_utc": utc_now(), "books": books}


def changed(frozen, steps=STEPS):
    """The strategies whose plan or config is no longer the frozen one."""
    out = []
    for b in frozen["books"]:
        plan = steps / b["plan"]
        if not plan.exists() or sha(plan) != b["plan_sha256"] or sha(config_of(plan)) != b["config_sha256"]:
            out.append(b["key"])
    return out


def last_complete_day(coin_list, data=coins.DATA):
    """The latest day in the coins' daily files (the data tool writes finished days only)."""
    return max(coins.dates(c, data)[-1] for c in coin_list).isoformat()


def extend_data(python, coin_list):
    """Step 1 of an update: the data tool, unchanged, on the portfolio coins by name. Returns its lines."""
    r = subprocess.run([python, str(REPO / "trading-bot" / "tools" / "extend_kraken_daily.py"), "--coins", *coin_list],
                       capture_output=True, text=True, cwd=REPO / "trading-bot")
    return (r.stdout + r.stderr).strip()


def guard(python, window):
    """The existing holdout guard on the forward window: None when accepted, else its message (which holds no date)."""
    code = ("import json, sys; import holdout_policy as hp\n"
            "try:\n"
            "    hp.check_windows_before(json.loads(sys.argv[1]), hp.holdout_start_of(hp.load_policy()))\n"
            "except hp.HoldoutPolicyError as e:\n"
            "    print(e); sys.exit(3)\n")
    r = subprocess.run([python, "-c", code, json.dumps([window])], cwd=REPO / "trading-bot" / "backtest",
                       capture_output=True, text=True)
    if r.returncode == 0:
        return None
    return r.stdout.strip() if r.returncode == 3 else f"the guard could not be asked: {r.stderr.strip()[-300:]}"


def engine_dir(book, version, engine_root=None, steps=STEPS):
    if engine_root is not None:
        return Path(engine_root) / book["run"] / book["id"]
    return steps / "04_backtest" / book["run"] / f"forward_{version}" / "backtests" / book["id"]


def run_book(book, version, python, window, coin_list, engine_root=None, steps=STEPS):
    """One strategy, its plan unchanged, on the forward window: step 9's runner, then step 4's chart file. Returns
    (the chart file or None, the runner's line)."""
    dest = engine_dir(book, version, engine_root, steps)
    line = cr.backtest(steps / book["plan"], python, dest, [window], coin_list)
    subprocess.run([sys.executable, str(steps / "04_backtest" / "helper" / "chart_files.py"), str(dest)],
                   capture_output=True, text=True)
    chart = dest / "chart_bars.csv.gz"
    return (chart if chart.exists() else None), line


def day_returns(chart):
    """One strategy's record, per day and coin: `ret`, the change of its value between two days' last bars, and
    `hold`, the change of the coin's close between the same bars. A coin's first day in the record has neither."""
    b = pd.read_csv(chart, usecols=["coin", "window", "timestamp", "close", "value"])
    b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    b = b.sort_values(["coin", "timestamp"]).groupby(["coin", "day"], as_index=False).last()
    b["ret"] = b.groupby("coin").value.pct_change()
    b["hold"] = b.groupby("coin").close.pct_change()
    return b.set_index(["day", "coin"])[["ret", "hold"]]


def portfolio_and_holding(weights, charts):
    """The card's two returns, one row per day: coin by coin the weighted sum of the strategies' returns, then the mean
    over the coins; holding: on the same coin-days, the coin's close-to-close return, then the mean over the coins.
    Also how many coins and strategies had a return that day."""
    ret, hold = [], None
    for key, chart in charts.items():
        d = day_returns(chart)
        ret.append(d.ret.rename(key) * weights[key])
        hold = d.hold if hold is None else hold.combine_first(d.hold)
    if not ret:
        return pd.DataFrame(columns=["portfolio", "holding", "coins", "strategies"])
    R = pd.concat(ret, axis=1)
    per_coin = R.sum(axis=1, min_count=1).dropna()
    held = hold.reindex(per_coin.index)
    out = pd.DataFrame({"portfolio": per_coin.groupby(level="day").mean(),
                        "holding": held.groupby(level="day").mean(),
                        "coins": per_coin.groupby(level="day").size(),
                        "strategies": R.reindex(per_coin.index).notna().groupby(level="day").any().sum(axis=1)})
    return out.dropna(subset=["portfolio", "holding"])


def keep_forward(days, start_day):
    """Only the days strictly after the start day."""
    return days[days.index > pd.Timestamp(start_day)]


def read_days(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append(path, rows, start_day):
    """Adds lines at the end of days.csv; the lines already there are not touched. Refuses a day that is not after
    the start day and after the file's last day."""
    path = Path(path)
    have = read_days(path)
    last = have[-1]["day"] if have else start_day
    for r in rows:
        if not (r["day"] > start_day and r["day"] > last):
            raise ValueError(f"{r['day']} is not after the start day {start_day} and the file's last day {last}")
        last = r["day"]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerow(COLUMNS)
    if rows:
        with path.open("a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, COLUMNS, lineterminator="\n").writerows(rows)


def stats(returns):
    """Since the start: the compounded return, Sharpe (daily, 365 days a year) from 60 days, the worst fall."""
    r = pd.Series([float(x) for x in returns], dtype=float)
    if r.empty:
        return {"days": 0, "return": None, "sharpe": None, "worst_fall": None}
    c = (1 + r).cumprod()
    fall = float((1 - c / c.cummax().clip(lower=1.0)).max())          # the start (1.0) counts as a peak
    sd = r.std()
    sharpe = round(r.mean() / sd * math.sqrt(365), 3) if len(r) >= SHARPE_DAYS and sd > 0 else None
    return {"days": len(r), "return": float(c.iloc[-1] - 1), "sharpe": sharpe, "worst_fall": max(fall, 0.0)}


def record_text(frozen, rows, last=None):
    pct = lambda x: "-" if x is None else f"{100 * x:+.2f} %"
    p, h = stats([r["portfolio"] for r in rows]), stats([r["holding"] for r in rows])
    sharpe = lambda s: f"{s['sharpe']:+.2f}" if s["sharpe"] is not None else ("too few days" if s["days"] < SHARPE_DAYS else "-")
    start = frozen["start_day"]
    first = (dt.date.fromisoformat(start) + dt.timedelta(days=1)).isoformat()
    t = [f"# Forward record of {frozen['version']} (orchestration/forward_record/card.md)", "",
         f"- Start day: {start} (the version was built {frozen['made_utc']}, commit {str(frozen['version_commit'])[:10]});"
         f" the first forward day is {first}.",
         *(["- **A pretended start day, to prove the mechanism on past days: not a forward record.**"]
           if frozen.get("pretended_start_day") else []),
         f"- Strategies: {len(frozen['books'])}, frozen, at the version's weights (`frozen.json`).",
         f"- Days in `days.csv`: {len(rows)}" + (f", {rows[0]['day']} to {rows[-1]['day']}." if rows else
                                                 ": no forward day is complete yet."), "",
         "| Since the start | Days | Return | Sharpe | Worst fall |", "|---|---|---|---|---|",
         f"| The portfolio | {p['days']} | {pct(p['return'])} | {sharpe(p)} | {pct(p['worst_fall'] and -p['worst_fall'])} |",
         f"| Holding the same coins | {h['days']} | {pct(h['return'])} | {sharpe(h)} | {pct(h['worst_fall'] and -h['worst_fall'])} |",
         ""]
    if last:
        t += [f"## The last update ({last['utc']}, commit {last['commit'][:10]})", "",
              f"- Forward window: {first} to {last['until']}; {last['added']} day(s) added. The window's last day waits"
              f" for the next update (the engine closes every position on a window's last bar).",
              f"- Earlier days computed again: {last['same']} equal to the file, {last['different']} different"
              + (f" (first: {last['first_different']}; the file is not changed)" if last["different"] else "")
              + (f"; {last['absent']} computed day(s) before the file's last day are not in the file" if last["absent"] else "")
              + ".",
              f"- Strategies with a chart file: {last['ran']} of {len(frozen['books'])}.", ""]
        t += [f"- {line}" for line in last["lines"]] + [""]
    t += ["Not a ledger of trials: the own record of one frozen portfolio, one line per day, whatever the day shows.", ""]
    return "\n".join(t)


def update(version, python, update_data=False, folder=None, engine_root=None, start_day=None, until=None,
           portfolios=PORTFOLIOS, steps=STEPS, run_book=run_book, guard=guard, coin_list=None):
    """One update of the version's forward record. `folder`, `engine_root`, `start_day` and `until` are for a scratch
    record outside the repository (a pretended start day, to prove the mechanism on past days) and for the tests; the
    command line has none of them."""
    folder = Path(folder) if folder is not None else FUNC / version
    coin_list = coin_list or coins.portfolio_group()
    made_by = cr.commit()
    frozen_file = folder / "frozen.json"
    if frozen_file.exists():
        frozen = json.loads(frozen_file.read_text(encoding="utf-8"))
    else:
        frozen = freeze(version, portfolios, steps)
        if start_day:
            frozen.update({"start_day": start_day, "pretended_start_day": True})
        folder.mkdir(parents=True, exist_ok=True)
        write_atomic(frozen_file, json.dumps(frozen, indent=1) + "\n")
    start = frozen["start_day"]
    days_file = folder / "days.csv"
    append(days_file, [], start)                                        # the file exists from the first call
    said = [extend_data(python, coin_list)] if update_data else []
    until = until or last_complete_day(coin_list)
    last = None
    if until <= start:
        said.append(f"no forward day yet: the last complete day ({until}) is not after the start day ({start}); "
                    f"an update adds one line per complete day after {start}, the last one waiting for the next update")
    else:
        moved = changed(frozen, steps)
        if moved:
            sys.exit("forward record stopped, nothing written: no longer the frozen plan or config: " + "; ".join(moved))
        window = {"label": f"forward_{version}", "test": {"start": start, "end": until}}
        refused = guard(python, window)
        if refused:
            sys.exit(f"forward record stopped, nothing run, no day written: the holdout guard refuses the forward days "
                     f"({start} to {until}). The guard's message: {refused}")
        weights = {b["key"]: b["weight"] for b in frozen["books"]}
        charts, lines = {}, []
        for b in frozen["books"]:
            chart, line = run_book(b, version, python, window, coin_list, engine_root, steps)
            lines.append(line)
            if chart is not None:
                charts[b["key"]] = chart
        days = keep_forward(portfolio_and_holding(weights, charts), start)
        days = days[days.index < pd.Timestamp(until)]      # the window's last day waits: the engine closes every
        #                                                    position on a window's last bar, a cost the portfolio
        #                                                    would not pay; the day enters at the next update
        have = {r["day"]: r for r in read_days(days_file)}
        last_have = max(have) if have else start
        now, new, same, different, absent = utc_now(), [], 0, [], 0
        for day, r in days.iterrows():
            d = day.strftime("%Y-%m-%d")
            if d in have:
                eq = (abs(float(have[d]["portfolio"]) - r.portfolio) <= SAME
                      and abs(float(have[d]["holding"]) - r.holding) <= SAME)
                same += eq
                different += [] if eq else [d]
            elif d > last_have:
                new.append({"day": d, "portfolio": f"{r.portfolio:.10f}", "holding": f"{r.holding:.10f}",
                            "coins": int(r.coins), "strategies": int(r.strategies), "added_utc": now, "commit": made_by})
            else:
                absent += 1
        append(days_file, new, start)
        last = {"utc": now, "commit": made_by, "until": until, "added": len(new), "same": int(same),
                "different": len(different), "first_different": different[0] if different else None, "absent": absent,
                "ran": len(charts), "lines": lines}
        said.append(f"{len(new)} day(s) added" + (f" ({new[0]['day']} to {new[-1]['day']})" if new else "")
                    + f"; {int(same)} earlier day(s) computed again and equal, {len(different)} different")
    rows = read_days(days_file)
    write_atomic(folder / "record.md", record_text(frozen, rows, last))
    return {"version": version, "start_day": start, "until": until, "days": len(rows), "said": said, "last": last}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("version")
    a.add_argument("--python", required=True, help="a venv with trading-bot/requirements.txt")
    a.add_argument("--update-data", action="store_true", help="first extend the portfolio coins' daily files (network)")
    args = a.parse_args()
    r = update(args.version, args.python, args.update_data)
    for s in r["said"]:
        print(s)
    print(f"forward record of {r['version']}: start day {r['start_day']}, {r['days']} day(s) in days.csv, "
          f"last complete day {r['until']}")


if __name__ == "__main__":
    main()
