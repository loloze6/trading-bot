def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        # coin mean 10-bar return over all windows (grid)
        grid_all = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                grid_all.append(c[i + H] / c[i] - 1)
        drift = np.mean(grid_all) if grid_all else np.nan
        sd = np.std(grid_all) if grid_all else np.nan
        # daily mean coin return
        dr = pd.concat([d["coin_return"] for d in data["days"][coin].values()]).dropna()
        mdr = dr.mean()
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].values
            n = len(c)
            ret90 = pd.Series(c).pct_change(90).values
            ret30 = pd.Series(c).pct_change(30).values
            ma50 = pd.Series(c).rolling(50).mean().values
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, i=i, f=f[i], fwd=fwd, drift=drift, sd=sd,
                                 r90=ret90[i], r30=ret30[i],
                                 above50=(c[i] > ma50[i]) if not np.isnan(ma50[i]) else np.nan))
            d = data["days"][coin][w]
            bv = b.set_index(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].values
            # position-day gains
            g = alloc[:-1] * (c[1:] / c[:-1] - 1)
            bookrows.append(dict(coin=coin, w=w, gain=np.nansum(g), mkt=np.nansum(alloc[:-1]) * mdr,
                                 nbars=n - 1, shortbars=(alloc[:-1] < 0).sum(),
                                 bookret=d["book_return"].dropna().sum()))
    df = pd.DataFrame(rows)
    cs = df[df.f < 0].copy()
    cs["total_short"] = -cs.fwd
    cs["unusual_short"] = -(cs.fwd - cs.drift)
    out = {}
    out["cases"] = pd.Series(dict(n=len(cs), total=cs.total_short.mean(), unusual=cs.unusual_short.mean(),
                                  t_total=stats.ttest_1samp(cs.total_short, 0).statistic,
                                  share_win=(cs.total_short > 0).mean()))
    # by 90-day return bucket
    cs["r90b"] = pd.qcut(cs.r90, 5)
    out["by_r90"] = cs.groupby("r90b").agg(n=("total_short", "size"), total=("total_short", "mean"),
                                            unusual=("unusual_short", "mean"))
    cs["r30b"] = pd.qcut(cs.r30, 5)
    out["by_r30"] = cs.groupby("r30b").agg(n=("total_short", "size"), total=("total_short", "mean"),
                                            unusual=("unusual_short", "mean"))
    out["by_above50"] = cs.groupby("above50").agg(n=("total_short", "size"), total=("total_short", "mean"),
                                                   unusual=("unusual_short", "mean"))
    # non-case grid baseline in same buckets
    nc = df[(df.f >= 0)].copy()
    nc["r90b"] = pd.cut(nc.r90, cs["r90b"].cat.categories)
    out["noncase_fwd_by_r90"] = nc.groupby("r90b").fwd.agg(["size", "mean"])
    bk = pd.DataFrame(bookrows)
    out["book_by_window"] = bk.groupby("w")[["gain", "mkt", "bookret", "shortbars"]].sum()
    out["book_total"] = pd.Series(dict(gain=bk.gain.sum(), mkt=bk.mkt.sum(), timing=bk.gain.sum() - bk.mkt.sum(),
                                       shortshare=bk.shortbars.sum() / bk.nbars.sum()))
    cs["fb"] = pd.qcut(cs.f.abs(), 3, labels=["low", "mid", "high"])
    out["by_force"] = cs.groupby("fb").agg(n=("total_short", "size"), total=("total_short", "mean"),
                                            unusual=("unusual_short", "mean"))
    return out
