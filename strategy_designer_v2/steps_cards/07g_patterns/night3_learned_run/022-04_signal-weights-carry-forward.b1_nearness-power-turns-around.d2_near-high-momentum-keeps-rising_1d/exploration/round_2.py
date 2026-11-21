def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for H in [1, 3, 5, 10]:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i + H] / c[i] - 1)
            drift = np.mean(allr); usual = np.std(allr)
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values
                r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
                vol20 = pd.Series(r1).shift(1).rolling(20, min_periods=10).std().values
                ts = pd.to_datetime(b["timestamp"])
                nh = b.get("debug_info.components.near_high.post_pipeline_value")
                al = b["postRebalance_current_allocation"].values
                for i in range(0, len(c) - H, H):
                    fr = c[i + H] / c[i] - 1
                    recs.append(dict(coin=coin, w=w, H=H, r1z=r1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                                     nh=nh.iloc[i] if nh is not None else np.nan, yr=ts.iloc[i].year,
                                     wd=ts.iloc[i].dayofweek, ex=fr - drift, exu=(fr - drift) / usual,
                                     wi=int(w[1:]), side=np.sign(al[i])))
    df = pd.DataFrame(recs).dropna(subset=["r1z", "ex"])
    def tq(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean_ex_%": 100 * x.mean(), "str": g["exu"].mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    d = df.copy()
    d["q"] = d.groupby(["coin", "H"])["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["r1z_quint_by_H"] = d.groupby(["H", "q"]).apply(tq)
    d5 = d[d.H == 5].copy()
    out["r1z_top_by_coin"] = d5[d5.q == 4].groupby("coin").apply(tq)
    d5["half"] = np.where(d5.wi <= 12, "early", "late")
    out["r1z_top_minus_rest_by_half"] = d5.assign(top=d5.q == 4).groupby(["half", "top"]).apply(tq)
    res = []
    for H in [1, 3, 5, 10]:
        g = d[d.H == H]
        s = stats.linregress(g["r1z"].clip(-4, 4), g["exu"])
        res.append(dict(H=H, slope=s.slope, t=s.slope / s.stderr, n=len(g)))
        gp = g[g.r1z > 0]
        s = stats.linregress(gp["r1z"].clip(0, 4), gp["exu"])
        res.append(dict(H=-H, slope=s.slope, t=s.slope / s.stderr, n=len(gp)))
    out["r1z_slope_all_and_pos(H<0)"] = pd.DataFrame(res)
    d5["nht"] = d5.groupby("coin")["nh"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["r1z_top_by_nh_tercile"] = d5[d5.q == 4].groupby("nht").apply(tq)
    out["r1z_top_by_side"] = d5[d5.q == 4].groupby("side").apply(tq)
    # weekday on daily returns, all bars
    wdr = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["wd"] = pd.to_datetime(t["day"]).dt.dayofweek
            wdr.append(t[["wd", "coin_return", "book_return"]])
    W = pd.concat(wdr).dropna()
    out["daily_by_weekday"] = W.groupby("wd").agg(n=("coin_return", "size"),
        coin_mean_bp=("coin_return", lambda s: 1e4 * s.mean()),
        coin_t=("coin_return", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))),
        book_mean_bp=("book_return", lambda s: 1e4 * s.mean()))
    # book gain by side of position (daily, before cost approx)
    sg = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values; a = b["postRebalance_current_allocation"].values
            g = a[:-1] * (c[1:] / c[:-1] - 1)
            sg.append(pd.DataFrame({"side": np.sign(a[:-1]), "g": g, "r": c[1:] / c[:-1] - 1}))
    S = pd.concat(sg)
    out["bar_gain_by_side"] = S.groupby("side").agg(n=("g", "size"), gain_bp=("g", lambda s: 1e4 * s.mean()),
        t=("g", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))), coin_ret_bp=("r", lambda s: 1e4 * s.mean()))
    return out
