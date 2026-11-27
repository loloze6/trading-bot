def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    allret = {}
    for coin, wins in data["bars"].items():
        rr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            for i in range(0, len(b) - H, H):
                rr.append(c[i + H] / c[i] - 1)
        allret[coin] = np.mean(rr) if rr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]; v = b["volume"]
            lr = np.log(c).diff()
            f = pd.DataFrame({
                "ret1": c.pct_change(),
                "ret3": c.pct_change(3),
                "ret5": c.pct_change(5),
                "ret10": c.pct_change(10),
                "ret20": c.pct_change(20),
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "range_rel": ((h - l) / c) / ((h - l) / c).rolling(20).mean(),
                "dist_hi20": c / h.rolling(20).max() - 1,
                "vol10_vs30": lr.rolling(10).std() / lr.rolling(30).std(),
                "vshock": np.log(v / v.rolling(20).mean()),
                "volratio": b.get("debug_info.components.vol_change.last_history_value"),
                "upday_run": (lr > 0).astype(int).rolling(5).sum(),
            })
            f["fwd"] = c.shift(-H) / c - 1 - allret[coin]
            f["inprof"] = (b["regime"] == "unknown").astype(int)
            f["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            f["year"] = pd.to_datetime(b["timestamp"]).dt.year
            f["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            f["coin"] = coin; f["win"] = w
            f["pos"] = b["postRebalance_current_allocation"]
            g = f.iloc[list(range(0, len(b) - H, H))]
            rows.append(g)
    d = pd.concat(rows)
    d = d[d["fwd"].notna()]
    p = d[d["inprof"] == 1]
    out = {"n_grid_all": len(d), "n_grid_prof": len(p), "mean_fwd_prof": p["fwd"].mean(),
           "t_fwd_prof": stats.ttest_1samp(p["fwd"], 0).statistic}
    feats = ["ret1","ret3","ret5","ret10","ret20","clv","range_rel","dist_hi20","vol10_vs30","vshock","volratio","upday_run"]
    res = []
    for ft in feats:
        q = p[[ft, "fwd", "day"]].dropna()
        if len(q) < 50: continue
        x = (q[ft] - q[ft].mean()) / q[ft].std()
        X = np.c_[np.ones(len(q)), x.values]
        beta = np.linalg.lstsq(X, q["fwd"].values, rcond=None)[0]
        e = q["fwd"].values - X @ beta
        # cluster by day
        dfc = pd.DataFrame({"d": q["day"].values, "s0": e, "s1": e * x.values})
        S = dfc.groupby("d")[["s0","s1"]].sum().values
        XtX = np.linalg.inv(X.T @ X)
        V = XtX @ (S.T @ S) @ XtX
        tq = pd.qcut(q[ft], 3, labels=False, duplicates="drop")
        m = q.groupby(tq)["fwd"].mean()
        res.append({"feat": ft, "n": len(q), "slope_per_sd": beta[1], "t_clu": beta[1] / np.sqrt(V[1,1]),
                    "low3": m.iloc[0], "mid3": m.iloc[1] if len(m)>2 else np.nan, "high3": m.iloc[-1]})
    out["feat_slopes_in_profile"] = pd.DataFrame(res)
    out["by_wd_prof"] = p.groupby("wd")["fwd"].agg(["mean","count"])
    out["by_year_prof"] = p.groupby("year")["fwd"].agg(["mean","count"])
    out["by_coin_prof"] = p.groupby("coin")["fwd"].agg(["mean","count"])
    # compare outside profile for same features
    q = d[d["inprof"] == 0]
    res2 = []
    for ft in feats:
        qq = q[[ft,"fwd"]].dropna()
        if len(qq) < 50: continue
        r = stats.pearsonr(qq[ft], qq["fwd"])
        res2.append({"feat": ft, "n": len(qq), "corr": r[0], "p": r[1]})
    out["feat_corr_out_profile"] = pd.DataFrame(res2)
    return out
