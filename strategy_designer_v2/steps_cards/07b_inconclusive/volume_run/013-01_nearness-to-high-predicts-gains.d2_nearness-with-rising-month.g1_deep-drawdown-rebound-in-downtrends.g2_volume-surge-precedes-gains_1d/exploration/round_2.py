def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = pd.Series(c).pct_change().values
            for h in (7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, year=yr[i], h=h, f=f[i], r1=r1[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    d = d.dropna(subset=["r1", "f", "ex"])
    d["fs"] = d["f"] * np.sign(d["r1"])

    def st(x, y):
        if len(x) < 10 or x.std() == 0:
            return np.nan, np.nan, len(x)
        r = stats.linregress(x, y)
        return r.slope, r.slope / r.stderr, len(x)

    out = {}
    for h in (7, 14):
        g = d[d.h == h]
        pc = []
        for k, gg in g.groupby("coin"):
            s, t, n = st(gg["fs"], gg["ex"]); s2, t2, _ = st(gg["f"], gg["ex"])
            pc.append(dict(coin=k, signed_slope=s, signed_t=t, plain_t=t2, n=n))
        out[f"per_coin_signed_{h}"] = pd.DataFrame(pc)
        py = []
        for k, gg in g.groupby("year"):
            s, t, n = st(gg["fs"], gg["ex"]); py.append(dict(year=k, slope=s, t=t, n=n))
        out[f"per_year_signed_{h}"] = pd.DataFrame(py)
    g = d[d.h == 7].copy()
    g["fq"] = pd.qcut(g["fs"].rank(method="first"), 6, labels=False)
    out["signed_sextile_7"] = g.groupby("fq").agg(fsmean=("fs", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    # down-day only: higher volume -> lower return?
    res = []
    for lab, gg in [("up", g[g.r1 > 0]), ("down", g[g.r1 <= 0])]:
        gg = gg.copy(); gg["q"] = pd.qcut(gg["f"].rank(method="first"), 3, labels=False)
        m = gg.groupby("q")["ex"].agg(["mean", "size"]); m["side"] = lab
        res.append(m.reset_index())
    out["side_tercile_7"] = pd.concat(res)
    return out
