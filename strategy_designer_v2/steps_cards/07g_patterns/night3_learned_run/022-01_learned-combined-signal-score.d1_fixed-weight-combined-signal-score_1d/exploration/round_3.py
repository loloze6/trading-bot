def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float))
            n = len(c)
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            past = {k: c.pct_change(k) / (vol * np.sqrt(k)) for k in (2, 3, 5, 7)}
            for off in range(5):
                for i in range(off, n - 5, 5):
                    d = {"coin": coin, "w": w, "off": off, "r5": c[i+5]/c[i]-1,
                         "vol": vol[i], "yr": ts.iloc[i].year}
                    for k in past:
                        v = past[k][i]
                        d[f"z{k}"] = v if np.isfinite(v) else np.nan
                    recs.append(d)
    G = pd.DataFrame(recs)
    stat = G[G.off == 0].groupby("coin")["r5"].agg(["mean", "std"])
    G = G.join(stat, on="coin")
    G["u"] = G["r5"] - G["mean"]
    G["un"] = G["u"] / G["std"]
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    for k in (2, 3, 5, 7):
        G[f"z{k}c"] = G[f"z{k}"].clip(-4, 4)
    out["lookback_t_by_offset"] = pd.DataFrame({f"z{k}": G.groupby("off").apply(lambda g: tt(g[f"z{k}c"]*g["un"])["t"]) for k in (2, 3, 5, 7)})
    A = G[G.off == 0].copy()
    out["z3_by_coin_t_off0"] = A.groupby("coin").apply(lambda g: tt(g["z3c"]*g["un"]))
    out["z3_by_coin_t_alloff_mean"] = G.groupby(["coin", "off"]).apply(lambda g: tt(g["z3c"]*g["un"])["t"]).unstack()
    out["z3_by_year_off0"] = A.groupby("yr").apply(lambda g: tt(g["z3c"]*g["un"]))
    A["vh"] = A.groupby("coin")["vol"].transform(lambda s: s > s.median())
    out["z3_by_vol_half_off0"] = A.groupby("vh").apply(lambda g: tt(g["z3c"]*g["un"]))
    G["zb"] = pd.cut(G["z3"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["z3_buckets_all_off"] = G.groupby("zb").agg(un=("un", "mean"), u=("u", "mean"), n=("u", "count"))
    S = A.dropna(subset=["z3"]); S = S[S.z3.abs() > 1]
    out["size_z3_gt1_off0"] = pd.Series({"unusual": (np.sign(S.z3)*S.u).mean(), "total": (np.sign(S.z3)*S.r5).mean(),
                                         "strength": (np.sign(S.z3)*S.un).mean(), "n": len(S)})
    Sup = S[S.z3 > 1]; Sdn = S[S.z3 < -1]
    out["size_z3_sides"] = pd.DataFrame({"up": [Sup.u.mean(), Sup.un.mean(), len(Sup)],
                                         "down_signed": [-Sdn.u.mean(), -Sdn.un.mean(), len(Sdn)]},
                                        index=["unusual", "strength", "n"])
    return out
