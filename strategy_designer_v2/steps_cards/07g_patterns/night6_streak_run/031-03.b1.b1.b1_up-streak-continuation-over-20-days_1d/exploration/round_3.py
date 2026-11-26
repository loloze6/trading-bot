import pandas as pd, numpy as np

def ct(d, col):
    d = d.dropna(subset=[col])
    n = len(d)
    if n < 5: return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": np.nan, "t": np.nan})
    m = d[col].mean()
    e = (d[col] - m).groupby(d["ts"]).sum()
    se = np.sqrt((e**2).sum()) / n
    return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": m, "t": m/se if se > 0 else np.nan})

def qbin(x, k):
    r = x.rank(method="first")
    if r.notna().sum() < k * 3:
        return pd.Series(np.nan, index=x.index)
    return pd.qcut(r, k, labels=False, duplicates="drop")

def explore(data):
    bars = data["bars"]; out = {}
    drift1 = {}; drift20 = {}
    for c, ws in bars.items():
        a, b = [], []
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl)
            a += [cl[i+1]/cl[i]-1 for i in range(0, n-1)]
            b += [cl[i+20]/cl[i]-1 for i in range(0, n-20, 20)]
        drift1[c] = np.mean(a) if a else np.nan
        drift20[c] = np.mean(b) if b else np.nan
    rows = []; frames = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; r = cl.shift(-1)/cl - 1
            al = df["postRebalance_current_allocation"].fillna(0)
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({"ts": ts, "coin": c, "gain": al*r, "drift": al*drift1[c], "al": al}))
            f = pd.DataFrame({"coin": c, "ts": ts, "pos": np.arange(len(cl))})
            for L in (60, 120):
                f[f"p{L}"] = cl/cl.shift(L) - 1
            f["p20"] = cl/cl.shift(20) - 1
            fw = cl.shift(-20)/cl - 1
            f["u20"] = np.where(f["pos"] % 20 == 0, fw - drift20[c], np.nan)
            f["dd90"] = cl/cl.rolling(90).max() - 1
            f["fc"] = df["forecast"].values
            frames.append(f)
    G = pd.concat(rows, ignore_index=True).dropna()
    dG = G.groupby("ts")[["gain", "drift"]].mean()
    tm = dG["gain"] - dG["drift"]
    out["book: mean daily gain, from drift, timing"] = pd.Series({"gain": dG["gain"].mean(), "from_drift": dG["drift"].mean(),
        "timing": tm.mean(), "timing_t": tm.mean()/(tm.std()/np.sqrt(len(tm))), "mean_alloc": G["al"].mean(), "days": len(dG)})
    T = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): T.append(df.assign(coin=c))
    T = pd.concat(T, ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False).values
    out["trade concentration"] = pd.Series({"n": len(p), "share_positive": (p > 0).mean(),
        "sum_all": p.sum(), "sum_top5pct": p[:max(1, len(p)//20)].sum(), "sum_top10pct": p[:len(p)//10].sum(),
        "mean": p.mean(), "median": np.median(p)})
    A = pd.concat(frames, ignore_index=True)
    for col in ("p60", "p120", "dd90"):
        A["q"] = A.groupby("coin")[col].transform(lambda x: qbin(x, 5))
        out[f"{col} quintile: u20"] = A.groupby("q").apply(lambda d: ct(d, "u20"))
    A["q"] = A.groupby("coin")["p20"].transform(lambda x: qbin(x, 5))
    A["act"] = (A["fc"] > 0).astype(int)
    out["p20 quintile x active: u20"] = A.groupby(["q", "act"]).apply(lambda d: ct(d, "u20"))
    return out
