def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            vol30 = r.rolling(30, min_periods=25).std()
            vpct = vol30.rolling(365, min_periods=200).apply(lambda a: (a <= a[-1]).mean(), raw=True)
            df = pd.DataFrame({
                "coin": coin, "ts": pd.to_datetime(b["timestamp"]),
                "z": r / sd, "n1": c.shift(-1) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "vrel": r.rolling(10).std() / r.rolling(60, min_periods=40).std(),
                "clv": (c - b["low"]) / rng, "rngz": (rng / c) / sd, "vpct": vpct,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["n1"] - d.groupby("coin")["n1"].transform("mean")
    d = d.dropna(subset=["clv", "x1", "rngz"])
    d["day"] = d["ts"].dt.floor("D")

    def ct(g, col):
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(g) if G > 1 else np.nan
        return pd.Series({"n": len(g), "days": G, "mean": m, "t_day": m / se if se else np.nan})

    out = {}
    d["trb"] = pd.cut(d["tr60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    d["ag"] = np.where(d["vpct"] > 0.5, "agit", "calm")
    d["rq"] = pd.qcut(d["rngz"], 4, labels=False)
    hi = d[d["clv"] >= 0.7]
    out["next excess, high close, by range quartile"] = hi.groupby("rq").apply(lambda g: ct(g, "x1"))
    out["next excess, high close & range top half, by trend x agit"] = hi[hi["rq"] >= 2].dropna(subset=["trb"]).groupby(["trb", "ag"]).apply(lambda g: ct(g, "x1"))
    out["next excess, high close & range top half, by year"] = hi[hi["rq"] >= 2].groupby(d["ts"].dt.year).apply(lambda g: ct(g, "x1"))
    # graded: short signal = clv-centred x range size
    d["sig"] = (2 * d["clv"] - 1) * d["rngz"]
    d["g"] = -d["sig"] * d["x1"]
    out["graded clv x range fade, by trend x agit"] = d.dropna(subset=["trb"]).groupby(["trb", "ag"]).apply(lambda g: ct(g, "g"))
    # up-day fade by vol ratio quartile
    d["fz"] = -np.sign(d["z"]) * d["x1"]
    d["vq"] = pd.qcut(d["vrel"], 4, labels=False)
    up = d[d["z"] > 1]; dn = d[d["z"] < -1]
    out["up-day fade by vol-ratio quartile"] = up.groupby("vq").apply(lambda g: ct(g, "fz"))
    out["down-day fade by vol-ratio quartile"] = dn.groupby("vq").apply(lambda g: ct(g, "fz"))
    out["down-day fade top vol-ratio quartile by year"] = dn[dn["vq"] == 3].groupby(d["ts"].dt.year).apply(lambda g: ct(g, "fz"))
    out["down-day fade top vol-ratio, by trend"] = dn[dn["vq"] == 3].dropna(subset=["trb"]).groupby(["trb", "ag"]).apply(lambda g: ct(g, "fz"))
    # Monday continuation by year
    mon = d[(d["ts"].dt.weekday == 0) & (d["z"].abs() > 1)]
    out["Monday |z|>1 fade by year"] = mon.groupby(d["ts"].dt.year).apply(lambda g: ct(g, "fz"))
    return out
