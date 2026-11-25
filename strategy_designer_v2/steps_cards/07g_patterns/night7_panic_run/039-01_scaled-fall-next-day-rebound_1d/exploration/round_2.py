def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": z, "z_prev": z.shift(1),
                "fwd1": r.shift(-1),
                "ret5": c / c.shift(5) - 1,
                "ret5sd": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "ret60": c / c.shift(60) - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "vrel": b["volume"] / b["volume"].rolling(30, min_periods=20).mean(),
                "sdrel": sd / sd.rolling(90, min_periods=40).median(),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["fwd1"].mean()
    d["ex1"] = d["fwd1"] - d["coin"].map(mu)
    d["day"] = d["ts"].dt.floor("D")
    d["yr"] = d["ts"].dt.year

    def ols_cl(g, xcols, y="ex1"):
        g = g.dropna(subset=xcols + [y])
        X = np.column_stack([np.ones(len(g))] + [g[c].values for c in xcols])
        Y = g[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        e = Y - X @ beta
        XtX_inv = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        V = XtX_inv @ (S.T @ S) @ XtX_inv
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"coef": beta, "t_day": beta / se},
                            index=["const"] + xcols).assign(n=len(g), days=g["day"].nunique())

    def stat_cl(g):
        g = g.dropna(subset=["ex1"])
        s = g.groupby("day")["ex1"].sum() - g.groupby("day")["ex1"].size() * g["ex1"].mean()
        n = len(g)
        se = np.sqrt((s ** 2).sum()) / n if n > 1 else np.nan
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean%": 100 * g["ex1"].mean(),
                          "t_day": g["ex1"].mean() / se if se else np.nan})

    out = {}
    dn = d[d["z"] < 0].copy()
    dn["fall"] = -dn["z"]
    dn["lv"] = np.log(dn["vrel"])
    dn["fall_x_lv"] = dn["fall"] * dn["lv"]
    out["down: ex1 ~ fall"] = ols_cl(dn, ["fall"])
    out["down: ex1 ~ fall + lv + fall*lv"] = ols_cl(dn, ["fall", "lv", "fall_x_lv"])
    dn1 = dn[dn["z"] < -1]
    out["z<-1 by vrel quartile"] = dn1.groupby(pd.qcut(dn1["vrel"], 4)).apply(stat_cl)
    out["z<-1 & vrel>1.5 by year"] = dn1[dn1["vrel"] > 1.5].groupby("yr").apply(stat_cl)
    # ret5 multi-day fall
    dn["r5n"] = -dn["ret5sd"]
    out["down: ex1 ~ fall + r5n"] = ols_cl(dn, ["fall", "r5n"])
    d["r5n"] = -d["ret5sd"]
    out["all: ex1 ~ r5n"] = ols_cl(d, ["r5n"])
    out["all: by ret5sd bin"] = d.groupby(pd.cut(d["ret5sd"], [-np.inf, -2, -1, 0, 1, 2, np.inf])).apply(stat_cl)
    out["ret5sd<-1 by year"] = d[d["ret5sd"] < -1].groupby("yr").apply(stat_cl)
    # close location
    d["lowclose"] = 0.5 - d["clv"]
    out["all: ex1 ~ lowclose + z"] = ols_cl(d, ["lowclose", "z"])
    out["up days: ex1 ~ lowclose"] = ols_cl(d[d["z"] > 0], ["lowclose"])
    out["clv<0.3 by year"] = d[d["clv"] < 0.3].groupby("yr").apply(stat_cl)
    out["clv>0.7 by year"] = d[d["clv"] > 0.7].groupby("yr").apply(stat_cl)
    # rebound fade
    fd = d[(d["z_prev"] < -1) & (d["z"] > 0)].copy()
    out["fade: by rebound z"] = fd.groupby(pd.cut(fd["z"], [0, 0.5, 1, 2, np.inf])).apply(stat_cl)
    out["fade: ex1 ~ z"] = ols_cl(fd, ["z"])
    out["fade by year"] = fd.groupby("yr").apply(stat_cl)
    out["up day after up/down prev"] = d[d["z"] > 0].groupby(pd.cut(d["z_prev"], [-np.inf, -1, 0, 1, np.inf])).apply(stat_cl)
    # agitation
    out["z<-1 by sdrel>1"] = dn1.groupby(dn1["sdrel"] > 1).apply(stat_cl)
    dn["agit"] = (dn["sdrel"] > 1).astype(float)
    dn["fall_x_agit"] = dn["fall"] * dn["agit"]
    out["down: ex1 ~ fall + agit + fall*agit"] = ols_cl(dn, ["fall", "agit", "fall_x_agit"])
    out["z<-1 & sdrel>1 by year"] = dn1[dn1["sdrel"] > 1].groupby("yr").apply(stat_cl)
    return out
