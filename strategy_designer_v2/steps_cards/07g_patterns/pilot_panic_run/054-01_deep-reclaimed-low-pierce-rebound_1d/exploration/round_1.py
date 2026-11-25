def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            n = len(b)
            if n < 40: continue
            c = b["close"].values; lo = b["low"].values; hi = b["high"].values; op = b["open"].values
            fwd = np.full(n, np.nan)
            fwd[:n-H] = c[H:] / c[:n-H] - 1
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            prevlow = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            prevhigh = pd.Series(hi).shift(1).rolling(30, min_periods=30).max().values
            r5 = np.full(n, np.nan); r5[5:] = c[5:] / c[:-5] - 1
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            rng = (hi - lo) / c
            clv = np.where(hi > lo, (c - lo) / (hi - lo), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "fwd": fwd, "r1": r1, "r5": r5,
                "vol20": vol20, "rng": rng, "clv": clv,
                "pierce": (lo < prevlow), "reclaim": (lo < prevlow) & (c >= prevlow),
                "depth": np.where((lo < prevlow) & (c >= prevlow), (prevlow - lo) / prevlow, 0.0),
                "breakdown": c < prevlow,
                "upbreak_fail": (hi > prevhigh) & (c <= prevhigh),
                "upbreak": c > prevhigh,
                "regime": b["regime"].values, "wd": ts.dt.weekday.values, "year": ts.dt.year.values,
                "alloc": b["postRebalance_current_allocation"].values,
            })
            d["grid"] = (d["pos"] % H == 0)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    drift = D[D.grid].groupby("coin")["fwd"].mean()
    sd = D[D.grid].groupby("coin")["fwd"].std()
    D["un"] = D["fwd"] - D["coin"].map(drift)
    D["str"] = D["un"] / D["coin"].map(sd)
    D["inprof"] = D["regime"].isin(["mean_reversion", "unknown"])
    G = D[D.grid]

    def summ(mask, frame=G):
        x = frame.loc[mask, "un"].dropna()
        if len(x) < 3: return [len(x), np.nan, np.nan]
        return [len(x), x.mean(), x.mean() / (x.std() / np.sqrt(len(x)))]

    out = {}
    cond = {}
    # event-based (all bars, events not on grid necessarily) - use all bars, note overlap
    for nm, m in [("all", D.index == D.index),
                  ("reclaim", D.reclaim), ("reclaim_inprof", D.reclaim & D.inprof),
                  ("reclaim_outprof", D.reclaim & ~D.inprof),
                  ("breakdown_close", D.breakdown), ("breakdown_inprof", D.breakdown & D.inprof),
                  ("upbreak_fail", D.upbreak_fail), ("upbreak_close", D.upbreak),
                  ("inprof_any", D.inprof), ("outprof", ~D.inprof)]:
        cond[nm] = summ(m, D)
    out["events_allbars_un5"] = pd.DataFrame(cond, index=["n", "mean_un", "t"]).T
    # r1 deciles on grid
    G2 = G.dropna(subset=["r1", "vol20"]).copy()
    G2["r1z"] = G2["r1"] / G2["vol20"]
    G2["q"] = pd.qcut(G2["r1z"], 10, labels=False)
    out["un5_by_r1z_decile"] = G2.groupby("q")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G2["q5"] = pd.qcut(G2["r5"], 10, labels=False)
    out["un5_by_r5_decile"] = G2.groupby("q5")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G2["cq"] = pd.qcut(G2["clv"], 5, labels=False)
    out["un5_by_closeloc_quint"] = G2.groupby("cq")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G2["vq"] = pd.qcut(G2["vol20"], 5, labels=False)
    out["un5_by_vol_quint"] = G2.groupby("vq")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["un5_by_weekday"] = G.groupby("wd")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["un5_by_regime"] = G.groupby("regime")["un"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["un5_by_window"] = G.groupby("win")["un"].agg(["count", "mean"])
    # 1-day forward after large moves (all bars, 1-day horizon non-overlapping trivially)
    D["f1"] = D.groupby(["coin", "win"])["r1"].shift(-1)
    D2 = D.dropna(subset=["r1z"] if "r1z" in D else ["r1", "vol20", "f1"]).copy()
    D2["r1z"] = D2["r1"] / D2["vol20"]
    D2["q"] = pd.qcut(D2["r1z"], 10, labels=False)
    out["f1_by_r1z_decile"] = D2.groupby("q")["f1"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # reclaim depth grading, in profile and all
    R = D[D.reclaim].copy()
    if len(R) > 5:
        R["dq"] = pd.qcut(R["depth"].rank(method="first"), 3, labels=False)
        out["reclaim_by_depth_tercile"] = R.groupby("dq")[["depth", "un"]].mean().assign(n=R.groupby("dq").size())
        out["reclaim_by_clv_half"] = R.groupby(R["clv"] > 0.5)["un"].agg(["count", "mean"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    if len(T):
        out["trades"] = T["net_profit_loss_percent"].describe()
    return out
