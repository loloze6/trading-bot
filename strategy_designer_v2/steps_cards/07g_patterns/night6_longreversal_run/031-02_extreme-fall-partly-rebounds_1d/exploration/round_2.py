def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for h in (3, 7, 14):
                for t in range(0, n - h, h):
                    if t < 60: continue
                    sd = np.nanstd(lr[t-59:t+1])
                    r = dict(h=h, coin=coin, win=w, ts=pd.Timestamp(df["timestamp"].iloc[t]).floor("D"),
                             yr=pd.Timestamp(df["timestamp"].iloc[t]).year,
                             fwd=c[t+h]/c[t]-1, p14=c[t]/c[t-14]-1, sd=sd)
                    r["p14z"] = np.log(c[t]/c[t-14]) / (sd*np.sqrt(14))
                    r["p7z"] = np.log(c[t]/c[t-7]) / (sd*np.sqrt(7))
                    r["p30z"] = np.log(c[t]/c[t-30]) / (sd*np.sqrt(30))
                    rows.append(r)
    D = pd.DataFrame(rows)
    D["ex"] = D["fwd"] - D.groupby(["h","coin"])["fwd"].transform("mean")
    D["exs"] = D["ex"] / D.groupby(["h","coin"])["fwd"].transform("std")
    def cl_slope(d, x, y="exs"):
        d = d.dropna(subset=[x, y])
        X = d[x] - d[x].mean(); Y = d[y] - d[y].mean()
        b = (X*Y).sum()/(X*X).sum()
        e = Y - b*X
        s = (X*e).groupby(d["ts"]).sum()
        G = len(s)
        if G < 5: return np.nan, np.nan, len(d), G
        se = np.sqrt((s**2).sum()*G/(G-1))/(X*X).sum()
        return b, b/se, len(d), G
    res = []
    for h in (3, 7, 14):
        for x in ("p7z", "p14z", "p30z"):
            b, t, n, G = cl_slope(D[D.h == h], x)
            res.append(dict(h=h, x=x, slope=round(b,4), t_day=round(t,2), n=n, days=G))
    out["slope momentum by h (std units, day-clustered)"] = pd.DataFrame(res)
    d7 = D[D.h == 7]
    res = []
    for coin, g in d7.groupby("coin"):
        b, t, n, G = cl_slope(g, "p14z"); res.append(dict(grp=coin, slope=round(b,4), t=round(t,2), n=n))
    for y, g in d7.groupby("yr"):
        b, t, n, G = cl_slope(g, "p14z"); res.append(dict(grp=str(y), slope=round(b,4), t=round(t,2), n=n))
    # vol regime split
    d7 = d7.assign(vq=d7.groupby("coin")["sd"].rank(pct=True))
    for nm, g in (("lowvol", d7[d7.vq <= 0.5]), ("highvol", d7[d7.vq > 0.5])):
        b, t, n, G = cl_slope(g, "p14z"); res.append(dict(grp=nm, slope=round(b,4), t=round(t,2), n=n))
    # up vs down side
    for nm, g in (("p14z>0", d7[d7.p14z > 0]), ("p14z<0", d7[d7.p14z < 0])):
        b, t, n, G = cl_slope(g, "p14z"); res.append(dict(grp=nm, slope=round(b,4), t=round(t,2), n=n))
    out["h7 p14z slope by coin/year/vol/side"] = pd.DataFrame(res)
    d7 = d7.assign(Q=np.ceil(d7.groupby("coin")["p14z"].rank(pct=True)*5).clip(1,5))
    out["h7 p14z quintiles"] = d7.groupby("Q").agg(n=("ex","size"), ex=("ex","mean"), fwd=("fwd","mean"))
    # weekday, one value per day (mean over coins)
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day","coin_return","book_return"]].copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    DD["ex"] = DD["coin_return"] - DD.groupby("coin")["coin_return"].transform("mean")
    day = DD.groupby("day")["ex"].mean().reset_index()
    day["wd"] = pd.to_datetime(day["day"]).dt.weekday
    day["yr"] = pd.to_datetime(day["day"]).dt.year
    out["weekday per-day mean"] = day.groupby("wd")["ex"].agg(["count","mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    sat = day[day.wd == 5].groupby("yr")["ex"].mean(); thu = day[day.wd == 3].groupby("yr")["ex"].mean()
    out["sat & thu by year"] = pd.DataFrame({"sat": sat, "thu": thu})
    # book trades
    T = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): x = df.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    T["ef"] = T["entry_forecast"].astype(float)
    out["trades summary"] = T.groupby(pd.qcut(T["ef"].rank(method="first"), 3, labels=False))["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
