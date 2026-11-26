def explore(data):
    import numpy as np, pandas as pd
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
            for h in (1, 2, 3):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                     r1=r1[i], vol=vol[i], fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    d = d.dropna(subset=["r1", "vol"]).copy()
    d["fall"] = (-d["r1"]).clip(lower=0)
    d["z"] = d["fall"] / d["vol"]
    d["fxv"] = d["fall"] * d["vol"]

    def cl_t(x, y, day):
        x = x - x.mean(); y = y - y.mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - b * x
        s = pd.Series(x * e).groupby(day.values).sum()
        se = np.sqrt((s ** 2).sum()) / (x * x).sum()
        return b, b / se

    out = {}
    res = []
    for h in (1, 2, 3):
        g = d[d.h == h]
        r = dict(h=h, n=len(g), days=g["day"].nunique())
        for k in ("fall", "z", "fxv"):
            r["t_all_" + k] = cl_t(g[k].values, g["ex"].values, g["day"])[1]
        res.append(r)
    out["all grid points (0 on up days), clustered t"] = pd.DataFrame(res)

    g = d[(d.h == 2)].copy()
    pc = []
    for coin, gg in g.groupby("coin"):
        pc.append(dict(coin=coin, n=len(gg), t_z=cl_t(gg["z"].values, gg["ex"].values, gg["day"])[1],
                       t_fxv=cl_t(gg["fxv"].values, gg["ex"].values, gg["day"])[1]))
    out["h2 per coin, all points"] = pd.DataFrame(pc)
    py = []
    for y, gg in g.groupby("year"):
        py.append(dict(year=y, n=len(gg), t_z=cl_t(gg["z"].values, gg["ex"].values, gg["day"])[1],
                       t_fxv=cl_t(gg["fxv"].values, gg["ex"].values, gg["day"])[1]))
    out["h2 per year, all points"] = pd.DataFrame(py)

    f = g[g.r1 < 0].copy()
    f["vhi"] = f.groupby("coin")["vol"].transform(lambda s: s > s.median())
    vs = []
    for v, gg in f.groupby("vhi"):
        vs.append(dict(high_vol=v, n=len(gg), mean_ex=gg["ex"].mean(),
                       t_fall=cl_t(gg["fall"].values, gg["ex"].values, gg["day"])[1],
                       t_z=cl_t(gg["z"].values, gg["ex"].values, gg["day"])[1]))
    out["h2 falls: by vol half"] = pd.DataFrame(vs)
    f["zq"] = f.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["h2 falls by z quintile"] = f.groupby("zq").agg(n=("ex", "count"), mean_ex=("ex", "mean"),
                                                        mean_z=("z", "mean"))
    u = g[g.r1 > 0].copy()
    u["rise_z"] = u["r1"] / u["vol"]
    out["h2 up days: t of ex on rise/vol"] = cl_t(u["rise_z"].values, u["ex"].values, u["day"])[1]
    out["usual 2d move (mean std over coins)"] = g.groupby("coin")["fwd"].std().mean()
    return out
