def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    # grand mean of h-bar returns per coin (all windows), non-overlapping
    def grid_mean(coin, h):
        v = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - h, h):
                v.append(c[i + h] / c[i] - 1)
        return np.mean(v) if v else np.nan
    out = {}
    for h in (1, 3, 5, 10):
        recs = []
        for coin in bars:
            gm = grid_mean(coin, h)
            for w, b in bars[coin].items():
                b = b.reset_index(drop=True)
                c = b["close"]
                r = c.pct_change()
                sma = c.rolling(20, min_periods=20).mean()
                sd = r.rolling(20, min_periods=20).std()
                st = (c - sma) / (sma * sd)
                ret1 = r
                rng = (b["high"] - b["low"]) / c
                pos_close = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
                vol_ratio = r.rolling(10).std() / r.rolling(40).std()
                agit = (b["regime"] == "chop").astype(int)
                wd = pd.to_datetime(b["timestamp"]).dt.weekday
                yr = pd.to_datetime(b["timestamp"]).dt.year
                day = pd.to_datetime(b["timestamp"]).dt.floor("D")
                cv = c.values
                for i in range(0, len(cv) - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, st=st.iloc[i], r1=ret1.iloc[i],
                                     r5=(cv[i] / cv[i - 5] - 1) if i >= 5 else np.nan,
                                     rng=rng.iloc[i], pc=pos_close.iloc[i], vr=vol_ratio.iloc[i],
                                     ag=agit.iloc[i], wd=wd.iloc[i], yr=yr.iloc[i], day=day.iloc[i],
                                     y=cv[i + h] / cv[i] - 1 - gm))
        rows.append(pd.DataFrame(recs))
    D = pd.concat(rows)
    res = []
    for h, g in D.groupby("h"):
        for ag, gg in g.groupby("ag"):
            for var in ["st", "r1", "r5", "rng", "pc", "vr"]:
                x = gg[[var, "y"]].dropna()
                x = x[np.isfinite(x[var])]
                if len(x) < 50: continue
                rr, p = stats.spearmanr(x[var], x["y"])
                sl = stats.linregress(x[var], x["y"])
                res.append(dict(h=h, agitated=ag, var=var, n=len(x), spearman=round(rr, 3),
                                slope_t=round(sl.slope / sl.stderr, 2)))
    out["corr_by_h_agit_var"] = pd.DataFrame(res)
    # stretch quintile means, h=5 and 10, by agitation
    q = []
    for h in (5, 10):
        g = D[D.h == h].dropna(subset=["st"]).copy()
        g["qq"] = pd.qcut(g["st"], 5, labels=False)
        t = g.groupby(["ag", "qq"])["y"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
        t.columns = ["mean", "n", "t"]
        t["h"] = h
        q.append(t.reset_index())
    out["stretch_quintiles"] = pd.concat(q).round(4)
    g = D[D.h == 1]
    out["weekday_1d"] = g.groupby("wd")["y"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).round(4)
    g5 = D[D.h == 5].dropna(subset=["st"])
    out["st_corr_by_window_h5"] = g5.groupby("w").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.st, x.y)[0]})).round(3)
    out["regime_share"] = D[D.h == 1].groupby("coin")["ag"].mean().round(3)
    return out
