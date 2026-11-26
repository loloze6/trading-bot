def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    allgrid = {}
    h = 5
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for i in range(0, n - h, h):
                allgrid.setdefault(coin, []).append(c[i + h] / c[i] - 1)
            vol = df["volume"].values
            cs = pd.Series(c)
            r20 = cs.pct_change(20).values
            r60 = cs.pct_change(60).values
            v30 = pd.Series(vol).rolling(30).mean()
            vr = np.log(v30 / v30.shift(30)).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, year=yr[i], fc=df["forecast"].iloc[i],
                    reg=df["regime"].iloc[i], fwd=c[i + h] / c[i] - 1,
                    r20=r20[i], r60=r60[i], vr=vr[i]))
    R = pd.DataFrame(rows)
    mu = {k: np.mean(v) for k, v in allgrid.items()}
    R["ex"] = R["fwd"] - R.coin.map(mu)
    R["sx"] = -R["ex"]
    def summ(g, col="sx"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(),
            t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    F = R[(R.r60 < -0.10) & R.r20.notna() & R.vr.notna()].copy()
    F["r20b"] = pd.cut(F.r20, [-1, -0.30, -0.20, -0.10, -0.05, 0, 10],
                       labels=["<-30", "-30..-20", "-20..-10", "-10..-5", "-5..0", ">0"])
    F["vrb"] = np.where(F.vr < 0, "shrink", "growth")
    out["falling_r20_by_volside"] = F.groupby(["r20b", "vrb"]).apply(summ)
    deep = F[(F.r20 < -0.10) & (F.r20 >= -0.20) & (F.vr < 0)]
    out["deep_shrink_by_year"] = deep.groupby("year").apply(summ)
    out["deep_shrink_by_coin"] = deep.groupby("coin").apply(summ)
    allr = F[F.vr < 0].copy()
    allr["vrq"] = pd.qcut(allr.vr, 3, labels=["most_shrink", "mid", "least"])
    out["falling_shrink_all_r20_by_vr_tercile"] = allr.groupby("vrq").apply(summ)
    neg = F[F.r20 < 0].copy()
    neg["depth_x_shrink"] = neg.r20 * np.minimum(neg.vr, 0)
    nz = neg[neg.depth_x_shrink > 0].copy()
    nz["q"] = pd.qcut(nz.depth_x_shrink, 3, labels=["low", "mid", "high"])
    out["depth_x_shrink_tercile"] = nz.groupby("q").apply(summ)
    out["by_year_all_shrink_r20neg"] = neg[neg.vr < 0].groupby("year").apply(summ)
    return out
