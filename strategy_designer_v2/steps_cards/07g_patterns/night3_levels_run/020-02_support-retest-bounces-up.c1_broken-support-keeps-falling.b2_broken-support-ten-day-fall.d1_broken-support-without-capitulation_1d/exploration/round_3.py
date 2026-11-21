def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    dd = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vv = r1.rolling(20, min_periods=10).std().shift(1)
            z = r1 / vv
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "z": z, "r1": r1,
                              "yr": ts.dt.year, "wd": ts.dt.dayofweek})
            for h in [1, 2, 3, 5]:
                d["f%d" % h] = c.shift(-h) / c - 1
            d["pos"] = np.arange(len(b))
            dd.append(d)
    dd = pd.concat(dd).dropna(subset=["z", "f1"])
    for h in [1, 2, 3, 5]:
        dd["x%d" % h] = dd["f%d" % h] - dd.groupby("coin")["f%d" % h].transform("mean")
    dd["zd"] = pd.qcut(dd["z"], 10, labels=False)

    def tt(s):
        s = s.dropna()
        return pd.Series({"mean": s.mean(), "n": len(s),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    out["next1_excess_by_z_decile"] = dd.groupby("zd")["x1"].apply(tt).unstack()
    for h in [2, 3, 5]:
        g = dd[dd["pos"] % h == 0]
        out["next%d_excess_by_z_decile_nonoverlap" % h] = g.groupby("zd")["x%d" % h].apply(tt).unstack()
    low = dd[dd["zd"] == 0]
    out["d0_next1_by_coin"] = low.groupby("coin")["x1"].apply(tt).unstack()
    out["d0_next1_by_year"] = low.groupby("yr")["x1"].apply(tt).unstack()
    out["d0_next1_share_of_windows_positive"] = float(
        (low.groupby(["coin", "w"])["x1"].mean() > 0).mean())
    out["d0_next1_median"] = float(low["x1"].median())
    out["d0_next1_trim_mean_5pct"] = float(stats.trim_mean(low["x1"], 0.05))
    neg = dd[dd["z"] < 0]
    rho, p = stats.spearmanr(neg["z"], neg["x1"])
    out["down_days_spearman_z_vs_next1"] = pd.Series({"rho": rho, "p": p, "n": len(neg)})
    pc = []
    for coin, d in neg.groupby("coin"):
        r_, p_ = stats.spearmanr(d["z"], d["x1"])
        pc.append(dict(coin=coin, rho=r_, p=p_, n=len(d)))
    out["down_days_spearman_by_coin"] = pd.DataFrame(pc)
    return out
