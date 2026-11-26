import pandas as pd, numpy as np

def tclust(x, day):
    d = pd.DataFrame(dict(x=x, day=day)).dropna()
    if len(d) < 3: return np.nan, len(d), 0
    m = d.x.mean(); s = (d.x - m).groupby(d.day).sum()
    G = len(s)
    if G < 2: return np.nan, len(d), G
    se = np.sqrt((s**2).sum() * G/(G-1)) / len(d)
    return m/se, len(d), G

def slope_clust(x, y, day):
    d = pd.DataFrame(dict(x=x, y=y, day=day)).dropna()
    if len(d) < 5: return np.nan, np.nan, len(d)
    xc = d.x - d.x.mean(); b = (xc*(d.y-d.y.mean())).sum()/(xc**2).sum()
    e = d.y - d.y.mean() - b*xc
    s = (xc*e).groupby(d.day).sum(); G = len(s)
    se = np.sqrt((s**2).sum()*G/(G-1))/(xc**2).sum()
    return b, b/se, len(d)

def explore(data):
    bars = data["bars"]
    cm = {}; cm1 = {}
    for c, ws in bars.items():
        r = []; r1 = []
        for w, b in ws.items():
            cl = b["close"].values
            r += [cl[i+14]/cl[i]-1 for i in range(0, len(cl)-14, 14)]
            r1 += list(cl[1:]/cl[:-1]-1)
        cm[c] = np.mean(r); cm1[c] = np.mean(r1)
    G = []; D = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True); cl = b["close"]
            lr = cl.pct_change(); sd30 = lr.rolling(30, min_periods=20).std()
            agit = sd30 > sd30.expanding(min_periods=20).median()
            s7 = (cl/cl.shift(7)-1)/(sd30*np.sqrt(7))
            r7 = cl/cl.shift(7)-1
            ret60 = cl/cl.shift(60)-1
            ret30 = cl/cl.shift(30)-1
            f14 = cl.shift(-14)/cl-1; f7 = cl.shift(-7)/cl-1
            ts = pd.to_datetime(b["timestamp"])
            trend = np.where(ret60 > .1, "rising", np.where(ret60 < -.1, "falling", np.where(ret60.isna(), "na", "choppy")))
            df = pd.DataFrame(dict(coin=c, day=ts.dt.normalize(), s7=s7, r7=r7, ret60=ret60, ret30=ret30,
                                   x14=f14-cm[c], x7=f7-cm[c]/2, trend=trend, agit=agit, yr=ts.dt.year))
            G.append(df.iloc[list(range(0, len(b)-14, 14))])
            D.append(pd.DataFrame(dict(coin=c, day=ts.dt.normalize(), s1=lr/sd30, nx=lr.shift(-1)-cm1[c],
                                       nx3=(cl.shift(-3)/cl-1)-3*cm1[c], trend=trend, agit=agit, yr=ts.dt.year)))
    g = pd.concat(G).dropna(subset=["x14", "s7"]); d = pd.concat(D).dropna(subset=["nx", "s1"])
    out = {}
    # A: falling trend, rising week
    rows = []
    for lab, sub in [("falling all", g[g.trend=="falling"]),
                     ("falling, s7>0", g[(g.trend=="falling")&(g.s7>0)]),
                     ("falling calm s7>0", g[(g.trend=="falling")&(g.s7>0)&(~g.agit)]),
                     ("falling agit s7>0", g[(g.trend=="falling")&(g.s7>0)&(g.agit)]),
                     ("choppy s7>0", g[(g.trend=="choppy")&(g.s7>0)]),
                     ("rising s7>0", g[(g.trend=="rising")&(g.s7>0)]),
                     ("all ret60 known s7>0", g[(g.trend!="na")&(g.s7>0)])]:
        b, tb, n = slope_clust(sub.s7, sub.x14, sub.day)
        t, n2, Gd = tclust(sub.x14, sub.day)
        b7, tb7, _ = slope_clust(sub.s7, sub.x7, sub.day)
        rows.append(dict(set=lab, n=n, days=Gd, mean_x14=sub.x14.mean(), t_mean=t, slope14=b, t_slope14=tb, slope7=b7, t_slope7=tb7))
    out["A: x14 on s7 by trend"] = pd.DataFrame(rows).set_index("set").round(4)
    fs = g[(g.trend=="falling")&(g.s7>0)]
    a = fs.groupby("yr").agg(n=("x14","size"), mx14=("x14","mean")); out["A: falling s7>0 by year"] = a.round(4)
    a = fs.groupby("coin").agg(n=("x14","size"), mx14=("x14","mean")); out["A: falling s7>0 by coin"] = a.round(4)
    fs2 = fs.copy(); fs2["q"] = pd.qcut(fs2.s7, 3, labels=False)
    out["A: falling s7>0 terciles"] = fs2.groupby("q").agg(n=("x14","size"), lo=("s7","min"), hi=("s7","max"), mx14=("x14","mean"), med=("x14","median")).round(4)
    # B: large scaled down day next day
    rows = []
    for lab, sub in [("all", d), ("rising", d[d.trend=="rising"]), ("choppy", d[d.trend=="choppy"]),
                     ("falling", d[d.trend=="falling"]), ("calm", d[~d.agit]), ("agit", d[d.agit]),
                     ("choppy calm", d[(d.trend=="choppy")&(~d.agit)]), ("rising calm", d[(d.trend=="rising")&(~d.agit)]),
                     ("falling calm", d[(d.trend=="falling")&(~d.agit)])]:
        neg = sub[sub.s1 < 0]
        b, tb, n = slope_clust(-neg.s1, neg.nx, neg.day)
        bot = neg[neg.s1 < -1.09]
        t, n2, Gd = tclust(bot.nx, bot.day)
        t3, _, _ = tclust(bot.nx3, bot.day)
        rows.append(dict(set=lab, n_neg=n, slope=b, t_slope=tb, n_big=n2, days_big=Gd, mnx_big=bot.nx.mean(), t_big=t, mnx3_big=bot.nx3.mean(), t3=t3))
    out["B: next-day after scaled fall"] = pd.DataFrame(rows).set_index("set").round(5)
    bot = d[d.s1 < -1.09]
    out["B: big fall by year"] = bot.groupby("yr").agg(n=("nx","size"), m=("nx","mean")).round(5)
    # C: weekday clustered
    rows = []
    for wd in range(7):
        sub = d[pd.to_datetime(d.day).dt.dayofweek == wd]
        t, n, Gd = tclust(sub.nx, sub.day); rows.append(dict(wd=wd, n=n, days=Gd, m=sub.nx.mean(), t=t))
    out["C: weekday next-day clustered"] = pd.DataFrame(rows).set_index("wd").round(5)
    return out
