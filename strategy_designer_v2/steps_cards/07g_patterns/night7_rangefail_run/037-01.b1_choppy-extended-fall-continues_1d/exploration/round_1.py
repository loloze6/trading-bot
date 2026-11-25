import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r10 = c / c.shift(10) - 1
            z5 = r5 / (sd20 * np.sqrt(5))
            z1 = r1 / sd20.shift(1)
            z20 = r20 / (sd20 * np.sqrt(20))
            vp = sd20.rank(pct=True)
            f5 = c.shift(-5) / c - 1
            f10 = c.shift(-10) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "regime": b["regime"],
                               "z5": z5, "z1": z1, "z20": z20, "r20": r20, "r10": r10, "vp": vp, "f5": f5, "f10": f10,
                               "rng": rng, "clpos": clpos, "r1n": r1.shift(-1),
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g5 = d[d.pos % 5 == 0].copy()
    drift5 = g5.groupby("coin")["f5"].mean()
    g5["u5"] = g5["f5"] - g5["coin"].map(drift5)
    g10 = d[d.pos % 10 == 0].copy()
    drift10 = g10.groupby("coin")["f10"].mean()
    g10["u10"] = g10["f10"] - g10["coin"].map(drift10)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    g5["zb"] = pd.cut(g5["z5"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["u5 by regime x z5 bin (long dir)"] = g5.groupby(["regime", "zb"], observed=True).apply(lambda x: ct(x, "u5")).round(4)
    g5["z20b"] = pd.cut(g5["z20"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["u5 by regime x z20 bin"] = g5.groupby(["regime", "z20b"], observed=True).apply(lambda x: ct(x, "u5")).round(4)
    g10["zb"] = pd.cut(g10["z5"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["u10 by z5 bin all"] = g10.groupby("zb", observed=True).apply(lambda x: ct(x, "u10")).round(4)
    g5["vb"] = pd.cut(g5["vp"], [0, .25, .5, .75, 1])
    out["u5 by vol quartile x regime"] = g5.groupby(["regime", "vb"], observed=True).apply(lambda x: ct(x, "u5")).round(4)
    # next-day return after big one-day moves (all bars)
    d["z1b"] = pd.cut(d["z1"], [-np.inf, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, np.inf])
    dd = d.copy(); dd["dr1"] = dd["r1n"] - dd.groupby("coin")["r1n"].transform("mean")
    out["next-day unusual by z1 bin"] = dd.groupby("z1b", observed=True).apply(lambda x: ct(x, "dr1")).round(4)
    out["next-day unusual by weekday"] = dd.groupby("wd").apply(lambda x: ct(x, "dr1")).round(4)
    g5["cb"] = pd.cut(g5["clpos"], [0, .2, .4, .6, .8, 1], include_lowest=True)
    out["u5 by close-in-range"] = g5.groupby("cb", observed=True).apply(lambda x: ct(x, "u5")).round(4)
    g5["rngq"] = g5.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    out["u5 by day-range quartile"] = g5.groupby("rngq").apply(lambda x: ct(x, "u5")).round(4)
    # tested signal by window
    sig = g5[(g5.regime == "trending") & (g5.z5 < 0)].copy(); sig["s"] = -sig["u5"]
    out["short-dir u5 of signal by window"] = sig.groupby("w").apply(lambda x: ct(x, "s")).round(4)
    out["regime shares"] = d["regime"].value_counts(normalize=True).round(3)
    return out
