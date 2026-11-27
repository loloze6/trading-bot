def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            rng = (h - l)
            sd30 = r.rolling(30, min_periods=30).std()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c - 1,
                "width": rng / rng.rolling(30, min_periods=30).mean(),
                "loc": (c - l) / rng.replace(0, np.nan), "z": r / sd30,
                "tr60": c / c.shift(60) - 1, "tr20": c / c.shift(20) - 1,
                "pct": sd30.expanding(min_periods=90).apply(lambda x: (x <= x[-1]).mean(), raw=True),
                "regime": b["regime"]}))
    df = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    df["ex"] = df["nxt"] - df["coin"].map(df.groupby("coin")["nxt"].mean())
    d2 = df.dropna(subset=["nxt2"])
    df["ex2"] = df["nxt2"] - df["coin"].map(d2.groupby("coin")["nxt2"].mean())
    df["day"] = df["ts"].dt.floor("D"); df["year"] = df["ts"].dt.year

    def ct(sub, col="ex"):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": np.nan, "mean%": np.nan, "t": np.nan})
        v = s[col]; m = v.mean()
        dev = (v - m).groupby(s["day"]).sum(); D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(v)
        return pd.Series({"n": len(v), "days": D, "mean%": 100 * m, "t": m / se})

    s = df.dropna(subset=["width", "loc", "tr60", "pct"]).copy()
    s["score"] = s["width"] * (0.5 - s["loc"])
    s["trend"] = np.where(s["tr60"] > 0.1, "rising", np.where(s["tr60"] < -0.1, "falling", "choppy"))
    s["agit"] = np.where(s["pct"] > 0.5, "agit", "calm")
    out = {}
    lowc = s[(s["score"] > 0)].copy()
    lowc["sq"] = pd.qcut(lowc["score"], 4, labels=["q1", "q2", "q3", "q4"])
    out["low-close score quartile x trend60 (1d)"] = lowc.groupby(["trend", "sq"], observed=True).apply(ct)
    out["low-close top quartile, trend x agit (1d)"] = lowc[lowc["sq"] == "q4"].groupby(["trend", "agit"]).apply(ct)
    out["low-close top quartile, trend x agit (2d)"] = lowc[lowc["sq"] == "q4"].groupby(["trend", "agit"]).apply(ct, col="ex2")
    ris = lowc[(lowc["trend"] == "rising") & (lowc["sq"] == "q4")]
    out["rising q4 by year"] = ris.groupby("year").apply(ct)
    out["rising q4 by today's z"] = ris.assign(zb=pd.cut(ris["z"], [-99, -2, -1, 0, 99])).groupby("zb", observed=True).apply(ct)
    out["rising q4 by coin"] = ris.groupby("coin").apply(ct)
    return out
