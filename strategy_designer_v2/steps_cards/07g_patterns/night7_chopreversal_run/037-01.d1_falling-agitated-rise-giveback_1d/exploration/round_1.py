def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "win": w, "z": z, "r": r, "nx": nxt - drift,
                               "nx2": nxt2 - 2 * drift, "reg": b["regime"].astype(str),
                               "pos": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.dayofweek, "yr": ts.dt.year, "sd": sd,
                               "clv": clv, "pos_idx": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "nx"])
    d["prof"] = np.where(d["reg"] == "chop", "out", "in")
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])

    def agg(g, col="nx"):
        x = g[col].dropna()
        n = len(x)
        m = x.mean()
        t = m / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean%": 100 * m, "t": t})

    out = {}
    out["regime counts"] = d["reg"].value_counts()
    out["next day by z, in/out profile"] = d.groupby(["prof", "zb"]).apply(agg).round(3)
    g2 = d[d["pos_idx"] % 2 == 0]
    out["next 2 days by z, in/out (grid 2)"] = g2.groupby(["prof", "zb"]).apply(lambda g: agg(g, "nx2")).round(3)
    rise = d[(d["z"] > 0) & (d["z"] <= 1)]
    out["ordinary rise next day by coin x prof"] = rise.groupby(["coin", "prof"]).apply(agg).round(3)
    out["ordinary rise next day by year x prof"] = rise.groupby(["yr", "prof"]).apply(agg).round(3)
    out["next day by weekday x prof"] = d.groupby(["prof", "wd"]).apply(agg).round(3)
    d["clvb"] = pd.cut(d["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["next day by close location"] = d.groupby(["prof", "clvb"]).apply(agg).round(3)
    d["sdq"] = d.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["rise in (0,1] next day by vol tercile"] = rise.assign(sdq=d.loc[rise.index, "sdq"] if False else None).pipe(lambda x: x).shape[0]
    rr = d[(d["z"] > 0) & (d["z"] <= 1)]
    out["ordinary rise by vol tercile x prof"] = rr.groupby(["sdq", "prof"]).apply(agg).round(3)
    return out
