def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        b = b.reset_index(drop=True).copy()
        c = b["close"].astype(float)
        r1 = c.pct_change()
        vol30 = r1.rolling(30, min_periods=20).std()
        b["z1"] = r1 / vol30
        b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
        rng = (b["high"] - b["low"]) / c
        b["rngz"] = rng / rng.rolling(30, min_periods=20).mean()
        b["z2"] = (c / c.shift(2) - 1) / (vol30 * np.sqrt(2))
        b["volratio"] = vol30 / r1.rolling(180, min_periods=60).std()
        for h in (1, 2):
            b[f"f{h}"] = c.shift(-h) / c - 1
        b["fz1"] = b["f1"] / vol30
        b["pos"] = np.arange(len(b)); b["win"] = w
        ts = pd.to_datetime(b["timestamp"])
        b["wd"] = ts.dt.weekday; b["yr"] = ts.dt.year
        b["alloc"] = b["postRebalance_current_allocation"]
        b["fc"] = b["forecast"]
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out = {}
    g = B.dropna(subset=["z1", "clv", "f1", "fz1"]).copy()
    mu1 = B["f1"].mean()
    g["ex"] = g["f1"] - mu1
    # multivariate: ex1 scaled by vol on z1 and clv
    X = np.column_stack([np.ones(len(g)), g["z1"], g["clv"] - 0.5])
    y = g["fz1"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg fz1 ~ z1 + clv"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z1", "clv"]).round(4)
    # by year correlations
    def yc(col, tgt="fz1"):
        r = []
        for y_, gg in g.groupby("yr"):
            rr = gg[col].corr(gg[tgt]); n = len(gg)
            r.append((y_, rr, rr * np.sqrt((n - 2) / (1 - rr ** 2)), n))
        return pd.DataFrame(r, columns=["yr", "corr", "t", "n"]).set_index("yr").round(3)
    out["z1 -> next day, by year"] = yc("z1")
    out["clv -> next day, by year"] = yc("clv")
    # clv within up and down days
    for nm, cond in (("down", g["z1"] < 0), ("up", g["z1"] > 0)):
        gg = g[cond].copy()
        gg["bin"] = pd.qcut(gg["clv"], 4, labels=False)
        t = gg.groupby("bin").agg(mean_ex=("ex", "mean"), sd=("ex", "std"), n=("ex", "size"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        rr = gg["clv"].corr(gg["fz1"])
        t["corr"] = rr; t["corr_t"] = rr * np.sqrt((len(gg) - 2) / (1 - rr ** 2))
        out[f"clv on {nm} days -> f1"] = t.drop(columns="sd").round(4)
    # z1 graded by vol ratio
    gv = g.dropna(subset=["volratio"]).copy()
    gv["vb"] = pd.qcut(gv["volratio"], 3, labels=False)
    r = []
    for vb, gg in gv.groupby("vb"):
        rr = gg["z1"].corr(gg["fz1"]); n = len(gg)
        r.append((vb, gg["volratio"].median(), rr, rr * np.sqrt((n - 2) / (1 - rr ** 2)), n))
    out["z1->f1 corr by volratio tercile"] = pd.DataFrame(r, columns=["vb", "med", "corr", "t", "n"]).round(3)
    # 2-day horizon grid
    g2 = B[B["pos"] % 2 == 0].dropna(subset=["z1", "clv", "f2"]).copy()
    g2["ex"] = g2["f2"] - B[B["pos"] % 2 == 0]["f2"].mean()
    for col in ("z1", "clv", "z2"):
        rr, _ = stats.pearsonr(g2[col], g2["ex"])
        out[f"{col} -> f2 corr_t"] = round(float(rr * np.sqrt((len(g2) - 2) / (1 - rr ** 2))), 3)
    # size of strongest case: combined score
    g["score"] = -(g["z1"]) + -(g["clv"] - 0.5) * 2
    g["sb"] = pd.qcut(g["score"], 5, labels=False)
    t = g.groupby("sb").agg(mean_f1=("f1", "mean"), mean_ex=("ex", "mean"), sd=("ex", "std"), n=("ex", "size"))
    t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
    out["combined score quintile -> f1"] = t.drop(columns="sd").round(4)
    out["mean f1 all"] = round(float(mu1), 5)
    # weekday by halves of years
    g["half"] = np.where(g["yr"] <= 2021, "2018-21", "2022-25")
    wd = g.groupby(["half", "wd"])["ex"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday ex by half"] = wd.drop(columns="std").round(4)
    # book: next-day return of book after the largest coin down days
    out["alloc mean by z1 quintile (same bar)"] = g.groupby(pd.qcut(g["z1"], 5, labels=False))["alloc"].mean().round(3)
    return out
