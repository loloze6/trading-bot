def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            scale = r.abs().rolling(720, min_periods=240).mean().shift(1)
            vbase = v.rolling(720, min_periods=240).mean().shift(1)
            z = r / scale; vr = v / vbase
            vol24 = r.rolling(24).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "vr": vr,
                              "r1": r, "vol24": vol24, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "alloc": b["postRebalance_current_allocation"]})
            for h in (2, 6, 24):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon from non-overlapping grid
    drift = {}
    for h in (1, 2, 6, 24):
        for coin, g in D.groupby("coin"):
            s = g[g["pos"] % h == 0][f"f{h}"].dropna()
            drift[(coin, h)] = s.mean()
    for h in (1, 2, 6, 24):
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(lambda k: drift[(k, h)])

    def ev(mask, h, signed=True, name=None):
        E = D[mask & D[f"x{h}"].notna()].copy()
        E["cell"] = E["pos"] // h
        E = E.groupby(["coin", "w", "cell"]).head(1)
        x = E[f"x{h}"] * (np.sign(E["z"]) if signed else 1)
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    az = D["z"].abs()
    zb = pd.cut(az, [0, 1, 2, 3, 5, 8, 1e9], labels=["<1", "1-2", "2-3", "3-5", "5-8", ">8"])
    vb = pd.cut(D["vr"], [0, 1, 2, 4, 1e9], labels=["v<1", "v1-2", "v2-4", "v>4"])
    for h in (2, 6, 24):
        tab = {}
        for sgn, sm in (("up", D["z"] > 0), ("dn", D["z"] < 0)):
            for zl in ["2-3", "3-5", "5-8", ">8"]:
                for vl in ["v<1", "v1-2", "v2-4", "v>4"]:
                    s = ev(sm & (zb == zl) & (vb == vl), h)
                    tab[(sgn, zl, vl)] = s
        T = pd.DataFrame(tab).T
        T = T[T["n"] >= 20]
        out[f"continuation h{h} (signed, excess)"] = T.round(3)
    # hour of day 1h returns
    H = D.dropna(subset=["x1"]).groupby("hour")["x1"].agg(["mean", "std", "count"])
    H["t"] = H["mean"] / (H["std"] / np.sqrt(H["count"])); H["mean%"] = 100 * H["mean"]
    out["hour of day 1h excess"] = H[["mean%", "t", "count"]].round(4)
    # abs return by hour
    out["mean abs 1h ret by hour %"] = (100 * D.groupby("hour")["r1"].apply(lambda s: s.abs().mean())).round(3)
    # weekday daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    DD = pd.concat(dd, ignore_index=True)
    DD["wd"] = pd.to_datetime(DD["day"]).dt.weekday
    W = DD.dropna(subset=["coin_return"]).groupby("wd")["coin_return"].agg(["mean", "std", "count"])
    W["t"] = W["mean"] / (W["std"] / np.sqrt(W["count"]))
    out["weekday coin daily"] = W.round(5)
    # vol regime: 24h forward by vol24 tercile within coin
    D["volq"] = D.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 3, labels=False))
    vt = {}
    for q in (0, 1, 2):
        vt[q] = ev((D["volq"] == q), 24, signed=False)
    out["24h excess by vol tercile (unsigned)"] = pd.DataFrame(vt).T.round(3)
    # book: long vs flat, gain from market vs timing
    DD["by_year"] = pd.to_datetime(DD["day"]).dt.year
    B = DD.dropna(subset=["book_return"]).groupby("by_year")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book vs coin by year"] = B.round(5)
    out["share bars in position"] = float((D["alloc"].abs() > 1e-6).mean())
    return out
