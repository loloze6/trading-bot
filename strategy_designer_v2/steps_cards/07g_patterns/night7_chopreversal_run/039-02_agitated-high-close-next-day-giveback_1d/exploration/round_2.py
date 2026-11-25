def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            clv = (c - l) / rng.replace(0, np.nan)
            r0 = c.pct_change()
            r1 = c.shift(-1) / c - 1
            r2 = c.shift(-2) / c - 1
            relrng = (rng / c) / (rng / c).rolling(30, min_periods=10).mean()
            vol20 = r0.rolling(20, min_periods=10).std()
            z0 = r0 / vol20
            r3b = c / c.shift(3) - 1
            z3b = r3b / (vol20 * np.sqrt(3))
            tr = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.dayofweek, "year": ts.dt.year, "clv": clv, "r0": r0, "z0": z0,
                               "z3b": z3b, "r1": r1, "r2": r2,
                               "relrng": relrng, "tr": tr, "agit": (b["regime"] != "chop").astype(int)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["r1"] - d.groupby("coin")["r1"].transform("mean")
    d["s1"] = d["x1"] / d.groupby("coin")["r1"].transform("std")
    g2 = d[d.pos % 2 == 0].copy()
    g2["s2"] = (g2["r2"] - g2.groupby("coin")["r2"].transform("mean")) / g2.groupby("coin")["r2"].transform("std")

    def clt(sub, y, xs):
        s = sub.dropna(subset=[y] + xs)
        if len(s) < 50: return [np.nan] * (2 * len(xs)) + [len(s)]
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xs]); Y = s[y].values
        XtX = np.linalg.inv(X.T @ X); bta = XtX @ X.T @ Y; e = Y - X @ bta
        gg = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        V = XtX @ (gg.T @ gg) @ XtX; se = np.sqrt(np.diag(V))
        out = []
        for i in range(1, len(xs) + 1): out += [bta[i], bta[i] / se[i]]
        return out + [len(s)]

    res = {}
    A = d[d.agit == 1].copy(); C = d[d.agit == 0].copy()
    A["tq"] = pd.cut(A["tr"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out = []
    for nm, s in [("agit", A), ("calm", C), ("agit_fall", A[A.tq == "fall"]), ("agit_rise", A[A.tq == "rise"])]:
        out.append([nm, "z0"] + clt(s, "s1", ["z0"])[:2] + [np.nan, np.nan] + [clt(s, "s1", ["z0"])[-1]])
        out.append([nm, "neg z0 only"] + clt(s[s.z0 < 0], "s1", ["z0"])[:2] + [np.nan, np.nan] + [clt(s[s.z0 < 0], "s1", ["z0"])[-1]])
        out.append([nm, "pos z0 only"] + clt(s[s.z0 > 0], "s1", ["z0"])[:2] + [np.nan, np.nan] + [clt(s[s.z0 > 0], "s1", ["z0"])[-1]])
        out.append([nm, "clv+z0"] + clt(s, "s1", ["clv", "z0"]))
        out.append([nm, "z3b"] + clt(s, "s1", ["z3b"])[:2] + [np.nan, np.nan] + [clt(s, "s1", ["z3b"])[-1]])
    res["slopes by profile"] = pd.DataFrame(out, columns=["set", "x", "b1", "t1", "b2", "t2", "n"])
    # z0 down tail by year in agitated
    t = A[A.z0 < -1.5].dropna(subset=["s1"]).groupby("year")["s1"].agg(["mean", "count"])
    res["agit z0<-1.5 next-day std by year"] = t
    res["agit z0<-1.5 by coin"] = A[A.z0 < -1.5].dropna(subset=["s1"]).groupby("coin")["s1"].agg(["mean", "count"])
    # 2-day horizon
    G = g2[g2.agit == 1]
    res["2d agit slopes"] = pd.DataFrame([["z0"] + clt(G, "s2", ["z0"]), ["clv"] + clt(G, "s2", ["clv"])],
                                         columns=["x", "b", "t", "n"])
    # weekday by year
    d["wdg"] = d["wd"].map({2: "wed", 3: "thu", 4: "fri"}).fillna("other")
    res["weekday by year"] = d.dropna(subset=["s1"]).pivot_table(index="year", columns="wdg", values="s1", aggfunc="mean")
    # wide range x z0 in agitated
    A["rq"] = pd.qcut(A["relrng"], 3, labels=["narrow", "mid", "wide"])
    out = []
    for k, s in A.groupby("rq"): out.append([str(k)] + clt(s, "s1", ["z0"]) )
    res["agit z0 slope by range width"] = pd.DataFrame(out, columns=["rq", "b", "t", "n"])
    return res
