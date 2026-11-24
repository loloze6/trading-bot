def explore(data):
    import numpy as np, pandas as pd
    rows = []
    bars = data["bars"]
    for coin in bars:
        # coin-level normal 3-day drift and usual move on non-overlapping grid
        allg = []
        for w, b in bars[coin].items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            allg.append(c[idx + 3] / c[idx] - 1)
        allg = np.concatenate(allg) if allg else np.array([])
        if len(allg) < 10:
            continue
        drift, usual = allg.mean(), allg.std()
        d1 = []
        for w, b in bars[coin].items():
            d1.append(b["close"].pct_change().values[1:])
        d1 = np.concatenate(d1)
        sd1 = np.nanstd(d1)
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = h - l
            mult = rng / rng.rolling(20).mean()
            loc = (c - l) / rng.replace(0, np.nan)
            past5 = c.shift(1) / c.shift(6) - 1
            ret5 = c / c.shift(5) - 1
            r1 = c / c.shift(1) - 1
            body = (c - o) / rng.replace(0, np.nan)
            volr = (rng.rolling(20).mean() / c)
            volr_rel = volr / volr.rolling(60, min_periods=20).mean()
            fwd = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - 3, 3):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].floor("D"),
                                 wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                 mult=mult.iloc[i], loc=loc.iloc[i], past5=past5.iloc[i],
                                 ret5z=ret5.iloc[i] / (usual * np.sqrt(5 / 3)), r1z=r1.iloc[i] / sd1,
                                 body=body.iloc[i], volrel=volr_rel.iloc[i],
                                 un=(fwd.iloc[i] - drift), str=(fwd.iloc[i] - drift) / usual))
    df = pd.DataFrame(rows).dropna(subset=["un"])

    def ct(g, col="str"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series(dict(n=len(g), days=0, mean=np.nan, t=np.nan))
        s = g.groupby("day")[col].agg(["sum", "count"])
        m = s["sum"].sum() / s["count"].sum()
        D = len(s)
        se = np.sqrt(((s["sum"] - s["count"] * m) ** 2).sum() * D / max(D - 1, 1)) / s["count"].sum()
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    df["fall"] = np.where(df.past5 < 0, "fall5", "rise5")
    df["wide"] = pd.cut(df.mult, [0, 0.8, 1.2, 1.5, 2, 99], labels=["<.8", ".8-1.2", "1.2-1.5", "1.5-2", ">2"])
    df["locq"] = pd.cut(df["loc"], [-.01, .25, .5, .75, 1.01], labels=["low", "q2", "q3", "high"])
    out["str by fall x locq (wide>=1.5)"] = df[df.mult >= 1.5].groupby(["fall", "locq"]).apply(ct)
    out["str by fall x wide"] = df.groupby(["fall", "wide"]).apply(ct)
    df["r1q"] = pd.qcut(df.r1z, 7)
    out["str by 1day return z bins"] = df.groupby("r1q").apply(ct)
    df["r5q"] = pd.qcut(df.ret5z, 7)
    out["str by 5day return z bins"] = df.groupby("r5q").apply(ct)
    df["vq"] = pd.qcut(df.volrel, 5)
    out["str by rel vol quintile"] = df.groupby("vq").apply(ct)
    out["str by weekday"] = df.groupby("wd").apply(ct)
    df["vq_x_r1"] = np.sign(df.r1z).astype(str)
    out["str by relvol x sign r1"] = df.groupby(["vq", "vq_x_r1"]).apply(ct)
    out["corr str with features"] = df[["str", "mult", "loc", "r1z", "ret5z", "body", "volrel"]].corr()["str"]
    # book: largest gain/loss days, coin return around
    bd = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            d = d.reset_index(drop=True)
            d["cnext"] = d["coin_return"].shift(-1)
            d["cprev"] = d["coin_return"].shift(1)
            bd.append(d.dropna(subset=["book_return"]))
    bd = pd.concat(bd)
    act = bd[bd.book_return != 0]
    out["book active days stats"] = pd.Series(dict(n=len(act), mean=act.book_return.mean(),
                                                   share_pos=(act.book_return > 0).mean()))
    q = act.book_return.quantile([0.05, 0.95])
    out["coin ret around book extremes"] = pd.DataFrame({
        "worst5%": act[act.book_return <= q.iloc[0]][["cprev", "coin_return", "cnext"]].mean(),
        "best5%": act[act.book_return >= q.iloc[1]][["cprev", "coin_return", "cnext"]].mean()})
    return out
