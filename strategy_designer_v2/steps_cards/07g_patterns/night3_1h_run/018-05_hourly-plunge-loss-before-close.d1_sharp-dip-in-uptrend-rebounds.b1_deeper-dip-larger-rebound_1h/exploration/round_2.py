def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ma = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / ma
            r30 = c / c.shift(720) - 1
            fwd = c.shift(-H) / c - 1
            fc = b["forecast"].astype(float).reset_index(drop=True)
            idx = np.arange(0, len(c), H)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "z": z.iloc[idx].values,
                                      "r30s": (r30 / ma).iloc[idx].values, "fc": fc.iloc[idx].values,
                                      "fwd": fwd.iloc[idx].values, "year": ts.iloc[idx].dt.year.values}))
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["u"] = (g["fwd"] - g["drift"]) / g["sd"]
    g["ur"] = g["fwd"] - g["drift"]
    gg = g.dropna(subset=["z", "r30s"]).copy()
    def tt(s):
        n = len(s); return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    up = gg[gg["r30s"] > 0].copy()
    out = {}
    up["zq"] = pd.qcut(up["z"], 10, labels=False)
    out["up_z_deciles_u"] = up.groupby("zq").apply(lambda x: pd.concat([tt(x["u"]), pd.Series({"z_med": x["z"].median(), "ur_bps": x["ur"].mean() * 1e4, "fc_mean": x["fc"].mean()})]))
    out["up_spearman_negz_u"] = pd.Series({"all_up": stats.spearmanr(-up["z"], up["u"])[0],
                                           "falls_only": stats.spearmanr(-up.loc[up.z < 0, "z"], up.loc[up.z < 0, "u"])[0],
                                           "n_falls": (up.z < 0).sum()})
    dip = up[up["zq"] <= 1]
    out["dip_by_coin"] = dip.groupby("coin")["u"].apply(tt).unstack()
    dip = dip.assign(half=np.where(dip["wn"] <= 12, "w1-12", "w13-24"))
    out["dip_by_half"] = dip.groupby("half")["u"].apply(tt).unstack()
    out["dip_by_year"] = dip.groupby("year")["u"].apply(tt).unstack()
    dip = dip.assign(tq=pd.qcut(dip["r30s"], 3, labels=False))
    out["dip_by_trend_strength"] = dip.groupby("tq").apply(lambda x: pd.concat([tt(x["u"]), pd.Series({"r30s_med": x["r30s"].median()})]))
    out["dip_down_trend_ref"] = tt(gg[(gg.r30s <= 0) & (gg.z < gg.z.quantile(0.15))]["u"])
    # weekday from daily coin returns
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["w"] = w
            x["wd"] = pd.to_datetime(d["day"]).dt.weekday.values
            x["year"] = pd.to_datetime(d["day"]).dt.year.values
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["cu"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["daily_coin_by_weekday_bps"] = D.groupby("wd")["cu"].apply(lambda s: tt(s * 1e4)).unstack()
    fri = D[D.wd == 4]
    out["friday_by_coin_bps"] = fri.groupby("coin")["cu"].apply(lambda s: tt(s * 1e4)).unstack()
    out["friday_by_year_bps"] = fri.groupby("year")["cu"].apply(lambda s: tt(s * 1e4)).unstack()
    # book worst days
    B = D.dropna(subset=["book_return"])
    q = B["book_return"].quantile([0.01, 0.99])
    out["book_tail_days"] = pd.DataFrame({
        "worst1pct": [len(B[B.book_return <= q[0.01]]), B[B.book_return <= q[0.01]]["book_return"].mean() * 1e4, B[B.book_return <= q[0.01]]["coin_return"].mean() * 1e4],
        "best1pct": [len(B[B.book_return >= q[0.99]]), B[B.book_return >= q[0.99]]["book_return"].mean() * 1e4, B[B.book_return >= q[0.99]]["coin_return"].mean() * 1e4]},
        index=["n", "book_bps", "coin_bps"])
    return out
