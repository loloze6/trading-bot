def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            r4 = np.full(n, np.nan); r4[:-4] = c[4:]/c[:-4]-1
            r24 = np.full(n, np.nan); r24[:-24] = c[24:]/c[:-24]-1
            p72 = np.full(n, np.nan); p72[72:] = c[72:]/c[:-72]-1
            p24 = np.full(n, np.nan); p24[24:] = c[24:]/c[:-24]-1
            lr = pd.Series(np.log(c)).diff()
            vol24 = lr.rolling(24).std().values
            v = b["volume"].astype(float)
            vrel = (v / v.rolling(168, min_periods=48).mean()).values
            d = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                              "pos": np.arange(n), "r1": r1, "r4": r4, "r24": r24, "p72": p72, "p24": p24,
                              "vol24": vol24, "vrel": vrel,
                              "alloc": b["postRebalance_current_allocation"].astype(float).values})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # hour of bar close = hour+1 (timestamp is start)
    D["chour"] = (D["hour"] + 1) % 24
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(x)})
    # 1. 1h return by closing hour (1-bar non-overlapping), and volume ratio
    g = D.groupby("hour")
    h1 = g["r1"].apply(tt).unstack()
    h1["vrel"] = g["vrel"].mean()
    out["1h ret next bar by bar-start hour (+vol ratio)"] = h1.round(6)
    # 2. 4h ret from settlement close vs others, by 72h z-quintile (per coin quantiles)
    D["q72"] = D.groupby("coin")["p72"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    D["settle"] = D["chour"].isin([0, 8, 16])
    S = D[D["chour"] % 4 == 0]  # entry at closes 0,4,8,...: 4h grid aligned
    m = S.groupby(["q72", "settle"])["r4"].apply(tt).unstack()
    out["4h ret from close at 4h-grid hours: 72h quintile x settle"] = m.round(6)
    # 3. 24h reversal after large 24h moves (grid every 24 bars)
    G = D[D["pos"] % 24 == 0].copy()
    G["q24"] = G.groupby("coin")["p24"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["24h fwd by past 24h quintile (grid)"] = G.groupby("q24")["r24"].apply(tt).unstack().round(5)
    G["q72"] = G.groupby("coin")["p72"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["24h fwd by past 72h quintile (grid)"] = G.groupby("q72")["r24"].apply(tt).unstack().round(5)
    # 4. vol tercile 4h return (grid 4)
    F = D[D["pos"] % 4 == 0].copy()
    F["qv"] = F.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["4h fwd by 24h vol tercile"] = F.groupby("qv")["r4"].apply(tt).unstack().round(6)
    # 5. weekday 1h
    out["1h ret by weekday"] = D.groupby("wd")["r1"].apply(tt).unstack().round(6)
    # 6. book: gross position gain vs net
    D["gain"] = D["alloc"] * D["r1"]
    act = D[D["alloc"].abs() > 0]
    out["gross gain per active bar"] = tt(act["gain"]).round(7)
    out["gross gain per active bar by coin"] = act.groupby("coin")["gain"].apply(tt).unstack().round(7)
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = pd.Series({"n": len(tr), "gross%": tr["profit_loss_percent"].mean(), "net%": tr["net_profit_loss_percent"].mean(),
                               "dur_min": tr["duration_minutes"].mean(), "short_share": (tr["side"]=="SHORT").mean()}).round(4)
    dy = pd.concat([d for ws in data["days"].values() for d in ws.values()])
    out["book daily"] = tt(dy["book_return"]).round(6)
    return out
