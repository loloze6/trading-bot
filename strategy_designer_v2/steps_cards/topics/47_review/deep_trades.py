"""Topic 47, the trades in depth (operator, 2026-11-23: "do forecasts at 20 lose more than at 5? deep analysis and
statistics; be creative"). From the trade table (trade_table.py, clean_excursions.py), per bar size:
  A. the forecast's level: bands of |forecast| at entry; per band: trades, win rate, the result per unit (net_pct: the
     price move after costs, the bet's quality) and the result for the portfolio (net_portfolio_return_pct: sized by
     the position, the money); 95 % intervals by resampling whole days (trades of one day are not independent); within
     each book too (the book's mean taken away). A regression of the result on |forecast| with each book its own base,
     its slope's t from errors clustered by day.
  D. costs and churn: the fees against the gross result; trades reopened on the same coin and side within 3 bars of
     the last exit (paying the round trip again).
  E. coins and years: the result per coin and per year; out of fold, do the coins that lost on three folds lose on the
     fourth?
  F. losing streaks: per book and coin, runs of losing trades against the runs expected if trades were independent
     (the Wald-Wolfowitz runs test): z < 0 means losses follow losses more than chance.
  G. how a trade ends: by holding time.
  python3 topics/47_review/deep_trades.py TRADES.csv.gz"""
import sys, warnings
import numpy as np, pandas as pd
from scipy import stats as ss

warnings.simplefilter("ignore")
rng = np.random.default_rng(5)
d = pd.read_csv(sys.argv[1]); d["entry_time"] = pd.to_datetime(d.entry_time, format="ISO8601")
d["day"] = d.entry_time.dt.normalize()
d["money"] = d.net_portfolio_return_pct
BANDS = [0, 2.5, 5, 10, 15, 19.999, 20.001]
LABELS = ["0-2.5", "2.5-5", "5-10", "10-15", "15-20", "20 (cap)"]


def day_ci(x, col, n=300):
    """95 % interval of the mean of col, resampling whole days."""
    g = x.groupby("day")[col].agg(["sum", "count"])
    s, c = g["sum"].to_numpy(), g["count"].to_numpy()
    idx = rng.integers(0, len(g), (n, len(g)))
    m = s[idx].sum(1) / c[idx].sum(1)
    return np.quantile(m, [0.025, 0.975])


def fe_slope(x, ycol, xcol):
    """Slope of ycol on xcol with each book its own base (both demeaned within book); t from errors clustered by day."""
    y = x[ycol] - x.groupby("book")[ycol].transform("mean"); z = x[xcol] - x.groupby("book")[xcol].transform("mean")
    b = (z * y).sum() / (z * z).sum(); e = y - b * z
    meat = (z * e).groupby(x["day"]).sum().pow(2).sum(); se = np.sqrt(meat) / (z * z).sum()
    return b, b / se


pd.set_option("display.width", 230)
for bar, x in d.groupby("bar"):
    x = x.copy()
    print(f"\n######## {bar}: {len(x):,} trades, {x.book.nunique()} books, {x.day.nunique():,} days")
    # A. the forecast's level
    x["band"] = pd.cut(x.abs_forecast, BANDS, labels=LABELS, include_lowest=True)
    x["net_in_book"] = x.net_pct - x.groupby("book").net_pct.transform("mean")
    x["win_in_book"] = x.win - x.groupby("book").win.transform("mean")
    rows = []
    for band, y in x.groupby("band", observed=True):
        lo, hi = day_ci(y, "net_pct"); mlo, mhi = day_ci(y, "money")
        rows.append({"band": band, "trades": len(y), "books": y.book.nunique(), "win": y.win.mean(), "win_vs_own_book": y.win_in_book.mean(),
                     "per_unit": y.net_pct.mean(), "per_unit_95": f"{lo:+.2f}..{hi:+.2f}", "per_unit_vs_own_book": y.net_in_book.mean(),
                     "money": y.money.mean(), "money_95": f"{mlo:+.3f}..{mhi:+.3f}", "share_of_total_money": y.money.sum() / x.money.sum()})
    print("A. by the forecast's size at entry:"); print(pd.DataFrame(rows).round(3).to_string(index=False))
    for ycol in ("net_pct", "win", "money"):
        b, t = fe_slope(x.assign(win=x.win.astype(float)), ycol, "abs_forecast")
        print(f"   slope of {ycol} per forecast point, each book its own base: {b:+.5f} (t {t:+.2f}, errors clustered by day)")
    by_book = x.groupby("book").apply(lambda g: ss.spearmanr(g.abs_forecast, g.net_pct)[0] if g.abs_forecast.nunique() > 3 else np.nan).dropna()
    print(f"   per book, rank correlation of |forecast| with the result: median {by_book.median():+.3f}; positive in {int((by_book > 0).sum())} of {len(by_book)} books")
    # D. costs and churn
    gross = x.net_pct + 0.10
    print(f"D. fees: {0.10 * len(x):,.0f} points paid against a gross result of {gross.sum():,.0f} points: fees take {0.10 * len(x) / gross.clip(lower=0).sum():.1%} of the gross gains; "
          f"the net result is {x.net_pct.sum() / gross.sum():.1%} of the gross")
    x = x.sort_values(["book", "symbol", "entry_time"])
    prev_exit = x.groupby(["book", "symbol"]).entry_time.shift(1) + pd.to_timedelta(x.groupby(["book", "symbol"]).holding_bars.shift(1).fillna(0) * (24 if bar == "1d" else 1), unit="h")
    same_side = x.direction == x.groupby(["book", "symbol"]).direction.shift(1)
    gap = (x.entry_time - prev_exit) / pd.Timedelta(hours=24 if bar == "1d" else 1)
    re = same_side & (gap <= 3) & (gap >= 0)
    print(f"   reopened on the same coin and side within 3 bars of the last exit: {re.mean():.1%} of trades; their mean result {x[re].net_pct.mean():+.3f} % against {x[~re].net_pct.mean():+.3f} % for the others")
    # E. coins and years
    yr = x.groupby(x.entry_time.dt.year).agg(trades=("win", "size"), win=("win", "mean"), per_unit=("net_pct", "mean"), money=("money", "sum"))
    print("E. by year:", yr.round(3).to_dict("index"))
    co = x.groupby("symbol").agg(trades=("win", "size"), win=("win", "mean"), per_unit=("net_pct", "mean"), money=("money", "sum"))
    print("   by coin:", co.round(3).to_dict("index"))
    hits = tot = 0
    for book, y in x.groupby("book"):
        for f in y.fold.dropna().unique():
            tr = y[y.fold != f].groupby("symbol").net_pct.sum(); te = y[y.fold == f].groupby("symbol").net_pct.sum()
            losers = tr[tr < 0].index.intersection(te.index)
            hits += int((te[losers] < 0).sum()); tot += len(losers)
    print(f"   coins that lost on three folds, on the fourth: lose again {hits} of {tot} ({hits / max(tot, 1):.0%}; 50 % = no carry-over)")
    # F. losing streaks
    zs = []
    for _, y in x.groupby(["book", "symbol"]):
        w = y.win.to_numpy()
        n1, n2 = w.sum(), (~w).sum()
        if n1 < 10 or n2 < 10: continue
        runs = 1 + (w[1:] != w[:-1]).sum(); mu = 2 * n1 * n2 / (n1 + n2) + 1
        var = 2 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
        zs.append((runs - mu) / np.sqrt(var))
    zs = np.array(zs)
    print(f"F. runs test over {len(zs)} book-coin series: median z {np.median(zs):+.2f}; z below -2 (losses cluster) in {(zs < -2).mean():.0%}, above +2 in {(zs > 2).mean():.0%} (5 % expected by chance)")
    # G. holding time
    x["held"] = pd.cut(x.holding_bars, [0, 1, 2, 5, 10, 1e9], labels=["1", "2", "3-5", "6-10", ">10"])
    print("G. by bars held:", x.groupby("held", observed=True).agg(trades=("win", "size"), win=("win", "mean"), per_unit=("net_pct", "mean"), share_of_money=("money", lambda s: s.sum() / x.money.sum())).round(3).to_dict("index"))
