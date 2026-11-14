def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for wi, (w, b) in enumerate(wins.items()):
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            d = pd.DataFrame({
                "coin": coin, "w": w, "wn": wi + 1, "i": np.arange(len(b)),
                "r1": r1, "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f10": c.shift(-10) / c - 1,
                "z": r1 / vol20.shift(1),
                "pos20": (c - lo20) / (hi20 - lo20),
                "newhi": c >= hi20,
                "above50": c > c.rolling(50).mean(),
                "clv": (c - l) / (h - l),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "bk": b["postRebalance_total_value"].astype(float).pct_change().shift(-1),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def agg(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan, "hit": (x > 0).mean()})

    out = {}
    D["dn"] = D["z"] < -0.5
    out["dn_f1_by_coin"] = D[D["dn"]].groupby("coin")["f1"].apply(agg).unstack()
    out["dn_f1_by_year"] = D[D["dn"]].groupby("yr")["f1"].apply(agg).unstack()
    out["dn_f1_by_trend"] = D[D["dn"]].groupby("above50")["f1"].apply(agg).unstack()
    out["dn_f1_vs_fc_active"] = D[D["dn"]].groupby(D.loc[D["dn"], "fc"] > 0)["f1"].apply(agg).unstack()
    D3 = D[D["i"] % 3 == 0]
    out["dn_f3_nonov"] = D3.groupby("dn")["f3"].apply(agg).unstack()
    out["clv_f1"] = D.groupby(pd.cut(D["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01]))["f1"].apply(agg).unstack()
    out["dn_clv_f1"] = D[D["dn"]].groupby(pd.cut(D.loc[D["dn"], "clv"], [-0.01, 0.33, 0.66, 1.01]))["f1"].apply(agg).unstack()
    out["thufri_by_coin"] = D[D["wd"].isin([3, 4])].groupby("coin")["f1"].apply(agg).unstack()
    out["thufri_by_year"] = D[D["wd"].isin([3, 4])].groupby("yr")["f1"].apply(agg).unstack()
    out["monwed_by_year"] = D[D["wd"].isin([0, 2])].groupby("yr")["f1"].apply(agg).unstack()
    D10 = D[D["i"] % 10 == 0]
    nh = D10[D10["newhi"]]
    out["newhi_f10_by_coin"] = nh.groupby("coin")["f10"].apply(agg).unstack()
    out["newhi_f10_by_trend"] = nh.groupby("above50")["f10"].apply(agg).unstack()
    out["newhi_f10_by_z"] = nh.groupby(pd.cut(nh["z"], [-99, 1, 2, 99]))["f10"].apply(agg).unstack()
    out["book_day_by_wd"] = D.groupby("wd")["bk"].apply(agg).unstack()
    return out
