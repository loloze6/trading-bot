"""Topic 51, the impact run (runs/TOPIC51_IMPACT_RUN.md): our books on the engine before topic 51 (commit e72a6b97f9:
a move to flat can be refused by the rebalance band) and after it (the working branch: never refused), the same plans and
data. Reads the records step 4 wrote in a scratch folder, runs step 6 on each (to the same folder), step 5's committed
measure.py on 5 books, and writes one row per book and period, then P4's portfolio (equal capital), to impact.csv.

  python3 topics/51_review/impact.py FOLDER --python VENV_PYTHON
FOLDER holds books.csv (run, id, bar, plan, groups, unseen) and <engine>/<period>/<id>/ (engine: before, after; period:
insample, unseen_2016_2017, unseen_2026). Step 6 writes to <engine>/<period>_checks/, step 5 to <engine>/verdicts/.

Measures, per book, period and engine: step 6's answer and its measure values (Sharpe, Calmar, mean daily return on
days in a position); days in a position: the (coin, window, UTC day) triples in which the coin held a position after
one of the day's bars (postRebalance_current_allocation not 0); for a specialist (a night 7 book whose idea names a
market profile, topics/49_review/night7_ideas_full.csv), the share of those days inside its profile (the profile of
common/market_profile.md, `profile_of` of topics/49_review/night7_measures.py, read from that file: one definition).
The "before" reruns are checked against the committed records: each window's net return in run.md, the same.

Why this can't leak: it reads finished records after the fact; a day's profile uses closes up to that day only.
"""
import argparse, ast, json, re, subprocess, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = Path(__file__).resolve().parent; STEPS = HERE.parents[1]
sys.path.insert(0, str(STEPS / "orchestration" / "ideas_similarities_check" / "helper"))
sys.path.insert(0, str(HERE.parent / "44_review"))
from book_returns import book_returns  # noqa: E402
from p2_weights import calmar, sharpe  # noqa: E402

# profile_of and its imports, taken from night7_measures.py without running that script
_src = (HERE.parent / "49_review" / "night7_measures.py").read_text()
_fn = next(n for n in ast.parse(_src).body if isinstance(n, ast.FunctionDef) and n.name == "profile_of")
_ns = {"functools": __import__("functools"), "np": np, "pd": pd, "DATA": STEPS.parents[1] / "trading-bot" / "local_data"}
exec(compile(ast.Module([_fn], []), "night7_measures.py", "exec"), _ns)
profile_of = _ns["profile_of"]

ENGINES = ("before", "after")
PERIODS = ("insample", "unseen_2016_2017", "unseen_2026")
STEP5_BOOKS = ["038-01_agitated-fall-next-day-rebound_1d", "034-02_rising-break-swings-continues_1d",
               "035-01.b1_calm-market-nearness-to-high_1d",
               "002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d",
               "011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d"]


def step6(rec, checks, py):
    res = checks / rec.name / "result.json"
    if not res.exists():
        subprocess.run([py, STEPS / "06_profitability/helper/check_profitability.py", rec, "--checks-dir", checks],
                       check=True, capture_output=True)
    return json.loads(res.read_text())


def held_days(rec, profile):
    """Days in a position, and those inside the profile (None when the book names no profile)."""
    n = inside = 0
    for coin in sorted(p for p in rec.iterdir() if p.is_dir()):
        prof = profile_of(coin.name) if profile else None
        for f in coin.glob("w*/bars.csv.gz"):
            b = pd.read_csv(f, usecols=["timestamp", "postRebalance_current_allocation"])
            b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
            d = b.assign(h=b.postRebalance_current_allocation.fillna(0).abs() > 1e-9).groupby("day").h.any()
            d = d[d]
            n += len(d)
            if profile:
                p = d.index.map(prof).to_series().fillna("")
                inside += int(p.apply(lambda s: bool(s) and all(w in s.split() for w in profile.split())).sum())
    return n, (inside / n if profile and n else None)


def net_returns(run_md):
    """{(coin, window): net return %} from a run.md's tables."""
    out, coin = {}, None
    for line in run_md.read_text().splitlines():
        m = re.match(r"- (\w+): \d+ of \d+ windows run", line)
        if m:
            coin = m.group(1)
        m = re.match(r"\| (w\d+) \| [^|]+\| [^|]+\| ([-\d.]+) \|", line)
        if m and coin:
            out[(coin, m.group(1))] = m.group(2)
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument("folder", type=Path)
    a.add_argument("--python", required=True)
    args = a.parse_args()
    S = args.folder.resolve()
    books = pd.read_csv(S / "books.csv")
    n7 = pd.read_csv(HERE.parent / "49_review" / "night7_ideas_full.csv")
    profiles = {f"{t.idea}_1d": t.profile for t in n7[n7.arm == "new"].itertuples() if isinstance(t.profile, str)}
    rows, series, faithful = [], {}, []
    for b in books.itertuples():
        for period in PERIODS:
            recs = {e: S / e / period / b.id for e in ENGINES}
            if not all((r / "run.md").exists() and list(r.glob("*/w*/bars.csv.gz")) for r in recs.values()):
                continue
            row = {"book": b.id.split("_")[0], "id": b.id, "run": b.run, "groups": b.groups, "bar": b.bar, "period": period,
                   "profile": profiles.get(b.id, "") if "N7" in b.groups else ""}
            res = {}
            for e, rec in recs.items():
                r = res[e] = step6(rec, S / e / f"{period}_checks", args.python)
                m = {x["measure"]: x for x in r["measures"]}
                days, share = held_days(rec, row["profile"])
                row.update({f"step6_{e}": r["status"], f"sharpe_{e}": m["sharpe_min"]["value"],
                            f"calmar_{e}": m["calmar_min"]["value"], f"mean_daily_in_position_{e}": m["avg_daily_return_min"]["value"],
                            f"trades_per_day_{e}": m["trade_frequency_min"]["value"], f"days_in_position_{e}": days,
                            f"inside_profile_{e}": share})
                if "P4" in b.groups:
                    series.setdefault((period, e), {})[b.id] = book_returns(rec, "1d").set_index(["window", "period"]).book
            mb = {x["measure"]: x for x in res["before"]["measures"]}
            row["flip"] = row["step6_before"] != row["step6_after"]
            row["crossed"] = "; ".join(x["label"] for x in res["after"]["measures"] if x["passed"] != mb[x["measure"]]["passed"])
            committed = STEPS / "04_backtest" / b.run / ("backtests" if period == "insample" else f"{period}/backtests") / b.id / "run.md"
            if committed.exists():
                c, r = net_returns(committed), net_returns(recs["before"] / "run.md")
                row["before_equals_committed"] = c == r
            if period == "insample" and b.id in STEP5_BOOKS:
                plan = Path(b.plan); vd = STEPS / "05_verification" / b.run / "verdicts" / b.id
                for e in ENGINES:
                    out = S / e / "verdicts"
                    if not (out / b.id / "result.json").exists():
                        subprocess.run([sys.executable, STEPS / "05_verification/helper/make_verdict.py", plan, "--python", args.python,
                                        "--records-root", S / e / period, "--verdicts-dir", out, "--measure", vd / "measure.py"],
                                       check=True, capture_output=True)
                    v = json.loads((out / b.id / "result.json").read_text())
                    row[f"step5_{e}"] = json.dumps(v, sort_keys=True)
                row["step5_same"] = row["step5_before"] == row["step5_after"]
                row["step5_before"] = row["step5_before"][:120]; row.pop("step5_after")
            rows.append(row)
    for (period, e), s in sorted(series.items()):
        R = pd.DataFrame(s).fillna(0.0).sort_index(); p = R.mean(axis=1).to_numpy()
        c, ann, fall = calmar(p)
        row = next((r for r in rows if r["book"] == "P4 portfolio" and r["period"] == period), None)
        if row is None:
            row = {"book": "P4 portfolio", "groups": "P4", "period": period}; rows.append(row)
        row.update({f"sharpe_{e}": sharpe(p), f"calmar_{e}": c, f"yearly_{e}": ann, f"worst_fall_{e}": fall, f"books_{e}": R.shape[1]})
    out = pd.DataFrame(rows)
    for c in [c for c in out if c.startswith(("days_in_position_", "books_"))]:
        out[c] = out[c].astype("Int64")
    out.to_csv(HERE / "impact.csv", index=False, float_format="%.4g")
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    show = ["book", "groups", "period", "step6_before", "step6_after", "crossed", "sharpe_before", "sharpe_after",
            "days_in_position_before", "days_in_position_after", "inside_profile_before", "inside_profile_after"]
    print(out[[c for c in show if c in out]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
