def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42, "14d":84}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            rng = (df["high"] - df["low"]) / c
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=30).mean()
            z = r6 / mabs
            rr = rng.rolling(6).mean() / rng.rolling(180, min_periods=30).mean()
            r1d_prev = c / c.shift(6) - 1
            r7prev = c / c.shift(42) - 1
            vol = np.log(c).diff().rolling(180, min_periods=30).std()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "z": z, "rr": rr, "prev7": r7prev, "vol": vol,
                              "hour": pd.to_datetime(df["timestamp"]).dt.hour,
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                              "fc": df["forecast"]})
            for k, h in H.items():
                d["f" + k] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # coin means per horizon on non-overlapping grid
    for k, h in H.items():
        g = A[A["pos"] % h == 0]
        m = g.groupby("coin")["f" + k].mean()
        A["x" + k] = A["f" + k] - A["coin"].map(m)
    def summ(sub, col):
        s = sub[col].dropna()
        n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    # 1: graded by scaled 24h fall, 3d horizon, all bars on grid 18
    g18 = A[A["pos"] % 18 == 0].dropna(subset=["z", "rr", "x3d"]).copy()
    g18["zq"] = pd.cut(g18["z"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    out["x3d by scaled 24h return"] = g18.groupby("zq", observed=True).apply(lambda s: summ(s, "x3d"))
    g18["rq"] = pd.cut(g18["rr"], [0, 0.7, 1, 1.5, 2, 3, np.inf])
    out["x3d by range ratio (all bars)"] = g18.groupby("rq", observed=True).apply(lambda s: summ(s, "x3d"))
    # 2: falls z<=-2 split by range ratio
    f = g18[g18["z"] <= -2]
    out["x3d falls z<=-2 by range ratio"] = f.groupby("rq", observed=True).apply(lambda s: summ(s, "x3d"))
    # 3: panic horizons on own grids
    res = {}
    for k, h in H.items():
        g = A[(A["pos"] % h == 0) & (A["z"] <= -2) & (A["rr"] >= 3)]
        res[k] = summ(g, "x" + k)
        res[k + "_fall_only_z<=-2"] = summ(A[(A["pos"] % h == 0) & (A["z"] <= -2)], "x" + k)
    out["horizons panic vs fall"] = pd.DataFrame(res).T
    # 4: within falls, correlation with z, rr, prev7
    ff = f.dropna(subset=["prev7"])
    out["falls corr"] = pd.DataFrame({c_: [stats.spearmanr(ff[c_], ff["x3d"])[0], stats.spearmanr(ff[c_], ff["x3d"])[1]] for c_ in ["z", "rr", "prev7", "vol"]}, index=["rho", "p"])
    # 5: rises symmetric
    up = g18[g18["z"] >= 2]
    out["rises z>=2 by range ratio"] = up.groupby("rq", observed=True).apply(lambda s: summ(s, "x3d"))
    # 6: falls by coin
    out["falls z<=-2 by coin"] = f.groupby("coin").apply(lambda s: summ(s, "x3d"))
    # 7: hour and weekday of all bars, 1d horizon grid 6
    g6 = A[A["pos"] % 6 == 0]
    out["x1d by weekday (grid6)"] = g6.groupby("wd").apply(lambda s: summ(s, "x1d"))
    # 8: book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    b = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily"] = pd.Series({"mean_book": b["book_return"].mean(), "mean_coin": b["coin_return"].mean(),
                                   "corr": b.corr().iloc[0, 1], "n_days": len(b),
                                   "share_days_flat": (b["book_return"].abs() < 1e-9).mean()})
    alloc = pd.concat([bars[c][w]["postRebalance_current_allocation"] for c in bars for w in bars[c]])
    out["allocation"] = alloc.describe()
    return out
