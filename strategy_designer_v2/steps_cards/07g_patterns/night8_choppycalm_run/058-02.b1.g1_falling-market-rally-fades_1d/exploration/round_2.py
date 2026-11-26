def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            ret60 = c / c.shift(60) - 1
            hi20 = b["high"].astype(float).rolling(20).max()
            lo20 = b["low"].astype(float).rolling(20).min()
            pos = (c - lo20) / (hi20 - lo20)
            vol30 = r.rolling(30).std()
            vrank = vol30.rolling(90, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos, "ret60": ret60,
                               "vrank": vrank, "day": ts.dt.floor("D"), "yr": ts.dt.year, "wd": ts.dt.weekday,
                               "n1": c.shift(-1) / c - 1, "n3": c.shift(-3) / c - 1, "n5": c.shift(-5) / c - 1})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ["n1", "n3", "n5"]:
        d[h + "u"] = d[h] - d.groupby("coin")[h].transform("mean")
    d["trend"] = np.where(d.ret60 > 0.10, "rising", np.where(d.ret60 < -0.10, "falling", "choppy"))
    d.loc[d.ret60.isna(), "trend"] = np.nan
    d["agit"] = np.where(d.vrank > 0.5, "agit", "calm")
    d.loc[d.vrank.isna(), "agit"] = np.nan

    def ct(g, col):
        x = g.dropna(subset=[col])
        if len(x) < 3:
            return pd.Series({"n": len(x), "days": x.day.nunique(), "mean%": np.nan, "t_day": np.nan})
        dev = (x[col] - x[col].mean()).groupby(x.day).sum()
        K = len(dev)
        se = np.sqrt((dev ** 2).sum() * K / max(K - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": K, "mean%": 100 * x[col].mean(), "t_day": x[col].mean() / se})

    for h, k in [("n3u", 3), ("n5u", 5)]:
        g = d[d.i % k == 0].dropna(subset=["pos", "trend", h]).copy()
        g["pq"] = pd.cut(g.pos, [-0.01, 0.1, 0.25, 0.5, 0.75, 1.01])
        out[f"falling pos x agit {h}"] = g[g.trend == "falling"].dropna(subset=["agit"]).groupby(["agit", "pq"], observed=True).apply(lambda x: ct(x, h)).round(3)
        out[f"choppy pos {h}"] = g[g.trend == "choppy"].groupby("pq", observed=True).apply(lambda x: ct(x, h)).round(3)
        f = g[g.trend == "falling"]
        f = f.assign(low=f.pos <= 0.25)
        out[f"falling low<=.25 by year {h}"] = f[f.low].groupby("yr").apply(lambda x: ct(x, h)).round(3)
        out[f"falling corr pos {h}"] = pd.Series({"spearman": f[["pos", h]].corr(method="spearman").iloc[0, 1], "n": len(f)}).round(3)
    # weekday, day-clustered, by trend
    e = d.dropna(subset=["n1u", "trend"])
    out["weekday day-clustered"] = e.groupby("wd").apply(lambda x: ct(x, "n1u")).round(3)
    out["weekday by year thu+fri minus mon+wed"] = e.groupby("yr").apply(lambda x: pd.Series({
        "thufri%": 100 * x[x.wd.isin([3, 4])].n1u.mean(), "monwed%": 100 * x[x.wd.isin([0, 2])].n1u.mean()})).round(3)
    return out
