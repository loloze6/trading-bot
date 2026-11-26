def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            r5 = c.pct_change(5)
            sd5 = r5.rolling(30, min_periods=20).std()
            z5 = r5 / (sd * np.sqrt(5))
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            tr60 = c / c.shift(60) - 1
            vrel = sd / sd.rolling(90, min_periods=60).median()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "z5": z5,
                               "fwd": fwd, "fwd1": fwd1, "rng": rng, "clpos": clpos, "tr60": tr60,
                               "vrel": vrel, "inprof": (b["regime"] == "unknown").astype(int),
                               "fc": b["forecast"], "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = {}
    for coin, g in d.groupby("coin"):
        gg = g[g["pos"] % H == 0]
        drift[coin] = gg["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    g = d[(d["pos"] % H == 0)].dropna(subset=["z", "ex"])
    out = {}
    def summ(gr, col="ex"):
        a = gr.agg(n=(col, "size"), mean=(col, "mean"), sd=(col, "std"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["n"]))
        return a
    g["zb"] = pd.cut(g["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["ex5 by z bin, all"] = summ(g.groupby("zb"))
    out["ex5 by z bin x inprof"] = summ(g.groupby(["inprof", "zb"]))
    g2 = g.dropna(subset=["vrel"]).copy()
    g2["agit"] = (g2["vrel"] > 1).astype(int)
    out["ex5 by z bin x agit(proxy)"] = summ(g2.groupby(["agit", "zb"]))
    g3 = g.dropna(subset=["tr60"]).copy()
    g3["tr"] = pd.cut(g3["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out["ex5 by z bin x trend"] = summ(g3.groupby(["tr", "zb"]))
    g["z5b"] = pd.cut(g["z5"], [-99, -2, -1, 0, 1, 2, 99])
    out["ex5 by 5d z bin"] = summ(g.groupby("z5b"))
    out["ex5 by weekday"] = summ(g.groupby("wd"))
    # slopes
    sl = {}
    for name, sub in [("all", g), ("inprof", g[g.inprof == 1]), ("outprof", g[g.inprof == 0])]:
        s = stats.linregress(sub["z"], sub["ex"])
        sl[name] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(sub)}"
    out["slope ex on z"] = pd.Series(sl)
    # daily next-day by z, all bars (1-day horizon, no overlap)
    d1 = d.dropna(subset=["z", "fwd1"]).copy()
    d1["zb"] = pd.cut(d1["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["next day by z bin"] = summ(d1.groupby("zb"), "fwd1")
    d1["cb"] = pd.cut(d1["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["next day by close position"] = summ(d1.groupby("cb"), "fwd1")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    br = dd.groupby(["win", "day"])["book_return"].mean()
    out["book mean by window"] = dd.groupby("win")[["book_return", "coin_return"]].mean()
    out["share in profile by coin"] = d.groupby("coin")["inprof"].mean()
    return out
