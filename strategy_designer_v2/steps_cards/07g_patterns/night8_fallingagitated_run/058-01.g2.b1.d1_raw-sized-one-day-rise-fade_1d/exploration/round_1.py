def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "inprof": (b["regime"] == "unknown").astype(int),
                "z1": r1 / sd,
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "z10": (c / c.shift(10) - 1) / (sd * np.sqrt(10)),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "sdl": sd,
                "pos": b["postRebalance_current_allocation"],
            })
            d["i"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["year"] = D["ts"].dt.year

    out = {}
    for h, col in [(1, "f1"), (3, "f3"), (5, "f5")]:
        g = D[D["i"] % h == 0].copy()
        g["u"] = g[col] - g.groupby("coin")[col].transform("mean")
        D.loc[g.index, "u%d" % h] = g["u"]

    def tab(sub, key, ucol):
        s = sub.dropna(subset=[key, ucol])

        def f(x):
            pd_ = x.groupby("day")[ucol].sum()
            n = len(x)
            m = x[ucol].mean()
            se = np.sqrt(((pd_ - x.groupby("day").size() * m) ** 2).sum()) / n if n > 1 else np.nan
            return pd.Series({"n": n, "days": x["day"].nunique(), "mean": m, "t": m / se if se > 0 else np.nan})

        return s.groupby(key).apply(f)

    for z in ["z1", "z3", "z5", "z10"]:
        D[z + "b"] = pd.cut(D[z], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    for prof in [1, 0]:
        S = D[D["inprof"] == prof]
        for z in ["z1", "z3", "z5"]:
            out["prof%d_%s_u3" % (prof, z)] = tab(S, z + "b", "u3")
        out["prof%d_z10_u5" % prof] = tab(S, "z10b", "u5")
        out["prof%d_z1_u1" % prof] = tab(S, "z1b", "u1")

    D["volq"] = D.groupby("coin")["sdl"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["all_volq_u3"] = tab(D, "volq", "u3")
    out["all_wd_u1"] = tab(D, "wd", "u1")
    out["prof1_wd_u1"] = tab(D[D["inprof"] == 1], "wd", "u1")
    out["share_inprof"] = float(D["inprof"].mean())

    dy = pd.concat([x.assign(coin=c, win=w) for c, ws in data["days"].items() for w, x in ws.items()])
    bk = dy.groupby("day")["book_return"].mean()
    out["book_by_year"] = bk.groupby(pd.to_datetime(bk.index).year).agg(["mean", "count", "std"])
    return out
