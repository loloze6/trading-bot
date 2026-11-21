import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 26
    rows = []
    coinmean = {}
    coinsd = {}
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                g.append(c[i + H] / c[i] - 1)
        coinmean[coin] = np.mean(g) if g else np.nan
        coinsd[coin] = np.std(g) if g else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            # 52-bar back return for trend context
            for i in range(0, n - H, H):
                if f[i] <= 0:
                    continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "fc": f[i],
                     "ex26": c[i + H] / c[i] - 1 - coinmean[coin],
                     "tot26": c[i + H] / c[i] - 1,
                     "sd": coinsd[coin]}
                for h in (5, 10):
                    r["r%d" % h] = c[i + h] / c[i] - 1
                r["r52"] = c[i + 52] / c[i] - 1 if i + 52 < n else np.nan
                r["past26"] = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    d["wx"] = d["fc"] * d["ex26"]
    d["strength"] = d["ex26"] / d["sd"]
    def summ(g):
        return pd.Series({"n": len(g), "wmean": g["wx"].sum() / g["fc"].sum(),
                          "t_wx": g["wx"].mean() / (g["wx"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_ex": g["ex26"].mean(), "median_ex": g["ex26"].median(),
                          "share_pos": (g["ex26"] > 0).mean(), "mean_str": g["strength"].mean()})
    out = {}
    out["all"] = summ(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_quintile"] = d.groupby("fq").apply(lambda g: pd.concat([summ(g), pd.Series({"fc_mean": g["fc"].mean()})]))
    d["pq"] = pd.qcut(d["past26"].rank(method="first"), 4, labels=False)
    out["by_past26_quartile"] = d.dropna(subset=["past26"]).groupby("pq").apply(summ)
    # trimmed
    lo, hi = d["wx"].quantile([0.02, 0.98])
    dt = d[(d["wx"] > lo) & (d["wx"] < hi)]
    out["trimmed_2pct"] = summ(dt).to_frame().T
    out["big_coins_vs_other"] = d.assign(core=d["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])).groupby("core").apply(summ)
    out["spearman_fc_ex"] = stats.spearmanr(d["fc"], d["ex26"]).correlation
    out["spearman_past26_ex"] = stats.spearmanr(d["past26"], d["ex26"], nan_policy="omit").correlation
    out["mean_tot_r5_r10_r26_r52"] = d[["r5","r10","tot26","r52"]].mean().to_frame("mean")
    return out
