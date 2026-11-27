def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            sd = r.rolling(30, min_periods=20).std()
            rng = (h - l) / c
            loc = (c - l) / (h - l).replace(0, np.nan)  # 1 = high
            d = pd.DataFrame({
                "coin": coin, "win": w, "loc": loc, "rngv": rng / sd, "ret1": r / sd,
                "ret5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "nxt": nxt, "ux": nxt - drift, "inprof": (b["regime"] != "chop").values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "yr": pd.to_datetime(b["timestamp"]).dt.year.values,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
                "vol": b["volume"].astype(float) / b["volume"].astype(float).rolling(30, min_periods=20).mean(),
            })
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["ux", "loc", "rngv"])
    D["side"] = 2 * D["loc"] - 1  # +1 at high
    D["fade"] = -np.sign(D["side"]) * D["ux"]

    def ct(x, days):
        g = pd.DataFrame({"x": x.values, "d": days.values}).groupby("d")["x"].sum()
        n = len(g); m = x.mean()
        se = np.sqrt((g - g.mean() * 0).pow(2).sum() * 0 + ((g - x.mean() * pd.DataFrame({"d": days.values}).groupby("d").size()) ** 2).sum()) / len(x)
        se *= np.sqrt(n / (n - 1)) if n > 1 else np.nan
        return m / se if se > 0 else np.nan

    def tab(df, by):
        out = df.groupby(by).apply(lambda g: pd.Series({
            "n": len(g), "mean_ux_%": 100 * g["ux"].mean(), "t": ct(g["ux"], g["day"])}))
        return out.round(3)

    res = {}
    res["inprof share"] = float(D["inprof"].mean())
    D["locq"] = pd.cut(D["loc"], [-0.01, .1, .25, .5, .75, .9, 1.01], labels=["0-.1", ".1-.25", ".25-.5", ".5-.75", ".75-.9", ".9-1"])
    res["loc bins, in profile"] = tab(D[D.inprof], "locq")
    res["loc bins, out of profile"] = tab(D[~D.inprof], "locq")
    D["rq"] = D.groupby("coin")["rngv"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    ext = D[(D["loc"] <= .25) | (D["loc"] >= .75)].copy()
    ext["end"] = np.where(ext["loc"] >= .75, "high", "low")
    res["extreme close x range tercile x profile"] = ext.groupby(["inprof", "end", "rq"]).apply(lambda g: pd.Series({
        "n": len(g), "mean_ux_%": 100 * g["ux"].mean(), "t": ct(g["ux"], g["day"])})).round(3)
    D["r1q"] = D.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["next day by 1d return quintile (all)"] = tab(D, "r1q")
    D["r5q"] = D.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["next day by 5d return quintile (all)"] = tab(D, "r5q")
    res["weekday (all)"] = tab(D, "wd")
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res["volume tercile x end (extreme closes)"] = ext.assign(vq=D.loc[ext.index, "vq"] if False else ext["vol"].rank(pct=True).mul(3).clip(upper=2.999).astype(int)).groupby(["end", "vq"]).apply(lambda g: pd.Series({"n": len(g), "mean_ux_%": 100 * g["ux"].mean(), "t": ct(g["ux"], g["day"])})).round(3)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, win=w))
    B = pd.concat(bd).dropna(subset=["book_return"])
    bk = B.groupby("day")["book_return"].mean()
    res["book daily: n, mean%, top5 share of sum"] = pd.Series({"n": len(bk), "mean%": 100 * bk.mean(),
        "sum%": 100 * bk.sum(), "top5 sum%": 100 * bk.nlargest(5).sum(), "bottom5 sum%": 100 * bk.nsmallest(5).sum()})
    res["year x in profile, high-quarter closes"] = tab(D[(D["loc"] >= .75) & D.inprof], "yr")
    return res
