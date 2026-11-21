import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            hi = c.rolling(90, min_periods=20).max()
            depth_raw = c / hi - 1
            r90 = c / c.shift(min(89, max(n-1,1))) - 1  # not used
            r20 = c / c.shift(20) - 1
            r5p = c / c.shift(5) - 1
            lr = np.log(c).diff()
            vol20 = lr.rolling(20, min_periods=10).std()
            vol60 = lr.rolling(60, min_periods=20).std()
            fwd = c.shift(-H) / c - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, i=i, regime=b.loc[i, "regime"],
                                 fc=b.loc[i, "forecast"], alloc=b.loc[i, "postRebalance_current_allocation"],
                                 depth=depth_raw[i], r20=r20[i], r5p=r5p[i],
                                 volratio=vol20[i] / vol60[i] if vol60[i] > 0 else np.nan,
                                 fwd=fwd[i], pos=i / n))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    out = {}
    out["grid counts by regime"] = g.groupby("regime")["ex"].agg(["count", "mean"])
    mr = g[g.regime == "mean_reversion"].copy()
    nm = g[g.regime != "mean_reversion"].copy()
    def qtab(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        t = d.groupby("q").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"),
                               ex=("ex", "mean"), fwd=("fwd", "mean"))
        t["t"] = d.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t
    out["MR: excess by depth quintile"] = qtab(mr, "depth")
    out["notMR: excess by depth quintile"] = qtab(nm, "depth")
    out["MR: excess by 20d return quintile"] = qtab(mr, "r20")
    out["MR: excess by 5d past return quintile"] = qtab(mr, "r5p")
    out["MR: excess by vol ratio quintile"] = qtab(mr, "volratio")
    out["ALL: excess by 20d return quintile"] = qtab(g, "r20")
    out["ALL: excess by depth quintile"] = qtab(g, "depth")
    out["MR by coin"] = mr.groupby("coin")["ex"].agg(["count", "mean"])
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    byw = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book vs coin mean daily by window"] = byw
    out["book vs coin by year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    # worst book days: what regime/held
    out["book daily by coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                    booksd=("book_return", "std"))
    # avg allocation when MR
    out["mean alloc MR"] = float(mr["alloc"].mean())
    return out
