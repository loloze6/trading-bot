def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r,
                "r1": r.shift(-1), "r2": r.shift(-2), "r3": r.shift(-3),
            })
            d["z"] = r / r.abs().rolling(60, min_periods=20).mean()
            rng = (b["high"] - b["low"]).astype(float)
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan)) * 2 - 1
            d["vrel"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            d["r5"] = c / c.shift(5) - 1
            d["agit"] = (b["regime"] != "chop").astype(int)
            d["wd"] = d["day"].dt.weekday
            d["year"] = d["day"].dt.year
            d["pos"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    for k in ["r1", "r2", "r3"]:
        D[k + "x"] = D[k] - D["coin"].map(mu)
    D["dayid"] = D["day"].astype("int64")

    def cl_ols(df, y, xs):
        df = df.dropna(subset=[y] + xs)
        if len(df) < 30:
            return {"n": len(df)}
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        Y = df[y].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ Y
        e = Y - X @ b
        g = df["dayid"].values
        S = np.zeros((X.shape[1], X.shape[1]))
        for gg in np.unique(g):
            m = g == gg
            s = X[m].T @ e[m]
            S += np.outer(s, s)
        G = len(np.unique(g)); N, K = X.shape
        V = XtX @ S @ XtX * G / (G - 1) * (N - 1) / (N - K)
        t = b / np.sqrt(np.diag(V))
        out = {"n": N, "days": G}
        for i, x in enumerate(["const"] + xs):
            out["b_" + x] = b[i]; out["t_" + x] = t[i]
        return out

    res = {}
    reg = []
    for a in [1, 0]:
        for side, m in [("down", D["z"] < 0), ("up", D["z"] > 0)]:
            sub = D[(D["agit"] == a) & m]
            for y in ["r1x", "r2x", "r3x"]:
                o = cl_ols(sub, y, ["z"]); o.update({"agit": a, "side": side, "y": y})
                reg.append(o)
        sub = D[D["agit"] == a]
        o = cl_ols(sub, "r1x", ["z", "clv"]); o.update({"agit": a, "side": "both+clv", "y": "r1x"}); reg.append(o)
        o = cl_ols(sub, "r1x", ["z"]); o.update({"agit": a, "side": "both", "y": "r1x"}); reg.append(o)
    res["regressions"] = pd.DataFrame(reg).set_index(["agit", "side", "y"]).round(5)

    D["zq"] = pd.qcut(D["z"], 10, labels=False)
    res["decile_next"] = D.groupby(["zq", "agit"]).agg(
        z=("z", "mean"), r1x=("r1x", "mean"), n=("r1x", "count")).unstack("agit").round(4)

    # interactions on agitated down days
    ad = D[(D["agit"] == 1) & (D["z"] < 0)].copy()
    ad["zv"] = ad["z"] * np.log(ad["vrel"])
    ad["z5"] = ad["z"] * ad["r5"]
    res["agit_down_vol_inter"] = pd.Series(cl_ols(ad, "r1x", ["z", "zv"])).round(4)
    res["agit_down_r5"] = pd.Series(cl_ols(ad, "r1x", ["z", "r5"])).round(4)
    res["agit_down_weekday"] = ad.groupby("wd")["r1x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    res["agit_down_year"] = ad.groupby("year")["r1x"].agg(["mean", "count"]).round(4)
    res["agit_down_coin"] = ad.groupby("coin").apply(lambda s: pd.Series(cl_ols(s, "r1x", ["z"]))[["n", "b_z", "t_z"]]).round(4)

    # book's largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    B = pd.concat(dd, ignore_index=True)
    B["prev_coin"] = B.groupby(["coin"])["coin_return"].shift(1)
    B = B.dropna(subset=["book_return"])
    act = B[B["book_return"] != 0]
    q = act["book_return"].quantile([0.05, 0.95])
    res["book_tails"] = pd.DataFrame({
        "worst5": act[act["book_return"] <= q.iloc[0]][["book_return", "coin_return", "prev_coin"]].mean(),
        "best5": act[act["book_return"] >= q.iloc[1]][["book_return", "coin_return", "prev_coin"]].mean(),
        "all_active": act[["book_return", "coin_return", "prev_coin"]].mean(),
    }).round(4)
    res["book_by_weekday"] = act.groupby(pd.to_datetime(act["day"]).dt.weekday)["book_return"].agg(["mean", "count"]).round(5)
    return res
