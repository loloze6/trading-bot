import numpy as np, pandas as pd
from scipy import stats

def _er(c, n=60, s=5):
    ch = (c - c.shift(n)).abs()
    vol = c.diff().abs().rolling(n).sum()
    return (ch / vol).rolling(s).mean()

def _t(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            ph = hi.shift(1).rolling(60).max(); pl = lo.shift(1).rolling(60).min()
            df = pd.DataFrame({"coin": coin, "w": w, "ts": ts, "c": c, "er": _er(c),
                               "up": (c / ph - 1) * 100, "dn": (c / pl - 1) * 100,
                               "width": (ph / pl - 1) * 100, "pos": np.arange(len(b)),
                               "r1": c.shift(-1) / c - 1,
                               "f10": c.shift(-10) / c - 1, "f10_20": c.shift(-20) / c.shift(-10) - 1,
                               "f20": c.shift(-20) / c - 1,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            df["yr"] = ts.dt.year; df["wd"] = ts.dt.dayofweek
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin on 10- and 20-grids
    d10 = A[(A.pos % 10 == 0)].groupby("coin")["f10"].mean()
    d20 = A[(A.pos % 20 == 0)].groupby("coin")["f20"].mean()
    d1 = A.groupby("coin")["r1"].mean()
    A["ex10"] = A.f10 - A.coin.map(d10); A["ex10_20"] = A.f10_20 - A.coin.map(d10)
    A["ex20"] = A.f20 - A.coin.map(d20); A["ex1"] = A.r1 - A.coin.map(d1)
    # weekday: next-day return from close of weekday wd, per coin, clustered by day
    W = A.dropna(subset=["ex1"]).copy(); W["nwd"] = (W.wd + 1) % 7
    day = W.groupby(["ts", "nwd"])["ex1"].mean().reset_index()
    out["nextday_excess_by_weekday_dayclustered"] = day.groupby("nwd")["ex1"].agg(
        n="size", mean="mean", t=_t).round(5)
    Wy = W.groupby(["ts", "nwd", "yr"])["ex1"].mean().reset_index()
    piv = Wy.groupby(["yr", "nwd"])["ex1"].mean().unstack().round(4)
    out["weekday_mean_by_year"] = piv
    out["weekday_mean_by_coin"] = W.groupby(["coin", "nwd"])["ex1"].mean().unstack().round(4)
    # breakouts: first bar, once per 10-cell
    A["cell"] = A.pos // 10
    prev_up = A.groupby(["coin", "w"])["up"].shift(1); prev_dn = A.groupby(["coin", "w"])["dn"].shift(1)
    U = A[(A.up > 0) & (prev_up <= 0) & (A.er <= 0.3)].drop_duplicates(["coin", "w", "cell"])
    Dn = A[(A.dn < 0) & (prev_dn >= 0) & (A.er <= 0.3)].drop_duplicates(["coin", "w", "cell"])
    def agg(df, cols):
        r = {}
        for col in cols:
            x = df.dropna(subset=[col])
            g = x.groupby("ts")[col].mean()
            r[col] = {"n_days": len(g), "mean": g.mean(), "t": _t(g)}
        return pd.DataFrame(r).T.round(4)
    out["up_trendless_ex10_ex10_20_ex20"] = agg(U, ["ex10", "ex10_20", "ex20"])
    out["down_trendless_long_ex10_ex10_20_ex20"] = agg(Dn, ["ex10", "ex10_20", "ex20"])
    # down break graded by width
    Dn = Dn.dropna(subset=["ex10"]).copy()
    Dn["wb"] = pd.qcut(Dn.width, 3)
    out["down_trendless_by_width"] = Dn.groupby("wb", observed=True)["ex10"].agg(n="size", mean="mean", t=_t).round(4)
    U2 = U.dropna(subset=["ex20"]).copy(); U2["wb"] = pd.qcut(U2.width, 3)
    out["up_trendless_ex20_by_width"] = U2.groupby("wb", observed=True)["ex20"].agg(n="size", mean="mean", t=_t).round(4)
    out["up_trendless_ex20_by_year"] = U2.groupby("yr")["ex20"].agg(n="size", mean="mean").round(4)
    # book: biggest daily returns
    Ds = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for w, d in ws.items()], ignore_index=True)
    bk = Ds.dropna(subset=["book_return"])
    bk = bk[bk.book_return != 0]
    q = bk.book_return.quantile([0.05, 0.95])
    out["book_nonzero_days"] = pd.Series({"n": len(bk), "mean": bk.book_return.mean(), "q05": q.iloc[0], "q95": q.iloc[1],
                                          "share_gain_top5pct": bk.book_return[bk.book_return > q.iloc[1]].sum() / bk.book_return.sum()}).round(4)
    return out
