def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "r1": r1, "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                               "volrank": vol30 / vol30.expanding(30).median(),
                               "f10": c.shift(-10) / c - 1, "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                               "regime": b["regime"], "wd": ts.dt.weekday,
                               "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "rng": (b["high"] - b["low"]) / c})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["trend"] = np.where(d.r60 > 0.1, "rising", np.where(d.r60 < -0.1, "falling", "choppy"))
    d["agit"] = np.where(d.volrank > 1, "agit", "calm")
    sd10 = d[d.pos % 10 == 0].groupby("coin").f10.std()
    dr10 = d[d.pos % 10 == 0].groupby("coin").f10.mean()
    d["u10"] = d.f10 - d.coin.map(dr10)
    d["s30"] = d.r30 / (d.coin.map(sd10) * np.sqrt(3))
    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "days": np.nan, "mean": np.nan, "t_day": np.nan})
        dev = x.groupby("day")[col].sum() - x.groupby("day")[col].size() * x[col].mean()
        G = len(dev); se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": x[col].mean(), "t_day": x[col].mean() / se})
    out = {}
    # choppy month continuation: signed move u10 * sign(r30), every offset grid
    res = []
    for off in range(10):
        g = d[(d.pos % 10 == off) & (d.trend == "choppy")].dropna(subset=["u10", "r30"]).copy()
        g["sig"] = g.u10 * np.sign(g.r30)
        for side, gg in [("up", g[g.r30 > 0]), ("down", g[g.r30 < 0])]:
            s = ct(gg, "sig"); s["off"] = off; s["side"] = side
            s["corr"] = gg[["s30", "u10"]].corr().iloc[0, 1]
            res.append(s)
    R = pd.DataFrame(res)
    out["choppy_cont_by_offset_side"] = R.groupby("side")[["n", "mean", "t_day", "corr"]].agg(["mean", "min", "max"])
    # choppy by agitation, offset 0, by s30 terciles
    g = d[(d.pos % 10 == 0) & (d.trend == "choppy")].dropna(subset=["u10", "r30", "volrank"]).copy()
    g["q"] = pd.qcut(g.s30, 3, labels=["low", "mid", "high"])
    out["choppy_agit_q"] = g.groupby(["agit", "q"]).apply(lambda x: ct(x, "u10"))
    out["choppy_by_year"] = g.groupby(g.day.dt.year).apply(lambda x: pd.Series({"n": len(x), "corr": x[["s30", "u10"]].corr().iloc[0, 1]}))
    # next-day rebound after big down day, clustered, by trend x agit
    dd = d.dropna(subset=["f1", "r1", "volrank"]).copy()
    dd["z"] = dd.r1 / dd.groupby("coin").r1.transform("std")
    big = dd[dd.z < dd.z.quantile(0.1)]
    out["rebound_bigdown_by_profile"] = big.groupby(["trend", "agit"]).apply(lambda x: ct(x, "f1"))
    out["rebound_bigup_short_by_profile"] = dd[dd.z > dd.z.quantile(0.9)].groupby(["trend", "agit"]).apply(lambda x: ct(x, "f1"))
    out["weekday_clustered"] = dd.groupby("wd").apply(lambda x: ct(x, "f1"))
    out["weekday_by_trend_thu_fri"] = dd[dd.wd.isin([3, 4])].groupby(["trend", "agit"]).apply(lambda x: ct(x, "f1"))
    # close near low, high close next day by profile
    dd["lowc"] = dd.clpos < 0.2
    out["lowclose_by_profile"] = dd[dd.lowc].groupby(["trend", "agit"]).apply(lambda x: ct(x, "f1"))
    out["highclose_by_profile"] = dd[dd.clpos > 0.8].groupby(["trend", "agit"]).apply(lambda x: ct(x, "f1"))
    return out
