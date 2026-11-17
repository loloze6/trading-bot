def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 14
    # flipped book: daily, from bar positions; daily book returns as recorded
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r = c.pct_change()
            pos = b["postRebalance_current_allocation"].shift(1)
            share = b["debug_info.components.rsi_below_share.last_history_value"]
            r60 = c.pct_change(60).shift(1)
            g = pos * r
            df = pd.DataFrame(dict(day=ts.dt.floor("D"), g=g, flip=-g, r=r, pos=pos, share=share.shift(1), r60=r60))
            df["coin"] = coin; df["win"] = w; df["year"] = ts.dt.year
            recs.append(df)
    D = pd.concat(recs).dropna(subset=["g"])
    daily = D.groupby(["win", "day"]).agg(g=("g", "mean"), flip=("flip", "mean"), r=("r", "mean")).reset_index()
    sh = lambda x: x.mean() / x.std() * np.sqrt(365)
    out["sharpe book/flip/hold"] = pd.Series(dict(book=sh(daily.g), flip=sh(daily.flip), hold=sh(daily.r), flip_mean=daily.flip.mean(), hold_mean=daily.r.mean()))
    bw = daily.groupby("win").agg(book=("g", "sum"), flip=("flip", "sum"), hold=("r", "sum"))
    out["share of windows flip>0, book>0"] = pd.Series(dict(flip_pos=(bw.flip > 0).mean(), book_pos=(bw.book > 0).mean(), n=len(bw)))
    lo = {}
    for w in bw.index:
        x = daily[daily.win != w]
        lo[w] = sh(x.flip)
    out["flip sharpe leave-one-out min/max"] = pd.Series(dict(mn=min(lo.values()), mx=max(lo.values())))
    # graded: grid 14d returns vs share and vs 60d return
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            s = b["debug_info.components.rsi_below_share.last_history_value"].values
            r60 = pd.Series(c).pct_change(60).values
            r30 = pd.Series(c).pct_change(30).values
            for i in np.arange(0, len(c) - H, H):
                rows.append(dict(coin=coin, r=c[i+H]/c[i]-1, share=s[i], r60=r60[i], r30=r30[i]))
    G = pd.DataFrame(rows)
    G["r"] = G.r - G.groupby("coin").r.transform("mean")
    out["corr share vs r30, r60"] = pd.Series(dict(r30=G[["share","r30"]].corr().iloc[0,1], r60=G[["share","r60"]].corr().iloc[0,1]))
    res = {}
    for col in ["share", "r30", "r60"]:
        x = G.dropna(subset=[col, "r"])
        s = stats.linregress(x[col], x.r)
        res[col] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(x))
    out["grid fwd14 regressed on"] = pd.DataFrame(res).T
    x = G.dropna(subset=["r60"]).copy()
    x["q"] = pd.qcut(x.r60, 5, labels=False)
    out["fwd14 by r60 quintile"] = x.groupby("q").agg(r60=("r60","mean"), share=("share","mean"), r=("r","mean"), n=("r","size"))
    # share within uptrend: does high below-share in uptrend predict lower
    x["up"] = x.r60 > 0
    out["share slope within r60 sign"] = x.groupby("up").apply(lambda g: pd.Series(dict(slope=stats.linregress(g.share.fillna(0), g.r).slope, t=stats.linregress(g.share.fillna(0), g.r).slope/stats.linregress(g.share.fillna(0), g.r).stderr, n=len(g))))
    return out
