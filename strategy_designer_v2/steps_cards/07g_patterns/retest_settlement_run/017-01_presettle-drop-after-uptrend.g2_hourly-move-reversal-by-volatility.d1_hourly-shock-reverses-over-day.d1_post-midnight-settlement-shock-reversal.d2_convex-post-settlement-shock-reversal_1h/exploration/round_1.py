def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(24, min_periods=20).std()
            z = r1 / vol
            r24 = c.shift(-24) / c - 1
            r4 = c.shift(-4) / c - 1
            # prior 24h return (trend)
            p24 = c / c.shift(24) - 1
            vol720 = r1.rolling(720, min_periods=200).median() if False else r1.abs().rolling(720, min_periods=200).mean()
            volratio = r1.abs().rolling(24, min_periods=20).mean() / vol720
            v = b["volume"].astype(float)
            vrel = v / v.rolling(24 * 7, min_periods=48).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year, "z": z, "r24": r24, "r4": r4, "p24": p24,
                               "vr": volratio, "vrel": vrel, "vol": vol,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "nxt": c.shift(-1) / c - 1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin on 24h grid: approximate with mean r24 over hour-0 rows (one per day, non-overlapping)
    d = A[A.hour == 0].groupby("coin")["r24"].mean()
    A["d"] = A["coin"].map(d)
    A["ex24"] = A["r24"] - A["d"]
    A["fade"] = -np.sign(A["z"]) * A["ex24"]
    A["slope"] = -A["z"] * A["ex24"]
    out = {}
    # by hour: one case per day per hour -> non-overlapping within each hour
    g = A.dropna(subset=["z", "ex24"])
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["fade_by_hour"] = g.groupby("hour")["fade"].apply(tt).unstack()
    out["slope_by_hour"] = g.groupby("hour")["slope"].apply(tt).unstack()
    # size buckets at hour 0 and pooled other hours
    g = g.copy()
    g["zb"] = pd.cut(g["z"].abs(), [0, 0.5, 1, 1.5, 2, 3, 100])
    h0 = g[g.hour == 0]
    out["h0_by_size"] = h0.groupby("zb")["fade"].apply(tt).unstack()
    oth = g[g.hour != 0]
    out["other_hours_by_size"] = oth.groupby("zb")["fade"].apply(tt).unstack()
    # by coin and year, hour 0
    out["h0_by_coin"] = h0.groupby("coin")["fade"].apply(tt).unstack()
    out["h0_by_year"] = h0.groupby("year")["fade"].apply(tt).unstack()
    out["h0_by_weekday"] = h0.groupby("wd")["fade"].apply(tt).unstack()
    h0 = h0.copy()
    h0["vrq"] = pd.qcut(h0["vr"], 4, duplicates="drop")
    out["h0_by_volregime"] = h0.groupby("vrq")["fade"].apply(tt).unstack()
    h0["trend_with"] = np.sign(h0["z"]) == np.sign(h0["p24"] - h0["z"] * 0)
    out["h0_by_move_with_prior24"] = h0.groupby("trend_with")["fade"].apply(tt).unstack()
    # 4h fade at hour 0
    h0["fade4"] = -np.sign(h0["z"]) * h0["r4"]
    out["h0_fade4"] = tt(h0["fade4"])
    # volume by hour
    out["vrel_by_hour"] = A.groupby("hour")["vrel"].median()
    # mean raw hourly return by hour (t)
    out["nxt_by_hour"] = A.dropna(subset=["nxt"]).groupby("hour")["nxt"].apply(tt).unstack()
    return out
