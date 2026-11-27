def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r1 = c.pct_change()
            b["r1"] = r1
            b["r3p"] = c / c.shift(3) - 1
            b["r5p"] = c / c.shift(5) - 1
            b["r10p"] = c / c.shift(10) - 1
            sd = r1.rolling(20).std()
            b["sd20"] = sd
            b["z1"] = r1 / sd
            b["z5"] = b["r5p"] / (sd * np.sqrt(5))
            b["depth"] = (c - h.rolling(20).max()) / h.rolling(20).max() / sd
            b["fromlow"] = (c - l.rolling(20).min()) / l.rolling(20).min() / sd
            rng = (h - l)
            b["clv"] = (c - l) / rng.replace(0, np.nan)
            b["rngz"] = (rng / c) / sd
            b["volz"] = np.log(b["volume"] / b["volume"].rolling(20).mean())
            b["f1"] = c.shift(-1) / c - 1
            b["f3"] = c.shift(-3) / c - 1
            b["f5"] = c.shift(-5) / c - 1
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["fc"] = (b["regime"] == "unknown")
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    # coin mean 3-bar return on grid
    g3 = d[d["pos"] % 3 == 0].dropna(subset=["f3"])
    m3 = g3.groupby("coin")["f3"].mean()
    d["ex3"] = d["f3"] - d["coin"].map(m3)
    fc = d[(d["fc"]) & (d["pos"] % 3 == 0)].dropna(subset=["ex3"])
    out = {}
    out["n falling calm grid cases"] = len(fc)
    out["fc by coin"] = fc.groupby("coin")["ex3"].agg(["count", "mean"])
    def q(col, k=5):
        s = fc.dropna(subset=[col])
        s = s.assign(qq=pd.qcut(s[col], k, labels=False, duplicates="drop"))
        t = s.groupby("qq").agg(n=("ex3", "size"), lo=(col, "min"), hi=(col, "max"),
                                mean=("ex3", "mean"), sd=("ex3", "std"))
        t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
        sl = stats.linregress(s[col], s["ex3"])
        t["slope_t_all"] = sl.slope / sl.stderr
        return t
    for col in ["depth", "fromlow", "z1", "z5", "r10p", "clv", "rngz", "volz", "sd20"]:
        out["ex3 by " + col] = q(col)
    out["ex3 by weekday"] = fc.groupby("wd")["ex3"].agg(["count", "mean"])
    out["ex3 by window"] = fc.groupby("win")["ex3"].agg(["count", "mean"])
    return out
