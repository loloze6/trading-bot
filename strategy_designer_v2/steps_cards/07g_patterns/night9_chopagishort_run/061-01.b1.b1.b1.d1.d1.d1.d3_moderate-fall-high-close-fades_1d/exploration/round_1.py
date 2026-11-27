def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            loc = (c - b["low"]) / rng
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r1 = c / c.shift(1) - 1
            vol = r1.rolling(30).std()
            f2 = c.shift(-2) / c - 1
            f5 = c.shift(-5) / c - 1
            inprof = b["regime"].isin(["unknown", "mean_reversion"])
            ts = pd.to_datetime(b["timestamp"])
            for h, f in ((2, f2), (5, f5)):
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "loc": loc.iloc[idx].values,
                                  "r1": r1.iloc[idx].values, "r5": r5.iloc[idx].values,
                                  "r20": r20.iloc[idx].values, "r60": r60.iloc[idx].values,
                                  "vol": vol.iloc[idx].values,
                                  "fwd": f.iloc[idx].values, "inprof": inprof.iloc[idx].values,
                                  "regime": b["regime"].iloc[idx].values,
                                  "wd": ts.iloc[idx].dt.weekday.values,
                                  "yr": ts.iloc[idx].dt.year.values,
                                  "day": ts.iloc[idx].dt.floor("D").values})
                rows.append(d)
    df = pd.concat(rows).dropna(subset=["fwd"])
    # drift per coin and horizon
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["unus"] = df["fwd"] - df["drift"]

    def summ(g):
        n = len(g); m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series({"n": n, "mean_unus": m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan,
                          "mean_tot": g["fwd"].mean()})

    d5 = df[df.h == 5].copy(); d2 = df[df.h == 2].copy()
    for name, d in (("h5", d5), ("h2", d2)):
        d["locb"] = pd.cut(d["loc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
        out[f"{name} loc bins, in profile"] = d[d.inprof].groupby("locb").apply(summ)
        out[f"{name} loc bins, out profile"] = d[~d.inprof].groupby("locb").apply(summ)
    d5["r20b"] = pd.cut(d5["r20"], [-1, -.2, -.1, 0, .1, .2, 10])
    d5["r5neg"] = d5["r5"] < 0
    out["h5 in profile by r20 bin and r5neg"] = d5[d5.inprof].groupby(["r20b", "r5neg"]).apply(summ)
    out["h5 out profile by r20 bin"] = d5[~d5.inprof].groupby("r20b").apply(summ)
    d5["r1z"] = d5["r1"] / d5["vol"]
    d5["r1b"] = pd.qcut(d5["r1z"], 5)
    out["h5 by scaled 1d return quintile, in profile"] = d5[d5.inprof].groupby("r1b").apply(summ)
    out["h5 by scaled 1d return quintile, out profile"] = d5[~d5.inprof].groupby("r1b").apply(summ)
    out["h5 by regime"] = d5.groupby("regime").apply(summ)
    out["h5 in profile by year"] = d5[d5.inprof].groupby("yr").apply(summ)
    out["h5 by weekday all"] = d5.groupby("wd").apply(summ)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    if tr:
        T = pd.concat(tr)
        out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                                   "median_net": T["net_profit_loss_percent"].median(),
                                   "win": (T["net_profit_loss_percent"] > 0).mean(),
                                   "mean_days": T["duration_minutes"].mean() / 1440})
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
