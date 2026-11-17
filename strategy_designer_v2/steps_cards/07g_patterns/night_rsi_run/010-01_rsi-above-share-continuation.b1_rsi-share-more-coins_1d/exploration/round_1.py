def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    H = 14
    # coin mean 14d return over all windows (non-overlapping grid)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(cl)
            r1 = pd.Series(cl).pct_change()
            vol30 = r1.rolling(30, min_periods=20).std().values
            for i in range(0, n - H, H):
                fwd = cl[i + H] / cl[i] - 1
                d = {"coin": c, "win": w, "fwd": fwd, "fc": df["forecast"].iloc[i],
                     "raw": df.get("debug_info.components.rsi_share.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                     "vol30": vol30[i]}
                for L in (3, 7, 14, 30, 60):
                    d[f"past{L}"] = cl[i] / cl[i - L] - 1 if i >= L else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    res = []
    for col in ["fc", "raw", "past3", "past7", "past14", "past30", "past60", "vol30"]:
        s = g[[col, "ex"]].dropna()
        lr = stats.linregress(s[col], s["ex"])
        res.append({"x": col, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["pooled slopes on 14d excess fwd"] = pd.DataFrame(res)
    # per coin slope for past14, past30, vol30
    pc = []
    for c, s0 in g.groupby("coin"):
        for col in ["fc", "past14", "past30", "vol30"]:
            s = s0[[col, "ex"]].dropna()
            lr = stats.linregress(s[col], s["ex"])
            pc.append({"coin": c, "x": col, "n": len(s), "t": lr.slope / lr.stderr})
    out["per coin t"] = pd.DataFrame(pc).pivot(index="coin", columns="x", values="t")
    # quintiles
    for col in ["fc", "past30", "vol30"]:
        s = g[[col, "ex"]].dropna().copy()
        s["q"] = s.groupby(g.loc[s.index, "coin"])[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out[f"quintile {col}"] = s.groupby("q")["ex"].agg(["count", "mean", "std"])
    # daily: next day return after large moves, by weekday
    dd = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            r = df["close"].pct_change()
            z = r / r.rolling(30, min_periods=20).std().shift(1)
            dd.append(pd.DataFrame({"coin": c, "r": r, "z": z, "nxt": r.shift(-1),
                                    "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                                    "pos": df["postRebalance_current_allocation"],
                                    "yr": pd.to_datetime(df["timestamp"]).dt.year}))
    D = pd.concat(dd)
    D["nxt_ex"] = D["nxt"] - D.groupby("coin")["r"].transform("mean")
    D["zb"] = pd.cut(D["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["next day excess by today z"] = D.groupby("zb")["nxt_ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    D["r_ex"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    out["weekday excess return"] = D.groupby("wd")["r_ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # book decomposition
    D["gain"] = D["pos"] * D["nxt"]
    mu = D.groupby("coin")["nxt"].transform("mean")
    out["book gain split"] = pd.Series({"mean gain": D["gain"].mean(), "market part": (D["pos"]*mu).mean(),
                                        "mean pos": D["pos"].mean(), "share long": (D["pos"] > 0).mean()})
    out["gain by year"] = D.groupby("yr").agg(gain=("gain", "mean"), pos=("pos", "mean"), coin=("nxt", "mean"))
    return out
