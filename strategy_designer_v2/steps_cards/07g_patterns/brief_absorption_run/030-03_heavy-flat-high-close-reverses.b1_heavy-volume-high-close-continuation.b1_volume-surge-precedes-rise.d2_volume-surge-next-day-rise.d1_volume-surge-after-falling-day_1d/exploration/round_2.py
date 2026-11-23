import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b.sort_values("timestamp")["close"].pct_change() for b in wins.values()])
        mu = allr.mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            r = b["close"].pct_change()
            sd = r.rolling(20, min_periods=15).std().shift(1)
            d["z"] = r / sd
            d["vr"] = b["volume"] / b["volume"].rolling(20, min_periods=15).mean().shift(1)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            d["clv"] = (b["close"] - b["low"]) / rng
            d["r5z"] = (b["close"] / b["close"].shift(5) - 1) / (sd * np.sqrt(5))
            d["volreg"] = sd / sd.rolling(120, min_periods=40).median()
            d["nx"] = b["close"].shift(-1) / b["close"] - 1 - mu
            d["nxs"] = d["nx"] / sd
            d["nx3"] = b["close"].shift(-3) / b["close"] - 1 - 3 * mu
            d["pos3"] = (np.arange(len(b)) % 3 == 0)
            ts = pd.to_datetime(b["timestamp"])
            d["wd"] = ts.dt.weekday
            d["yr"] = ts.dt.year
            d["coin"] = coin; d["win"] = w
            d["alloc"] = b["postRebalance_current_allocation"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def summ(g, col="nx"):
        x = g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    # regression nx (scaled) on z, clv, vr, z*vr, r5z
    R = D.dropna(subset=["nxs", "z", "clv", "vr", "r5z", "volreg"]).copy()
    R["clvc"] = R["clv"] - 0.5
    R["lvr"] = np.log(R["vr"])
    R["zneg_lvr"] = np.minimum(R["z"], 0) * R["lvr"]
    R["zneg_vreg"] = np.minimum(R["z"], 0) * np.log(R["volreg"])
    X = R[["z", "clvc", "lvr", "zneg_lvr", "r5z", "zneg_vreg"]].values
    X = np.column_stack([np.ones(len(X)), X])
    y = R["nxs"].clip(-6, 6).values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=X.shape[1])
    out["regression nx/sd"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
        index=["const", "z", "clv-0.5", "log vr", "min(z,0)*log vr", "r5z", "min(z,0)*log volreg"])
    # clv within z bins
    R["zb"] = pd.cut(R["z"], [-99, -1, -0.3, 0.3, 1, 99], labels=False)
    R["cb"] = pd.cut(R["clv"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=False)
    t = R.groupby(["zb", "cb"]).apply(summ)
    out["nx% by z bin x clv bin"] = t["mean%"].unstack()
    out["t by z bin x clv bin"] = t["t"].unstack()
    # down-day by volreg tercile, stability by year
    R["vlq"] = pd.qcut(R["volreg"], 3, labels=False)
    big = R[R["z"] < -1]
    out["z<-1: nx by volreg tercile"] = big.groupby("vlq").apply(summ)
    out["z<-1, top volreg: by year"] = big[big["vlq"] == 2].groupby("yr").apply(summ)
    out["z<-1, top volreg: by coin"] = big[big["vlq"] == 2].groupby("coin").apply(summ)
    # 5d momentum top quintile 3-day forward, by year and coin
    G = D[D["pos3"]].dropna(subset=["r5z", "nx3"]).copy()
    G["r5q"] = pd.qcut(G["r5z"], 5, labels=False)
    top = G[G["r5q"] == 4]
    out["r5 top quintile nx3 by year"] = top.groupby("yr").apply(lambda g: summ(g, "nx3"))
    out["r5 top quintile nx3 by coin"] = top.groupby("coin").apply(lambda g: summ(g, "nx3"))
    G["r5d"] = pd.qcut(G["r5z"], 10, labels=False)
    out["nx3 by r5 decile"] = G.groupby("r5d").apply(lambda g: summ(g, "nx3"))
    # weekday stability
    wk = D.dropna(subset=["nx"]).copy()
    wk["thfr"] = wk["wd"].isin([3, 4])
    out["Thu+Fri minus others by year"] = wk.groupby("yr").apply(
        lambda g: pd.Series({"diff%": 100 * (g[g.thfr].nx.mean() - g[~g.thfr].nx.mean()),
                             "t": stats.ttest_ind(g[g.thfr].nx, g[~g.thfr].nx, equal_var=False)[0]}))
    # book: worst/best day contexts
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin))
    B = pd.concat(bk).dropna(subset=["book_return"])
    q1, q99 = B["book_return"].quantile([0.02, 0.98])
    out["book worst 2% days: coin return mean%"] = pd.Series({
        "worst book days coin ret%": 100 * B[B.book_return <= q1].coin_return.mean(),
        "best book days coin ret%": 100 * B[B.book_return >= q99].coin_return.mean(),
        "n worst": (B.book_return <= q1).sum()})
    return out
