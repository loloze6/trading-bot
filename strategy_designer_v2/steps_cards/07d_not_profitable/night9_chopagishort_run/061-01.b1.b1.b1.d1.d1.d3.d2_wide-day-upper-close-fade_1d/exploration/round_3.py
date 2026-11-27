def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    allb = []
    for c in bars:
        drifts = []; per = {}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].values
            for h in [2, 5]:
                x = np.full(len(b), np.nan); x[:-h] = cl[h:] / cl[:-h] - 1; b[f"f{h}"] = x
            drifts += list(b["f5"].values[::5][~np.isnan(b["f5"].values[::5])])
            b["loc"] = (b["close"] - b["low"]) / (b["high"] - b["low"])
            b["ret5"] = b["close"].pct_change(5)
            b["ret1"] = b["close"].pct_change()
            b["vol20"] = b["ret1"].rolling(20).std()
            b["vol5"] = b["ret1"].rolling(5).std()
            b["vr"] = b["vol5"] / b["vol20"]
            b["z5"] = b["ret5"] / (b["vol20"] * np.sqrt(5))
            b["inprof"] = b["regime"] != "chop"
            b["g"] = np.arange(len(b)) % 5 == 0
            b["coin"] = c; b["w"] = w
            b["day"] = b["timestamp"].astype(str).str[:10]
            b["pos"] = b["postRebalance_current_allocation"].abs() > 1e-6
            b["bret"] = b["postRebalance_total_value"].pct_change()
            per[w] = b
        drift = np.mean(drifts)
        for w, b in per.items():
            b["drift"] = drift; allb.append(b)
    A = pd.concat(allb).reset_index(drop=True)
    A["um5"] = -(A["f5"] - A["drift"])
    A["s2"] = -A["f2"]
    def tt(s, d):
        ok = s.notna(); s = s[ok]; d = d[ok]
        if len(s) < 4: return pd.Series({"um": s.mean(), "t": np.nan, "n": len(s), "days": d.nunique()})
        m = s.mean(); dev = (s - m).groupby(d.values).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"um": m, "t": m / se, "n": len(s), "days": G})
    P = A[A["inprof"]].dropna(subset=["loc", "ret5", "vol20"]).copy()
    P["sit"] = (P["loc"] >= 0.5) & (P["ret5"] < 0)
    S = P[P["sit"]]
    for col in ["z5", "ret5", "ret1", "vol20", "vr"]:
        q1, q2 = S[col].quantile([1/3, 2/3])
        P["q"] = np.where(P[col] <= q1, "lo", np.where(P[col] <= q2, "mid", "hi"))
        r = {}
        for (sit, q), sub in P.groupby(["sit", "q"]):
            r[f"{'sit' if sit else 'notsit'}_{q}"] = tt(sub["um5"], sub["day"])
        out[f"in-profile 5d short unusual by {col} (sit terciles)"] = pd.DataFrame(r).T
    # z5 terciles: horizon 2 vs 5 on sit
    q1, q2 = S["z5"].quantile([1/3, 2/3])
    S = S.assign(q=np.where(S["z5"] <= q1, "lo", np.where(S["z5"] <= q2, "mid", "hi")))
    out["sit by z5: 2d raw short"] = S.groupby("q").apply(lambda x: tt(x["s2"], x["day"]))
    # notsit with negative ret5 (low close) by z5
    N = P[(P["ret5"] < 0) & (P["loc"] < 0.5)]
    N = N.assign(q=np.where(N["z5"] <= q1, "lo", np.where(N["z5"] <= q2, "mid", "hi")))
    out["ret5<0 low close by z5 (5d short unusual)"] = N.groupby("q").apply(lambda x: tt(x["um5"], x["day"]))
    # book's in-position bar returns by state at entry? use bars in position: mean book bar return by vol20 tercile coin-relative
    A["vrel"] = A.groupby("coin")["vol20"].transform(lambda s: s.rank(pct=True))
    H = A[A["pos"]].copy()
    H["vq"] = pd.qcut(H["vrel"], 3, labels=["lo", "mid", "hi"])
    out["book bar return in position by coin-relative vol20"] = H.groupby("vq", observed=True)["bret"].agg(["mean", "std", "count", "sum"])
    P["vrel"] = A.loc[P.index, "vrel"]
    P["vq"] = pd.cut(P["vrel"], [0, 1/3, 2/3, 1.0], labels=["lo", "mid", "hi"])
    r = {}
    for (sit, q), sub in P.groupby(["sit", "vq"], observed=True):
        r[f"{'sit' if sit else 'notsit'}_{q}"] = tt(sub["um5"], sub["day"])
    out["in-profile by coin-relative vol20"] = pd.DataFrame(r).T
    return out
