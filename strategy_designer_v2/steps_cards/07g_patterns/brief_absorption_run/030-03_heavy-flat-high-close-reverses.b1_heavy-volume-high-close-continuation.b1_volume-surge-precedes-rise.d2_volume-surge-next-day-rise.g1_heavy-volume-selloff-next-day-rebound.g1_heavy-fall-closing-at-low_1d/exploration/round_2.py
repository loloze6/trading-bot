def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = np.concatenate([pd.Series(b["close"].astype(float).values).pct_change().dropna().values for b in wins.values()])
        mu = allr.mean(); sd = allr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            h, l, c, v = [b[k].astype(float) for k in ["high","low","close","volume"]]
            ts = pd.to_datetime(b["timestamp"])
            r = c.pct_change()
            vr = v / v.shift(1).rolling(20).mean()
            rng = (h - l).replace(0, np.nan)
            cl = (c - l) / rng
            vol20 = r.rolling(20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "vr": vr, "cl": cl, "vol20": vol20,
                               "vrel": vol20 / sd, "z": r / vol20, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "pos": np.arange(len(b))})
            df["f1"] = c.shift(-1) / c - 1 - mu
            for k in [2, 3]:
                df[f"f{k}"] = c.shift(-k) / c - 1 - k * mu
            df["f1n"] = df["f1"] / vol20
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(g, col="f1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    def ols(df, y, xs):
        d = df[[y] + xs].replace([np.inf, -np.inf], np.nan).dropna()
        X = np.column_stack([np.ones(len(d))] + [d[x].values for x in xs])
        beta, *_ = np.linalg.lstsq(X, d[y].values, rcond=None)
        res = d[y].values - X @ beta
        s2 = res @ res / (len(d) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"coef": beta, "t": beta / se}, index=["const"] + xs).assign(n=len(d))
    dn = D[D.r < 0].copy()
    dn["clow"] = 1 - dn["cl"]
    dn["lvr"] = np.log(dn["vr"])
    dn["clow_lvr"] = dn["clow"] * dn["lvr"]
    out["down days: f1 on z, clow, lvr, product"] = ols(dn, "f1", ["z", "clow", "lvr", "clow_lvr"])
    out["down days: f1 on r, vol20, r*vrel"] = ols(dn.assign(rv=dn.r * dn.vrel), "f1", ["r", "vrel", "rv"])
    out["all days: f1 on r, r*vrel"] = ols(D.assign(rv=D.r * D.vrel), "f1", ["r", "rv"])
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    D["rq"] = D.groupby("volq")["r"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["high-vol tercile: next day by r quintile"] = D[D.volq == 2].groupby("rq").apply(summ)
    out["low-vol tercile: next day by r quintile"] = D[D.volq == 0].groupby("rq").apply(summ)
    hv = D[D.volq == 2].copy(); hv["sgn"] = -np.sign(hv["r"]); hv["rev"] = hv["sgn"] * hv["f1"]
    out["high-vol reversal by year"] = hv.groupby("yr").apply(lambda g: summ(g, "rev"))
    out["high-vol reversal by coin"] = hv.groupby("coin").apply(lambda g: summ(g, "rev"))
    out["high-vol reversal horizons (grid)"] = pd.DataFrame({k: summ(hv.assign(x=hv["sgn"] * hv[k])[hv.pos % int(k[1:]) == 0], "x") for k in ["f1", "f2", "f3"]}).T
    out["weekday by year (t)"] = D.groupby(["yr", "wd"]).apply(lambda g: summ(g)["t"]).unstack()
    dd = D[D.r < 0]
    out["forecast distribution down days"] = dd["fc"].describe()
    top = dd[dd.fc >= dd.fc.quantile(0.8)]
    out["top-fifth by vol tercile"] = top.groupby("volq").apply(summ)
    out["top-fifth by year"] = top.groupby("yr").apply(summ)
    # held days after signal: allocation > 0 on bars where forecast 0
    D["held_nofc"] = (D.alloc.abs() > 0.01) & (D.fc == 0)
    out["next day when held with forecast 0 vs >0"] = D[D.alloc.abs() > 0.01].groupby("held_nofc").apply(summ)
    return out
