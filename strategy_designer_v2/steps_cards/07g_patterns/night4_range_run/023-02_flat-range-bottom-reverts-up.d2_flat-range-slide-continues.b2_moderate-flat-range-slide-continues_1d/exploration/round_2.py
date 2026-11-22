import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    # weekday effect robustness
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    DD["day"] = pd.to_datetime(DD["day"])
    DD["wd"] = DD["day"].dt.dayofweek
    DD["yr"] = DD["day"].dt.year
    DD["sat"] = DD["wd"].isin([4, 5]).astype(int)
    def wt(g):
        a = g.loc[g["sat"] == 1, "coin_return"]; b = g.loc[g["sat"] == 0, "coin_return"]
        t = stats.ttest_ind(a, b, equal_var=False).statistic if len(a) > 2 and len(b) > 2 else np.nan
        return pd.Series({"n_fri_sat": len(a), "mean_fri_sat": a.mean(), "mean_other": b.mean(), "diff": a.mean() - b.mean(), "t": t})
    out["fri+sat minus other days, by coin"] = DD.groupby("coin").apply(wt)
    out["fri+sat minus other days, by year"] = DD.groupby("yr").apply(wt)
    # market-day average to remove cross-coin correlation
    M = DD.groupby(["win", "day"]).agg(r=("coin_return", "mean"), wd=("wd", "first"), yr=("yr", "first")).reset_index()
    out["coin-average day return by weekday (one obs per day)"] = M.groupby("wd")["r"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # weekday by vol level of the coin's trailing 20-day vol
    DD = DD.sort_values(["coin", "win", "day"])
    DD["vol20"] = DD.groupby(["coin", "win"])["coin_return"].transform(lambda s: s.shift(1).rolling(20).std())
    DD["r7"] = DD.groupby(["coin", "win"])["close"].transform(lambda s: s.shift(1) / s.shift(8) - 1)
    DD["volq"] = DD.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fri+sat diff by vol tercile"] = DD.dropna(subset=["volq"]).groupby("volq").apply(wt)
    DD["r7s"] = np.sign(DD["r7"])
    out["fri+sat diff by sign of prior 7-day return"] = DD.dropna(subset=["r7s"]).groupby("r7s").apply(wt)

    # trend side: direction of 30-day move x ext bucket, non-overlapping 5-bar
    H = 5; rows = []
    for coin, wins in data["bars"].items():
        tmp = []; gr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = hi.rolling(30).max() - lo.rolling(30).min()
            nmr = (c - c.shift(30)).abs() / rng
            dir30 = np.sign(c - c.shift(30))
            r10 = c / c.shift(10) - 1
            ext = r10 / r10.abs().rolling(60, min_periods=20).mean()
            fwd = c.shift(-H) / c - 1
            d = pd.DataFrame({"nmr": nmr, "dir30": dir30, "ext": ext, "fwd": fwd,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year}).iloc[::H]
            d["coin"] = coin; d["win"] = w
            gr.append(d["fwd"].dropna()); tmp.append(d)
        m = pd.concat(gr).mean()
        for d in tmp:
            d["unus"] = d["fwd"] - m; rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["unus", "nmr", "ext"])
    def summ(g):
        x = g["unus"]; n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    D["flat"] = np.where(D["nmr"] <= 0.3, "flat", "trend")
    D["extb"] = pd.cut(D["ext"], [-10, -1, 0, 1, 10])
    T = D[D["flat"] == "trend"]
    out["trend: dir30 x ext bucket"] = T.groupby(["dir30", "extb"], observed=True).apply(summ)
    # graded: nmr as continuous, momentum strength: unusual move x sign(ext) by nmr tercile
    D["nmrq"] = pd.qcut(D["nmr"], 4, labels=False)
    D["mom"] = D["unus"] * np.sign(D["ext"])
    out["fwd5 in direction of 10d move, by nmr quartile"] = D.groupby("nmrq").apply(lambda g: pd.Series({"n": len(g), "mean": g["mom"].mean(), "t": g["mom"].mean() / (g["mom"].std() / np.sqrt(len(g)))}))
    T2 = D[D["nmrq"] == 3]
    out["top nmr quartile: momentum by coin"] = T2.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "mean": g["mom"].mean(), "t": g["mom"].mean() / (g["mom"].std() / np.sqrt(len(g)))}))
    out["top nmr quartile: momentum by year"] = T2.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "mean": g["mom"].mean(), "t": g["mom"].mean() / (g["mom"].std() / np.sqrt(len(g)))}))
    return out
