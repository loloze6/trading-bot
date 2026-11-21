import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []  # grid h=5 cases with features
    ent = []   # entries
    for coin, wins in bars.items():
        # coin mean and std of 5-bar returns over all windows
        allr = {h: [] for h in (5, 10, 20)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        mu = {h: np.mean(allr[h]) for h in allr}
        sd = {h: np.std(allr[h], ddof=1) for h in allr}
        for w, df in wins.items():
            c = df["close"].values; hi = df["high"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            ts = pd.to_datetime(df["timestamp"])
            for t in range(0, n - 5, 5):
                fwd = c[t + 5] / c[t] - 1
                r5 = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                r1 = c[t] / c[t - 1] - 1 if t >= 1 else np.nan
                r30 = c[t] / c[t - 30] - 1 if t >= 30 else np.nan
                vol = np.nanstd(lr[t - 19:t + 1]) if t >= 20 else np.nan
                d20 = c[t] / np.max(c[t - 20:t]) - 1 if t >= 20 else np.nan
                rows.append(dict(coin=coin, ex=(fwd - mu[5]) / sd[5], exr=fwd - mu[5],
                                 r1=r1, r5=r5, r30=r30, vol=vol, d20=d20,
                                 wd=ts.iloc[t].dayofweek, yr=ts.iloc[t].year,
                                 active=f[t] > 0, fc=f[t]))
            # entries: forecast from 0 to >0
            for t in range(1, n):
                if f[t] > 0 and f[t - 1] <= 0:
                    d = dict(coin=coin, yr=ts.iloc[t].year,
                             r30=c[t] / c[t - 30] - 1 if t >= 30 else np.nan)
                    for h in (5, 10, 20):
                        d[f"x{h}"] = (c[t + h] / c[t] - 1 - mu[h]) if t + h < n else np.nan
                        d[f"s{h}"] = d[f"x{h}"] / sd[h] if t + h < n else np.nan
                    # days 6-10 and 11-20 alone
                    d["x6_10"] = (c[t + 10] / c[t + 5] - 1 - mu[5]) if t + 10 < n else np.nan
                    ent.append(d)
    R = pd.DataFrame(rows); E = pd.DataFrame(ent)
    out = {}
    def grp(col, q=5):
        d = R.dropna(subset=[col]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("b").agg(n=("ex", "size"), strength=("ex", "mean"), exret=("exr", "mean"),
                              feat=(col, "median"))
        g["t"] = d.groupby("b")["ex"].apply(tstat)
        return g
    for col in ["r1", "r5", "r30", "vol", "d20"]:
        out["by_" + col] = grp(col)
    g = R.groupby("wd").agg(n=("ex", "size"), strength=("ex", "mean"))
    g["t"] = R.groupby("wd")["ex"].apply(tstat); out["by_weekday_start"] = g
    g = R.groupby("active").agg(n=("ex", "size"), strength=("ex", "mean"), exret=("exr", "mean"))
    g["t"] = R.groupby("active")["ex"].apply(tstat); out["active_vs_flat"] = g
    # d20 x r30 sign
    d = R.dropna(subset=["d20", "r30"]).copy()
    d["mom"] = np.where(d.r30 > 0, "up30", "down30")
    d["b"] = pd.qcut(d.d20.rank(method="first"), 4, labels=False)
    g = d.groupby(["mom", "b"]).agg(n=("ex", "size"), strength=("ex", "mean"), d20=("d20", "median"))
    g["t"] = d.groupby(["mom", "b"])["ex"].apply(tstat); out["d20_by_mom"] = g
    # entries persistence
    s = {}
    for k in ["x5", "x10", "x20", "x6_10", "s5", "s10", "s20"]:
        s[k] = [E[k].mean(), tstat(E[k]), E[k].notna().sum()]
    out["entries_persist"] = pd.DataFrame(s, index=["mean", "t", "n"]).T
    g = E.groupby("yr").agg(n=("x5", "count"), x5=("x5", "mean"), x10=("x10", "mean"))
    out["entries_by_year"] = g
    return out
