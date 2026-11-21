def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.copy()
            b["r1"] = b["close"].pct_change()
            allr.append(b["r1"].dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=10).std()
            z = r1 / vol
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (c - b["low"]) / rng
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": z, "clv": clv, "regime": b["regime"],
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "vol": vol,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            for h in [1, 2, 3, 5]:
                d[f"f{h}"] = c.shift(-h) / c - 1 - mu * h
            d["fnext2_after1"] = c.shift(-3) / c.shift(-1) - 1 - 2 * mu
            d["gain"] = d["alloc"] * (c.shift(-1) / c - 1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}

    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # quadrants: z bins x regime, next-day drift-adjusted return
    D["zb"] = pd.cut(D["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    q = D.groupby(["regime", "zb"], observed=True)["f1"].apply(tstat).unstack()
    out["next1_by_regime_zbin"] = q

    # persistence: 2-day after first day, for big moves
    out["days2to3_by_regime_zbin"] = D.groupby(["regime", "zb"], observed=True)["fnext2_after1"].apply(tstat).unstack()

    # within regime falls: clv effect
    fa = D[D["z"] < -1].copy()
    fa["clvb"] = pd.cut(fa["clv"], [0, 0.2, 0.5, 1.0001], include_lowest=True)
    out["falls_z<-1_by_regime_clv"] = fa.groupby(["regime", "clvb"], observed=True)["f1"].apply(tstat).unstack()
    ri = D[D["z"] > 1].copy()
    ri["clvb"] = pd.cut(ri["clv"], [0, 0.5, 0.8, 1.0001], include_lowest=True)
    out["rises_z>1_by_regime_clv"] = ri.groupby(["regime", "clvb"], observed=True)["f1"].apply(tstat).unstack()

    # vol level: tercile of vol per coin, active cases directional
    act = D[D["fc"] != 0].copy()
    act["dir"] = np.sign(act["fc"]) * act["f1"]
    act["volq"] = act.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["active_dir_by_volq"] = act.groupby(["volq"])["dir"].apply(tstat).unstack()
    out["active_dir_by_side_weekday"] = act.groupby([np.sign(act["fc"]), "wd"])["dir"].apply(tstat).unstack()
    out["active_dir_by_side_year"] = act.groupby([np.sign(act["fc"]), "yr"])["dir"].apply(tstat).unstack()
    out["active_dir_by_side_coin"] = act.groupby([np.sign(act["fc"]), "coin"])["dir"].apply(tstat).unstack()
    # horizons for active cases
    hz = {}
    for h in [1, 2, 3, 5]:
        a = act[act["pos"] % h == 0]
        for s in [1, -1]:
            x = (np.sign(a["fc"]) * a[f"f{h}"])[np.sign(a["fc"]) == s]
            hz[(h, s)] = tstat(x)
    out["active_dir_by_horizon_side"] = pd.DataFrame(hz).T
    # all bars weekday drift-adjusted
    out["all_bars_weekday"] = D.groupby("wd")["f1"].apply(tstat).unstack()
    # book's largest gains/losses: what preceded (z, regime)
    g = D.dropna(subset=["gain"])
    g = g[g["alloc"] != 0]
    g["gq"] = pd.qcut(g["gain"], 10, labels=False, duplicates="drop")
    out["gain_decile_profile"] = g.groupby("gq").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                     z=("z", "mean"), absz=("z", lambda s: s.abs().mean()),
                                                     vol=("vol", "mean"), long_share=("alloc", lambda s: (s > 0).mean()))
    return out
