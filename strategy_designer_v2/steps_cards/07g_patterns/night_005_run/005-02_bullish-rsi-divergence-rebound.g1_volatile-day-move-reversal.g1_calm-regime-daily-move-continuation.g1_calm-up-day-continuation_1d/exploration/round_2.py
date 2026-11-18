def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            sc=r1/r1.abs().rolling(60,min_periods=30).mean().shift(1)
            vol=r1.rolling(20,min_periods=15).std()
            vr=vol.rolling(100,min_periods=50).rank(pct=True)
            r20p=c/c.shift(20)-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),r1=r1,sc=sc,vr=vr,r20p=r20p,
                f5=c.shift(-5)/c-1,f10=c.shift(-10)/c-1,f2=c.shift(-2)/c-1,yr=ts.dt.year))
            rows.append(d)
    D=pd.concat(rows)
    out={}
    G=D[D.pos%5==0].dropna(subset=["f5","sc"]).copy()
    G["asc"]=G.sc.abs()
    # decile of scaled move
    G["dec"]=pd.qcut(G.sc,10,labels=False)
    t=G.groupby("dec")["f5"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    t["lo"]=G.groupby("dec").sc.min();t["hi"]=G.groupby("dec").sc.max()
    out["f5 by decile of sc (60d scale)"]=t
    # abs move quintile -> f5 and sign split
    G["aq"]=pd.qcut(G.asc,5,labels=False)
    out["f5 by |sc| quintile x sign"]=G.groupby(["aq",G.sc>0])["f5"].agg(["count","mean"]).unstack()
    # slope of f5 on |sc|
    s=stats.linregress(G.asc,G.f5);out["slope f5~|sc|"]=pd.Series(dict(slope=s.slope,t=s.slope/s.stderr,n=len(G)))
    # tails vs middle Welch
    top=G[G.aq==4];rest=G[G.aq<4]
    out["top |sc| quintile vs rest"]=pd.Series(dict(diff=top.f5.mean()-rest.f5.mean(),t=stats.ttest_ind(top.f5,rest.f5,equal_var=False).statistic,n_top=len(top)))
    # robustness: by coin, by year, by window sign
    out["top|sc| by coin x sign"]=top.groupby(["coin",top.sc>0])["f5"].agg(["count","mean"])
    yy=G.groupby(["yr"]).apply(lambda g:g[g.aq==4].f5.mean()-g[g.aq<4].f5.mean())
    out["top|sc| minus rest by year"]=yy
    # by vol rank half
    G["calm"]=G.vr<0.5
    out["top|sc| by calm x sign"]=top.assign(calm=top.vr<0.5).groupby(["calm",top.sc>0])["f5"].agg(["count","mean"])
    # 10-day grid
    H=D[D.pos%10==0].dropna(subset=["f10","sc"]).copy();H["asc"]=H.sc.abs()
    H["aq"]=pd.qcut(H.asc,5,labels=False)
    t=H.groupby("aq")["f10"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["f10 by |sc| quintile (10d grid)"]=t
    # 2-day grid
    K=D[D.pos%2==0].dropna(subset=["f2","sc"]).copy();K["asc"]=K.sc.abs()
    K["aq"]=pd.qcut(K.asc,5,labels=False)
    t=K.groupby("aq")["f2"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["f2 by |sc| quintile (2d grid)"]=t
    # 20d momentum graded
    s=stats.linregress(G.dropna(subset=["r20p"]).r20p,G.dropna(subset=["r20p"]).f5)
    out["slope f5~r20p"]=pd.Series(dict(slope=s.slope,t=s.slope/s.stderr))
    return out
