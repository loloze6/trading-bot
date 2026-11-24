def explore(data):
    import numpy as np, pandas as pd
    recs = []
    for coin, wins in data["bars"].items():
        cd = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            ratio = rng / rng.rolling(20).mean()
            r20 = c / c.shift(20) - 1
            r3p = c / c.shift(3) - 1
            clv = (c - l) / rng.replace(0, np.nan)
            body = (c - o) / rng.replace(0, np.nan)
            vol20 = np.log(c).diff().rolling(20).std()
            fwd = c.shift(-3) / c - 1
            idx = np.arange(0, len(b), 3)
            g = pd.DataFrame({"ts": b["timestamp"].values[idx], "ratio": ratio.values[idx], "r20": r20.values[idx],
                              "r3p": r3p.values[idx], "clv": clv.values[idx], "body": body.values[idx],
                              "vol20": vol20.values[idx], "fwd": fwd.values[idx]})
            g["coin"] = coin; g["win"] = w
            cd.append(g)
        d = pd.concat(cd)
        d["ex"] = d["fwd"] - d["fwd"].mean()
        recs.append(d)
    D = pd.concat(recs).dropna(subset=["fwd", "ratio", "r20", "vol20"]).reset_index(drop=True)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    D["r20z"] = D["r20"] / (D["vol20"] * np.sqrt(20))

    def creg(df, xcols, y="ex"):
        df = df.dropna(subset=xcols + [y])
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xcols])
        Y = df[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(df["day"].values).sum().values
        G = len(sc)
        V = XtXi @ (sc.T @ sc) @ XtXi * G / max(G - 1, 1)
        t = beta / np.sqrt(np.diag(V))
        return {f"b_{n}": bb for n, bb in zip(["c"] + xcols, beta)} | {f"t_{n}": tt for n, tt in zip(["c"] + xcols, t)} | {"n": len(df), "days": G}

    res = {}
    D["lratio"] = np.log(D["ratio"])
    rows = {}
    rows["all: ex~lratio"] = creg(D, ["lratio"])
    rows["r20>0: ex~lratio"] = creg(D[D["r20"] > 0], ["lratio"])
    rows["r20<=0: ex~lratio"] = creg(D[D["r20"] <= 0], ["lratio"])
    rows["all: ex~lratio+r20z+inter"] = creg(D.assign(inter=D["lratio"] * D["r20z"]), ["lratio", "r20z", "inter"])
    W = D[D["ratio"] >= 1.5]
    rows["wide: ex~r20z"] = creg(W, ["r20z"])
    rows["wide: ex~r20"] = creg(W, ["r20"])
    rows["wide r20>0: ex~clv"] = creg(W[W["r20"] > 0], ["clv"])
    rows["wide r20>0: ex~r3p"] = creg(W[W["r20"] > 0], ["r3p"])
    rows["wide: ex~vol20"] = creg(W, ["vol20"])
    rows["notwide: ex~r20z"] = creg(D[D["ratio"] < 1.5], ["r20z"])
    rows["wide: ex~r20z, no 2020-21"] = creg(W[~W["year"].isin([2020, 2021])], ["r20z"])
    res["regressions"] = pd.DataFrame(rows).T[["n", "days", "b_c", "t_c"] + [c for c in pd.DataFrame(rows).T.columns if c.startswith(("b_", "t_")) and c not in ("b_c", "t_c")]]

    # wide by r20z quintile x clv tercile
    W = W.copy()
    W["r20zq"] = pd.qcut(W["r20z"], 4, labels=False)
    W["clvt"] = pd.cut(W["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["lowclose", "mid", "highclose"])
    out = []
    for k, g in W.groupby(["r20zq", "clvt"], observed=True):
        per = g.groupby("day")["ex"].sum()
        out.append({"g": str(k), "n": len(g), "days": len(per), "mean_ex_%": 100 * g["ex"].mean(),
                    "t_day": per.mean() / (per.std(ddof=1) / np.sqrt(len(per)))})
    res["wide_r20zq_x_close_location"] = pd.DataFrame(out)

    # by coin: wide & r20>0 mean ex
    out = []
    for k, g in W[W["r20"] > 0].groupby("coin"):
        out.append({"coin": k, "n": len(g), "mean_ex_%": 100 * g["ex"].mean()})
    res["wide_r20pos_by_coin"] = pd.DataFrame(out)

    # book: concentration of gains
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bd.append(dd.assign(coin=coin, win=w))
    B = pd.concat(bd).dropna(subset=["book_return"])
    br = B.groupby("day")["book_return"].mean().sort_values()
    tot = br.sum()
    res["book_concentration"] = pd.Series({"days": len(br), "sum_%": 100 * tot,
                                           "top10_days_sum_%": 100 * br.tail(10).sum(),
                                           "top30_days_sum_%": 100 * br.tail(30).sum(),
                                           "worst10_days_sum_%": 100 * br.head(10).sum()})
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    T["dur_d"] = T["duration_minutes"] / 1440
    res["trades_by_entry_forecast"] = T.groupby("fq", observed=True).agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
        dur=("dur_d", "mean"))
    return res
