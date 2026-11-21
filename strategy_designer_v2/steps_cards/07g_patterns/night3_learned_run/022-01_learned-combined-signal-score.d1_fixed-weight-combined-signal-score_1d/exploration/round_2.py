def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            n = len(c)
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            r3 = c.pct_change(3)
            vol3 = vol*np.sqrt(3)
            ts = pd.to_datetime(b["timestamp"])
            for off in range(5):
                for i in range(off, n-5, 5):
                    recs.append({"coin": coin, "w": w, "off": off, "r5": c[i+5]/c[i]-1,
                                 "z1": r1[i]/vol[i] if vol[i] > 0 else np.nan,
                                 "z3": r3[i]/vol3[i] if vol3[i] > 0 else np.nan,
                                 "vol": vol[i], "yr": ts.iloc[i].year,
                                 "fc": b["forecast"].iloc[i]})
    G = pd.DataFrame(recs)
    g0 = G[G.off == 0]
    stat = g0.groupby("coin")["r5"].agg(["mean", "std"])
    G = G.join(stat, on="coin")
    G["un"] = (G["r5"] - G["mean"]) / G["std"]
    G["u"] = G["r5"] - G["mean"]
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    G["z1c"] = G["z1"].clip(-4, 4)
    G["z3c"] = G["z3"].clip(-4, 4)
    out["z1_prod_by_offset"] = G.groupby("off").apply(lambda g: tt(g["z1c"]*g["un"]))
    out["z3_prod_by_offset"] = G.groupby("off").apply(lambda g: tt(g["z3c"]*g["un"]))
    A = G[G.off == 0].copy()
    out["z1_prod_by_coin"] = A.groupby("coin").apply(lambda g: tt(g["z1c"]*g["un"]))
    out["z1_prod_by_year"] = A.groupby("yr").apply(lambda g: tt(g["z1c"]*g["un"]))
    out["z1_prod_by_window"] = A.groupby("w").apply(lambda g: tt(g["z1c"]*g["un"]))
    # all offsets pooled, buckets (overlap across offsets, descriptive)
    G["zb"] = pd.cut(G["z1"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["z1_buckets_all_offsets"] = G.groupby("zb").agg(un=("un", "mean"), u=("u", "mean"), n=("u", "count"))
    out["z1_buckets_by_coin_off0"] = A.assign(zb=pd.cut(A["z1"], [-np.inf, -1, 1, np.inf])).pivot_table(index="coin", columns="zb", values="u", aggfunc="mean")
    # vol regime: z1 effect in high vs low vol half
    A["vh"] = A.groupby("coin")["vol"].transform(lambda s: s > s.median())
    out["z1_prod_by_vol_half"] = A.groupby("vh").apply(lambda g: tt(g["z1c"]*g["un"]))
    # z1 effect controlling fc: residual of un on fc
    out["corr_z1_fc"] = float(A[["z1", "fc"]].corr().iloc[0, 1])
    # strength of z1 idea as size: cases with |z1|>1, direction sign(z1)
    S = A.dropna(subset=["z1"])
    S = S[S.z1.abs() > 1]
    out["size_z1_gt1"] = pd.Series({"unusual": (np.sign(S.z1)*S.u).mean(), "strength": (np.sign(S.z1)*S.un).mean(), "n": len(S)})
    return out
