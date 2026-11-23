def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20, min_periods=10).std()
            vol120 = r.rolling(120, min_periods=60).std()
            vratio = np.log(vol20 / vol120)
            z = r / vol20.shift(1)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (2 * c - b["high"] - b["low"]) / rng
            v = b["volume"].astype(float)
            vrel = np.log(v / v.shift(1).rolling(20, min_periods=10).mean())
            nxt = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"], utc=True)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "z": z, "clv": clv, "vrel": vrel,
                "vratio": vratio, "vol20": vol20, "nxt": nxt, "year": ts.dt.year, "wd": ts.dt.dayofweek,
                "alloc": b["postRebalance_current_allocation"].astype(float)}))
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d = d.dropna(subset=["z", "clv", "vrel", "ex", "vratio"])
    def summ(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    d["vrq"] = pd.qcut(d["vratio"], 3, labels=False)
    out["all days by vol ratio tercile (past-only)"] = d.groupby("vrq").apply(summ)
    f = d[d["z"] < -1].copy()
    out["falls z<-1 by vol ratio tercile"] = f.groupby("vrq").apply(summ)
    f["zb"] = pd.cut(f["z"], [-99, -2, -1.5, -1])
    out["falls depth x vol ratio"] = f.groupby(["vrq", "zb"]).apply(summ).reset_index()
    out["falls high vratio by year"] = f[f["vrq"] == 2].groupby("year").apply(summ)
    out["falls high vratio by coin"] = f[f["vrq"] == 2].groupby("coin").apply(summ)
    # regression per standardized vars
    X = d[["z", "clv", "vrel"]].copy()
    X["clv_x_v"] = d["clv"] * d["vrel"]
    X["z_x_vr"] = d["z"].clip(upper=0) * d["vratio"]
    X = (X - X.mean()) / X.std()
    X["const"] = 1.0
    y = d["ex"].values
    beta, *_ = np.linalg.lstsq(X.values, y, rcond=None)
    res = y - X.values @ beta
    s2 = res.var(ddof=X.shape[1])
    cov = s2 * np.linalg.inv(X.values.T @ X.values)
    out["regression ex (coef in %/sd)"] = pd.DataFrame({"coef%": 100*beta, "t": beta/np.sqrt(np.diag(cov))}, index=X.columns)
    # low close + heavy volume, outside big falls
    nf = d[d["z"] > -1].copy()
    nf["clvq"] = pd.qcut(nf["clv"], 3, labels=False)
    nf["vq"] = pd.qcut(nf["vrel"], 3, labels=False)
    out["non-falls clv x vol"] = nf.groupby(["vq", "clvq"]).apply(summ).reset_index()
    hv = d[(d["vrel"] > d["vrel"].quantile(2/3)) & (d["clv"] < d["clv"].quantile(0.2))]
    out["heavy vol low close by year"] = hv.groupby("year").apply(summ)
    out["weekday by year half"] = d.assign(h=(d["year"] >= 2022).astype(int)).groupby(["h", "wd"]).apply(summ).reset_index()
    return out
