def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; 
            b["nxt"] = c.shift(-1)/c - 1
            b["dayret"] = c/c.shift(1) - 1
            b["ret20"] = c/c.shift(20) - 1
            rng = (b["high"]-b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"])/rng
            v = b["volume"]
            b["vr"] = v/ v.shift(1).rolling(20).mean() - 1
            b["absret"] = b["dayret"].abs()
            b["vol20"] = b["dayret"].rolling(20).std()
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"]*b["nxt"]
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B = B.dropna(subset=["nxt"])
    drift = B.groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(drift)
    B["sig"] = B["forecast"] > 0
    def summ(g):
        return pd.Series({"n": len(g), "mean_nxt%": g["nxt"].mean()*100,
                          "mean_ex%": g["ex"].mean()*100,
                          "t_ex": g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                          "mean_gain%": g["gain"].mean()*100})
    # close location, day return sign, trend, by signal
    B["clv_bin"] = pd.cut(B["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["low","mid","high"])
    B["day_up"] = np.where(B["dayret"] > 0, "up", "down")
    B["trend"] = np.where(B["ret20"] > 0, "tr_up", "tr_down")
    out["by_sig_clv"] = B.groupby(["sig","clv_bin"]).apply(summ)
    out["by_sig_dayup"] = B.groupby(["sig","day_up"]).apply(summ)
    out["by_sig_trend"] = B.groupby(["sig","trend"]).apply(summ)
    B["abs_q"] = pd.qcut(B["absret"], 3, labels=["small","medium","big"])
    out["by_sig_absmove"] = B.groupby(["sig","abs_q"]).apply(summ)
    S = B[B["sig"]].copy()
    S["fq"] = pd.qcut(S["forecast"], 4, labels=False, duplicates="drop")
    out["sig_by_forecast_q"] = S.groupby("fq").apply(summ)
    out["sig_by_dayup_clv"] = S.groupby(["day_up","clv_bin"]).apply(summ)
    # book daily
    drows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["wn"] = int(str(w).lstrip("w")); d["i"] = np.arange(len(d))
            drows.append(d)
    D = pd.concat(drows, ignore_index=True)
    bk = D.groupby(["wn","i"])[["book_return","coin_return"]].mean().dropna().sort_index()
    v = (1+bk["book_return"]).cumprod()
    dd = v/v.cummax()-1
    out["maxdd_book"] = float(dd.min())
    vh = (1+bk["coin_return"]).cumprod(); out["maxdd_hold"] = float((vh/vh.cummax()-1).min())
    # deepest fall location: window(s)
    trough = dd.idxmin()
    peak = v.loc[:trough].idxmax()
    out["deepest_fall_from_to_window"] = f"{peak} -> {trough}"
    seg = bk.loc[peak:trough]
    out["fall_book_vs_coin"] = pd.Series({"days": len(seg), "book_cum%": ((1+seg.book_return).prod()-1)*100,
                                          "coin_cum%": ((1+seg.coin_return).prod()-1)*100})
    out["book_by_window"] = bk.groupby(level=0).apply(lambda g: pd.Series({"book%": ((1+g.book_return).prod()-1)*100, "coin%": ((1+g.coin_return).prod()-1)*100, "dd%": (((1+g.book_return).cumprod()/(1+g.book_return).cumprod().cummax())-1).min()*100}))
    out["gain_by_year_sig"] = S.groupby("year").apply(summ)
    out["sig_by_trend_dayup"] = S.groupby(["trend","day_up"]).apply(summ)
    return out
