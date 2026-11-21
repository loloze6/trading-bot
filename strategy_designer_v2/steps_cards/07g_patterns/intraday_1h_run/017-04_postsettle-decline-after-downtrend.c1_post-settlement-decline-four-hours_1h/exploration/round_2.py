def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            r2 = np.full(n, np.nan); r2[:-2] = c[2:]/c[:-2]-1
            r4 = np.full(n, np.nan); r4[:-4] = c[4:]/c[:-4]-1
            r24 = np.full(n, np.nan); r24[:-24] = c[24:]/c[:-24]-1
            p72 = np.full(n, np.nan); p72[72:] = c[72:]/c[:-72]-1
            p24 = np.full(n, np.nan); p24[24:] = c[24:]/c[:-24]-1
            lr = pd.Series(np.log(c)).diff()
            vol24 = lr.rolling(24).std().values
            d = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year.values, "hour": ts.dt.hour.values,
                              "pos": np.arange(n), "r1": r1, "r2": r2, "r4": r4, "r24": r24, "p72": p72,
                              "p24": p24, "vol24": vol24})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(x)})
    # A. 24h reversal after falls: grid 24, deciles, z of p24 by vol
    G = D[D["pos"] % 24 == 0].copy()
    G["z24"] = G["p24"] / (G["vol24"] * np.sqrt(24))
    G["d"] = G.groupby("coin")["p24"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    out["24h fwd by past-24h decile"] = G.groupby("d")["r24"].apply(tt).unstack().round(5)
    low = G[G["d"] <= 1]
    out["bottom-2 deciles 24h fwd by coin"] = low.groupby("coin")["r24"].apply(tt).unstack().round(5)
    out["bottom-2 deciles 24h fwd by year"] = low.groupby("year")["r24"].apply(tt).unstack().round(5)
    sub = G.dropna(subset=["p24", "r24"])
    out["spearman p24 vs r24 by coin"] = sub.groupby("coin").apply(lambda x: pd.Series(stats.spearmanr(x["p24"], x["r24"]), index=["rho", "p"])).round(4)
    # graded within falls: excess r24 regressed on p24 among p24<0
    neg = sub[sub["p24"] < 0]
    out["slope r24 on p24 among falls"] = pd.Series(dict(zip(["slope", "int", "r", "p", "se"], stats.linregress(neg["p24"], neg["r24"])))).round(5)
    # B. hour 20-21 UTC (2h from bar start 20 => close of 19 bar). use r2 at bars starting 20, grid: one per day
    H = D[D["hour"] == 20]
    out["2h ret from 20:00 start by coin"] = H.groupby("coin")["r2"].apply(tt).unstack().round(6)
    out["2h ret from 20:00 start by year"] = H.groupby("year")["r2"].apply(tt).unstack().round(6)
    H = H.copy()
    H["qv"] = H.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["2h ret from 20:00 by vol tercile"] = H.groupby("qv")["r2"].apply(tt).unstack().round(6)
    # C. downtrend: 4h ret by entry close hour (hour+1) among bottom 72h quintile, 4h grid
    D["q72"] = D.groupby("coin")["p72"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    D["chour"] = (D["hour"] + 1) % 24
    S = D[(D["chour"] % 4 == 0) & (D["q72"] == 0)]
    out["bottom 72h quintile: 4h ret by entry close hour"] = S.groupby("chour")["r4"].apply(tt).unstack().round(6)
    S2 = D[(D["chour"] % 4 == 0) & (D["q72"] == 4)]
    out["top 72h quintile: 4h ret by entry close hour"] = S2.groupby("chour")["r4"].apply(tt).unstack().round(6)
    return out
