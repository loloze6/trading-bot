def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(df)
            fc = df["forecast"].values.astype(float)
            reg = df["regime"].astype(str).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(0, n, 5):
                r30 = c[t]/c[t-30]-1 if t >= 30 else np.nan
                r60 = c[t]/c[t-60]-1 if t >= 60 else np.nan
                vr = v[t-59:t-29].mean()/max(v[t-29:t+1].mean(),1e-12) if t >= 59 else np.nan
                rec = {"coin": coin, "w": w, "yr": yr[t], "fc": fc[t], "reg": reg[t], "r30": r30, "r60": r60, "vr": vr}
                for h in (5, 10):
                    rec["ret%d" % h] = c[t+h]/c[t]-1 if t+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in (5, 10):
        g["ex%d" % h] = -(g["ret%d" % h] - g.groupby("coin")["ret%d" % h].transform("mean"))
    def st(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    g["grp"] = np.where(g.reg == "unknown", "fall_calm",
                np.where(g.r60 < -0.10, "fall_agit", np.where(g.r60.isna(), "unk", "not_falling")))
    neg = g[g.r30 < 0].copy()
    out["r30neg_by_group_ex5"] = neg.groupby("grp")["ex5"].apply(st).unstack()
    out["r30neg_by_group_ex10"] = neg.groupby("grp")["ex10"].apply(st).unstack()
    neg["z"] = neg.r30
    res = []
    for gname, sub in neg.dropna(subset=["vr", "r30"]).groupby("grp"):
        if len(sub) < 30: continue
        sub = sub.copy()
        sub["prod"] = -sub.r30 * sub.vr
        res.append({"grp": gname, "n": len(sub),
                    "corr_depth_ex5": sub[["r30", "ex5"]].corr().iloc[0, 1] * -1,
                    "corr_vr_ex5": sub[["vr", "ex5"]].corr().iloc[0, 1],
                    "corr_prod_ex5": sub[["prod", "ex5"]].corr().iloc[0, 1],
                    "corr_prod_ex10": sub[["prod", "ex10"]].corr().iloc[0, 1]})
    out["gradients_by_group"] = pd.DataFrame(res)
    fa = neg[(neg.grp == "fall_agit")].dropna(subset=["vr"]).copy()
    fa["vrq"] = pd.qcut(fa.vr.rank(method="first"), 3, labels=["swell", "mid", "thin"])
    out["fall_agit_vol_tercile_ex5"] = fa.groupby("vrq")["ex5"].apply(st).unstack()
    out["fall_agit_by_year_ex5"] = fa.groupby("yr")["ex5"].apply(st).unstack()
    fc_ = g[g.fc < 0].dropna(subset=["vr"]).copy()
    fc_["vrq"] = pd.qcut(fc_.vr.rank(method="first"), 3, labels=["swell", "mid", "thin"])
    out["fall_calm_vol_tercile_ex10"] = fc_.groupby("vrq")["ex10"].apply(st).unstack()
    out["fall_calm_by_year_ex10"] = g[g.fc < 0].groupby("yr")["ex10"].apply(st).unstack()
    return out
