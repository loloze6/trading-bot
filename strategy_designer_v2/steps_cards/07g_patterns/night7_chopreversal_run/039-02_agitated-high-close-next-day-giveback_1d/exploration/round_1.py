def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            clv = (c - l) / rng.replace(0, np.nan)
            r0 = c.pct_change()
            r1 = c.shift(-1) / c - 1
            r3 = c.shift(-3) / c - 1
            relrng = (rng / c) / (rng / c).rolling(30, min_periods=10).mean()
            vol20 = r0.rolling(20, min_periods=10).std()
            z0 = r0 / vol20
            tr = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.dayofweek, "year": ts.dt.year, "clv": clv, "r0": r0, "z0": z0, "r1": r1, "r3": r3,
                               "relrng": relrng, "tr": tr, "agit": (b["regime"] != "chop").astype(int),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu1 = d.groupby("coin")["r1"].transform("mean")
    d["x1"] = d["r1"] - mu1
    sd1 = d.groupby("coin")["r1"].transform("std")
    d["s1"] = d["x1"] / sd1

    def clt(sub, y, xs):
        s = sub.dropna(subset=[y] + xs)
        if len(s) < 50: return [np.nan] * (2 * len(xs)) + [len(s)]
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xs]); Y = s[y].values
        XtX = np.linalg.inv(X.T @ X); bta = XtX @ X.T @ Y; e = Y - X @ bta
        g = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        V = XtX @ (g.T @ g) @ XtX
        se = np.sqrt(np.diag(V))
        out = []
        for i in range(1, len(xs) + 1): out += [bta[i], bta[i] / se[i]]
        return out + [len(s)]

    res = {}
    # 1 CLV quintiles by agitation
    d["q"] = pd.qcut(d["clv"], 5, labels=False)
    t = d.dropna(subset=["s1", "q"]).groupby(["agit", "q"])["s1"].agg(["mean", "count"])
    res["std next-day by clv quintile x agit"] = t
    # 2 slopes clv alone and with day return, by agit
    out = []
    for a in [0, 1]:
        s = d[d.agit == a]
        out.append([a] + clt(s, "s1", ["clv"])[:2] + clt(s, "s1", ["clv", "z0"]))
    res["slope s1 on clv | clv+z0"] = pd.DataFrame(out, columns=["agit", "b_clv", "t_clv", "b_clv2", "t_clv2", "b_z0", "t_z0", "n"])
    # 3 interactions in agitated: by range width, by day sign, by trend
    A = d[d.agit == 1].copy()
    out = []
    A["rq"] = pd.qcut(A["relrng"], 3, labels=["narrow", "mid", "wide"])
    for k, s in A.groupby("rq"): out.append(["range_" + str(k)] + clt(s, "s1", ["clv"]))
    for k, s in A.groupby(A["r0"] > 0): out.append(["dayup_" + str(k)] + clt(s, "s1", ["clv"]))
    A["tq"] = pd.cut(A["tr"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    for k, s in A.groupby("tq"): out.append(["trend_" + str(k)] + clt(s, "s1", ["clv"]))
    for k, s in A.groupby("year"): out.append(["year_" + str(k)] + clt(s, "s1", ["clv"]))
    for k, s in A.groupby("coin"): out.append(["coin_" + str(k)] + clt(s, "s1", ["clv"]))
    res["agitated clv slope by group"] = pd.DataFrame(out, columns=["grp", "b", "t", "n"])
    # 4 day-return z (own move) reversal across all, by agit
    out = []
    for a in [0, 1]:
        s = d[d.agit == a]; out.append([a] + clt(s, "s1", ["z0"]))
    s = d; out.append(["all_wide*clv"] + clt(s.assign(i=(s.clv - 0.5) * s.relrng), "s1", ["i"]))
    res["z0 slope by agit"] = pd.DataFrame(out, columns=["agit", "b", "t", "n"])
    # 5 3-day horizon, non-overlapping grid
    g = d[d.pos % 3 == 0].copy()
    g["x3"] = (g["r3"] - g.groupby("coin")["r3"].transform("mean")) / g.groupby("coin")["r3"].transform("std")
    out = []
    for a in [0, 1]: out.append([a] + clt(g[g.agit == a], "x3", ["clv"]))
    res["3d clv slope by agit"] = pd.DataFrame(out, columns=["agit", "b", "t", "n"])
    # 6 weekday
    wd = d.dropna(subset=["s1"]).groupby("wd")["s1"].agg(["mean", "count"])
    wd["t"] = wd["mean"] / (d.dropna(subset=["s1"]).groupby("wd")["s1"].std() / np.sqrt(wd["count"]))
    res["next-day std by weekday of signal"] = wd
    # 7 large moves by sign
    d["zb"] = pd.cut(d["z0"], [-99, -2, -1, 1, 2, 99])
    res["s1 after z0 bins x agit"] = d.dropna(subset=["s1", "zb"]).groupby(["agit", "zb"])["s1"].agg(["mean", "count"])
    # 8 book
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    bk = bd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk = bk.sort_values("book_return")
    n = len(bk); tot = bk["book_return"].sum()
    res["book summary"] = pd.Series({"days": n, "mean": bk.book_return.mean(), "sum": tot,
                                     "sum top5%": bk.book_return.iloc[-int(n * .05):].sum(),
                                     "sum bottom5%": bk.book_return.iloc[:int(n * .05)].sum(),
                                     "corr book coin": bk.corr().iloc[0, 1]})
    bk2 = bk.reset_index(); bk2["wd"] = pd.to_datetime(bk2["day"]).dt.dayofweek
    res["book by weekday"] = bk2.groupby("wd")["book_return"].agg(["mean", "count"])
    return res
