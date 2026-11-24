def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if c[i] > c[i-1]: up[i] = up[i-1] + 1
                if c[i] < c[i-1]: dn[i] = dn[i-1] + 1
            ts = pd.to_datetime(df["timestamp"])
            r60 = pd.Series(c).pct_change(60).values
            fc = df["forecast"].astype(float).values
            for h in (1, 2, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i, day=ts.iloc[i].normalize(),
                                     year=ts.iloc[i].year, fc=fc[i], up=up[i], dn=dn[i],
                                     r60=r60[i], ret=c[i+h]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30 or g[x].std() == 0: return pd.Series(dict(slope=np.nan, t=np.nan, n=len(g)))
        X = g[x].values - g[x].mean(); y = g["ex"].values
        b = (X*y).sum()/(X*X).sum(); e = y - y.mean() - b*X
        s = pd.DataFrame(dict(day=g["day"].values, s=X*e)).groupby("day")["s"].sum()
        se = np.sqrt((s**2).sum())/(X*X).sum()
        return pd.Series(dict(slope=b, t=b/se, n=len(g)))

    out = {}
    out["slope_by_h"] = d.groupby("h").apply(slope)
    d5 = d[d.h == 5]
    out["slope_by_coin_h5"] = d5.groupby("coin").apply(slope)
    out["slope_by_year_h5"] = d5.groupby("year").apply(slope)
    def bucket(v):
        return np.where(v == 0, "0", np.where(v == 1, "1", np.where(v == 2, "2", np.where(v == 3, "3", "4+"))))
    rows2 = []
    for h in (1, 3, 5, 10):
        g = d[d.h == h].copy()
        g["ub"] = bucket(g["up"]); g["db"] = bucket(g["dn"])
        a = g.groupby("ub")["ex"].agg(["mean", "count"]); a["side"] = "up"; a["h"] = h
        b = g.groupby("db")["ex"].agg(["mean", "count"]); b["side"] = "down"; b["h"] = h
        rows2 += [a, b]
    out["ex_by_streak_len"] = pd.concat(rows2).reset_index().rename(columns={"index": "len"})
    g = d5.copy(); g["regime"] = np.where(g["r60"] > 0, "r60>0", np.where(g["r60"] <= 0, "r60<=0", "na"))
    out["slope_by_r60_h5"] = g.groupby("regime").apply(slope)
    g["upx"] = g["up"]
    out["slope_rawup_by_r60_h5"] = g.groupby("regime").apply(lambda x: slope(x, "upx"))
    out["slope_rawdn_h_all"] = d.assign(dnx=d["dn"]).groupby("h").apply(lambda x: slope(x, "dnx"))
    return out
