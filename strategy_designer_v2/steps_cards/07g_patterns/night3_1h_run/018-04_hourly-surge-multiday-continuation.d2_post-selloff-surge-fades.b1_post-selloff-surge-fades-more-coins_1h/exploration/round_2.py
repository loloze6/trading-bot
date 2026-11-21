def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; rowsd = []
    for coin, wins in bars.items():
        prep = {}; allr = {48: [], 120: [], 240: []}; r24a = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            r1 = c.pct_change()
            vol720 = r1.rolling(720, min_periods=240).std()
            vol24 = r1.rolling(24, min_periods=24).std()
            vr = vol24 / vol720
            r24 = c / c.shift(24) - 1
            r30 = (c / c.shift(720) - 1) / (vol720 * np.sqrt(720))
            f = {h: c.shift(-h) / c - 1 for h in (48, 120, 240)}
            for h in f:
                allr[h] += list(f[h].iloc[np.arange(0, n, h)].dropna())
            f24 = c.shift(-24) / c - 1
            r24a += list(f24.iloc[np.arange(0, n, 24)].dropna())
            prep[w] = (n, f, f24, vr, r24, r30, ts)
        if len(allr[120]) < 10: continue
        mom = {h: (np.mean(allr[h]), np.std(allr[h])) for h in allr}
        m24 = (np.mean(r24a), np.std(r24a))
        for w, (n, f, f24, vr, r24, r30, ts) in prep.items():
            for h in (48, 120, 240):
                for i in np.arange(0, n, h):
                    if pd.isna(f[h].iloc[i]) or pd.isna(vr.iloc[i]): continue
                    rows.append(dict(coin=coin, win=w, yr=ts.iloc[i].year, h=h,
                        y=(f[h].iloc[i]-mom[h][0])/mom[h][1], ypct=f[h].iloc[i]-mom[h][0],
                        vr=vr.iloc[i], s24=np.sign(r24.iloc[i]), r30=r30.iloc[i]))
            for i in np.arange(0, n, 24):
                if pd.isna(f24.iloc[i]): continue
                rowsd.append(dict(coin=coin, win=w, yr=ts.iloc[i].year, wd=ts.iloc[i].dayofweek,
                    y=(f24.iloc[i]-m24[0])/m24[1]))
    A = pd.DataFrame(rows); D = pd.DataFrame(rowsd)
    res = {}
    def summ(df, key, col="y"):
        g = df.groupby(key)[col]; o = g.agg(["count", "mean", "std"])
        o["t"] = o["mean"]/(o["std"]/np.sqrt(o["count"])); return o.drop(columns="std")
    for h in (48, 120, 240):
        a = A[A.h == h].copy()
        a["vq"] = a.groupby("coin")["vr"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        o = summ(a, "vq"); o["mean_pct"] = a.groupby("vq")["ypct"].mean(); res[f"h{h} by vr quintile (per coin)"] = o
        if h == 120:
            a["vs"] = a["vq"].astype(str) + "_s" + a["s24"].astype(str)
            res["h120 vr quintile x sign of 24h return"] = summ(a, "vs")
            # within-window spearman
            sw = a.groupby("win").apply(lambda d: stats.spearmanr(d.vr, d.y)[0] if len(d) > 20 else np.nan)
            res["h120 vr spearman by window: share>0, mean, t"] = pd.Series({"share_pos": (sw > 0).mean(), "mean": sw.mean(),
                "t": sw.mean()/(sw.std()/np.sqrt(sw.notna().sum())), "nwin": sw.notna().sum()})
            sc = a.groupby("coin").apply(lambda d: stats.spearmanr(d.vr, d.y)[0])
            res["h120 vr spearman by coin"] = sc
            # top minus bottom by year
            yy = a[a.vq.isin([0, 4])].groupby(["yr", "vq"])["y"].mean().unstack()
            yy["top_minus_bottom"] = yy[4] - yy[0]; res["h120 vr top-bottom by year"] = yy
            d = a.dropna(subset=["r30"])
            sw2 = d.groupby("win").apply(lambda x: stats.spearmanr(x.r30, x.y)[0] if len(x) > 20 else np.nan)
            res["h120 r30 spearman by window"] = pd.Series({"share_pos": (sw2 > 0).mean(), "mean": sw2.mean(),
                "t": sw2.mean()/(sw2.std()/np.sqrt(sw2.notna().sum())), "nwin": sw2.notna().sum()})
            sc2 = d.groupby("coin").apply(lambda x: stats.spearmanr(x.r30, x.y)[0])
            res["h120 r30 spearman by coin: share>0"] = pd.Series({"share_pos": (sc2 > 0).mean(), "mean": sc2.mean()})
    wy = D.groupby(["yr", "wd"])["y"].mean().unstack()
    res["1d weekday mean by year"] = wy
    ww = D.groupby(["win", "wd"])["y"].mean().unstack()
    res["1d weekday: share of windows positive"] = (ww > 0).mean()
    return res
