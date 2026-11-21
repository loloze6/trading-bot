import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            ret1 = c.pct_change()
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            vol20 = ret1.rolling(20, min_periods=15).std()
            hi = c.rolling(90, min_periods=30).max()
            lo = c.rolling(90, min_periods=30).min()
            pos = (c - lo) / (hi - lo)
            rng = (b["high"] - b["low"]) / c
            fc = b["forecast"].astype(float)
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for t in range(0, n - 5, 5):
                rows.append(dict(coin=coin, w=w, r5=c[t+5]/c[t]-1, past5=past5[t], past20=past20[t],
                                 vol20=vol20[t], pos90=pos[t], rng=rng[t], fc=fc[t], wd=wd[t], r1=ret1[t]))
            for t in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, r1=ret1[t], nxt=c[t+1]/c[t]-1, wd=wd[t+1], vol=vol20[t], rng=rng[t]))
    g = pd.DataFrame(rows); d = pd.DataFrame(daily)
    g["drift"] = g.groupby("coin")["r5"].transform("mean")
    g["sd"] = g.groupby("coin")["r5"].transform("std")
    g["ex"] = g["r5"] - g["drift"]; g["st"] = g["ex"] / g["sd"]
    d["drift"] = d.groupby("coin")["nxt"].transform("mean"); d["ex"] = d["nxt"] - d["drift"]
    out = {}
    def bucket(df, col, k=5):
        df = df.dropna(subset=[col]).copy()
        df["q"] = df.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), k, labels=False))
        r = df.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), strength=("st", "mean"))
        r["t"] = r["mean_ex"] / (r["sd"] / np.sqrt(r["n"]))
        return r.drop(columns="sd")
    for col in ["past5", "past20", "vol20", "pos90", "rng", "r1"]:
        out["5d ex by " + col + " quintile"] = bucket(g, col)
    g["active"] = (g["fc"] > 0).astype(int)
    out["5d ex by forecast>0"] = g.groupby("active")["ex"].agg(["size", "mean", "std"])
    out["5d ex by weekday"] = g.groupby("wd")["ex"].agg(["size", "mean"])
    # per-coin slopes of past20 and pos90
    sl = []
    for coin, s in g.dropna(subset=["past20", "pos90"]).groupby("coin"):
        sl.append(dict(coin=coin, rho_past20=stats.spearmanr(s["past20"], s["ex"])[0],
                       rho_pos90=stats.spearmanr(s["pos90"], s["ex"])[0],
                       rho_past5=stats.spearmanr(s["past5"], s["ex"])[0], n=len(s)))
    out["per coin spearman"] = pd.DataFrame(sl)
    # daily next-day by today's return quintile, and by weekday
    dd = d.dropna(subset=["r1"]).copy()
    dd["q"] = dd.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    r = dd.groupby("q")["ex"].agg(["size", "mean", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["size"]))
    out["next day ex by today ret quintile"] = r
    r = dd.groupby("wd")["ex"].agg(["size", "mean", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["size"]))
    out["next day ex by weekday"] = r
    # book: daily returns, coin, position
    bk = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            x = dy[["book_return", "coin_return"]].dropna().copy(); x["coin"] = coin; x["w"] = w
            bk.append(x)
    bk = pd.concat(bk)
    bm = bk.groupby(level=0).mean(numeric_only=True) if False else bk
    out["book by window mean ret"] = bk.groupby("w")[["book_return", "coin_return"]].mean().T
    out["book by coin"] = bk.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    return out
