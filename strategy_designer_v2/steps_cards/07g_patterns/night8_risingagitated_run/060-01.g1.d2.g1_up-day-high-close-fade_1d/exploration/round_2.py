def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": ((c - l) / rng).values,
                "r1": (c / c.shift(1) - 1).values,
                "rngrel": (rng / c).values,
                "nxt": (c.shift(-1) / c - 1).values,
                "regime": b["regime"].values,
                "dayk": ts.dt.strftime("%Y%m%d").values,
                "year": ts.dt.year.values,
            })
            df["r5"] = df["r1"].pipe(lambda s: (c / c.shift(5) - 1).values)
            df["rngz"] = df["rngrel"] / pd.Series(df["rngrel"]).rolling(20).mean().shift(1)
            df["r1z"] = df["r1"] / pd.Series(df["r1"]).rolling(20).std().shift(1)
            df["unus"] = df["nxt"] - drift
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "loc", "r1"])
    d["inprof"] = d["regime"] != "chop"

    def ct(g):
        s = g.groupby("dayk")["unus"].sum()
        G = len(s)
        n = len(g)
        m = g["unus"].mean()
        dev = (g["unus"] - m).groupby(g["dayk"]).sum()
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return pd.Series({"n": n, "days": G, "mean_unus": m, "t_day": m / se if se else np.nan})

    out = {}
    up = d[d.inprof & (d.r1 > 0)].copy()
    up["rngq"] = pd.qcut(up["rngz"], 4)
    out["prof up days: range vs prior 20d"] = up.groupby("rngq").apply(ct)
    up["r5q"] = pd.qcut(up["r5"], 4)
    out["prof up days: 5d return"] = up.groupby("r5q").apply(ct)
    up["r1zq"] = pd.qcut(up["r1z"], 4)
    out["prof up days: r1 / 20d sd"] = up.groupby("r1zq").apply(ct)
    up["wide"] = up["rngz"] > up["rngz"].median()
    out["prof up days wide: by window"] = up[up.wide].groupby("win").apply(ct)
    out["prof up days wide: by coin"] = up[up.wide].groupby("coin").apply(ct)
    out["prof up days all"] = ct(up).to_frame().T
    dn = d[d.inprof & (d.r1 <= 0)].copy()
    dn["rngq"] = pd.qcut(dn["rngz"], 4)
    out["prof down days: range vs prior 20d"] = dn.groupby("rngq").apply(ct)
    o = d[~d.inprof & (d.r1 > 0)].copy()
    o["rngq"] = pd.qcut(o["rngz"], 4)
    out["out prof up days: range vs prior 20d"] = o.groupby("rngq").apply(ct)
    return out
