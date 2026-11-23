"""Topic 44, P4: the fixed portfolio (runs/PORTFOLIO_UNSEEN_RUN.md) on each unseen period. Per period:
  - each book's daily returns from its unseen record (04_backtest/<run>/<period>/backtests/<id>/chart_bars.csv.gz; the
    book's return a day = the mean of its coins' returns, as in P1); a book with no record there is named and left out;
  - the portfolio: the mean of its books' daily returns that day (equal capital among the books with a record);
  - holds: its Sharpe after costs above 0 (the book part of common/unseen_dates.md); Calmar, yearly, worst fall;
  - holding the coins: the mean daily return of the coins its books trade (each coin's close to close), same days;
  - the books alone: each book's own unseen result (orchestration/unseen_test/<run>/<id>.json): holds, Sharpe.
  python3 topics/44_review/p4_portfolio.py"""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
sys.path.insert(0, str(HERE.parent / "47_review"))
import streaks as st          # noqa: E402
from p2_weights import calmar, sharpe   # noqa: E402

PERIODS = ["unseen_2016_2017", "unseen_2026"]
books = pd.read_csv(HERE / "p1_candidates_earning.csv"); books = books[books.status == "candidate"]
rows, summary = [], []
for period in PERIODS:
    series, coins, missing = {}, set(), []
    for b in books.itertuples():
        rec = STEPS / "04_backtest" / b.run / period / "backtests" / b.id
        res = STEPS / "orchestration" / "unseen_test" / b.run / f"{b.id}.json"
        own = json.load(open(res))["periods"].get(period, {}) if res.exists() else {}
        if not (rec / "chart_bars.csv.gz").exists():
            missing.append(b.family); rows.append({"period": period, "family": b.family, "bar": b.bar, "record": False}); continue
        ret, _ = st.per_coin(rec); s = ret.mean(axis=1).fillna(0.0)
        series[b.family] = s; coins |= set(ret.columns)
        rows.append({"period": period, "family": b.family, "bar": b.bar, "record": True, "days": len(s),
                     "sharpe_from_days": sharpe(s.to_numpy()) if s.std() > 0 else np.nan, "calmar": calmar(s.to_numpy())[0],
                     "own_holds": own.get("holds"), "own_step5": own.get("step5"), "own_sharpe": own.get("sharpe"),
                     "own_holding_sharpe": own.get("holding_sharpe")})
    if not series:
        print(f"{period}: no book has a record"); continue
    R = pd.DataFrame(series).fillna(0.0).sort_index(); p = R.mean(axis=1).to_numpy()
    days = R.index.get_level_values("day")
    px = {}
    for c in sorted(coins):
        f = DATA / f"kraken_{c}_1d.csv"
        cl = pd.read_csv(f, usecols=["timestamp", "close"]); cl["timestamp"] = pd.to_datetime(cl.timestamp, format="ISO8601")
        px[c] = cl.drop_duplicates("timestamp").set_index("timestamp").close
    hold = pd.DataFrame(px).pct_change().reindex(days).mean(axis=1).fillna(0.0).to_numpy()
    c, a, fall = calmar(p); hc, ha, hfall = calmar(hold)
    b = pd.DataFrame([r for r in rows if r["period"] == period and r["record"]])
    summary.append({"period": period, "books_with_a_record": len(series), "left_out": ",".join(missing) or "-", "days": len(p),
                    "portfolio_sharpe": sharpe(p), "portfolio_holds": sharpe(p) > 0, "portfolio_calmar": c,
                    "portfolio_yearly_pct": 100 * a, "portfolio_worst_fall_pct": 100 * fall,
                    "holding_sharpe": sharpe(hold), "holding_yearly_pct": 100 * ha, "holding_worst_fall_pct": 100 * hfall,
                    "books_holding": f"{int((b.own_holds == True).sum())} of {len(b)}",
                    "books_sharpe_above_0": f"{int((b.sharpe_from_days > 0).sum())} of {len(b)}",
                    "books_median_sharpe": b.sharpe_from_days.median(), "books_median_calmar": b.calmar.median(),
                    "mean_correlation_between_books": R.corr().where(~np.eye(R.shape[1], dtype=bool)).stack().mean()})
pd.set_option("display.width", 220)
s = pd.DataFrame(summary); print(s.round(3).T.to_string())
d = pd.DataFrame(rows); print(d.round(2).to_string(index=False))
s.to_csv(HERE / "p4_portfolio.csv", index=False, float_format="%.4g"); d.to_csv(HERE / "p4_books.csv", index=False, float_format="%.4g")
