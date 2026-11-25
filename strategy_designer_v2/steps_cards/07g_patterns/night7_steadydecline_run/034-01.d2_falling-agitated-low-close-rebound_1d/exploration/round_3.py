def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                              "cl": (h - c) / rng, "r0": c / c.shift(1) - 1,
                              "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c - 1})
            lr = np.log(c).diff()
            d["vol30"] = lr.rolling(30, min_periods=20).std()
            d["volrel"] = d["vol30"] / d["vol30"].rolling(120, min_periods=40).median()
            d["ret60"] = c / c.shift(60) - 1
            d["r0s"] = d["r0"] / d["vol30"]
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["x1"] = df["r1"] - df.groupby("coin")["r1"].transform("mean")
    df["x2"] = df["r2"] - df.groupby("coin")["r2"].transform("mean")
    df["day"] = df["ts"].dt.floor("D")
    df["agit"] = (df["volrel"] > 1).astype(int)
    df["trend"] = np.select([df["ret60"] > 0.1, df["ret60"] < -0.1], ["rise", "fall"], "chop")
    df.loc[df["ret60"].isna(), "trend"] = np.nan
    df["year"] = df["ts"].dt.year
    df = df.dropna(subset=["x1", "r0s", "cl"])
    df["r0c"] = df["r0s"].clip(-4, 4)
    out = {}
    def tday(s, sig, col="x1"):
        p = (-s[sig]) * s[col]
        dm = p.groupby(s["day"]).sum()
        return len(s), len(dm), dm.mean() / (dm.std() / np.sqrt(len(dm))), stats.spearmanr(-s[sig], s[col])[0]
    res = []
    for (tr, ag), s in df.dropna(subset=["trend"]).groupby(["trend", "agit"]):
        n, nd, t, rho = tday(s, "r0c")
        n2, nd2, t2, rho2 = tday(s.dropna(subset=["x2"]), "r0c", "x2")
        res.append({"trend": tr, "agit": ag, "n": n, "days": nd, "t_x1": t, "rho_x1": rho, "t_x2": t2})
    out["rev_trend_agit"] = pd.DataFrame(res)
    df["vb"] = pd.qcut(df["volrel"], 4, labels=False)
    res = []
    for k, s in df.groupby("vb"):
        n, nd, t, rho = tday(s, "r0c")
        res.append({"vb": k, "volrel_med": s.volrel.median(), "n": n, "days": nd, "t": t, "rho": rho})
    out["rev_by_volq_all"] = pd.DataFrame(res)
    ag = df[df.agit == 1]
    res = []
    for key in ["coin", "year"]:
        for k, s in ag.groupby(key):
            n, nd, t, rho = tday(s, "r0c")
            res.append({"by": key, "k": str(k), "n": n, "days": nd, "t": t, "rho": rho})
    out["rev_agit_by"] = pd.DataFrame(res)
    ag = ag.copy(); ag["rq"] = pd.qcut(ag["r0c"], 5, labels=False)
    g = []
    for k, s in ag.groupby("rq"):
        dm = s.groupby("day")["x1"].mean()
        g.append({"rq": k, "r0s_med": s.r0s.median(), "n": len(s), "days": len(dm),
                  "mean_x1_pct": 100 * s.x1.mean(), "t": dm.mean() / (dm.std() / np.sqrt(len(dm)))})
    out["agit_r0_quint"] = pd.DataFrame(g)
    # partial: cl vs r0 in agitated, day-clustered by sum of residual products
    X = np.column_stack([np.ones(len(ag)), ag["cl"] - 0.5, ag["r0c"]])
    beta, *_ = np.linalg.lstsq(X, ag["x1"].values, rcond=None)
    e = ag["x1"].values - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    sc = pd.DataFrame(X * e[:, None]).groupby(ag["day"].values).sum().values
    V = XtXi @ (sc.T @ sc) @ XtXi
    out["ols_agit_clustered"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(V))}, index=["c", "cl", "r0c"])
    return out
