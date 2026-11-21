def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            a = b["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            r1 = c.shift(-1) / c - 1
            pos.append(pd.DataFrame({"coin": coin, "a": a, "r1": r1}))
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / mabs
            hi = c.rolling(720, min_periods=120).max()
            dd = c / hi - 1
            ddz = dd / mabs
            for h in (24, 72, 120):
                idx = np.arange(0, len(c) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.iloc[idx].values,
                    "dd": dd.iloc[idx].values, "ddz": ddz.iloc[idx].values, "fwd": fwd.values}))
    p = pd.concat(pos).dropna()
    p["mu"] = p.groupby("coin")["r1"].transform("mean")
    out["book_gain_bps_per_bar"] = pd.Series({
        "mean_alloc": p["a"].mean(), "share_short": (p["a"] < 0).mean(),
        "total": 1e4 * (p["a"] * p["r1"]).mean(),
        "drift_part": 1e4 * (p["a"] * p["mu"]).mean(),
        "timing_part": 1e4 * (p["a"] * (p["r1"] - p["mu"])).mean()})
    df = pd.concat(rows).dropna(subset=["fwd"])
    g = df.groupby(["coin", "h"])["fwd"]
    df["ex"] = df["fwd"] - g.transform("mean"); df["st"] = df["ex"] / g.transform("std")
    d = df.dropna(subset=["z", "dd"])
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex_pct": 100*x["ex"].mean(), "mean_tot_pct": 100*x["fwd"].mean(),
                          "strength": x["st"].mean(), "t": stats.ttest_1samp(x["st"], 0).statistic if len(x) > 2 else np.nan})
    d["ddb"] = pd.qcut(d["ddz"], 6)
    out["by_ddz_sextile_h"] = d.groupby(["h", "ddb"]).apply(summ).reset_index()
    deep = d[d["dd"] <= -0.3].copy()
    deep["zb"] = pd.cut(deep["z"], [-99, -2, -1, 0, 1, 99])
    out["deep_by_z"] = deep.groupby(["h", "zb"]).apply(summ).reset_index()
    out["deep_z_le_-1_by_coin_h72"] = deep[(deep.z <= -1) & (deep.h == 72)].groupby("coin").apply(summ)
    out["spearman_ddz_st"] = d.groupby("h").apply(lambda x: stats.spearmanr(-x["ddz"], x["st"]).correlation)
    return out
