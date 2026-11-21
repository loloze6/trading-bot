def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H = 336
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            n = len(c)
            r1 = pd.Series(np.log(c)).diff()
            vol = r1.rolling(720, min_periods=300).std().values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - H, H):
                if i < 168: continue
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, r7=c[i]/c[i-168]-1,
                                 r3=c[i]/c[i-72]-1 if i>=72 else np.nan,
                                 r14=c[i]/c[i-336]-1 if i>=336 else np.nan,
                                 vol=vol[i], f336=c[i+H]/c[i]-1, f168=c[i+168]/c[i]-1, f72=c[i+72]/c[i]-1))
    g = pd.DataFrame(rows)
    for col in ["f336","f168","f72"]:
        g[col+"x"] = g[col]-g.groupby("coin")[col].transform("mean")
    g["z7"] = g["r7"]/(g["vol"]*np.sqrt(168))
    def slope(df, x, y):
        d = df[[x,y]].dropna()
        if len(d) < 10: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        r = stats.linregress(d[x], d[y])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope/r.stderr))
    res = {}
    for x in ["r3","r7","r14","z7"]:
        for y in ["f72x","f168x","f336x"]:
            res[(x,y)] = slope(g, x, y)
    out["pooled slopes past ret -> future excess"] = pd.DataFrame(res).T.round(4)
    out["r7->f336x by coin"] = g.groupby("coin").apply(lambda d: slope(d,"r7","f336x")).round(4)
    out["r7->f336x by year"] = g.groupby("year").apply(lambda d: slope(d,"r7","f336x")).round(4)
    g["r7q"] = g.groupby("coin")["r7"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    a = g.groupby("r7q").agg(n=("f336","size"), total=("f336","mean"), excess=("f336x","mean"))
    out["r7 quintile total & excess 336"] = a.round(4)
    # 1-day fall rebound
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            r24 = pd.Series(c).pct_change(24)
            sd = r24.rolling(720, min_periods=300).std()
            for i in range(720, len(c)-168, 72):
                rows.append(dict(coin=coin, year=ts.iloc[i].year, z=r24.iloc[i]/sd.iloc[i],
                                 f24=c[i+24]/c[i]-1, f72=c[i+72]/c[i]-1, f168=c[i+168]/c[i]-1))
    d = pd.DataFrame(rows).dropna()
    for col in ["f24","f72","f168"]:
        d[col+"x"] = d[col]-d.groupby("coin")[col].transform("mean")
    neg = d[d.z<0].copy(); neg["s"] = -neg["z"]
    out["fall size -> rebound slopes"] = pd.DataFrame({y: slope(neg,"s",y) for y in ["f24x","f72x","f168x"]}).T.round(4)
    out["fall z<-1: f72x by coin"] = d[d.z<-1].groupby("coin")["f72x"].agg(["size","mean"]).round(4)
    out["fall z<-1: f72x by year"] = d[d.z<-1].groupby("year")["f72x"].agg(["size","mean"]).round(4)
    out["fall z<-1 total f72 mean"] = float(d[d.z<-1]["f72"].mean())
    pos = d[d.z>0].copy()
    out["rise size -> next slopes"] = pd.DataFrame({y: slope(pos,"z",y) for y in ["f24x","f72x","f168x"]}).T.round(4)
    # weekday daily coin returns per coin
    dd = pd.concat([df.assign(coin=c) for c, ws in data["days"].items() for df in ws.values()])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    dd["yr"] = pd.to_datetime(dd["day"]).dt.year
    dd["cx"] = dd["coin_return"]-dd.groupby("coin")["coin_return"].transform("mean")
    out["daily excess bps by weekday x coin"] = (dd.groupby(["coin","wd"])["cx"].mean().unstack()*1e4).round(1)
    out["thu minus fri? daily excess bps wd x year"] = (dd.groupby(["yr","wd"])["cx"].mean().unstack()*1e4).round(1)
    return out
