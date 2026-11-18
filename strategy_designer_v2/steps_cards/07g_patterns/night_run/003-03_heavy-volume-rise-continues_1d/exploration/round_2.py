import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(n))

def explore(data):
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            z = r / sd
            rv = v / v.rolling(30, min_periods=20).mean()
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            rng = (b["high"] - b["low"]) / c / sd
            r5 = c / c.shift(5) - 1
            fwd = c.shift(-5) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), 5)
            rows.append(pd.DataFrame({"coin": coin, "z": z.iloc[idx].values, "rv": rv.iloc[idx].values,
                "clv": clv.iloc[idx].values, "rng": rng.iloc[idx].values, "r5": r5.iloc[idx].values,
                "fwd": fwd.iloc[idx].values, "pos": b["postRebalance_current_allocation"].iloc[idx].values,
                "yr": ts.iloc[idx].dt.year.values}))
            daily.append(pd.DataFrame({"coin": coin, "r": r.values, "wd": ts.dt.dayofweek.values,
                "yr": ts.dt.year.values, "pos": b["postRebalance_current_allocation"].shift(1).values}))
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    Dd = pd.concat(daily, ignore_index=True).dropna(subset=["r"])
    out = {}
    def agg(df, keys):
        return df.groupby(keys, observed=True)["ex"].agg(mean="mean", n="count", t=_t).round(4)
    # weekday of the day's own return (daily, non-overlapping)
    wd = Dd.groupby("wd")["r"].agg(mean="mean", n="count", t=_t).round(4)
    out["daily return by weekday"] = wd
    Dd["wk"] = Dd["wd"].isin([5, 6])
    out["weekend minus weekday daily by coin"] = Dd.groupby("coin").apply(
        lambda d: pd.Series({"diff": d.loc[d.wk, "r"].mean() - d.loc[~d.wk, "r"].mean(),
                             "t": stats.ttest_ind(d.loc[d.wk, "r"], d.loc[~d.wk, "r"], equal_var=False).statistic})).round(4)
    out["weekend minus weekday daily by year"] = Dd.groupby("yr").apply(
        lambda d: pd.Series({"diff": d.loc[d.wk, "r"].mean() - d.loc[~d.wk, "r"].mean(),
                             "t": stats.ttest_ind(d.loc[d.wk, "r"], d.loc[~d.wk, "r"], equal_var=False).statistic})).round(4)
    # close location quintile
    H = G.dropna(subset=["clv"]).copy()
    H["q"] = pd.qcut(H["clv"], 5, labels=False)
    out["close location quintile"] = agg(H, ["q"])
    out["close location by coin spearman"] = H.groupby("coin").apply(
        lambda d: pd.Series(stats.spearmanr(d["clv"], d["ex"]), index=["rho", "p"])).round(4)
    # range in usual moves
    H = G.dropna(subset=["rng"]).copy(); H["q"] = pd.qcut(H["rng"], 5, labels=False)
    out["range/sd quintile"] = agg(H, ["q"])
    # down days, thin vs heavy: continuous
    H = G.dropna(subset=["z", "rv"])
    dn = H[H.z < -0.3]
    out["down days: spearman rv vs ex, z vs ex"] = pd.Series({
        "rho_rv": stats.spearmanr(dn.rv, dn.ex)[0], "p_rv": stats.spearmanr(dn.rv, dn.ex)[1],
        "rho_z": stats.spearmanr(dn.z, dn.ex)[0], "n": len(dn)}).round(4)
    up = H[H.z > 0.3]
    out["up days: spearman rv vs ex, z vs ex"] = pd.Series({
        "rho_rv": stats.spearmanr(up.rv, up.ex)[0], "p_rv": stats.spearmanr(up.rv, up.ex)[1],
        "rho_z": stats.spearmanr(up.z, up.ex)[0], "p_z": stats.spearmanr(up.z, up.ex)[1], "n": len(up)}).round(4)
    out["all: spearman z vs ex by coin"] = H.groupby("coin").apply(
        lambda d: pd.Series(stats.spearmanr(d["z"], d["ex"]), index=["rho", "p"])).round(4)
    # book: exposure and decomposition
    Dd2 = Dd.dropna(subset=["pos"])
    cm = Dd2.groupby("coin")["r"].transform("mean")
    out["book exposure"] = pd.Series({"mean_pos": Dd2["pos"].mean(), "share_in": (Dd2["pos"].abs() > 0.01).mean(),
        "gain_total": (Dd2["pos"] * Dd2["r"]).mean(), "gain_market": (Dd2["pos"] * cm).mean(),
        "timing": (Dd2["pos"] * (Dd2["r"] - cm)).mean()})
    return out
