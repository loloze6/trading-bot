def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]
    mu = {}
    for c in bars:
        r = pd.concat([b["close"].pct_change() for b in bars[c].values()])
        mu[c] = r.mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"]; r1 = cl.pct_change()
            d = pd.DataFrame({"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["r1"] = r1.values
            d["r3"] = (cl / cl.shift(3) - 1).values
            d["r60"] = (cl / cl.shift(60) - 1).values
            sd = r1.rolling(30, min_periods=20).std()
            d["sd"] = sd.values
            d["rr"] = (((b["high"] - b["low"]) / cl) / sd).values
            d["clpos"] = ((cl - b["low"]) / (b["high"] - b["low"])).values
            d["f1"] = (cl.shift(-1) / cl - 1).values
            d["f2"] = (cl.shift(-2) / cl - 1).values
            d["regime"] = b["regime"].values
            d["inprof"] = b["regime"].isin(["mean_reversion", "unknown"]).values
            d["alloc"] = b["postRebalance_current_allocation"].values
            d["gain"] = (b["postRebalance_current_allocation"] * (cl.shift(-1) / cl - 1)).values
            d["mu"] = mu[c]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["trend"] = np.where(D.r60 > 0.10, "rising", np.where(D.r60 < -0.10, "falling", "choppy"))
    def summ(X, col="f1"):
        h = int(col[1:])
        X = X.dropna(subset=[col])
        u = -(X[col] - X["mu"] * h)
        g = u.groupby(X["day"]).sum()
        n = len(u)
        t = g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan
        return pd.Series({"n": n, "days": len(g), "mean_u": u.mean(), "t_day": t})
    # book gain without w14 and without top trades
    out["gain_excl_w14"] = pd.Series({"all": D.gain.sum(), "excl_w14": D[D.win != "w14"].gain.sum(),
                                      "w14_share": D[D.win == "w14"].gain.sum() / D.gain.sum()})
    # gain by range quartile of the cases (bar gains)
    C = D[D.regime == "mean_reversion"].dropna(subset=["rr"]).copy()
    C["rr_q"] = pd.qcut(C["rr"], 4, labels=False)
    out["book_gain_by_rr_q"] = C.groupby("rr_q").gain.sum()
    out["top_rrq_by_window"] = C[C.rr_q == 3].groupby("win").apply(summ)
    out["top_rrq_excl_w14"] = summ(C[(C.rr_q == 3) & (C.win != "w14")])
    # situation (up day, r3<0) everywhere, by range quartile, by trend
    S = D[(D.r1 > 0) & (D.r3 < 0)].dropna(subset=["rr"]).copy()
    S["rr_q"] = pd.qcut(S["rr"], 4, labels=False)
    out["situation_all_by_rrq"] = S.groupby("rr_q").apply(summ)
    out["situation_all_by_trend_rrq"] = S.groupby(["trend", "rr_q"]).apply(summ)
    out["situation_out_prof_by_rrq_excl_w14"] = S[(~S.inprof) & (S.win != "w14")].groupby("rr_q").apply(summ)
    # all up days anywhere, wide-range by close position
    U = D[D.r1 > 0].dropna(subset=["rr", "clpos"]).copy()
    U["rr_q"] = pd.qcut(U["rr"], 4, labels=False)
    U["cl_hi"] = U["clpos"] > 0.5
    out["updays_all_rrq_clhi"] = U.groupby(["cl_hi", "rr_q"]).apply(summ)
    out["updays_all_rrq_r3neg"] = U.groupby([U.r3 < 0, "rr_q"]).apply(summ)
    out["situation_top_rrq_by_year"] = S[S.rr_q == 3].groupby("year").apply(summ)
    out["situation_top_rrq_f2"] = S[S.rr_q == 3].groupby("inprof").apply(lambda x: summ(x, "f2"))
    return out
