def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            rng = (h - l).replace(0, np.nan)
            cl = (c - l) / rng  # 1 at high
            body = (c - o) / o
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            rngrel = (h - l) / c
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for H in (1, 5):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, n, H)
                d = pd.DataFrame({"coin": coin, "w": w, "H": H, "fwd": fwd.iloc[idx].values,
                                  "vr": vr.iloc[idx].values, "cl": cl.iloc[idx].values,
                                  "body": body.iloc[idx].values, "r1": r1.iloc[idx].values,
                                  "r5p": r5p.iloc[idx].values, "vol20": vol20.iloc[idx].values,
                                  "rngrel": rngrel.iloc[idx].values, "wd": wd.iloc[idx].values,
                                  "fc": b["forecast"].iloc[idx].values})
                rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby(["coin", "H"])["fwd"].transform("mean")
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    D5 = D[D.H == 5].copy(); D1 = D[D.H == 1].copy()
    D5["heavy"] = pd.cut(D5["vr"], [0, 1, 1.5, 2, 3, 100], labels=["<1", "1-1.5", "1.5-2", "2-3", ">3"])
    D5["clq"] = pd.cut(D5["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["low", "q2", "mid", "q4", "high"])
    out["5d_by_volratio"] = D5.groupby("heavy").apply(summ)
    out["5d_by_closeloc"] = D5.groupby("clq").apply(summ)
    hv = D5[D5.vr >= 1.5]
    out["5d_heavy_vr>=1.5_by_closeloc"] = hv.groupby("clq").apply(summ)
    out["5d_heavy_by_dayreturn_sign"] = hv.groupby(np.sign(hv["r1"])).apply(summ)
    D5["r1q"] = pd.qcut(D5["r1"], 5, labels=False)
    out["5d_by_prev1d_return_quint"] = D5.groupby("r1q").apply(summ)
    D5["r5q"] = pd.qcut(D5["r5p"], 5, labels=False)
    out["5d_by_prev5d_return_quint"] = D5.groupby("r5q").apply(summ)
    D5["volq"] = pd.qcut(D5["vol20"], 5, labels=False)
    out["5d_by_vol20_quint"] = D5.groupby("volq").apply(summ)
    D5["rngq"] = pd.qcut(D5["rngrel"], 5, labels=False)
    out["5d_by_dayrange_quint"] = D5.groupby("rngq").apply(summ)
    out["1d_by_weekday"] = D1.groupby("wd").apply(summ)
    D1["r1q"] = pd.qcut(D1["r1"], 5, labels=False)
    out["1d_by_prev1d_return_quint"] = D1.groupby("r1q").apply(summ)
    D1["clq"] = pd.cut(D1["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["low", "q2", "mid", "q4", "high"])
    out["1d_by_closeloc"] = D1.groupby("clq").apply(summ)
    # flat heavy days (the idea's situation) by close location, 5d
    fl = D5[(D5.vr >= 2) & (D5.body.abs() <= 0.01)]
    out["5d_flat_heavy_by_closeloc"] = fl.groupby(pd.cut(fl["cl"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])).apply(summ)
    # book trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
