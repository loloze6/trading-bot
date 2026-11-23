def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean%": x.mean()*100, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    L = {3: [], 5: [], 10: []}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            pm = c.shift(1).rolling(20).max()
            exc = c / pm - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            # breakout streak: number of breakout closes in last 5 days
            brk = (c > pm).astype(float)
            streak5 = brk.rolling(5).sum()
            pos = np.arange(len(b))
            for H in L:
                f = pd.DataFrame({"coin": coin, "win": w, "fwd": c.shift(-H)/c - 1, "exc": exc,
                                  "excv": exc / vol20, "r20v": r20 / (vol20*np.sqrt(20)),
                                  "streak5": streak5, "year": ts.dt.year})
                L[H].append(f[pos % H == 0])
    for H, l in L.items():
        d = pd.concat(l, ignore_index=True).dropna(subset=["fwd", "exc"])
        d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        d["exz"] = d["ex"] / d.groupby("coin")["fwd"].transform("std")
        bk = d[d["exc"] > 0]
        out[f"H{H}_brk_noXRP"] = tt(bk[bk["coin"] != "XRPUSD"]["ex"]).round(3)
        out[f"H{H}_brk_strength_exz_mean"] = round(bk["exz"].mean(), 4)
        if H == 5:
            out["H5_brk_by_year"] = bk.groupby("year")["ex"].apply(tt).unstack().round(3)
            out["H5_brk_windows_pos_share"] = round((bk.groupby(["coin", "win"])["ex"].mean() > 0).mean(), 3)
            out["H5_brk_by_win_noncoin"] = bk.groupby("win")["ex"].mean().gt(0).mean().round(3)
            dd = d.dropna(subset=["r20v"])
            dd = dd.assign(q=pd.qcut(dd["r20v"].rank(method="first"), 5, labels=False))
            out["H5_by_r20v_quintile"] = dd.groupby("q")["ex"].apply(tt).unstack().round(3)
            out["H5_spearman_r20v"] = round(stats.spearmanr(dd["r20v"], dd["exz"])[0], 4)
            out["H5_by_streak5"] = d.groupby("streak5")["ex"].apply(tt).unstack().round(3)
    return out
