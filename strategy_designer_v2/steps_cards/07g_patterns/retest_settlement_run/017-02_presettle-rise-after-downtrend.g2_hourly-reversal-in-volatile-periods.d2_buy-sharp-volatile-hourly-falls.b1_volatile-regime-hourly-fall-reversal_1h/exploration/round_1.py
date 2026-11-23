def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourly = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            usual = vol24.rolling(720, min_periods=240).mean()
            z = r1 / usual
            vr = vol24 / usual
            past24 = c / c.shift(24) - 1
            past72 = c / c.shift(72) - 1
            past24z = past24 / (usual * np.sqrt(24))
            fwd24 = c.shift(-24) / c - 1
            fwd1 = c.shift(-1) / c - 1
            volu = b["volume"].astype(float)
            vrel = volu / volu.rolling(168, min_periods=48).median()
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                               "z": z.values, "vr": vr.values, "p24z": past24z.values, "p72": past72.values,
                               "f24": fwd24.values, "f1": fwd1.values, "vrel": vrel.values,
                               "fc": b["forecast"].astype(float).values, "year": ts.dt.year.values})
            df["pos"] = np.arange(len(df))
            hourly.append(df)
    H = pd.concat(hourly, ignore_index=True)
    # coin mean 24h on grid
    G = H[H["pos"] % 24 == 0].dropna(subset=["f24"])
    cm = G.groupby("coin")["f24"].mean()
    H["x24"] = H["f24"] - H["coin"].map(cm)
    # hour of day, 1h forward returns sampled non-overlapping (each bar one hour, h=1 so all bars)
    hh = H.dropna(subset=["f1"]).groupby("hour")["f1"].agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    hh["vol_rel_med"] = H.groupby("hour")["vrel"].median()
    hh["absret"] = H.groupby("hour")["f1"].apply(lambda s: s.abs().mean())
    out["by_hour_1h_fwd"] = hh[["mean", "t", "count", "vol_rel_med", "absret"]]
    # z bins -> next 24h excess, grid sample of signal bars
    Gs = H[(H["pos"] % 24 == 0)].dropna(subset=["x24", "z", "vr"])
    Gs = Gs.assign(zb=pd.cut(Gs["z"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf]),
                   vrh=np.where(Gs["vr"] >= 1, "hi", "lo"))
    g = Gs.groupby(["vrh", "zb"], observed=True)["x24"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["z_by_vol_24h_excess"] = g[["mean", "t", "count"]]
    # vol ratio bins
    Gs["vrb"] = pd.qcut(Gs["vr"], 5)
    g = Gs.groupby("vrb", observed=True)["x24"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["vr_quintile_24h_excess"] = g[["mean", "t", "count"]]
    # past 24h trend z -> next 24h
    Gs2 = Gs.dropna(subset=["p24z"])
    Gs2 = Gs2.assign(pb=pd.qcut(Gs2["p24z"], 5))
    g = Gs2.groupby(["vrh", "pb"], observed=True)["x24"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["past24_trend_by_vol_24h_excess"] = g[["mean", "t", "count"]]
    # weekday
    g = Gs.groupby("wd")["x24"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_24h_excess"] = g[["mean", "t", "count"]]
    # per coin z<-2 high vol
    sub = Gs[(Gs["z"] < -2) & (Gs["vrh"] == "hi")]
    g = sub.groupby("coin")["x24"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["coin_sharpfall_hivol"] = g[["mean", "t", "count"]]
    # book days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["cnext"] = d["coin_return"].shift(-1); d["cprev"] = d["coin_return"].shift(1)
            D.append(d)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    q = D["book_return"].quantile([0.02, 0.98])
    D["bk"] = np.where(D["book_return"] <= q.iloc[0], "worst2%", np.where(D["book_return"] >= q.iloc[1], "best2%", "mid"))
    out["book_extremes"] = D.groupby("bk")[["book_return", "coin_return", "cprev", "cnext"]].mean()
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("year")[["book_return", "coin_return"]].mean()
    return out
