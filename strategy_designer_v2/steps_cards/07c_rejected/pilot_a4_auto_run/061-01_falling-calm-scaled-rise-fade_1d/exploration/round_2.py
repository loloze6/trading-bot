def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = pd.concat([df["close"].astype(float).reset_index(drop=True).pct_change().dropna() for df in wins.values()])
        mu = allr.mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            fc = (df["regime"] == "unknown")
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for L in [1, 3, 5]:
                zL = (c / c.shift(L) - 1) / (sd * np.sqrt(L))
                for h in [1, 2, 3, 5]:
                    fwd = c.shift(-h) / c - 1
                    for i in range(0, n, h):
                        if pd.isna(fwd.iloc[i]) or pd.isna(zL.iloc[i]) or not fc.iloc[i]:
                            continue
                        rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, L=L, h=h, z=zL.iloc[i],
                                         ex=fwd.iloc[i] - h * mu, tot=fwd.iloc[i], day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)
    def tclu(g):
        n = len(g); m = g["ex"].mean()
        sdv = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((sdv ** 2).sum()) / n
        return pd.Series(dict(n=n, days=g["day"].nunique(), mean_pct=100 * m, tot_pct=100 * g["tot"].mean(),
                              t=m / se if se > 0 else np.nan))
    def cslope(g):
        x = g["z"].values; y = g["ex"].values
        xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
        a = y.mean() - b * x.mean(); e = y - a - b * x
        sc = pd.Series(xm * e).groupby(g["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (xm ** 2).sum()
        return pd.Series(dict(n=len(g), slope_pct=100 * b, t=b / se))
    out = {}
    d["zb"] = pd.cut(d["z"], [-99, -1.5, -1, -0.5, 0, 0.5, 1, 99])
    out["bins_L_h"] = d.groupby(["L", "h", "zb"], observed=True).apply(tclu).round(3)
    out["down_slope"] = d[d.z < 0].groupby(["L", "h"]).apply(cslope).round(3)
    dn = d[(d.L == 1) & (d.z < -1)]
    out["fall1_coin_h1h2"] = dn[dn.h.isin([1, 2])].groupby(["h", "coin"]).apply(tclu).round(3)
    out["fall1_year_h1h2"] = dn[dn.h.isin([1, 2])].groupby(["h", "year"]).apply(tclu).round(3)
    dn3 = d[(d.L == 3) & (d.z < -1)]
    out["fall3_year_h3"] = dn3[dn3.h == 3].groupby("year").apply(tclu).round(3)
    return out
