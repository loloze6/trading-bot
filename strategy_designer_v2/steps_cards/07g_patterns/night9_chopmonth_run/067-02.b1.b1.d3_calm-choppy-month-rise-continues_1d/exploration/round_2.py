def explore(data):
    import numpy as np, pandas as pd
    H = 7
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ret60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            hl = (b["high"] - b["low"]).astype(float)
            rng = hl / c
            rngrel = rng / rng.rolling(30).median()
            clpos = (c - b["low"]) / hl.replace(0, np.nan)
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b), H):
                if pd.isna(fwd.iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                 inprof=(b["regime"].iloc[i] == "unknown"), ret60=ret60.iloc[i],
                                 r1=r1.iloc[i], rng=rng.iloc[i], rngrel=rngrel.iloc[i], clpos=clpos.iloc[i],
                                 vol30=vol30.iloc[i], fwd=fwd.iloc[i], fwd1=fwd1.iloc[i], fwd3=fwd3.iloc[i]))
    g = pd.DataFrame(rows)
    for k in ["fwd", "fwd1", "fwd3"]:
        g["ex_" + k] = g[k] - g["coin"].map(g.groupby("coin")[k].mean())
    g["trend"] = np.where(g.ret60 > 0.10, "rising", np.where(g.ret60 < -0.10, "falling", "choppy"))
    g.loc[g.ret60.isna(), "trend"] = "na"
    g["clc"] = g["clpos"] - 0.5
    g["clc_scaled"] = g["clc"] * g["rng"] / g["vol30"]
    out = {}

    def clus_slope(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 20:
            return dict(n=len(d), days=0, slope=np.nan, t=np.nan)
        X = np.column_stack([np.ones(len(d)), d[x].values])
        Y = d[y].values
        XtX = np.linalg.inv(X.T @ X)
        beta = XtX @ X.T @ Y
        e = Y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = d["day"].nunique()
        V = XtX @ meat @ XtX * G / (G - 1) * (len(d) - 1) / (len(d) - 2)
        return dict(n=len(d), days=G, slope=beta[1], t=beta[1] / np.sqrt(V[1, 1]))

    res = []
    for x in ["clc", "clc_scaled", "rng", "rngrel", "r1"]:
        for y in ["ex_fwd1", "ex_fwd3", "ex_fwd"]:
            r = clus_slope(g, x, y); r.update(x=x, y=y, grp="all"); res.append(r)
    out["clustered slopes all"] = pd.DataFrame(res)
    res = []
    for tr in ["rising", "choppy", "falling"]:
        for x in ["clc", "clc_scaled", "rngrel"]:
            r = clus_slope(g[g.trend == tr], x, "ex_fwd"); r.update(x=x, trend=tr); res.append(r)
    out["slopes by trend 7d"] = pd.DataFrame(res)
    res = []
    for yr, d in g.groupby("year"):
        for x in ["clc", "rngrel"]:
            r = clus_slope(d, x, "ex_fwd"); r.update(x=x, year=yr); res.append(r)
    out["slopes by year 7d"] = pd.DataFrame(res)
    # interaction: wide range with close position
    d = g.dropna(subset=["rngrel", "clpos", "ex_fwd"]).copy()
    d["wide"] = pd.qcut(d.rngrel, 3, labels=["narrow", "mid", "wide"])
    d["cl"] = pd.cut(d.clpos, [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    out["wide x close pos mean ex 7d"] = d.pivot_table(index="wide", columns="cl", values="ex_fwd", aggfunc="mean")
    out["wide x close pos n"] = d.pivot_table(index="wide", columns="cl", values="ex_fwd", aggfunc="size")
    # close pos quintile by trend
    d["cq"] = pd.qcut(d.clpos, 5, labels=False, duplicates="drop")
    out["close pos quintile x trend mean ex 7d"] = d.pivot_table(index="cq", columns="trend", values="ex_fwd", aggfunc="mean")
    out["close pos quintile x trend n"] = d.pivot_table(index="cq", columns="trend", values="ex_fwd", aggfunc="size")
    out["close pos quintile by coin top-minus-bottom"] = d.groupby("coin").apply(
        lambda s: s[s.cq == 4].ex_fwd.mean() - s[s.cq == 0].ex_fwd.mean())
    return out
