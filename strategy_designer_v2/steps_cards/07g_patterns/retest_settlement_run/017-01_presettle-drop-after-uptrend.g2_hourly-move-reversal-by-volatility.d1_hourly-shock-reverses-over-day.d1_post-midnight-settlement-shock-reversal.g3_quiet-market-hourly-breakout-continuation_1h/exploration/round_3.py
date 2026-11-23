def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; clock = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            v24 = r.rolling(24).std(); v720 = r.rolling(720).std()
            z = r / v24; ratio = v24 / v720
            ret24 = c / c.shift(24) - 1
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            fwd = c.shift(-24) / c - 1
            idx = np.arange(0, n, 24)
            rows.append(pd.DataFrame({"coin": coin, "z": z.values[idx], "ratio": ratio.values[idx],
                                      "fwd": fwd.values[idx], "yr": ts.dt.year.values[idx]}))
            # clock-time stretches: decision at close of bar opening at hour H-1 (i.e. bar closes at H:00)
            for H, L in ((13, 3), (13, 1), (23, 3), (23, 1)):
                sel = np.where(((ts.dt.hour + 1) % 24 == H).values)[0]
                f = (c.shift(-L) / c - 1).values[sel]
                clock.append(pd.DataFrame({"coin": coin, "H": H, "L": L, "fwd": f,
                                           "trend": ret24.values[sel], "yr": ts.dt.year.values[sel]}))
    G = pd.concat(rows).dropna(subset=["z", "fwd"])
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["un"] = G["fwd"] - G["drift"]; G["usual"] = G.groupby("coin")["fwd"].transform("std")
    G["sun"] = -np.sign(G["z"]) * G["un"]; G["stot"] = -np.sign(G["z"]) * G["fwd"]
    G["zq"] = pd.qcut(G["z"].abs(), 4, labels=False)
    def tt(x): return x.mean() / x.std() * np.sqrt(len(x))
    out = {}
    a = G.groupby("zq").agg(n=("sun", "size"), absz=("z", lambda x: x.abs().mean()),
                            unusual=("sun", "mean"), total=("stot", "mean"))
    a["strength"] = (G["sun"] / G["usual"]).groupby(G["zq"]).mean()
    a["t"] = G.groupby("zq")["sun"].apply(tt)
    out["all regimes: 24h reversal by |z| quartile"] = a
    def reg(d, x, y):
        if len(d) < 50: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d[x], d[y]); return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    out["all regimes 24h slope by year"] = G.groupby("yr").apply(lambda d: reg(d, "z", "un"))
    C = pd.concat(clock).dropna(subset=["fwd", "trend"])
    C["un"] = C["fwd"] - C.groupby(["coin", "H", "L"])["fwd"].transform("mean")
    C["trz"] = C["trend"] / C.groupby("coin")["trend"].transform("std")
    C["s"] = np.sign(C["trend"]) * C["un"]
    out["clock slope un~trend z by H,L"] = C.groupby(["H", "L"]).apply(lambda d: reg(d, "trz", "un"))
    for H in (13, 23):
        d = C[(C.H == H) & (C.L == 3)].copy()
        d["q"] = pd.qcut(d["trz"].abs(), 4, labels=False)
        b = d.groupby("q").agg(n=("s", "size"), signed_un=("s", "mean"))
        b["t"] = d.groupby("q")["s"].apply(tt)
        out[f"H{H} 3h trend-signed by |trend z| quartile"] = b
        out[f"H{H} 3h slope by year"] = d.groupby("yr").apply(lambda x: reg(x, "trz", "un"))
        out[f"H{H} 3h slope by coin"] = d.groupby("coin").apply(lambda x: reg(x, "trz", "un"))
    return out
