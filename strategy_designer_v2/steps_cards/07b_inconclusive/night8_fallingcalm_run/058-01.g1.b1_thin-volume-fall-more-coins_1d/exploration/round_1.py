def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    allgrid = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(df)
            fc = df["forecast"].values.astype(float)
            reg = df["regime"].astype(str).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # 30d return and volume ratio recomputed inside window
            r30 = np.full(n, np.nan); vr = np.full(n, np.nan)
            for t in range(n):
                if t >= 30: r30[t] = c[t]/c[t-30]-1
                if t >= 59: vr[t] = v[t-59:t-29].mean()/max(v[t-29:t+1].mean(),1e-12)
            for t in range(0, n, 5):
                rec = {"coin": coin, "w": w, "t": t, "yr": yr[t], "fc": fc[t], "reg": reg[t],
                       "r30": r30[t], "vr": vr[t]}
                for h in (1, 3, 5, 10, 20):
                    rec["ret%d" % h] = c[t+h]/c[t]-1 if t+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in (1, 3, 5, 10, 20):
        g["m%d" % h] = g.groupby("coin")["ret%d" % h].transform("mean")
        g["ex%d" % h] = -(g["ret%d" % h] - g["m%d" % h])
    cs = g[g.fc < 0].copy()
    def st(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    out["horizons_cases"] = pd.DataFrame({h: st(cs["ex%d" % h]) for h in (1, 3, 5, 10, 20)}).T
    out["by_coin_ex5"] = cs.groupby("coin")["ex5"].apply(st).unstack()
    out["by_year_ex5"] = cs.groupby("yr")["ex5"].apply(st).unstack()
    cs["fq"] = pd.qcut(cs.fc.abs().rank(method="first"), 4, labels=False)
    out["by_absfc_quart"] = cs.groupby("fq").agg(n=("ex5", "size"), ex5=("ex5", "mean"), ex10=("ex10", "mean"), absfc=("fc", lambda x: x.abs().mean()))
    cs2 = cs.dropna(subset=["vr", "r30"])
    cs2["vrq"] = pd.qcut(cs2.vr.rank(method="first"), 3, labels=["swell", "mid", "thin"])
    cs2["dq"] = pd.qcut(cs2.r30.rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["vol_x_depth_ex5"] = cs2.pivot_table(index="dq", columns="vrq", values="ex5", aggfunc="mean")
    out["vol_x_depth_n"] = cs2.pivot_table(index="dq", columns="vrq", values="ex5", aggfunc="size")
    out["vol_tercile_ex5"] = cs2.groupby("vrq")["ex5"].apply(st).unstack()
    out["depth_tercile_ex5"] = cs2.groupby("dq")["ex5"].apply(st).unstack()
    # other profiles: grid bars with r30<0 outside the profile (regime not unknown)
    oth = g[(g.reg != "unknown") & (g.r30 < 0)]
    out["outside_profile_r30neg_ex5"] = st(oth["ex5"])
    out["outside_profile_r30neg_ex10"] = st(oth["ex10"])
    out["corr_r30_ex5_cases"] = float(cs2[["r30", "ex5"]].corr().iloc[0, 1])
    out["corr_vr_ex5_cases"] = float(cs2[["vr", "ex5"]].corr().iloc[0, 1])
    out["regime_counts"] = g.reg.value_counts()
    return out
