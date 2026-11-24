def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            r0 = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": (c - l) / rng.replace(0, np.nan), "r0": r0,
                "rngp": rng / c.shift(1),
                "ret60": c / c.shift(60) - 1,
                "vol30": r0.rolling(30, min_periods=20).std(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
            })
            d["volpct"] = d["vol30"].rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            d["z0"] = d["r0"] / d["vol30"].shift(1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f2"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["day"] = D["ts"].dt.floor("D")
    D["sig"] = 0.5 - D["clv"]
    D["rev"] = -D["z0"].clip(-4, 4)
    out = {}

    def tday(df, col):
        s = df.groupby("day")[col].sum().dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "days": len(s)})

    def bt(df, by, col="f1x"):
        g = df.dropna(subset=[col]).groupby(by)[col]
        return pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100, "t": g.mean() / (g.std() / np.sqrt(g.size()))})

    E = D.dropna(subset=["f1x", "z0", "clv", "rngp"]).copy()
    # multivariate: f1x on sig, rev
    X = np.column_stack([np.ones(len(E)), E["sig"], E["rev"] / 1.0])
    beta, *_ = np.linalg.lstsq(X, E["f1x"].values, rcond=None)
    res = E["f1x"].values - X @ beta
    # per-day clustered-ish t via per-day sum of score
    tabs = {}
    for i, nm in enumerate(["const", "sig(clv)", "rev(-z)"]):
        sc = pd.Series(X[:, i] * res, index=E.index).groupby(E["day"]).sum()
        XtX_inv = np.linalg.inv(X.T @ X)
        V = XtX_inv @ (np.column_stack([pd.Series(X[:, j] * res).groupby(E["day"].values).sum() for j in range(3)]).T @ np.column_stack([pd.Series(X[:, j] * res).groupby(E["day"].values).sum() for j in range(3)])) @ XtX_inv
        tabs[nm] = {"beta": beta[i], "t_dayclust": beta[i] / np.sqrt(V[i, i])}
    out["regression f1x ~ clv + day return z"] = pd.DataFrame(tabs).T
    # z-score reversal graded
    E["zq"] = pd.qcut(E["z0"], 7)
    out["next-day excess by day-return z septile"] = bt(E, "zq")
    sub2 = E[E["pos"] % 2 == 0]
    out["2d excess by z septile (grid)"] = bt(sub2, "zq", "f2x")
    # cell counts for down day x clv
    E["dn"] = pd.cut(E["z0"], [-99, -1.5, -0.5, 0.5, 1.5, 99], labels=["bigdn", "dn", "flat", "up", "bigup"])
    E["cq"] = pd.qcut(E["clv"], 3, labels=["low", "mid", "high"])
    g = E.groupby(["dn", "cq"])["f1x"]
    out["z bucket x clv tercile: mean%"] = (g.mean() * 100).unstack()
    out["z bucket x clv tercile: n"] = g.size().unstack()
    out["z bucket x clv tercile: t"] = (g.mean() / (g.std() / np.sqrt(g.size()))).unstack()
    # reversal product by profile
    E["p"] = E["rev"] * E["f1x"]
    E["tr"] = pd.cut(E["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    E["ag"] = np.where(E["volpct"] > 0.5, "agitated", np.where(E["volpct"].notna(), "calm", np.nan))
    out["rev*f1x by trend"] = E.dropna(subset=["tr"]).groupby("tr").apply(lambda x: tday(x, "p"))
    out["rev*f1x by agitation(profile def)"] = E[E["ag"] != "nan"].groupby("ag").apply(lambda x: tday(x, "p"))
    out["rev*f1x by coin"] = E.groupby("coin").apply(lambda x: tday(x, "p"))
    out["rev*f1x by year"] = E.assign(y=E["ts"].dt.year).groupby("y").apply(lambda x: tday(x, "p"))
    E["ps"] = E["sig"] * E["f1x"]
    out["clv*f1x by agitation(profile def)"] = E[E["ag"] != "nan"].groupby("ag").apply(lambda x: tday(x, "ps"))
    # range width graded: wide range days reversal
    E["rq"] = pd.qcut(E["rngp"] / E["vol30"].shift(0), 3, labels=["narrow", "mid", "wide"])
    out["rev*f1x by range width rel vol"] = E.dropna(subset=["rq"]).groupby("rq").apply(lambda x: tday(x, "p"))
    # weekday: next-day excess by weekday of the next day, in folds windows
    E["wd_next"] = (E["ts"] + pd.Timedelta(days=1)).dt.dayofweek
    out["excess return of the day by its weekday"] = bt(E, "wd_next")
    out["excess by weekday x window-half (w7-12 vs w13-18)"] = E.assign(half=np.where(E["win"].str[1:].astype(int) <= 12, "B-ish", "C-ish")).groupby(["wd_next", "half"])["f1x"].mean().unstack() * 100
    return out
