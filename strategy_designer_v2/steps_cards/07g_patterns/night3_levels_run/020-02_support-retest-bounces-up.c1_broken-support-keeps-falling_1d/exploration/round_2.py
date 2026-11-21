def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- weekday effect: per coin, per year, cross-coin averaged per day
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "ts": ts, "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                                      "nxt": (c.shift(-1) / c - 1).values}))
    R = pd.concat(rows).dropna(subset=["nxt"])
    R["nxt_dm"] = R["nxt"] - R.groupby("coin")["nxt"].transform("mean")
    R["wdg"] = np.where(R.wd.isin([3, 4]), "ThuFri", np.where(R.wd.isin([0, 2]), "MonWed", "other"))
    def tt(s):
        return pd.Series({"mean": s.mean(), "n": len(s), "t": s.mean() / s.std() * np.sqrt(len(s))})
    out["wd_per_coin_ThuFri_minus_MonWed"] = R.groupby("coin").apply(
        lambda g: pd.Series({"diff": g[g.wdg == "ThuFri"].nxt_dm.mean() - g[g.wdg == "MonWed"].nxt_dm.mean(),
                             "t": stats.ttest_ind(g[g.wdg == "ThuFri"].nxt_dm, g[g.wdg == "MonWed"].nxt_dm, equal_var=False).statistic})).round(4)
    # cross-coin mean per day (removes shared-move double counting)
    X = R.groupby(["ts", "wd", "yr", "wdg"])["nxt_dm"].mean().reset_index()
    out["wd_daily_avg_coins"] = X.groupby("wd")["nxt_dm"].apply(tt).unstack().round(5)
    out["ThuFri_minus_MonWed_by_year"] = X.groupby("yr").apply(
        lambda g: pd.Series({"diff": g[g.wdg == "ThuFri"].nxt_dm.mean() - g[g.wdg == "MonWed"].nxt_dm.mean(),
                             "n": len(g),
                             "t": stats.ttest_ind(g[g.wdg == "ThuFri"].nxt_dm, g[g.wdg == "MonWed"].nxt_dm, equal_var=False).statistic})).round(4)
    W = R.copy(); W["wnum"] = W.win.str[1:].astype(int)
    W["half"] = np.where(W.wnum <= 12, "w1-w12", "w13-w24")
    XW = W.groupby(["ts", "half", "wdg"])["nxt_dm"].mean().reset_index()
    out["ThuFri_minus_MonWed_by_half"] = XW.groupby("half").apply(
        lambda g: pd.Series({"diff": g[g.wdg == "ThuFri"].nxt_dm.mean() - g[g.wdg == "MonWed"].nxt_dm.mean(),
                             "t": stats.ttest_ind(g[g.wdg == "ThuFri"].nxt_dm, g[g.wdg == "MonWed"].nxt_dm, equal_var=False).statistic})).round(4)
    # ---- 20-day momentum in high volatility, 5-day horizon, non-overlap
    H = 5; cs = []
    for coin, wins in data["bars"].items():
        f5 = []
        for w, b in wins.items():
            c = b["close"].values; idx = np.arange(0, len(c) - H, H); f5 += list(c[idx + H] / c[idx] - 1)
        f5 = np.array(f5); drift = f5.mean(); sd = f5.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"]; r1 = c.pct_change()
            idx = np.arange(0, len(c) - H, H)
            d = pd.DataFrame({"ret20": (c / c.shift(20) - 1).iloc[idx].values,
                              "vol20": r1.rolling(20).std().iloc[idx].values,
                              "fc": b["forecast"].iloc[idx].values,
                              "y": ((c.shift(-H) / c - 1).iloc[idx].values - drift) / sd,
                              "yraw": (c.shift(-H) / c - 1).iloc[idx].values - drift,
                              "coin": coin, "win": w,
                              "wnum": int(w[1:])})
            cs.append(d)
    C = pd.concat(cs).dropna()
    C["vh"] = C.groupby("coin")["vol20"].transform(lambda s: s > s.median())
    C["z20"] = C["ret20"] / (C["vol20"] * np.sqrt(20))
    res = []
    for coin, g in C.groupby("coin"):
        for vh in [False, True]:
            gg = g[g.vh == vh]
            res.append([coin, vh, len(gg), round(stats.spearmanr(gg.z20, gg.y).correlation, 3)])
    out["mom_spearman_by_coin_vol"] = pd.DataFrame(res, columns=["coin", "highvol", "n", "rho"])
    hv = C[C.vh]
    hv = hv.assign(sgn=np.sign(hv.z20))
    hv["signed_y"] = hv.sgn * hv.yraw
    hv["signed_s"] = hv.sgn * hv.y
    out["highvol_mom_signed_move"] = pd.Series({"mean_raw": hv.signed_y.mean(), "strength": hv.signed_s.mean(),
                                                "n": len(hv), "t": hv.signed_y.mean() / hv.signed_y.std() * np.sqrt(len(hv))}).round(5)
    hv["half"] = np.where(hv.wnum <= 12, "w1-w12", "w13-w24")
    out["highvol_mom_by_half"] = hv.groupby("half")["signed_y"].apply(tt).unstack().round(5)
    # ---- forecast quintile per coin
    fcr = []
    for coin, g in C.groupby("coin"):
        fcr.append([coin, len(g), round(stats.spearmanr(g.fc, g.y).correlation, 3),
                    round(g[g.fc < 0].y.mean(), 3), round(g[g.fc == 0].y.mean(), 3)])
    out["fc_by_coin"] = pd.DataFrame(fcr, columns=["coin", "n", "rho", "y_fc_neg", "y_fc_zero"])
    return out
