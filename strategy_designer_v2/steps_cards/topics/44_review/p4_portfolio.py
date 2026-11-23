"""Topic 44, P4: the fixed portfolio (runs/PORTFOLIO_UNSEEN_RUN.md) on each unseen period. Per period:
  - each book's daily returns from its unseen record (04_backtest/<run>/<period>/backtests/<id>/), by step 6's
    definition (orchestration/ideas_similarities_check/helper/book_returns.py: per coin its value at each day's last
    bar, the day's return the mean of its coins'); a book with no record there is named and left out;
  - the portfolio: the mean of its books' daily returns that day (equal capital among the books with a record);
  - holds: its Sharpe after costs above 0 (the book part of common/unseen_dates.md); Calmar, yearly, worst fall;
  - holding: each book's coins held (book_returns' "hold"), averaged over the books like the portfolio;
  - the books alone: each book's own unseen result (orchestration/unseen_test/<run>/<id>.json): holds, Sharpe;
  - where the result comes from: each book's mean net position (its coins' positions averaged, long +, short -; from the
    record's chart files) and the correlation of its daily returns with holding its coins.
  python3 topics/44_review/p4_portfolio.py"""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
sys.path.insert(0, str(HERE.parent / "47_review"))
sys.path.insert(0, str(STEPS / "orchestration" / "ideas_similarities_check" / "helper"))
from book_returns import book_returns   # noqa: E402
from p2_weights import calmar, sharpe   # noqa: E402

PERIODS = ["unseen_2016_2017", "unseen_2026"]
books = pd.read_csv(HERE / "p1_candidates_earning.csv"); books = books[books.status == "candidate"]
rows, summary = [], []
for period in PERIODS:
    series, holds, missing = {}, {}, []
    for b in books.itertuples():
        rec = STEPS / "04_backtest" / b.run / period / "backtests" / b.id
        res = STEPS / "orchestration" / "unseen_test" / b.run / f"{b.id}.json"
        own = json.load(open(res))["periods"].get(period, {}) if res.exists() else {}
        try:
            br = book_returns(rec, "1d") if rec.is_dir() else None
            why = "no record"
        except FileNotFoundError:
            br, why = None, "record without its bars on this machine"
        if br is None or len(br) == 0:
            missing.append(b.family); rows.append({"period": period, "family": b.family, "bar": b.bar, "record": False, "why": why}); continue
        br = br.set_index(["window", "period"]).sort_index()
        s_ = br["book"]; series[b.family] = s_; holds[b.family] = br["hold"]
        net = np.nan
        if (rec / "chart_bars.csv.gz").exists():
            cb = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "position"])
            net = float(np.sign(cb.position).mean())
        rows.append({"period": period, "family": b.family, "bar": b.bar, "record": True, "days": len(s_),
                     "mean_net_position": net, "corr_with_holding": float(np.corrcoef(s_, br["hold"])[0, 1]) if s_.std() > 0 else np.nan,
                     "sharpe_from_days": sharpe(s_.to_numpy()) if s_.std() > 0 else np.nan, "calmar": calmar(s_.to_numpy())[0],
                     "own_holds": own.get("holds"), "own_step5": own.get("step5"), "own_sharpe": own.get("sharpe"),
                     "own_holding_sharpe": own.get("holding_sharpe")})
    if not series:
        print(f"{period}: no book has a record"); continue
    R = pd.DataFrame(series).fillna(0.0).sort_index(); p = R.mean(axis=1).to_numpy()
    hold = pd.DataFrame(holds).reindex(R.index).mean(axis=1).fillna(0.0).to_numpy()
    c, a, fall = calmar(p); hc, ha, hfall = calmar(hold)
    b = pd.DataFrame([r for r in rows if r["period"] == period and r["record"]])
    summary.append({"period": period, "books_with_a_record": len(series), "left_out": ",".join(missing) or "-", "days": len(p),
                    "portfolio_sharpe": sharpe(p), "portfolio_holds": sharpe(p) > 0, "portfolio_calmar": c,
                    "portfolio_yearly_pct": 100 * a, "portfolio_worst_fall_pct": 100 * fall,
                    "holding_sharpe": sharpe(hold), "holding_yearly_pct": 100 * ha, "holding_worst_fall_pct": 100 * hfall,
                    "books_holding": f"{int((b.own_holds == True).sum())} of {len(b)}",
                    "books_sharpe_above_0": f"{int((b.sharpe_from_days > 0).sum())} of {len(b)}",
                    "books_median_sharpe": b.sharpe_from_days.median(), "books_median_calmar": b.calmar.median(),
                    "portfolio_corr_with_holding": float(np.corrcoef(p, hold)[0, 1]),
                    "books_median_net_position": b.mean_net_position.median(),
                    "mean_correlation_between_books": R.corr().where(~np.eye(R.shape[1], dtype=bool)).stack().mean()})
pd.set_option("display.width", 220)
s = pd.DataFrame(summary); print(s.round(3).T.to_string())
d = pd.DataFrame(rows); print(d.round(2).to_string(index=False))
s.to_csv(HERE / "p4_portfolio.csv", index=False, float_format="%.4g"); d.to_csv(HERE / "p4_books.csv", index=False, float_format="%.4g")
