def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # coin mean daily return over all windows
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            fc = (df["regime"] == "unknown")
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for h in [1, 2, 3, 5]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(z.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, h=h, fc=bool(fc.iloc[i]),
                                     z=z.iloc[i], ex=fwd.iloc[i] - h * mu, day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)
    out = {}
    def tclu(g):
        s = g.groupby("day")["ex"].sum()
        n = len(g)
        m = g["ex"].mean()
        se = np.sqrt((s - s.count() * 0).pow(2).sum()) / n if n > 1 else np.nan
        # clustered se of mean: sqrt(sum_day (sum dev)^2)/n
        dev = g["ex"] - m
        sdv = dev.groupby(g["day"]).sum()
        se = np.sqrt((sdv ** 2).sum()) / n
        return pd.Series(dict(n=n, days=g["day"].nunique(), mean_pct=100 * m, t=m / se if se > 0 else np.nan))
    d["zb"] = pd.cut(d["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    fcd = d[d.fc]
    out["fc_by_h_zbin"] = fcd.groupby(["h", "zb"], observed=True).apply(tclu).round(3)
    out["notfc_h1_zbin"] = d[(~d.fc) & (d.h == 1)].groupby("zb", observed=True).apply(tclu).round(3)
    up = fcd[fcd.z > 0.5]
    out["fc_up_h1_coin"] = up[up.h == 1].groupby("coin").apply(tclu).round(3)
    out["fc_up_h1_year"] = up[up.h == 1].groupby("year").apply(tclu).round(3)
    out["fc_up_h3_year"] = up[up.h == 3].groupby("year").apply(tclu).round(3)
    # slope of ex on z for up days, by h
    sl = {}
    for h in [1, 2, 3, 5]:
        g = fcd[(fcd.h == h) & (fcd.z > 0)]
        res = stats.linregress(g["z"], g["ex"])
        sl[h] = dict(n=len(g), slope_pct=100 * res.slope, t=res.slope / res.stderr)
        g = fcd[(fcd.h == h) & (fcd.z < 0)]
        res = stats.linregress(g["z"], g["ex"])
        sl[f"{h}_down"] = dict(n=len(g), slope_pct=100 * res.slope, t=res.slope / res.stderr)
    out["slopes"] = pd.DataFrame(sl).T.round(3)
    out["fc_share"] = float(d[d.h == 1].fc.mean())
    return out
