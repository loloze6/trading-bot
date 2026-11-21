def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        grid_all = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                grid_all.append(c[i + H] / c[i] - 1)
        drift = np.mean(grid_all) if grid_all else np.nan
        sd = np.std(grid_all) if grid_all else np.nan
        dr = pd.concat([d["coin_return"] for d in data["days"][coin].values()]).dropna()
        mdr = dr.mean()
        for w, b in wins.items():
            c = b["close"].values.astype(float)
            f = b["forecast"].values.astype(float)
            n = len(c)
            s = pd.Series(c)
            ret90 = s.pct_change(90).values
            ret30 = s.pct_change(30).values
            ret10 = s.pct_change(10).values
            ma50 = s.rolling(50).mean().values
            hi90 = s.rolling(90, min_periods=20).max().values
            vol = s.pct_change().rolling(30).std().values
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, f=f[i], fwd=fwd, drift=drift, sd=sd,
                                 r90=ret90[i], r30=ret30[i], r10=ret10[i],
                                 dd=c[i] / hi90[i] - 1 if not np.isnan(hi90[i]) else np.nan,
                                 vol=vol[i],
                                 above50=float(c[i] > ma50[i]) if not np.isnan(ma50[i]) else np.nan))
            alloc = b["postRebalance_current_allocation"].values.astype(float)
            g = alloc[:-1] * (c[1:] / c[:-1] - 1)
            d = data["days"][coin][w]
            bookrows.append(dict(coin=coin, w=w, gain=np.nansum(g), mkt=np.nansum(alloc[:-1]) * mdr,
                                 nbars=n - 1, shortbars=(alloc[:-1] < 0).sum(),
                                 bookret=d["book_return"].dropna().sum(),
                                 coinret=d["coin_return"].dropna().sum()))
    df = pd.DataFrame(rows)
    cs = df[df.f < 0].copy()
    cs["total_short"] = -cs.fwd
    cs["unusual_short"] = -(cs.fwd - cs.drift)
    out = {}
    out["cases"] = pd.Series(dict(n=len(cs), total=cs.total_short.mean(), unusual=cs.unusual_short.mean(),
                                  t_total=stats.ttest_1samp(cs.total_short, 0).statistic,
                                  share_win=(cs.total_short > 0).mean(),
                                  grid_bars=len(df), share_cases=len(cs) / len(df)))
    def bucket(col, q=5):
        x = cs.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        g = x.groupby("b").agg(n=("total_short", "size"), lo=(col, "min"), hi=(col, "max"),
                               total=("total_short", "mean"), unusual=("unusual_short", "mean"),
                               t=("total_short", lambda v: stats.ttest_1samp(v, 0).statistic))
        return g
    for col in ["r90", "r30", "r10", "dd", "vol"]:
        out["by_" + col] = bucket(col)
    out["by_above50"] = cs.groupby("above50").agg(n=("total_short", "size"), total=("total_short", "mean"),
                                                   unusual=("unusual_short", "mean"))
    out["by_force"] = bucket("f", 3)
    # baseline: all grid bars fwd by r90 quintile (long side)
    a = df.dropna(subset=["r90"]).copy()
    a["b"] = pd.qcut(a.r90.rank(method="first"), 5, labels=False)
    out["all_fwd_by_r90"] = a.groupby("b").agg(n=("fwd", "size"), lo=("r90", "min"), hi=("r90", "max"),
                                               fwd=("fwd", "mean"))
    bk = pd.DataFrame(bookrows)
    out["book_by_window"] = bk.groupby("w")[["gain", "mkt", "bookret", "coinret", "shortbars"]].sum()
    out["book_total"] = pd.Series(dict(gain=bk.gain.sum(), mkt=bk.mkt.sum(), timing=bk.gain.sum() - bk.mkt.sum(),
                                       shortshare=bk.shortbars.sum() / bk.nbars.sum()))
    out["book_by_coin"] = bk.groupby("coin")[["gain", "mkt", "bookret", "coinret"]].sum()
    return out
