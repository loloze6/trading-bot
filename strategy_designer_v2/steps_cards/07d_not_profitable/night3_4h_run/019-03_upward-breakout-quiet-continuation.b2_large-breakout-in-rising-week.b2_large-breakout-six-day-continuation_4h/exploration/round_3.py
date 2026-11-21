def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    bad = {"w1", "w2", "w3", "w5", "w9"}
    recs = []; cases = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng180 = (hi - lo).rolling(180, min_periods=45).mean()
            r360 = cl / cl.shift(360) - 1
            r90 = cl / cl.shift(90) - 1
            lr = np.log(cl).diff()
            vol42 = lr.rolling(42).std()
            vol360 = lr.rolling(360, min_periods=120).std()
            vrel = vol42 / vol360
            vol_lvl = lr.rolling(180, min_periods=45).std()
            downdays = (lr.rolling(180, min_periods=45).apply(lambda x: (x < 0).mean(), raw=True))
            brk = (cl - hi.shift(1).rolling(12).max()) / rng180
            r42 = cl / cl.shift(42) - 1
            sig = (brk > 0) & (r42 > 0)
            fwd = cl.shift(-36) / cl - 1
            nxt = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            f = pd.DataFrame({"r360": r360, "r90": r90, "vrel": vrel, "vol": vol_lvl, "dn": downdays,
                              "a": a, "g": a * nxt, "brk": brk, "sig": sig, "fwd": fwd})
            f["coin"] = c; f["window"] = w; f["bad"] = w in bad
            recs.append(f)
            # one case per 36-bar grid cell: first signal bar in cell
            f2 = f.copy(); f2["cell"] = np.arange(len(f2)) // 36
            s = f2[f2["sig"] & f2["fwd"].notna()].groupby("cell").head(1)
            cases.append(s)
    F = pd.concat(recs)
    # drift per coin: grid 36-bar returns all windows
    drift = {}
    for c in coins:
        rr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 36, 36)
            rr += list(cl[idx + 36] / cl[idx] - 1)
        drift[c] = np.mean(rr)
    C = pd.concat(cases)
    C["u"] = C["fwd"] - C["coin"].map(drift)
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "n": len(x)})
    for col, bins in [("r360", [-5, -0.3, -0.1, 0, 0.2, 0.5, 20]), ("r90", [-5, -0.2, -0.05, 0, 0.05, 0.15, 20]),
                      ("vrel", [0, 0.7, 0.85, 1.0, 1.2, 10]), ("dn", [0, 0.46, 0.49, 0.52, 1])]:
        q = pd.cut(C[col], bins)
        out["cases_by_" + col] = C.groupby(q, observed=True)["u"].apply(tt).unstack()
        L = F[F["a"] > 0]
        ql = pd.cut(L[col], bins)
        out["longbars_by_" + col] = L.groupby([ql, "bad"], observed=True)["g"].agg(["mean", "count"]).unstack()
    out["cases_bad_vs_good"] = C.groupby("bad")["u"].apply(tt).unstack()
    out["share_cases_r360pos"] = C.groupby("bad")["r360"].apply(lambda x: (x.dropna() > 0).mean())
    return out
