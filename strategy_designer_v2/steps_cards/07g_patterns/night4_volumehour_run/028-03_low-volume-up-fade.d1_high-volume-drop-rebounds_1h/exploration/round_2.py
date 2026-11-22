def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": r1 / sd, "vr": vr,
                              "ts": ts, "fc": b["forecast"].values, "sd": sd})
            for h in [1, 2, 24]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["ret24z"] = (c / c.shift(24) - 1) / (sd * np.sqrt(24))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["hour"] = D["ts"].dt.hour; D["year"] = D["ts"].dt.year

    def tstat(x):
        x = x.dropna(); n = len(x)
        if n < 3: return pd.Series({"n": n, "mean_bp": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n))})

    D["u1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    late = D[D["hour"].isin([20, 21])]
    out["h1 unusual at 20-21 UTC by coin"] = late.groupby("coin")["u1"].apply(tstat).unstack()
    out["h1 unusual at 20-21 UTC by year"] = late.groupby("year")["u1"].apply(tstat).unstack()
    early = D[D["hour"].isin([0, 1, 2])]
    out["h1 unusual at 0-2 UTC by year"] = early.groupby("year")["u1"].apply(tstat).unstack()
    out["h1 unusual 20-21 UTC by weekday"] = late.groupby(late["ts"].dt.weekday)["u1"].apply(tstat).unstack()
    # graded? 20-21 UTC by intraday return so far (from 00 UTC) sign
    # extreme fall with heavy volume, 2h, grid
    g = D[D["pos"] % 2 == 0].copy()
    g["u2"] = g["f2"] - g.groupby("coin")["f2"].transform("mean")
    ext = g[(g["z"] < -2.5) & (g["vr"] > 4)]
    out["h2 unusual, z<-2.5 vr>4, by coin"] = ext.groupby("coin")["u2"].apply(tstat).unstack()
    out["h2 unusual, z<-2.5 vr>4, by year"] = ext.groupby("year")["u2"].apply(tstat).unstack()
    fall = g[g["z"] < -1.5].copy()
    fall["prod"] = -fall["z"] * fall["vr"]
    fall["pb"] = pd.qcut(fall["prod"], 5, labels=False, duplicates="drop")
    out["h2 unusual on falls by z*vr quintile"] = fall.groupby("pb")["u2"].apply(tstat).unstack()
    # 24h reversal, by coin and year
    g24 = D[D["pos"] % 24 == 0].copy()
    g24["u24"] = g24["f24"] - g24.groupby("coin")["f24"].transform("mean")
    g24["sig"] = -g24["ret24z"] * g24["u24"]  # positive if reversal
    g24["q"] = pd.qcut(g24["ret24z"], 5, labels=False, duplicates="drop")
    out["h24 unusual by 24h z quintile by coin"] = g24.groupby(["coin", "q"])["u24"].apply(tstat).unstack()
    out["corr ret24z vs next 24h unusual by year"] = g24.groupby("year").apply(lambda x: pd.Series({"n": x[["ret24z","u24"]].dropna().shape[0], "corr": x["ret24z"].corr(x["u24"])}))
    tr = pd.concat([df.assign(coin=c) for c in data["trades"] for df in data["trades"][c].values()])
    tr["year"] = pd.to_datetime(tr["entry_time"]).dt.year
    tr["top"] = tr["entry_forecast"] >= 14.81
    out["trade gross by top forecast and year"] = tr.groupby(["year", "top"])["profit_loss_percent"].agg(["count", "mean"]).unstack()
    return out
