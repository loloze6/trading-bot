def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["z3"] = (c / c.shift(3) - 1) / sd30
            b["z1"] = r1 / sd30
            b["r10"] = c / c.shift(10) - 1
            b["r20"] = c / c.shift(20) - 1
            b["sd30"] = sd30
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["rc"] = (b["regime"] == "unknown").astype(int)
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday
            b["yr"] = ts.dt.year
            b["day"] = ts.dt.floor("D")
            rng = (b["high"] - b["low"]) / c
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["rng_z"] = rng / sd30
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % H == 0)
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["grid"] & df["fwd"].notna()].copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    out = {}
    out["share rising calm"] = float(g["rc"].mean())
    def tab(sub, col, q=5):
        s = sub.dropna(subset=[col, "ex"]).copy()
        s["bin"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        t = s.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                                 mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")
    out["z3 bins, rising calm"] = tab(g[g.rc == 1], "z3")
    out["z3 bins, outside"] = tab(g[g.rc == 0], "z3")
    out["z1 bins, all"] = tab(g, "z1")
    out["r20 bins, all"] = tab(g, "r20")
    out["sd30 bins, all"] = tab(g, "sd30")
    out["clv bins, all"] = tab(g, "clv")
    out["rng_z bins, all"] = tab(g, "rng_z")
    # daily: weekday of next-day return
    d = df.dropna(subset=["fwd1"])
    dm = d.groupby("coin")["fwd1"].mean()
    d = d.assign(ex1=d["fwd1"] - d["coin"].map(dm))
    t = d.groupby("wd")["ex1"].agg(["size", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
    out["next-day excess by weekday of decision bar"] = t
    t = g.groupby(["yr"])["ex"].agg(["size", "mean"])
    out["5d excess by year"] = t
    # z3 by regime and year correlation
    s = g[g.rc == 1].dropna(subset=["z3"])
    out["corr z3 ex rising calm"] = float(stats.spearmanr(s.z3, s.ex)[0])
    s2 = g[g.rc == 0].dropna(subset=["z3"])
    out["corr z3 ex outside"] = float(stats.spearmanr(s2.z3, s2.ex)[0])
    # book: days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    bw = dd.groupby("win")[["book_return", "coin_return"]].mean()
    out["book vs coin mean daily by window"] = bw
    return out
