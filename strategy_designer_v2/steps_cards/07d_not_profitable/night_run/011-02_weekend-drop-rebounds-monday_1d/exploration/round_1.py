def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; dayrows = []
    for coin, wins in data["bars"].items():
        # coin mean 2-bar return on grid
        g2 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g2 += list(c[idx + 2] / c[idx] - 1)
        m2 = np.mean(g2)
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            b["wd"] = ts.dt.weekday.values
            b["year"] = ts.dt.year.values
            b["r1"] = b["close"].pct_change()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["f2"] = b["close"].shift(-2) / b["close"] - 1 - m2
            b["z"] = b["r1"] / b["r1"].rolling(20).std()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            v = b["volume"]
            b["wkvol"] = (v + v.shift(1)) / (2 * v.rolling(30).mean())
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","wd","year","r1","nxt","f2","z","ret20","ret5","wkvol","pos","forecast"]])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dayrows.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(dayrows, ignore_index=True)
    # book and holding
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_vs_hold"] = pd.Series({"book_mean": bk.book_return.mean(), "hold_mean": bk.coin_return.mean(),
        "book_sh": bk.book_return.mean()/bk.book_return.std()*np.sqrt(365),
        "hold_sh": bk.coin_return.mean()/bk.coin_return.std()*np.sqrt(365),
        "share_days_exposed": (B.pos.abs() > 0.01).mean()})
    # gain decomposition
    mu = B.groupby("coin")["r1"].mean()
    B["mu"] = B.coin.map(mu)
    B["gain"] = B.pos * B.nxt
    B["mkt"] = B.pos * B.mu
    out["decomp_by_wd_held"] = B[B.pos.abs() > 0.01].groupby("wd").agg(n=("gain","size"), mean_pos=("pos","mean"),
        gain=("gain","mean"), mkt=("mkt","mean"), nxt_mean=("nxt","mean"))
    # Sunday cases, graded by z (all, incl rises)
    S = B[(B.wd == 6)].dropna(subset=["z","f2"]).copy()
    S["zb"] = pd.qcut(S.z, 6, labels=False)
    def agg(df, key):
        r = df.groupby(key)["f2"].agg(["count","mean","std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r
    out["sun_z_sextile_f2"] = agg(S, "zb")
    # weekday drops for comparison (same z sextile cut points per day)
    W = B.dropna(subset=["z","f2"]).copy()
    W["drop"] = pd.cut(W.z, [-99,-1.5,-0.75,0,99], labels=["big","mid","small","rise"])
    r = W.groupby(["wd","drop"])["f2"].mean().unstack()
    out["f2_by_dayclosed_and_z"] = r
    Sd = S[S.z < 0].copy()
    Sd["trend"] = pd.qcut(Sd.ret20, 3, labels=["down","flat","up"])
    Sd["dz"] = pd.qcut(Sd.z, 2, labels=["deep","shallow"])
    out["sun_drops_trend_x_depth"] = Sd.groupby(["trend","dz"])["f2"].agg(["count","mean"]).unstack()
    Sd["vol"] = pd.qcut(Sd.wkvol, 3, labels=["lowvol","mid","highvol"])
    out["sun_drops_wkvol_x_depth"] = Sd.groupby(["vol","dz"])["f2"].agg(["count","mean"]).unstack()
    Sd["r5"] = pd.qcut(Sd.ret5, 3, labels=["r5down","mid","r5up"])
    out["sun_drops_ret5"] = agg(Sd, "r5")
    out["sun_drops_year"] = agg(Sd, "year")
    out["sun_drops_coin"] = agg(Sd, "coin")
    # Monday only vs Tue only
    S2 = S.copy(); S2["mon"] = S2.nxt
    out["sun_drop_mon_vs_tue"] = pd.Series({"mon_ret_after_drop": S[S.z<0].nxt.mean(), "mon_ret_after_rise": S[S.z>=0].nxt.mean(),
        "two_day_after_drop": S[S.z<0].f2.mean(), "two_day_after_rise": S[S.z>=0].f2.mean(), "n_drop": (S.z<0).sum()})
    return out
