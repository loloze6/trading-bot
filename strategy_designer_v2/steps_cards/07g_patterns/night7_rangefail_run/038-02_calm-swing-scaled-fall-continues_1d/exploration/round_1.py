def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            s5 = r5 / (sd20 * np.sqrt(5))
            f5 = c.shift(-5) / c - 1
            r1d = r1
            rng = (b["high"] - b["low"]) / c
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "s5": s5, "r5": r5,
                               "r1": r1d, "sd20": sd20, "f5": f5, "calm": (b["regime"] != "chop").astype(int),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float), "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "day": ts.dt.floor("D"), "rng": rng, "rng20": rng.rolling(20).mean()})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[(d["pos"] % 5 == 0) & d["f5"].notna() & d["s5"].notna()].copy()
    g["ex"] = g["f5"] - g.groupby("coin")["f5"].transform("mean")
    def tday(x):
        s = x.groupby(x.index).sum() if False else x
        return s
    def summ(sub):
        # day-clustered t of mean excess
        dd = sub.groupby("day")["ex"].sum()
        n = len(sub)
        m = sub["ex"].mean()
        se = np.sqrt((dd ** 2).sum()) / n if n > 1 else np.nan
        return pd.Series({"n": n, "days": sub["day"].nunique(), "mean_ex%": 100 * m, "t_day": m / se if se > 0 else np.nan})
    out = {}
    g["sbin"] = pd.cut(g["s5"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["ex by scaled5 bin x calm"] = g.groupby(["calm", "sbin"], observed=True).apply(summ)
    # slope of ex on s5 by calm
    res = {}
    for cm, sub in g.groupby("calm"):
        x = sub["s5"].values; y = sub["ex"].values
        X = np.c_[np.ones_like(x), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        sc = pd.DataFrame(X * e[:, None]).groupby(sub["day"].values).sum().values
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ (sc.T @ sc) @ XtXi
        res[cm] = {"slope%": 100 * beta[1], "t": beta[1] / np.sqrt(V[1, 1]), "n": len(sub)}
    out["slope ex on s5 by calm"] = pd.DataFrame(res).T
    # one-day moves: big daily return scaled
    g["z1"] = g["r1"] / g["sd20"]
    g["zbin"] = pd.cut(g["z1"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["ex by 1d z bin x calm"] = g.groupby(["calm", "zbin"], observed=True).apply(summ)
    # range compression
    g["rr"] = g["rng"] / g["rng20"]
    g["rrbin"] = pd.qcut(g["rr"], 5)
    out["ex by range ratio quintile"] = g.groupby("rrbin", observed=True).apply(summ)
    # vol level
    g["vbin"] = pd.qcut(g["sd20"], 5)
    out["ex by sd20 quintile"] = g.groupby("vbin", observed=True).apply(summ)
    # weekday daily return
    dd = d.dropna(subset=["r1"])
    out["daily ret by weekday"] = dd.groupby("wd")["r1"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["ex by year"] = g.groupby("yr").apply(summ)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            br.append(x.assign(coin=coin, win=w))
    br = pd.concat(br)
    br["side"] = 0
    out["book daily mean by window"] = br.groupby("win")[["book_return", "coin_return"]].mean() * 100
    return out
