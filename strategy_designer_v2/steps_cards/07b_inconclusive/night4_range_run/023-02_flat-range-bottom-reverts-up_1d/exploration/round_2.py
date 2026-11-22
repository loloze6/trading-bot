def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            rs += list(c[idx + 5] / c[idx] - 1)
        d0, sd0 = np.mean(rs), np.std(rs)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            hi = df["high"].rolling(30).max(); lo = df["low"].rolling(30).min()
            mid = (hi + lo) / 2
            dist = (c - mid) / c
            net = c - c.shift(29)
            nmr = net.abs() / (hi - lo)
            r5p = c / c.shift(5) - 1
            r90 = c / c.shift(90) - 1
            vol = np.log(c).diff().rolling(30).std()
            rngw = (hi - lo) / c
            cv = c.values
            for i in np.arange(0, len(cv) - 5, 5):
                rows.append(dict(coin=coin, fc=df["forecast"].iloc[i], dist=dist.iloc[i], nmr=nmr.iloc[i],
                                 net=net.iloc[i], r5p=r5p.iloc[i], r90=r90.iloc[i], vol=vol.iloc[i], rngw=rngw.iloc[i],
                                 ret=cv[i + 5] / cv[i] - 1 - d0, sd=sd0))
    R = pd.DataFrame(rows)
    def summ(g):
        g = g.dropna(subset=["ret"])
        return pd.Series(dict(n=len(g), mean=g.ret.mean(), t=g.ret.mean() / (g.ret.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    a = R[R.fc > 0].copy()
    out = {}
    a["net_up"] = (a.net > 0)
    out["by_net30_sign"] = a.groupby("net_up").apply(summ)
    a["r5_down"] = a.r5p < 0
    out["by_prior5d_sign"] = a.groupby("r5_down").apply(summ)
    a2 = a.dropna(subset=["r90"]).copy()
    a2["r90_up"] = a2.r90 > 0
    out["by_r90_sign"] = a2.groupby("r90_up").apply(summ)
    a3 = a.dropna(subset=["vol"]).copy()
    a3["vt"] = pd.qcut(a3.vol.rank(method="first"), 3, labels=False)
    out["by_vol_tercile"] = a3.groupby("vt").apply(summ)
    a4 = a.dropna(subset=["rngw"]).copy()
    a4["rt"] = pd.qcut(a4.rngw.rank(method="first"), 3, labels=False)
    out["by_rangewidth_tercile"] = a4.groupby("rt").apply(summ)
    a5 = a.dropna(subset=["r5p"]).copy()
    a5["pt"] = pd.qcut(a5.r5p.rank(method="first"), 3, labels=False)
    out["by_prior5d_tercile"] = a5.groupby("pt").apply(summ)
    # flat below mid, raw distance terciles
    fb = R[(R.dist < 0) & (R.nmr <= 0.3)].copy()
    fb["dt"] = pd.qcut((-fb.dist).rank(method="first"), 3, labels=False)
    out["flat_below_by_dist_tercile"] = fb.groupby("dt").apply(summ)
    # strength
    out["strength_active"] = pd.Series(dict(strength=(a.ret / a.sd).mean(), n=len(a)))
    return out
