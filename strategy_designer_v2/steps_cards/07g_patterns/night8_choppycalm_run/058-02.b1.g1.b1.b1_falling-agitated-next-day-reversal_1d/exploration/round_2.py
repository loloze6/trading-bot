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
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "z": r / sd,
                "n1": c.shift(-1) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "vrel": r.rolling(10).std() / r.rolling(60, min_periods=40).std(),
                "clv": (c - b["low"]) / rng,
                "rngz": (rng / c) / sd,
                "inprof": (b["regime"] == "unknown").astype(int),
                "pos": b["postRebalance_current_allocation"].astype(float),
                "i": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["n1"] - d.groupby("coin")["n1"].transform("mean")
    d = d.dropna(subset=["clv", "x1"])
    d["day"] = d["ts"].dt.floor("D")
    d["cs"] = 2 * d["clv"] - 1  # -1 at low, +1 at high
    d["g"] = -d["cs"] * d["x1"]   # gain of fading the close location

    def ct(g, col="g"):
        s = g.groupby("day")[col].sum(); n = g.groupby("day")[col].count()
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(g) if G > 1 else np.nan
        return pd.Series({"n": len(g), "days": G, "mean": m, "t_day": m / se if se else np.nan})

    out = {}
    out["clv fade all"] = ct(d)
    d["trb"] = pd.cut(d["tr60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    d["vb"] = pd.qcut(d["vrel"], 2, labels=["calmish", "agitish"])
    out["clv fade by trend x vol"] = d.dropna(subset=["trb", "vb"]).groupby(["trb", "vb"]).apply(ct)
    d["zb"] = pd.cut(d["z"].abs(), [0, 0.5, 1, 100])
    out["clv fade by |z|"] = d.groupby("zb").apply(ct)
    out["clv fade by profile flag"] = d.groupby("inprof").apply(ct)
    # high-close side only: next excess for clv>0.5, graded
    d["clvb"] = pd.cut(d["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    d["x1c"] = d["x1"]
    out["next excess by clv, rise trend"] = d[d["trb"] == "rise"].groupby("clvb").apply(lambda g: ct(g, "x1c"))
    out["next excess by clv, chop trend"] = d[d["trb"] == "chop"].groupby("clvb").apply(lambda g: ct(g, "x1c"))
    out["next excess by clv, fall trend"] = d[d["trb"] == "fall"].groupby("clvb").apply(lambda g: ct(g, "x1c"))
    # clv effect on low-z days (close position not explained by the day's move)
    out["clv fade, |z|<0.5, by year"] = d[d["z"].abs() < 0.5].groupby(d["ts"].dt.year).apply(ct)
    out["clv fade by year"] = d.groupby(d["ts"].dt.year).apply(ct)
    # weekday fade check, day-clustered, by side
    d["fz"] = -np.sign(d["z"]) * d["x1"]
    d["wd"] = d["ts"].dt.weekday
    big = d[d["z"].abs() > 1].copy()
    big["side"] = np.where(big["z"] > 0, "up", "down")
    out["z-fade |z|>1 weekday x side"] = big.groupby(["wd", "side"]).apply(lambda g: ct(g, "fz"))
    # clv fade by range size relative to swing
    d["rb"] = pd.qcut(d["rngz"], 4, labels=False)
    out["clv fade by range/swing quartile"] = d.groupby("rb").apply(ct)
    # book: share from long vs short
    d["bg"] = d["pos"] * d["n1"]
    out["book gain by side"] = d.groupby(np.sign(d["pos"]))["bg"].agg(["count", "sum", "mean"])
    return out
