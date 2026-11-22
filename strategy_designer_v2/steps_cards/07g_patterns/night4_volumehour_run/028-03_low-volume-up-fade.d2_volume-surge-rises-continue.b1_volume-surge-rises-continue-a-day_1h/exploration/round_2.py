def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": r / sd, "vr": vr, "r": r,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "pos": b["postRebalance_current_allocation"].astype(float)})
            df["f1"] = c.shift(-1) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            df["f6"] = c.shift(-6) / c - 1
            df["pos_idx"] = np.arange(len(df))
            # 2h return across hours 20 and 21: from close of hour 19 bar
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    usual1 = A.groupby("coin")["f1"].agg(["mean", "std"])
    A["s1"] = (A["f1"] - usual1.loc[A["coin"], "mean"].values) / usual1.loc[A["coin"], "std"].values
    # late US session hours 20-21 return, by coin, year, window half
    late = A[A["hour"].isin([20, 21])]
    out["h20-21 strength by coin"] = late.groupby("coin")["s1"].apply(tt).unstack().round(4)
    out["h20-21 strength by year"] = late.groupby("year")["s1"].apply(tt).unstack().round(4)
    late2 = late.copy(); late2["wn"] = late2["w"].str[1:].astype(int)
    late2["wgrp"] = pd.cut(late2["wn"], [0, 6, 12, 18, 24])
    out["h20-21 strength by window group"] = late2.groupby("wgrp")["s1"].apply(tt).unstack().round(4)
    out["h20-21 strength by weekday"] = late.groupby("wd")["s1"].apply(tt).unstack().round(4)
    # graded? by prior 24h return? by vol quintile
    A["sdq"] = A.groupby("coin")["z"].transform(lambda x: 0)
    # raw mean return hour 20-21 in percent
    out["h20-21 raw mean return %"] = late.groupby("coin")["f1"].mean().mul(100).round(4)
    # Asian hours 0-2 negative
    early = A[A["hour"].isin([0, 1, 2])]
    out["h0-2 strength by year"] = early.groupby("year")["s1"].apply(tt).unstack().round(4)
    out["h0-2 strength by coin"] = early.groupby("coin")["s1"].apply(tt).unstack().round(4)
    # high-volume falls -> 2h rebound, graded by vr, on grid of 2
    g = A[(A["pos_idx"] % 2 == 0)].dropna(subset=["z", "vr", "f2"]).copy()
    u2 = A[A["pos_idx"] % 2 == 0].groupby("coin")["f2"].agg(["mean", "std"])
    g["s2"] = (g["f2"] - u2.loc[g["coin"], "mean"].values) / u2.loc[g["coin"], "std"].values
    dn = g[g["z"] < -1.5].copy()
    dn["vq"] = pd.qcut(dn["vr"], 4, labels=False)
    out["falls z<-1.5: 2h strength by vol-ratio quartile"] = dn.groupby("vq")["s2"].apply(tt).unstack().round(3)
    out["falls z<-1.5 vr>3: by year"] = dn[dn["vr"] > 3].groupby("year")["s2"].apply(tt).unstack().round(3)
    # Thursday 24h by year
    g24 = A[A["pos_idx"] % 24 == 0].copy()
    c24 = []
    return out
