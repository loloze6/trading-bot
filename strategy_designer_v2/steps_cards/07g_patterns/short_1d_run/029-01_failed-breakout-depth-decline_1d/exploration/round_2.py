def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean%": x.mean()*100, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    recs = {3: [], 5: [], 10: []}
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            pm = c.shift(1).rolling(20).max()
            exc = c / pm - 1
            r1 = c.pct_change()
            vz = (b["volume"] - b["volume"].rolling(20).mean()) / b["volume"].rolling(20).std()
            vol20 = r1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            # new break within next 10 days
            brk = (c > pm)
            newbrk10 = brk[::-1].rolling(10, min_periods=1).max()[::-1].shift(-1)
            daily.append(pd.DataFrame({"coin": coin, "wd": ts.dt.weekday, "r": r1.shift(-1), "year": ts.dt.year}))
            for H in recs:
                pos = np.arange(len(b))
                f = pd.DataFrame({"coin": coin, "win": w, "fwd": c.shift(-H)/c - 1, "exc": exc,
                                  "exc_vol": exc / vol20, "vz": vz, "year": ts.dt.year,
                                  "fail": (b["forecast"].astype(float) < 0).astype(int),
                                  "newbrk10": newbrk10})
                recs[H].append(f[pos % H == 0])
    for H, L in recs.items():
        d = pd.concat(L, ignore_index=True).dropna(subset=["fwd", "exc"])
        d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        bk = d[d["exc"] > 0].copy()
        nb = d[d["exc"] <= 0]
        res = {"breakout": tt(bk["ex"]), "non_breakout": tt(nb["ex"])}
        out[f"H{H}_brk_vs_not"] = pd.DataFrame(res).T.round(3)
        if H == 5:
            bk["q"] = pd.qcut(bk["exc_vol"].rank(method="first"), 3, labels=False)
            out["H5_brk_by_size_tercile(exc/vol)"] = bk.groupby("q")["ex"].apply(tt).unstack().round(3)
            out["H5_brk_spearman_excvol"] = round(stats.spearmanr(bk["exc_vol"], bk["ex"], nan_policy="omit")[0], 4)
            out["H5_brk_by_coin"] = bk.groupby("coin")["ex"].apply(tt).unstack().round(3)
            bk["era"] = np.where(bk["year"] <= 2021, "2018-2021", "2022-2025")
            out["H5_brk_by_era"] = bk.groupby("era")["ex"].apply(tt).unstack().round(3)
            bk["vq"] = pd.qcut(bk["vz"].rank(method="first"), 2, labels=False)
            out["H5_brk_by_volz_half"] = bk.groupby("vq")["ex"].apply(tt).unstack().round(3)
            # 20-day high distance graded among non-breakout days
            nb = nb.copy()
            nb["q"] = pd.qcut(nb["exc"].rank(method="first"), 5, labels=False)
            out["H5_nonbrk_by_dist_quintile"] = nb.groupby("q")["ex"].apply(tt).unstack().round(3)
            out["H5_newbreak10_share_fail_vs_other"] = d.groupby("fail")["newbrk10"].mean().round(3)
    dd = pd.concat(daily, ignore_index=True).dropna(subset=["r"])
    dd["ex"] = dd["r"] - dd.groupby("coin")["r"].transform("mean")
    out["next_day_ex_by_weekday"] = dd.groupby("wd")["ex"].apply(tt).unstack().round(3)
    dd["era"] = np.where(dd["year"] <= 2021, "e1", "e2")
    out["next_day_ex_by_weekday_era"] = dd.groupby(["era", "wd"])["ex"].apply(tt).unstack().round(3)
    return out
