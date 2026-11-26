def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b); rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for H in (1, 2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, loc=loc[i], reg=b["regime"].iloc[i],
                                     fwd=c[i+H]/c[i]-1, wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                                     day=ts.iloc[i].normalize()))
    df = pd.DataFrame(rows)
    def pooled(d, key):
        res = []
        for k, g in d.groupby(key):
            s = g.groupby("day")["ex"].sum()
            nd = len(s); m = g["ex"].mean()
            se = np.sqrt((s - g.groupby("day")["ex"].count()*m).pow(2).sum())/len(g)
            res.append(dict(k=k, mean=m, cases=len(g), days=nd, t=m/se if se > 0 else np.nan))
        return pd.DataFrame(res).set_index("k").round(4)
    for H in (1, 2, 5):
        d = df[df.H == H].copy()
        d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        out[f"H{H} weekday pooled"] = pooled(d, "wd")
        d["locb"] = pd.cut(d["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=False)
        out[f"H{H} loc bin pooled (all bars)"] = pooled(d, "locb")
    d = df[df.H == 1].copy()
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["wy"] = d["wd"].astype(str) + "_" + d["yr"].astype(str)
    out["H1 Sun/Thu by year"] = pooled(d[d.wd.isin([3, 6])], "wy")
    d2 = df[df.H == 2].copy()
    d2["ex"] = d2["fwd"] - d2.groupby("coin")["fwd"].transform("mean")
    d2["wy"] = d2["wd"].astype(str) + "_" + d2["yr"].astype(str)
    out["H2 Sun by year"] = pooled(d2[d2.wd == 6], "wy")
    d2["hi"] = (d2["loc"] >= 0.8).astype(int).astype(str) + "_" + d2["yr"].astype(str)
    out["H2 loc>=0.8 vs not by year"] = pooled(d2, "hi")
    return out
