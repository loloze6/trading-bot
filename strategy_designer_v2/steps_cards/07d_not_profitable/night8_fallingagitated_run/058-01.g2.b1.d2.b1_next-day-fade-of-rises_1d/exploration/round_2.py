def explore(data):
    import pandas as pd, numpy as np
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30
            df = pd.DataFrame({"coin": c, "w": w, "z": z, "r": r,
                               "n1": cl.shift(-1) / cl - 1, "n2": cl.shift(-2) / cl - 1,
                               "n3": cl.shift(-3) / cl - 1, "n5": cl.shift(-5) / cl - 1,
                               "alloc": b["postRebalance_current_allocation"].fillna(0),
                               "fc": b["forecast"], "inprof": b["regime"] == "unknown",
                               "hi": b["high"] / cl - 1, "ts": b["timestamp"]})
            df["gain"] = df["alloc"] * df["n1"]
            recs.append(df)
    X = pd.concat(recs)
    mu = X.groupby("coin")["n1"].mean()
    X["drift"] = X["coin"].map(mu)
    P = X[X["inprof"] & (X["r"] > 0)].dropna(subset=["n1", "z"]).copy()
    P["zq"] = pd.qcut(P["z"], 4, labels=False)
    for h in [1, 2, 3, 5]:
        P["u%d" % h] = -(P["n%d" % h] - h * P["drift"])
    def ag(g):
        s = {"n": len(g), "zmin": g["z"].min(), "zmax": g["z"].max()}
        for h in [1, 2, 3, 5]:
            v = g["u%d" % h].dropna()
            s["u%d" % h] = v.mean(); s["t%d" % h] = v.mean() / (v.std() / np.sqrt(len(v)))
        s["share_up_next_gt2sd"] = (g["n1"] > 0.1).mean()
        s["sd_u1"] = g["u1"].std()
        s["alloc"] = g["alloc"].mean(); s["gain_sum"] = g["gain"].sum()
        return pd.Series(s)
    out["by_z_quartile_horizons"] = P.groupby("zq").apply(ag).round(4)
    # standardised forecast vs raw z
    out["corr_fc_z"] = round(P[["fc", "z"]].corr().iloc[0, 1], 3)
    P["fq"] = pd.qcut(P["fc"].rank(method="first"), 4, labels=False)
    out["by_forecast_quartile"] = P.groupby("fq").apply(ag)[["n", "u1", "t1", "u3", "t3", "alloc", "gain_sum"]].round(4)
    # hypothetical sizing: equal short of 1 unit on every profile up day, 1 day and 3 days, minus cost 0.22%
    cost = 0.0022
    for lab, sub in [("all", P), ("q0to2", P[P["zq"] <= 2]), ("q3", P[P["zq"] == 3])]:
        out["equal_short_net_1d_" + lab] = round((-sub["n1"] - cost).mean(), 5)
        out["equal_short_net_3d_" + lab] = round((-sub["n3"].dropna() - cost).mean(), 5)
    # big losing book days: which quartile held them
    L = P.sort_values("gain").head(30)
    out["worst30_case_losses_by_zq"] = L.groupby("zq")["gain"].agg(["count", "sum"]).round(4)
    out["total_case_gain"] = round(P["gain"].sum(), 4)
    # by year, mid quartiles vs top
    P["yr"] = pd.to_datetime(P["ts"]).dt.year
    P["mid"] = np.where(P["zq"] <= 2, "q0-2", "q3")
    out["by_year_mid_vs_top_u1"] = P.groupby(["yr", "mid"])["u1"].agg(["count", "mean"]).unstack().round(4)
    # out-of-profile check of 3-day for comparison
    Q = X[(~X["inprof"]) & (X["r"] > 0)].dropna(subset=["n3", "z"]).copy()
    Q["u3"] = -(Q["n3"] - 3 * Q["drift"])
    out["outside_up_3d_unus_short"] = round(Q["u3"].mean(), 5)
    return out
