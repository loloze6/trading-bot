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
            r60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            vpct = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "inprof": (b["regime"] == "unknown").astype(int),
                              "r1z": r1 / sd30, "z3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                              "r60": r60, "vpct": vpct, "yr": ts.dt.year, "day": ts.dt.floor("D")})
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def pooled_t(g, col):
        s = g.groupby("day")[col].sum()
        n = g.groupby("day")[col].size()
        m = g[col].mean()
        # day-pooled t: mean of case deviations, se from day sums
        dev = g[col] - 0
        sday = dev.groupby(g["day"]).sum()
        se = np.sqrt((sday ** 2).sum()) / len(g)
        return m / se if se > 0 else np.nan, sday.size
    # unusual move for each horizon, drift from all grid samples per coin
    res = []
    for h in (1, 2, 3, 5):
        G = D[D.pos % h == 0].copy()
        drift = G.groupby("coin")[f"f{h}"].mean()
        G["u"] = G[f"f{h}"] - G["coin"].map(drift)
        P = G[G.inprof == 1].dropna(subset=["u", "r1z"])
        q = P["r1z"].quantile(0.8)
        top = P[P.r1z >= q]
        t, nd = pooled_t(top, "u")
        rho, p = stats.spearmanr(P["r1z"], P["u"])
        pos = P[P.r1z > 0]
        rho2, p2 = stats.spearmanr(pos["r1z"], pos["u"])
        res.append({"h": h, "n_prof": len(P), "top20_n": len(top), "top20_mean": top["u"].mean(),
                    "top20_t_pooled": t, "days": nd, "rho_all": rho, "p_all": p,
                    "rho_upday": rho2, "p_upday": p2})
    out["oneday_rise_inprof_by_h"] = pd.DataFrame(res).round(4)
    G = D[D.pos % 2 == 0].copy()
    drift = G.groupby("coin")["f2"].mean(); G["u"] = G["f2"] - G["coin"].map(drift)
    P = G[(G.inprof == 1)].dropna(subset=["u", "r1z"])
    P = P[P.r1z > 0].copy()
    P["b"] = pd.qcut(P["r1z"], 4, labels=False)
    g = P.groupby("b")["u"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["f2_by_r1z_updays_inprof"] = g.round(4)
    top = P[P.b == 3]
    out["f2_top_updays_by_coin"] = top.groupby("coin")["u"].agg(["count", "mean"]).round(4)
    out["f2_top_updays_by_year"] = top.groupby("yr")["u"].agg(["count", "mean"]).round(4)
    # same one-day rise in other profiles (computed profile)
    G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G["agit"] = np.where(G.vpct > 0.5, "agit", "calm")
    Q = G.dropna(subset=["u", "r1z", "r60", "vpct"])
    Q = Q[Q.r1z > 0]
    rr = []
    for (tr, ag), g in Q.groupby(["trend", "agit"]):
        if len(g) > 30:
            qq = g["r1z"].quantile(0.75); tp = g[g.r1z >= qq]
            rho, p = stats.spearmanr(g["r1z"], g["u"])
            rr.append({"trend": tr, "agit": ag, "n": len(g), "top_mean": tp["u"].mean(),
                       "top_t": tp["u"].mean() / (tp["u"].std() / np.sqrt(len(tp))), "rho": rho, "p": p})
    out["f2_updays_by_profile"] = pd.DataFrame(rr).round(4)
    return out
