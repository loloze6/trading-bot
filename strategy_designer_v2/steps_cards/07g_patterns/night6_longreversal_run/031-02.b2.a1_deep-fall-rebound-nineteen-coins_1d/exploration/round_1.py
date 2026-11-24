def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # coin drift per horizon
    def grid(df, h):
        c = df["close"].values
        idx = np.arange(0, len(c) - h, h)
        return idx, c[idx + h] / c[idx] - 1
    rows = []
    for coin, wins in bars.items():
        # drift per horizon
        dr = {}
        for h in (7, 14, 30):
            allr = []
            for w, df in wins.items():
                _, r = grid(df.reset_index(drop=True), h)
                allr.extend(r)
            dr[h] = np.mean(allr) if allr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(c)
            ret1 = pd.Series(c).pct_change()
            vol20 = ret1.rolling(20).std().values
            for h in (7, 14, 30):
                idx, r = grid(df, h)
                for i, fr in zip(idx, r):
                    p7 = c[i] / c[i - 7] - 1 if i >= 7 else np.nan
                    p30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                    p60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    rows.append(dict(coin=coin, win=w, h=h, fr=fr, ur=fr - dr[h],
                                     p7=p7, p30=p30, p60=p60, vol=vol20[i],
                                     reg=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                                     wd=pd.Timestamp(df["timestamp"].iloc[i]).weekday(),
                                     yr=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     day=pd.Timestamp(df["timestamp"].iloc[i]).normalize()))
    R = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g["ur"].mean(); s = g["ur"].std()
        # day-clustered t
        d = g.groupby("day")["ur"].apply(lambda x: (x - m).sum())
        D = len(d)
        se = np.sqrt((d**2).sum() * D / max(D - 1, 1)) / n if n else np.nan
        return pd.Series(dict(n=n, days=D, mean_ur=m, t_cl=m / se if se > 0 else np.nan))
    # past-return quintiles, per coin standardized (rank within coin)
    for h in (7, 30):
        for past in ("p7", "p30", "p60"):
            g = R[(R.h == h)].dropna(subset=[past]).copy()
            g["q"] = g.groupby("coin")[past].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if len(x) >= 5 else np.nan)
            out[f"h{h}_by_{past}_quintile"] = g.dropna(subset=["q"]).groupby("q").apply(summ)
    g = R[R.h == 30].dropna(subset=["vol"]).copy()
    g["q"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False) if len(x) >= 3 else np.nan)
    out["h30_by_vol_tercile"] = g.dropna(subset=["q"]).groupby("q").apply(summ)
    g = R[R.h == 7].dropna(subset=["vol"]).copy()
    g["q"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False) if len(x) >= 3 else np.nan)
    out["h7_by_vol_tercile"] = g.dropna(subset=["q"]).groupby("q").apply(summ)
    out["h30_by_regime"] = R[R.h == 30].groupby("reg").apply(summ)
    out["h30_by_year"] = R[R.h == 30].groupby("yr").apply(summ)
    # weekday daily returns
    dl = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.dropna(subset=["coin_return"]).copy()
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            dl.append(d[["wd", "coin_return"]])
    D = pd.concat(dl)
    out["weekday_coin_ret"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # inside regime: fall90 vs fall30 components on grid
    g = R[(R.h == 30) & (R.fc > 0)]
    out["h30_fc_pos_count"] = len(g)
    # book: daily book returns by top/bottom
    bl = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["coin"] = coin; d["win"] = w
            bl.append(d)
    B = pd.concat(bl)
    br = B.groupby("day")["book_return"].mean().dropna()
    out["book_daily_mean_std"] = pd.Series(dict(mean=br.mean(), std=br.std(), n=len(br), top10_share=br.nlargest(10).sum() / br.sum(), bottom10_sum=br.nsmallest(10).sum()))
    return out
