import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy().reset_index(drop=True); x["coin"] = coin; x["win"] = w
            x["r7"] = x["close"].shift(1) / x["close"].shift(8) - 1
            x["r7_now"] = x["close"] / x["close"].shift(7) - 1
            x["fwd1"] = x["close"].shift(-1) / x["close"] - 1
            x["fwd2"] = x["close"].shift(-2) / x["close"] - 1
            dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    DD["day"] = pd.to_datetime(DD["day"])
    DD["wd"] = DD["day"].dt.dayofweek
    DD["yr"] = DD["day"].dt.year
    m1 = DD.groupby("coin")["coin_return"].transform("mean")
    DD["unus1"] = DD["coin_return"] - m1
    def s(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    fs = DD[DD["wd"].isin([4, 5])].dropna(subset=["r7", "unus1"]).copy()
    fs["r7q"] = fs.groupby("coin")["r7"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["fri/sat unusual day return by prior 7d quintile"] = fs.groupby("r7q")["unus1"].apply(s).unstack()
    ot = DD[~DD["wd"].isin([4, 5])].dropna(subset=["r7", "unus1"]).copy()
    ot["r7q"] = ot.groupby("coin")["r7"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["other days unusual by prior 7d quintile"] = ot.groupby("r7q")["unus1"].apply(s).unstack()
    # Thursday close -> fri+sat 2-day return, graded by 7-day return at Thursday close; one per week
    th = DD[DD["wd"] == 3].dropna(subset=["r7_now", "fwd2"]).copy()
    m2 = th.groupby("coin")["fwd2"].transform("mean")
    mall2 = DD.dropna(subset=["fwd2"]).groupby("coin")["fwd2"].transform("mean")
    th["unus2"] = th["fwd2"] - DD.loc[th.index, "coin"].map(DD.iloc[::2].dropna(subset=["fwd2"]).groupby("coin")["fwd2"].mean())
    th["q"] = th.groupby("coin")["r7_now"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["thu close: next 2d unusual by 7d quintile"] = th.groupby("q")["unus2"].apply(s).unstack()
    out["thu close: spearman r7 vs next2d, by coin"] = th.groupby("coin").apply(lambda g: pd.Series(stats.spearmanr(g["r7_now"], g["fwd2"])[:2], index=["rho", "p"]))
    out["thu close next2d unusual by year"] = th.groupby("yr")["unus2"].apply(s).unstack()

    # downtrend moderate-slide continuation, graded
    H = 5; rows = []
    for coin, wins in data["bars"].items():
        tmp = []; gr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = hi.rolling(30).max() - lo.rolling(30).min()
            nmr = (c - c.shift(30)) / rng
            r10 = c / c.shift(10) - 1
            ext = r10 / r10.abs().rolling(60, min_periods=20).mean()
            fwd = c.shift(-H) / c - 1
            d = pd.DataFrame({"nmr": nmr, "ext": ext, "fwd": fwd, "yr": pd.to_datetime(b["timestamp"]).dt.year}).iloc[::H]
            d["coin"] = coin; d["win"] = w
            gr.append(d["fwd"].dropna()); tmp.append(d)
        m = pd.concat(gr).mean()
        for d in tmp:
            d["unus"] = d["fwd"] - m; rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["unus", "nmr", "ext"])
    dn = D[(D["nmr"] < -0.3) & (D["ext"] < 0)].copy()
    dn["eb"] = pd.cut(dn["ext"], [-10, -2, -1.5, -1, -0.5, 0])
    out["downtrend (signed nmr<-0.3): unusual 5d by ext"] = dn.groupby("eb", observed=True)["unus"].apply(s).unstack()
    mod = dn[dn["ext"] > -1].copy()
    mod["nb"] = pd.cut(mod["nmr"], [-1.01, -0.7, -0.5, -0.3])
    out["downtrend moderate slide: unusual by signed nmr"] = mod.groupby("nb", observed=True)["unus"].apply(s).unstack()
    out["downtrend moderate slide by coin"] = mod.groupby("coin")["unus"].apply(s).unstack()
    out["downtrend moderate slide by year"] = mod.groupby("yr")["unus"].apply(s).unstack()
    out["downtrend moderate: raw total fwd5 mean, t"] = s(mod["fwd"])
    return out
