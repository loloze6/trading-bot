def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "r1": r.shift(-1), "r3": r.shift(-3)})
            d["z"] = r / r.abs().rolling(60, min_periods=20).mean()
            d["vrel"] = b["volume"].astype(float) / b["volume"].astype(float).rolling(20, min_periods=10).mean()
            d["agit"] = (b["regime"] != "chop").astype(int)
            d["wd"] = d["day"].dt.weekday
            d["year"] = d["day"].dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["r1x"] = D["r1"] - D["coin"].map(mu)
    D["r3x"] = D["r3"] - D["coin"].map(mu)
    D["dayid"] = D["day"].astype("int64")
    D["lv"] = np.log(D["vrel"])
    D["zv"] = D["z"] * D["lv"]

    def cl_ols(df, y, xs):
        df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=[y] + xs)
        if len(df) < 30:
            return {"n": len(df)}
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        Y = df[y].values
        XtX = np.linalg.inv(X.T @ X); bb = XtX @ X.T @ Y; e = Y - X @ bb
        g = df["dayid"].values
        S = np.zeros((X.shape[1],) * 2)
        for gg in np.unique(g):
            m = g == gg; s = X[m].T @ e[m]; S += np.outer(s, s)
        G = len(np.unique(g)); N, K = X.shape
        V = XtX @ S @ XtX * G / (G - 1) * (N - 1) / (N - K)
        t = bb / np.sqrt(np.diag(V))
        out = {"n": N, "days": G}
        for i, x in enumerate(["const"] + xs):
            out["b_" + x] = bb[i]; out["t_" + x] = t[i]
        return out

    res = {}
    reg = []
    for a in [1, 0]:
        for side, m in [("down", D["z"] < 0), ("up", D["z"] > 0)]:
            sub = D[(D["agit"] == a) & m]
            for xs in [["z", "zv"], ["zv"], ["z", "lv"]]:
                o = cl_ols(sub, "r1x", xs); o.update({"agit": a, "side": side, "xs": "+".join(xs)}); reg.append(o)
    res["vol_regs"] = pd.DataFrame(reg).set_index(["agit", "side", "xs"]).round(4)

    ad = D[(D["agit"] == 1) & (D["z"] < 0)].replace([np.inf, -np.inf], np.nan).dropna(subset=["lv", "r1x"]).copy()
    ad["fq"] = pd.qcut(-ad["z"], 3, labels=["small", "mid", "large"])
    ad["vq"] = pd.qcut(ad["lv"], 3, labels=["lowV", "midV", "highV"])
    res["agit_down_fall_x_vol"] = ad.pivot_table(index="fq", columns="vq", values="r1x", aggfunc="mean").round(4)
    res["agit_down_fall_x_vol_n"] = ad.pivot_table(index="fq", columns="vq", values="r1x", aggfunc="count")
    res["zv_by_coin"] = ad.groupby("coin").apply(lambda s: pd.Series(cl_ols(s, "r1x", ["zv"]))[["n", "b_zv", "t_zv"]]).round(4)
    res["zv_by_year"] = ad.groupby("year").apply(lambda s: pd.Series(cl_ols(s, "r1x", ["zv"]))[["n", "b_zv", "t_zv"]]).round(4)

    # weekday of agitated down days with grading
    res["z_by_weekday"] = ad.groupby("wd").apply(lambda s: pd.Series(cl_ols(s, "r1x", ["z"]))[["n", "b_const", "b_z", "t_z"]]).round(4)
    au = D[(D["agit"] == 1) & (D["z"] > 0)]
    res["agit_up_weekday_mean"] = au.groupby("wd")["r1x"].agg(["mean", "count"]).round(4)
    return res
