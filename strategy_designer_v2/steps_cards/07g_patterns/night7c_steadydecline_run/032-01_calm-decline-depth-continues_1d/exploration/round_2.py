def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            vol = d["volume"].astype(float)
            rng = (d["high"] - d["low"]).astype(float) / c
            f = pd.DataFrame({"ts": pd.to_datetime(d["timestamp"])})
            f["coin"] = coin; f["w"] = w; f["pos_in_w"] = np.arange(len(d))
            f["r1"] = c / c.shift(1) - 1
            f["sd20"] = f["r1"].rolling(20).std()
            f["z1"] = f["r1"] / f["sd20"].shift(1)
            f["vsp"] = vol / vol.rolling(28).mean().shift(1)
            f["rng_z"] = rng / rng.rolling(28).mean().shift(1)
            f["r3"] = c / c.shift(3) - 1
            for h in (1, 2, 3, 5):
                f[f"fwd{h}"] = c.shift(-h) / c - 1
            rows.append(f)
    A = pd.concat(rows)
    A["day"] = A["ts"].dt.floor("D"); A["wd"] = A["ts"].dt.dayofweek; A["yr"] = A["ts"].dt.year
    for h in (1, 2, 3, 5):
        A[f"ex{h}"] = A[f"fwd{h}"] - A.groupby("coin")[f"fwd{h}"].transform("mean")

    def tday(df, col):
        x = df.dropna(subset=[col])
        if len(x) < 3: return np.nan, np.nan, len(x)
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(x)
        return m, m / se, dev.size

    res = {}
    # weekday excess next day, by coin and by year (all bars, 1-day returns don't overlap)
    out = []
    for (k), x in A.groupby("wd"):
        m, t, n = tday(x, "ex1"); out.append({"wd": k, "ex1": m, "t": t, "days": n})
    res["weekday ex1"] = pd.DataFrame(out)
    tf = A[A.wd.isin([3, 4])]
    out = []
    for k, x in tf.groupby("coin"):
        m, t, n = tday(x, "ex1"); out.append({"coin": k, "ex1": m, "t": t, "n": n})
    for k, x in tf.groupby("yr"):
        m, t, n = tday(x, "ex1"); out.append({"coin": f"yr{k}", "ex1": m, "t": t, "n": n})
    for k, x in tf.groupby("w"):
        m, t, n = tday(x, "ex1"); out.append({"coin": k, "ex1": m, "t": t, "n": n})
    res["thu+fri bars ex1 by coin/year/window"] = pd.DataFrame(out)
    # reversal of standardized day moves, graded, horizons 1,2,3 (non-overlapping grid for h)
    out = []
    for h in (1, 2, 3):
        G = A[A.pos_in_w % h == 0].dropna(subset=["z1", f"ex{h}"]).copy()
        G["b"] = pd.qcut(G["z1"], 6, labels=False)
        for b, x in G.groupby("b"):
            m, t, n = tday(x, f"ex{h}")
            out.append({"h": h, "bucket": b, "z": x.z1.mean(), "ex": m, "t": t, "days": n})
    res["z1 sextile -> ex h"] = pd.DataFrame(out)
    # down day with volume spike vs no spike
    G = A.dropna(subset=["z1", "vsp", "ex1"]).copy()
    G["down"] = pd.cut(G.z1, [-99, -1.5, -0.5, 0.5, 1.5, 99], labels=False)
    G["spk"] = (G.vsp > G.groupby("coin")["vsp"].transform("median")).astype(int)
    out = []
    for k, x in G.groupby(["down", "spk"]):
        m, t, n = tday(x, "ex1"); out.append({"zbin": k[0], "volhigh": k[1], "ex1": m, "t": t, "days": n})
    res["z1 x volume -> ex1"] = pd.DataFrame(out)
    # big-down-day reversal by coin and by year
    big = G[G.z1 < -1.5]
    out = []
    for k, x in big.groupby("coin"):
        m, t, n = tday(x, "ex1"); out.append({"grp": k, "ex1": m, "t": t, "n": n})
    for k, x in big.groupby("yr"):
        m, t, n = tday(x, "ex1"); out.append({"grp": f"yr{k}", "ex1": m, "t": t, "n": n})
    res["z1<-1.5 ex1 by coin/year"] = pd.DataFrame(out)
    # slope of ex1 on z1 per coin
    out = []
    for k, x in G.groupby("coin"):
        b = np.polyfit(x.z1.clip(-4, 4), x.ex1, 1)[0]
        cr = np.corrcoef(x.z1.clip(-4, 4), x.ex1)[0, 1]
        out.append({"coin": k, "slope": b, "corr": cr, "t": cr*np.sqrt(len(x)-2)/np.sqrt(1-cr**2), "n": len(x)})
    res["slope ex1 on z1 per coin"] = pd.DataFrame(out)
    return res
