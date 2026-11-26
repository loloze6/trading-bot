import numpy as np, pandas as pd

def ct(v, d):
    v = np.asarray(v, float); m = ~np.isnan(v); v = v[m]; d = np.asarray(d)[m]
    n = len(v)
    if n < 5: return (np.nan, np.nan, n, 0)
    mu = v.mean()
    s = pd.Series(v - mu).groupby(d).sum()
    se = np.sqrt((s**2).sum()) / n
    return (mu, mu/se if se > 0 else np.nan, n, len(s))

def row(s, col, **kw):
    mu, t, n, nd = ct(s[col], s["day"])
    d = dict(mean=mu, t=t, n=n, days=nd); d.update(kw); return d

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc": b["forecast"].astype(float),
                "r20": c/c.shift(20)-1, "r1": r1,
                "vol20": r1.rolling(20).std(), "vol60": r1.rolling(60).std(),
                "f10": c.shift(-10)/c-1, "f20": c.shift(-20)/c-1})
            df["pos"] = np.arange(len(df))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    vmed = D.groupby("coin")["vol20"].median()
    sd20 = D.groupby("coin")["r20"].std()
    out = {}
    for h in (10, 20):
        G = D[(D["pos"] % h == 0) & D[f"f{h}"].notna()].copy()
        st = G.groupby("coin")[f"f{h}"].mean()
        G["ex"] = G[f"f{h}"] - G["coin"].map(st)
        G["vrel"] = G["vol20"] / G["coin"].map(vmed)
        G["vr2060"] = G["vol20"] / G["vol60"]
        G["z20"] = G["r20"] / G["coin"].map(sd20)
        G["dirx"] = G["ex"] * np.sign(G["r20"])
        G["year"] = G["day"].dt.year
        g = G.dropna(subset=["vrel", "dirx", "z20"]).copy()
        g["vq"] = pd.qcut(g["vrel"], 5, labels=False)
        out[f"h{h} dir ex by vol quintile"] = pd.DataFrame([row(s, "dirx", vq=k, vmid=s.vrel.median()) for k, s in g.groupby("vq")])
        if h == 10:
            g["vt"] = pd.qcut(g["vrel"], 3, labels=["low", "mid", "high"])
            g["side"] = np.sign(g["z20"])
            out["h10 dir ex by vol tercile x side"] = pd.DataFrame([row(s, "dirx", vt=a, side=b2) for (a, b2), s in g.groupby(["vt", "side"])])
            hi = g[g.vt == "high"].copy()
            hi["zq"] = pd.qcut(hi["z20"].abs(), 3, labels=False)
            out["h10 high-vol dir ex by |z20| tercile"] = pd.DataFrame([row(s, "dirx", zq=k, zmid=s.z20.abs().median()) for k, s in hi.groupby("zq")])
            hi["era"] = np.where(hi["year"] <= 2021, "<=2021", ">=2022")
            out["h10 high-vol dir ex by era"] = pd.DataFrame([row(s, "dirx", era=k) for k, s in hi.groupby("era")])
            out["h10 high-vol dir ex by coin"] = pd.DataFrame([row(s, "dirx", coin=k) for k, s in hi.groupby("coin")])
            # graded product: dirx scaled by vol rank, regression of ex on z20*vrel
            g["prod"] = g["z20"] * g["vrel"]
            out["h10 ex*sign by prod quintile"] = pd.DataFrame([row(s, "ex", pq=k, pmid=s["prod"].median()) for k, s in g.assign(pq=pd.qcut(g["prod"], 5, labels=False)).groupby("pq")])
            g["vrq"] = pd.qcut(g["vr2060"], 3, labels=["falling vol", "flat", "rising vol"])
            out["h10 dir ex by vol20/vol60 tercile"] = pd.DataFrame([row(s, "dirx", vr=k) for k, s in g.groupby("vrq")])
    return out
