def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            if len(b) < 220: continue
            r1 = c.pct_change(); vol = r1.rolling(180).std()
            l12 = lo.shift(1).rolling(12).min()
            h12 = hi.shift(1).rolling(12).max()
            rng = (hi - lo) / c; mrng = rng.rolling(180).mean()
            narrow = ((h12 - l12) / c) / mrng
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"dnz": (c - l12).clip(upper=0) / c / vol,
                               "r6z": (c / c.shift(6) - 1) / (vol * np.sqrt(6)),
                               "narrow": narrow, "ts": ts, "win": w,
                               "f18": c.shift(-18) / c - 1})
            df = df.iloc[::18]
            df = df[df["f18"].notna() & df["dnz"].notna() & df["r6z"].notna()]
            recs.append(df)
        if not recs: continue
        d = pd.concat(recs)
        d["u18"] = d["f18"] - d["f18"].mean()
        d["coin"] = coin
        rows.append(d)
    D = pd.concat(rows)
    def tm(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_u%": x.mean() * 100, "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    D["q6"] = pd.qcut(D["r6z"].rank(method="first"), 10, labels=False)
    # time-clustered: per bar time, mean over coins in that decile
    out["r6z decile, clustered by bar time"] = D.groupby("q6").apply(lambda g: tm(g.groupby("ts")["u18"].mean()))
    # idiosyncratic: subtract cross-coin mean at same bar time
    D["xmean"] = D.groupby("ts")["u18"].transform("mean")
    D["ncoin"] = D.groupby("ts")["u18"].transform("count")
    D["idio"] = D["u18"] - D["xmean"]
    out["r6z decile, coin minus same-time coin mean"] = D[D["ncoin"] >= 3].groupby("q6").apply(lambda g: tm(g["idio"]))
    # share of coins breaking down at same time
    D["isdn"] = (D["dnz"] < 0).astype(float)
    D["share_dn"] = D.groupby("ts")["isdn"].transform("mean")
    B = D[D["dnz"] < 0].copy()
    B["sq"] = pd.cut(B["share_dn"], [0, 0.2, 0.5, 1.01], labels=["few", "some", "many"])
    out["down-break by share of coins breaking same time"] = B.groupby("sq").apply(lambda g: tm(g["u18"]))
    out["down-break idio (coin minus same-time mean)"] = tm(B[B["ncoin"] >= 3]["idio"])
    # narrow graded, all grid bars, clustered
    D["qn"] = pd.qcut(D["narrow"].rank(method="first"), 5, labels=False)
    out["narrow quintile, clustered by bar time"] = D.groupby("qn").apply(lambda g: tm(g.groupby("ts")["u18"].mean()))
    out["narrow quintile, idio"] = D[D["ncoin"] >= 3].groupby("qn").apply(lambda g: tm(g["idio"]))
    out["distinct bar times"] = pd.Series({"times": D["ts"].nunique(), "cases": len(D)})
    return out
