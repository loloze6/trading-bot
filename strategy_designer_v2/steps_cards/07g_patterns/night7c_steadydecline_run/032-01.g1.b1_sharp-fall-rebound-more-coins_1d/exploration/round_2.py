def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            vsr = r / vol20.shift(1)
            ret20v = (c / c.shift(20) - 1) / (vol20 * np.sqrt(20))
            rng = (b["high"] - b["low"]) / c
            rngr = rng / rng.rolling(20).mean()
            volr = b["volume"] / b["volume"].rolling(20).mean()
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 5):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(ts.iloc[i])[:10], wd=ts.iloc[i].dayofweek,
                                     fwd=fwd.iloc[i], vsr=vsr.iloc[i], ret20v=ret20v.iloc[i],
                                     rngr=rngr.iloc[i], volr=volr.iloc[i], r=r.iloc[i]))
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")

    def pooled(g):
        s = g.groupby("day")["un"].sum()
        n = len(g)
        if len(s) < 3:
            return pd.Series(dict(n=n, days=len(s), mean_un=g["un"].mean(), t=np.nan))
        t = (s.sum() / n) / (s.std(ddof=1) * np.sqrt(len(s)) / n)
        return pd.Series(dict(n=n, days=len(s), mean_un=g["un"].mean(), t=t))

    def bywin(d, col):
        # per window: spearman of col vs un, sign count
        out = {}
        for w, g in d.dropna(subset=[col]).groupby("w"):
            if len(g) > 20:
                out[w] = stats.spearmanr(g[col], g["un"]).correlation
        s = pd.Series(out)
        return s

    def daypooled_slope(d, col):
        d = d.dropna(subset=[col, "un"]).copy()
        d["z"] = (d[col] - d[col].mean())
        d["p"] = d["z"] * d["un"]
        s = d.groupby("day")["p"].sum()
        beta = d["p"].sum() / (d["z"] ** 2).sum()
        t = s.sum() / (s.std(ddof=1) * np.sqrt(len(s)))
        return beta, t, len(s)

    res = {}
    # weekday, day pooled
    for h in (1, 2):
        d = df[df.h == h]
        res[f"h{h}_weekday_pooled"] = d.groupby("wd").apply(pooled)
    # pooled slopes and window consistency for candidate patterns
    sl = {}
    for h in (2, 5):
        d = df[df.h == h]
        for col in ("ret20v", "rngr", "volr", "vsr"):
            beta, t, nd = daypooled_slope(d, col)
            bw = bywin(d, col)
            sl[f"h{h}_{col}"] = dict(beta=beta, t_daypooled=t, days=nd, win_pos=(bw > 0).sum(), win_n=len(bw))
    res["slopes"] = pd.DataFrame(sl).T
    # range/volume expansion split by day's direction, h5 and h2
    for h in (2, 5):
        d = df[df.h == h].dropna(subset=["rngr", "r"]).copy()
        d["rq"] = pd.qcut(d["rngr"], 3, labels=["lo", "mid", "hi"])
        d["dir"] = np.where(d["r"] > 0, "up", "down")
        res[f"h{h}_range_by_dir"] = d.groupby(["rq", "dir"]).apply(pooled)
    # trend by window
    d = df[df.h == 5].dropna(subset=["ret20v"]).copy()
    d["tq"] = pd.qcut(d["ret20v"], 3, labels=["down", "mid", "up"])
    g = d.groupby(["w", "tq"])["un"].mean().unstack()
    res["h5_trend_by_window"] = g
    # signed: un in the direction of the 20d trend, graded by |ret20v|
    d["signed"] = np.sign(d["ret20v"]) * d["un"]
    d["aq"] = pd.qcut(d["ret20v"].abs(), 4, labels=False)
    res["h5_trend_signed_by_abs"] = d.assign(un=d["signed"]).groupby("aq").apply(pooled)
    return res
