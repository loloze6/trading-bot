def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r1).rolling(60, min_periods=40).std().values
            n = len(c)
            for h in (1, 2, 3, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                     r1=r1[i], vol=vol[i], fwd=c[i + h] / c[i] - 1,
                                     fc=float(df["forecast"].iloc[i]) if pd.notna(df["forecast"].iloc[i]) else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["fall"] = (-d["r1"]).clip(lower=0)
    d = d.dropna(subset=["r1", "vol"])
    out = {}

    def cl_t(x, y, day):
        x = x - x.mean(); y = y - y.mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - b * x
        s = pd.Series(x * e).groupby(day.values).sum()
        se = np.sqrt((s ** 2).sum()) / (x * x).sum()
        return b, b / se

    res = []
    for h in (1, 2, 3, 5):
        g = d[d.h == h]
        f = g[g.r1 < 0]
        b1, t1 = cl_t(f["fall"].values, f["ex"].values, f["day"])
        b2, t2 = cl_t((f["fall"] * f["vol"]).values, f["ex"].values, f["day"])
        b3, t3 = cl_t((f["fall"] / f["vol"]).values, f["ex"].values, f["day"])
        res.append(dict(h=h, n_falls=len(f), mean_ex_falldays=f["ex"].mean(), mean_ex_updays=g[g.r1 >= 0]["ex"].mean(),
                        t_fall=t1, t_fallxvol=t2, t_fall_over_vol=t3))
    out["by horizon (fall days)"] = pd.DataFrame(res)

    g = d[(d.h == 2) & (d.r1 < 0)].copy()
    g["z"] = g["fall"] / g["vol"]
    g["zq"] = g.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 4, labels=False))
    g["vq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["h2 mean ex by fall/vol quartile x vol tercile"] = g.pivot_table(index="zq", columns="vq", values="ex", aggfunc="mean")
    out["h2 count by quartile"] = g.groupby("zq")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    g["fq"] = g.groupby("coin")["fall"].transform(lambda s: pd.qcut(s, 4, labels=False))
    out["h2 by raw fall quartile"] = g.groupby("fq")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    pc = []
    for coin, gg in g.groupby("coin"):
        b, t = cl_t((gg["fall"] * gg["vol"]).values, gg["ex"].values, gg["day"])
        b2, t2 = cl_t(gg["fall"].values, gg["ex"].values, gg["day"])
        pc.append(dict(coin=coin, n=len(gg), t_fallxvol=t, t_fall=t2, mean_ex=gg["ex"].mean()))
    out["h2 per coin"] = pd.DataFrame(pc)
    py = []
    for y, gg in g.groupby("year"):
        b, t = cl_t(gg["fall"].values, gg["ex"].values, gg["day"])
        py.append(dict(year=y, n=len(gg), t_fall=t, mean_ex=gg["ex"].mean()))
    out["h2 per year"] = pd.DataFrame(py)
    # strength by fall size, using usual
    g["str"] = g["ex"] / g["usual"]
    out["h2 strength top quartile z"] = g[g.zq == 3]["str"].mean()
    return out
