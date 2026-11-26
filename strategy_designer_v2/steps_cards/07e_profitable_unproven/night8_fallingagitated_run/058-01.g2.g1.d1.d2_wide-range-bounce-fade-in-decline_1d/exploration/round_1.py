def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # coin mean daily return over all windows
    mu = {}
    for c in bars:
        r = pd.concat([b["close"].pct_change() for b in bars[c].values()])
        mu[c] = r.mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]
            r1 = cl.pct_change()
            d = pd.DataFrame({"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            d["r1"] = r1.values
            d["r3"] = (cl / cl.shift(3) - 1).values
            sd = r1.rolling(30, min_periods=20).std()
            d["sd"] = sd.values
            d["rr"] = (((b["high"] - b["low"]) / cl) / sd).values
            d["z1"] = (r1 / sd).values
            d["z3"] = ((cl / cl.shift(3) - 1) / (sd * np.sqrt(3))).values
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = (cl.shift(-h) / cl - 1).values
            d["regime"] = b["regime"].values
            d["inprof"] = b["regime"].isin(["mean_reversion", "unknown"]).values
            d["alloc"] = b["postRebalance_current_allocation"].values
            d["gain"] = (b["postRebalance_current_allocation"] * (cl.shift(-1) / cl - 1)).values
            d["mkt"] = (b["postRebalance_current_allocation"] * mu[c]).values
            d["mu"] = mu[c]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # book gain by coin / window / year (bar gains)
    out["gain_by_coin"] = D.groupby("coin").agg(gain=("gain", "sum"), mkt=("mkt", "sum"), n_pos=("alloc", lambda x: (x != 0).sum()))
    out["gain_by_window"] = D.groupby("win").agg(gain=("gain", "sum"), mkt=("mkt", "sum"))
    out["gain_by_year"] = D.groupby("year").agg(gain=("gain", "sum"), mkt=("mkt", "sum"))
    out["total_gain_vs_mkt"] = pd.Series({"gain": D["gain"].sum(), "mkt": D["mkt"].sum()})
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": p.sum(), "top5": p.head(5).sum(), "top10": p.head(10).sum(),
                               "win_share": (p > 0).mean(), "short_share": (T["side"] == "SHORT").mean(),
                               "mean_dur_days": T["duration_minutes"].mean() / 1440})
    # cases: active bars, horizons, unusual move short side
    C = D[D.regime == "mean_reversion"].dropna(subset=["rr"])
    def summ(X, col="f1"):
        u = -(X[col] - X["mu"] * int(col[1:]))
        u = u.dropna()
        return pd.Series({"n": len(u), "mean_u": u.mean(), "t": u.mean() / (u.std() / np.sqrt(len(u))) if len(u) > 2 else np.nan})
    out["case_horizons"] = pd.DataFrame({h: summ(C, h) for h in ["f1", "f2", "f3", "f5"]}).T
    C = C.copy()
    C["rr_q"] = pd.qcut(C["rr"], 4, labels=False)
    C["z1_q"] = pd.qcut(C["z1"], 4, labels=False)
    out["by_range_q"] = C.groupby("rr_q").apply(lambda x: summ(x))
    out["by_z1_q"] = C.groupby("z1_q").apply(lambda x: summ(x))
    out["case_by_window"] = C.groupby("win").apply(lambda x: summ(x))
    out["case_by_coin"] = C.groupby("coin").apply(lambda x: summ(x))
    # same situation outside profile
    S = D[(D.r1 > 0) & (D.r3 < 0)].dropna(subset=["rr"])
    out["situation_in_vs_out_profile"] = S.groupby("inprof").apply(lambda x: summ(x))
    # brief's theme: rise over 3 days in profile, graded by z3
    R = D[D.inprof & (D.r3 > 0)].dropna(subset=["z3"]).copy()
    R["z3_q"] = pd.qcut(R["z3"], 4, labels=False)
    out["brief_rise3_in_prof_by_z3q_f1"] = R.groupby("z3_q").apply(lambda x: summ(x, "f1"))
    out["brief_rise3_in_prof_by_z3q_f3"] = R.groupby("z3_q").apply(lambda x: summ(x, "f3"))
    # any up day in profile graded by range
    U = D[D.inprof & (D.r1 > 0)].dropna(subset=["rr"]).copy()
    U["rr_q"] = pd.qcut(U["rr"], 4, labels=False)
    U["dn3"] = U["r3"] < 0
    out["updays_prof_by_rr_q_and_r3neg"] = U.groupby(["dn3", "rr_q"]).apply(lambda x: summ(x))
    # any wide day in profile, by up/down
    P = D[D.inprof].dropna(subset=["rr"]).copy()
    P["rr_q"] = pd.qcut(P["rr"], 4, labels=False)
    P["up"] = P["r1"] > 0
    out["prof_all_days_by_up_rrq"] = P.groupby(["up", "rr_q"]).apply(lambda x: summ(x))
    out["corr_rr_u_cases"] = pd.Series(stats.spearmanr(C["rr"], -(C["f1"] - C["mu"]), nan_policy="omit"))
    return out
