def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        d3 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            d3 += list(c[idx + 3] / c[idx] - 1)
        drift3 = np.mean(d3)
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            vol = r.rolling(20, min_periods=15).std().shift(1)
            f = pd.DataFrame({
                "coin": coin, "win": w, "ts": ts.values, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "z": (r / vol).values,
                "f3": (b["close"].shift(-3) / b["close"] - 1 - drift3).values,
                "volrel": (vol / vol.rolling(60, min_periods=30).mean()).values,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["z", "f3"])
    out = {}

    def clustered(g, col="f3"):
        x = g[col].groupby(g["ts"]).mean().dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"cases": len(g), "dates": n, "mean": np.nan, "t_dates": np.nan})
        return pd.Series({"cases": len(g), "dates": n, "mean": x.mean(), "t_dates": x.mean() / (x.std() / np.sqrt(n))})

    # 1. non-Sunday large falls by volrel tercile, date-clustered
    B = A.dropna(subset=["volrel"]).copy()
    W = B[(B.wd != 6) & (B.z <= -2)].copy()
    W["rq"] = pd.qcut(W["volrel"], 3, labels=["calm", "mid", "turb"])
    out["weekday falls z<=-2 by volrel tercile, clustered"] = W.groupby("rq", observed=True).apply(clustered).round(4)
    W2 = B[(B.wd != 6) & (B.z <= -1.5)].copy()
    W2["rq"] = pd.qcut(W2["volrel"], 3, labels=["calm", "mid", "turb"])
    out["weekday falls z<=-1.5 by volrel tercile, clustered"] = W2.groupby("rq", observed=True).apply(clustered).round(4)
    # by weekday, turbulent half only
    Wt = W2[W2.volrel >= W2.volrel.median()]
    out["weekday falls z<=-1.5 turbulent half by weekday"] = Wt.groupby("wd").apply(clustered).round(4)
    out["weekday falls z<=-1.5 turbulent half by year"] = Wt.groupby("year").apply(clustered).round(4)
    # graded: per-coin slope of f3 on (-z)*volrel among falls (z<0), non-Sunday
    G = B[(B.wd != 6) & (B.z < 0)].copy()
    G["s"] = (-G["z"].clip(-6, 0)) * G["volrel"].clip(0, 4)
    cs = []
    for c, h in G.groupby("coin"):
        if len(h) > 50:
            lr = stats.linregress(h["s"], h["f3"]); cs.append({"coin": c, "slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(h)})
    cs = pd.DataFrame(cs)
    out["per-coin slope f3 on fall x volrel, non-Sunday"] = cs.round(4)
    m = G.groupby("ts")[["s", "f3"]].mean()
    lt = stats.linregress(m["s"], m["f3"])
    out["date-mean slope fall x volrel non-Sunday"] = pd.Series({"slope": lt.slope, "t": lt.slope / lt.stderr, "dates": len(m), "coins_pos": int((cs.slope > 0).sum()), "coins": len(cs)}).round(4)
    # 2. Sunday rises per coin
    S = A[A.wd == 6]
    pr = []
    for c, h in S.groupby("coin"):
        h2 = h[h.z >= 1]
        if len(h2) >= 5:
            pr.append({"coin": c, "mean": h2.f3.mean(), "n": len(h2)})
    pr = pd.DataFrame(pr)
    out["Sun rises z>=1 per coin"] = pr.round(4)
    # 3. Monday mid-bucket clustered
    M = A[(A.z.abs() < 1)]
    out["ordinary days |z|<1 by weekday, clustered"] = M.groupby("wd").apply(clustered).round(4)
    return out
