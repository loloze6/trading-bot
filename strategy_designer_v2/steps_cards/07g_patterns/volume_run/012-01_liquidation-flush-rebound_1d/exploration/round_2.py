def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r1 = cl.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            z = r1 / vol20
            vr = b["volume"] / b["volume"].rolling(30, min_periods=10).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            wick = (np.minimum(b["open"], cl) - b["low"]) / rng
            r5 = cl / cl.shift(5) - 1
            f3 = cl.shift(-3) / cl - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": c, "w": w, "z": z, "vr": vr, "wick": wick,
                "r5z": r5 / (vol20 * np.sqrt(5)), "f3": f3, "fc": b["forecast"],
                "wd": ts.dt.weekday, "year": ts.dt.year, "pos": np.arange(len(b))}))
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 3 == 0)].dropna(subset=["f3"]).copy()
    G["ex"] = G["f3"] - G.groupby("coin")["f3"].transform("mean")
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    dn = G[G["z"] < -1].dropna(subset=["vr", "wick"]).copy()
    dn["vrq"] = pd.qcut(dn["vr"], 3, labels=["lowvr", "midvr", "hivr"])
    dn["wkh"] = pd.qcut(dn["wick"], 2, labels=["lowwk", "hiwk"])
    out["falls vr x wick"] = dn.groupby(["vrq", "wkh"]).apply(summ)
    out["falls hivr by coin"] = dn[dn["vrq"] == "hivr"].groupby("coin").apply(summ)
    out["falls hivr by year"] = dn[dn["vrq"] == "hivr"].groupby("year").apply(summ)
    out["falls lowvr by coin"] = dn[dn["vrq"] == "lowvr"].groupby("coin").apply(summ)
    # graded: correlation of ex with vr*|z| among falls
    dn["fv"] = -dn["z"] * dn["vr"]
    out["falls spearman ex vs vr"] = stats.spearmanr(dn["vr"], dn["ex"])[0]
    out["falls spearman ex vs vr p"] = stats.spearmanr(dn["vr"], dn["ex"])[1]
    out["falls spearman ex vs wick"] = stats.spearmanr(dn["wick"], dn["ex"])[0]
    out["n falls"] = len(dn)
    # all falls (z<0) by vr quintile
    d0 = G[G["z"] < 0].dropna(subset=["vr"]).copy()
    d0["vrq"] = pd.qcut(d0["vr"], 5, labels=False)
    out["all down bars by vr quintile"] = d0.groupby("vrq").apply(summ)
    u0 = G[G["z"] > 0].dropna(subset=["vr"]).copy()
    u0["vrq"] = pd.qcut(u0["vr"], 5, labels=False)
    out["all up bars by vr quintile"] = u0.groupby("vrq").apply(summ)
    # 5d continuation robustness
    G["r5q"] = pd.qcut(G["r5z"], 5, labels=False)
    top = G[G["r5q"] == 4]
    out["top 5d quintile by coin"] = top.groupby("coin").apply(summ)
    out["top 5d quintile by year"] = top.groupby("year").apply(summ)
    out["spearman ex vs r5z"] = stats.spearmanr(G["r5z"], G["ex"], nan_policy="omit")[0]
    # Saturday by year
    D = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            d = d.copy(); d["coin"] = c
            dd = pd.to_datetime(d["day"]); d["wd"] = dd.dt.weekday; d["y"] = dd.dt.year
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    sat = D[D["wd"] == 5]
    out["saturday coin ret by year"] = sat.groupby("y")["coin_return"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    out["saturday coin ret by coin"] = sat.groupby("coin")["coin_return"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    return out
