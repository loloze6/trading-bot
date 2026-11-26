def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "inprof": (b["regime"] == "unknown").astype(int),
                              "z3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                              "z10": (c / c.shift(10) - 1) / (sd30 * np.sqrt(10)),
                              "r60": c / c.shift(60) - 1,
                              "vrel": sd30 / r1.expanding(min_periods=30).std(),
                              "yr": ts.dt.year, "day": ts.dt.floor("D"),
                              "f5": c.shift(-5) / c - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.pos % 5 == 0].copy()
    drift = G.groupby("coin")["f5"].mean()
    G["u"] = G["f5"] - G["coin"].map(drift)
    G = G.dropna(subset=["u", "z3", "z10"])
    def pt(g):
        sday = g["u"].groupby(g["day"]).sum()
        se = np.sqrt((sday ** 2).sum()) / len(g)
        return g["u"].mean() / se if se > 0 else np.nan, sday.size
    out = {}
    G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G.loc[G.r60.isna(), "trend"] = "na"
    G["agit"] = np.where(G.vrel > 1, "agit", "calm")
    rr = []
    for key, g in list(G.groupby("inprof")) :
        for col in ("z3", "z10"):
            lo = g[g[col] <= g[col].quantile(0.2)]; hi = g[g[col] >= g[col].quantile(0.8)]
            tl, dl = pt(lo); th, dh = pt(hi)
            rho, p = stats.spearmanr(g[col], g["u"])
            rr.append({"inprof": key, "col": col, "n": len(g), "lo_mean": lo.u.mean(), "lo_t": tl, "lo_days": dl,
                       "hi_mean": hi.u.mean(), "hi_t": th, "hi_days": dh, "rho": rho, "p": p})
    out["tails_by_inprof"] = pd.DataFrame(rr).round(4)
    O = G[(G.inprof == 0) & (G.trend != "na")]
    rr = []
    for (tr, ag), g in O.groupby(["trend", "agit"]):
        if len(g) < 40: continue
        lo = g[g.z10 <= g.z10.quantile(0.25)]; hi = g[g.z10 >= g.z10.quantile(0.75)]
        tl, dl = pt(lo); th, dh = pt(hi)
        rho, p = stats.spearmanr(g["z10"], g["u"])
        rr.append({"trend": tr, "agit": ag, "n": len(g), "lo_mean": lo.u.mean(), "lo_t": tl,
                   "hi_mean": hi.u.mean(), "hi_t": th, "rho": rho, "p": p})
    out["outprof_z10_by_profile"] = pd.DataFrame(rr).round(4)
    O2 = G[G.inprof == 0].copy()
    O2["b"] = pd.qcut(O2["z10"], 5, labels=False)
    out["outprof_z10_q_by_year"] = O2[O2.b.isin([0, 4])].groupby(["b", "yr"])["u"].agg(["count", "mean"]).round(4)
    out["outprof_z10_q_by_coin"] = O2[O2.b.isin([0, 4])].groupby(["b", "coin"])["u"].mean().unstack(0).round(4)
    return out
