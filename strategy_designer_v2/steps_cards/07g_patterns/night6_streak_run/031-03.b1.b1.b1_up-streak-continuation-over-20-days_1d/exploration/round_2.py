import pandas as pd, numpy as np

def ct(d, col):
    d = d.dropna(subset=[col])
    n = len(d)
    if n < 5: return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": np.nan, "t": np.nan})
    m = d[col].mean()
    e = (d[col] - m).groupby(d["ts"]).sum()
    se = np.sqrt((e**2).sum()) / n
    return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": m, "t": m/se if se > 0 else np.nan})

def explore(data):
    bars = data["bars"]; out = {}
    drift1 = {}; drift20 = {}
    for c, ws in bars.items():
        a, b = [], []
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl)
            a += [cl[i+1]/cl[i]-1 for i in range(0, n-1)]
            b += [cl[i+20]/cl[i]-1 for i in range(0, n-20, 20)]
        drift1[c] = np.mean(a); drift20[c] = np.mean(b)
    # book decomposition: market rise vs timing, per coin-day from bars
    rows = []
    frames = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; r = cl.shift(-1)/cl - 1
            al = df["postRebalance_current_allocation"].fillna(0)
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({"ts": ts, "coin": c, "gain": al*r, "drift": al*drift1[c], "al": al}))
            f = pd.DataFrame({"coin": c, "ts": ts, "pos": np.arange(len(cl))})
            for L in (60, 120, 180):
                f[f"p{L}"] = cl/cl.shift(L) - 1
            fw = cl.shift(-20)/cl - 1
            f["u20"] = np.where(f["pos"] % 20 == 0, fw - drift20[c], np.nan)
            hi = cl.rolling(180).max()
            f["dd180"] = cl/hi - 1
            frames.append(f)
    G = pd.concat(rows, ignore_index=True).dropna()
    dG = G.groupby("ts")[["gain", "drift"]].mean()
    out["book: mean daily gain, from drift, timing"] = pd.Series({"gain": dG["gain"].mean(), "from_drift": dG["drift"].mean(),
        "timing": (dG["gain"]-dG["drift"]).mean(),
        "timing_t": (dG["gain"]-dG["drift"]).mean()/((dG["gain"]-dG["drift"]).std()/np.sqrt(len(dG))),
        "mean_alloc": G["al"].mean(), "days": len(dG)})
    # trade skew
    T = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): T.append(df.assign(coin=c))
    T = pd.concat(T, ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False).values
    out["trade concentration"] = pd.Series({"n": len(p), "share_positive": (p > 0).mean(),
        "sum_all": p.sum(), "sum_top5pct": p[:max(1, len(p)//20)].sum(), "sum_top10pct": p[:len(p)//10].sum(),
        "mean": p.mean(), "median": np.median(p)})
    # longer trend quintiles
    A = pd.concat(frames, ignore_index=True)
    for L in (60, 120, 180):
        A["q"] = A.groupby("coin")[f"p{L}"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out[f"past{L} quintile: u20"] = A.groupby("q").apply(lambda d: ct(d, "u20"))
    A["q"] = A.groupby("coin")["dd180"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["distance from 180d high quintile: u20"] = A.groupby("q").apply(lambda d: ct(d, "u20"))
    return out
