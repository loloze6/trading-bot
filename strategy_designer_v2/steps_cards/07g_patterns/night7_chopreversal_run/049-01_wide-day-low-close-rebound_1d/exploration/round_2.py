def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l); r = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "ret1": c.shift(-1) / c - 1, "ret3": c.shift(-3) / c - 1,
                "r0": r, "r60": c / c.shift(60) - 1,
                "clv": (c - l) / rng.replace(0, np.nan),
                "rm": rng / rng.shift(1).rolling(30, min_periods=20).mean(),
                "z0": r / r.shift(1).rolling(30, min_periods=20).std(),
                "vol30": r.rolling(30, min_periods=20).std(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "pos": np.arange(len(b)),
            })
            d["volpct"] = d["vol30"].rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            d["gain"] = d["alloc"] * d["ret1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["ret1"].mean()
    D["ex1"] = D["ret1"] - D["coin"].map(mu1)
    D["day"] = D["ts"].dt.floor("D")
    out = {}
    def tday(s, dd):
        x = pd.DataFrame({"v": s, "d": dd}).dropna().groupby("d")["v"].sum()
        n = len(x)
        return x.mean() / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
    E = D.dropna(subset=["ex1", "clv", "rm", "z0"]).copy()
    E["sig"] = (0.5 - E["clv"]) * E["rm"]
    E["neg_z"] = -E["z0"]
    # multiple regression: ex1 on sig and -z0
    X = np.column_stack([np.ones(len(E)), E["sig"], E["neg_z"]])
    beta, *_ = np.linalg.lstsq(X, E["ex1"].values, rcond=None)
    res = E["ex1"].values - X @ beta
    # day-clustered se
    XtXi = np.linalg.inv(X.T @ X)
    g = pd.DataFrame(X * res[:, None]).groupby(E["day"].values).sum().values
    V = XtXi @ (g.T @ g) @ XtXi * len(g) / (len(g) - 1)
    out["joint reg ex1 on sig, -z0 (coef%, t)"] = pd.DataFrame({"coef%": beta * 100, "t": beta / np.sqrt(np.diag(V))}, index=["const", "sig", "neg_z"]).round(3)
    # agitation split
    E["agit"] = np.where(E["volpct"] > 0.5, "agitated", "calm")
    E.loc[E["volpct"].isna(), "agit"] = np.nan
    E["trend"] = pd.cut(E["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    rr = {}
    for k, s in list(E.dropna(subset=["agit"]).groupby("agit")) + list(E.dropna(subset=["trend"]).groupby("trend", observed=True)):
        sl = stats.linregress(s["sig"], s["ex1"])
        rr[k] = (sl.slope * 100, tday(s["sig"] * (s["ex1"] - s["ex1"].mean()), s["day"]), len(s))
    out["slope ex1 on sig by profile (slope%, t_day approx, n)"] = pd.DataFrame(rr, index=["slope%", "t", "n"]).T.round(3)
    # sides separated: low-close side vs high-close side, in agitation
    E["side"] = np.where(E["clv"] < 0.5, "lowclose", "highclose")
    E["rmq"] = pd.qcut(E["rm"], 3, labels=["narrow", "mid", "wide"])
    tab = {}
    for k, s in E.dropna(subset=["agit"]).groupby(["agit", "side", "rmq"], observed=True):
        tab[k] = (s["ex1"].mean() * 100, tday(s["ex1"], s["day"]), len(s))
    out["ex1 % by agitation x side x width (mean, t, n)"] = pd.DataFrame(tab, index=["mean%", "t", "n"]).T.round(3)
    # big down day by z, terciles within low close
    E["zq"] = pd.qcut(E["z0"], 5, labels=False)
    tz = {}
    for k, s in E.groupby("zq"):
        tz[k] = (s["ex1"].mean() * 100, tday(s["ex1"], s["day"]), len(s))
    out["ex1 % by today's z-return quintile (mean, t, n)"] = pd.DataFrame(tz, index=["mean%", "t", "n"]).T.round(3)
    # 3-day horizon on non-overlapping grid, sig quintile
    G = E[E["pos"] % 3 == 0].dropna(subset=["ret3"]).copy()
    mu3 = D[D["pos"] % 3 == 0].groupby("coin")["ret3"].mean()
    G["ex3"] = G["ret3"] - G["coin"].map(mu3)
    G["sq"] = pd.qcut(G["sig"], 5, labels=False)
    t3 = {}
    for k, s in G.groupby("sq"):
        t3[k] = (s["ex3"].mean() * 100, tday(s["ex3"], s["day"]), len(s))
    out["ex3 % by sig quintile, 3-day grid (mean, t, n)"] = pd.DataFrame(t3, index=["mean%", "t", "n"]).T.round(3)
    # book: daily returns, worst/best days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"]
    out["book: share of total gain from top 5% days, bottom 5% days"] = pd.Series({
        "top5%share": q[q >= q.quantile(0.95)].sum() / q.sum(),
        "bot5%share": q[q <= q.quantile(0.05)].sum() / q.sum(),
        "corr book vs coins": q.corr(bk["coin_return"]),
        "book mean on coin-up days%": q[bk["coin_return"] > 0].mean() * 100,
        "book mean on coin-down days%": q[bk["coin_return"] <= 0].mean() * 100}).round(3)
    return out
