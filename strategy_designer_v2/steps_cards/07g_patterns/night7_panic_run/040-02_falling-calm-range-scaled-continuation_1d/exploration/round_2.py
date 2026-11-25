def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            rr = ((b["high"] - b["low"]) / b["close"]).astype(float)
            mrr = rr.rolling(30, min_periods=20).mean().values
            r1 = pd.Series(c).pct_change().values
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            tr60 = pd.Series(c).pct_change(60).values
            ts = pd.to_datetime(b["timestamp"])
            reg = b["regime"].values
            pp = b.get("debug_info.components.scaled_fall.post_pipeline_value", pd.Series(np.nan, index=b.index)).astype(float).values
            lh = b.get("debug_info.components.scaled_fall.last_history_value", pd.Series(np.nan, index=b.index)).astype(float).values
            n = len(c); wn = int(w[1:])
            for t in range(0, n, 3):
                if t + 3 >= n: break
                past3 = c[t] / c[t-3] - 1 if t >= 3 else np.nan
                rows.append(dict(coin=coin, w=w, grp="early" if wn <= 12 else "late", fwd=c[t+3]/c[t]-1,
                                 sc=past3/mrr[t] if mrr[t] == mrr[t] else np.nan, pp=pp[t], lh=lh[t],
                                 reg=reg[t], tr=tr60[t], day=ts[t].normalize(),
                                 z=r1[t]/vol30[t] if vol30[t] == vol30[t] else np.nan))
            for t in range(1, n-1):
                daily.append(dict(coin=coin, grp="early" if wn <= 12 else "late", nxt=c[t+1]/c[t]-1,
                                  z=r1[t]/vol30[t] if vol30[t] == vol30[t] else np.nan,
                                  reg=reg[t], tr=tr60[t], day=ts[t].normalize()))
    g = pd.DataFrame(rows)
    g["un"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def clt(df, col="un"):
        s = df.groupby("day")[col].sum(); D = len(s)
        if D < 3: return (np.nan, D)
        m = df[col].mean(); se = np.sqrt((s - df.groupby("day").size()*m).pow(2).sum()*D/(D-1))/len(df)
        return (round(m,4), round(m/se,2), D)
    def summ(df, key):
        a = df.groupby(key)["un"].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    P = g[g["reg"] == "unknown"].dropna(subset=["sc"])
    # slope of unusual fwd on scaled 3-day return, day-clustered approx via sign
    def slope(df, x):
        df = df.dropna(subset=[x])
        xx = df[x] - df[x].mean(); b_ = (xx*df["un"]).sum()/(xx**2).sum()
        e = df["un"] - df["un"].mean() - b_*xx
        s = (xx*e).groupby(df["day"]).sum()
        se = np.sqrt((s**2).sum())/(xx**2).sum()
        return pd.Series(dict(slope=b_, t_cluster=b_/se, n=len(df), days=df["day"].nunique()))
    res = {}
    res["profile, sc"] = slope(P, "sc")
    res["profile, falls only sc"] = slope(P[P.sc < 0], "sc")
    res["profile, rises only sc"] = slope(P[P.sc > 0], "sc")
    res["profile, standardised forecast pp"] = slope(P, "pp")
    res["profile, raw lh"] = slope(P, "lh")
    res["profile early, sc"] = slope(P[P.grp == "early"], "sc")
    res["profile late, sc"] = slope(P[P.grp == "late"], "sc")
    O = g[(g["reg"] != "unknown")].dropna(subset=["sc"])
    res["out of profile, sc"] = slope(O, "sc")
    res["out, falling (tr60<-10%) sc"] = slope(O[O.tr < -0.10], "sc")
    res["out, rising sc"] = slope(O[O.tr > 0.10], "sc")
    res["out, choppy sc"] = slope(O[(O.tr >= -0.10) & (O.tr <= 0.10)], "sc")
    out["slope of unusual fwd3 on scaled 3d return"] = pd.DataFrame(res).T.round(4)
    P = P.assign(sgn=np.where(P.sc < 0, "fall", "rise"))
    out["profile clustered mean by sign"] = pd.DataFrame({k: clt(v) for k, v in P.groupby("sgn")}, index=["mean","t","days"]).T
    out["profile by coin x sign mean"] = P.groupby(["coin","sgn"])["un"].agg(["mean","count"]).unstack().round(4)
    out["profile by grp x sign"] = summ(P, ["grp","sgn"])
    d = pd.DataFrame(daily).dropna(subset=["z"])
    d["un"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["zq"] = pd.qcut(d["z"], 7, labels=False)
    big = d[d.zq == 0]
    out["next-day after biggest z-drops: by grp"] = summ(big, "grp")
    out["next-day after biggest z-drops: by coin"] = summ(big, "coin")
    big = big.assign(tb=np.select([big.tr < -0.1, big.tr > 0.1], ["falling","rising"], "choppy/na"))
    out["next-day after biggest z-drops: by trend"] = summ(big, "tb")
    out["next-day biggest z-drops clustered"] = str(clt(big))
    dn = d[d.z < 0].copy()
    out["next-day slope on z, down days"] = slope(dn, "z").round(4)
    out["next-day slope on z, up days"] = slope(d[d.z > 0], "z").round(4)
    # 3-day after one-day z drop on grid
    gg = g.dropna(subset=["z"])
    gg = gg.assign(zq=pd.qcut(gg.z, 7, labels=False))
    out["fwd3 unusual by today's z septile (grid)"] = summ(gg, "zq")
    return out
