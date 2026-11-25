def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in ws.items():
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]).values,
                "clv": ((h - c) / (h - l).replace(0, np.nan)).values,
                "rng": ((h - l) / c).values, "hc": ((h - c) / c).values,
                "dret": (c / o - 1).values, "r1": (c.shift(-1) / c - 1).values,
                "r2": (c.shift(-2) / c - 1).values,
                "inprof": (b["regime"] == "unknown").values})
            d["ex1"] = d["r1"] - mu
            d["ex2"] = d["r2"] - 2*mu
            d["rngz"] = d["rng"] / d["rng"].rolling(20, min_periods=10).mean().shift(1)
            d["hcz"] = d["hc"] / d["rng"].rolling(20, min_periods=10).mean().shift(1)
            d["ret60"] = (c / c.shift(60) - 1).values
            d["day"] = d["ts"].dt.floor("D")
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def clus(s, y, x):
        s = s.dropna(subset=[y, x])
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan, "days": 0})
        X = s[x] - s[x].mean(); Y = s[y]
        beta = (X*Y).sum() / (X*X).sum()
        e = Y - Y.mean() - beta*X
        g = (X*e).groupby(s["day"]).sum()
        se = np.sqrt((g**2).sum()) / (X*X).sum()
        return pd.Series({"n": len(s), "slope": beta, "t": beta/se, "days": s["day"].nunique()})
    def tday(s, y):
        s = s.dropna(subset=[y]); g = s.groupby("day")[y].apply(lambda v: (v - 0).sum())
        n = len(s); m = s[y].mean()
        se = np.sqrt(((s[y]-m).groupby(s["day"]).sum()**2).sum())/n if n>2 else np.nan
        return pd.Series({"n": n, "days": s["day"].nunique(), "mean": m, "t": m/se if se else np.nan})

    out = {}
    nw16 = D[D.win != "w16"]
    out["slope_clv_ex1_excl_w16"] = nw16.groupby("inprof").apply(lambda s: clus(s, "ex1", "clv"))
    out["slope_hcz_ex1_by_profile"] = D.groupby("inprof").apply(lambda s: clus(s, "ex1", "hcz"))
    out["slope_hcz_ex1_excl_w16"] = nw16.groupby("inprof").apply(lambda s: clus(s, "ex1", "hcz"))
    D["hczq"] = D.groupby("inprof")["hcz"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["hcz_quint_ex1"] = D.groupby(["inprof", "hczq"]).apply(lambda s: tday(s, "ex1")).unstack(0)
    bot = D[D.clv >= 0.8]
    out["bottom_by_profile_rng"] = bot.groupby(["inprof", D["rngz"].gt(1.2).rename("wide")]).apply(lambda s: tday(s, "ex1"))
    out["bottom_by_profile_excl_w16"] = bot[bot.win != "w16"].groupby("inprof").apply(lambda s: tday(s, "ex1"))
    out["bottom_by_profile_ex2"] = bot.groupby("inprof").apply(lambda s: tday(s, "ex2"))
    # out of profile split by own 60-day trend (computed within window)
    o = D[~D.inprof].copy()
    o["tr"] = pd.cut(o["ret60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["out_slope_by_trend"] = o.groupby("tr").apply(lambda s: clus(s, "ex1", "clv"))
    out["out_bottom_by_trend"] = o[o.clv >= 0.8].groupby("tr").apply(lambda s: tday(s, "ex1"))
    out["out_wide_slope_by_trend"] = o[o.rngz > 1.2].groupby("tr").apply(lambda s: clus(s, "ex1", "clv"))
    out["bottom_in_by_year"] = bot[bot.inprof].groupby(bot["ts"].dt.year).apply(lambda s: tday(s, "ex1"))
    # book: largest days
    dd = []
    for coin, ws in data["days"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna().reset_index()
    bk = bk.sort_values("book_return")
    out["book_worst10"] = bk.head(10)[["win", "book_return"]].reset_index(drop=True)
    out["book_best10"] = bk.tail(10)[["win", "book_return"]].reset_index(drop=True)
    out["book_share_top10_days"] = bk.tail(10)["book_return"].sum() / bk["book_return"].sum()
    return out
