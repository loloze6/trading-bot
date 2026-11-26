def explore(data):
    import pandas as pd, numpy as np
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])
            clv=(c-b["low"])/rng.replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":r/sd,"sd":sd,
                "fwd":c.shift(-H)/c-1,"fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,
                "ret60":c/c.shift(60)-1,"ret30":c/c.shift(30)-1,"clv":clv,"rngz":(rng/c)/sd,
                "day":ts.dt.floor("D")}))
    A=pd.concat(rows,ignore_index=True)
    A["agit"]=A.groupby("coin")["sd"].rank(pct=True)>0.5
    drift={h:A.loc[A.pos%h==0].groupby("coin")[f].mean() for h,f in [(5,"fwd"),(1,"fwd1"),(2,"fwd2")]}
    A["ex"]=A.fwd-A.coin.map(drift[5]); A["ex1"]=A.fwd1-A.coin.map(drift[1]); A["ex2"]=A.fwd2-A.coin.map(drift[2])
    def pt(g,col):
        g=g.dropna(subset=[col])
        if len(g)<5: return (len(g),np.nan,np.nan)
        m=g[col].mean(); s=(g[col]-m).groupby(g["day"]).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/(D-1))/len(g)
        return (len(g),m,m/se)
    def tab(G,by,col):
        o={k:pt(g,col) for k,g in G.groupby(by,observed=True)}
        return pd.DataFrame(o,index=["n","mean","t_day"]).T
    out={}
    G=A[A.pos%5==0].dropna(subset=["clv","ex"]).copy()
    G["clvq"]=pd.qcut(G.clv,5,labels=False)
    out["ex5 by clv quintile"]=tab(G,"clvq","ex")
    out["ex5 clv q x agit"]=tab(G,["agit","clvq"],"ex")
    G["tr"]=pd.cut(G.ret30,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["ex5 clv q x trend30"]=tab(G[G.clvq.isin([0,4])],["tr","clvq"],"ex")
    out["ex5 lowclv by window"]=G[G.clvq==0].groupby("w")["ex"].mean()
    # offset robustness
    res=[]
    for off in range(5):
        g=A[(A.pos%5==off)].dropna(subset=["clv","ex"]).copy()
        g["q"]=pd.qcut(g.clv,5,labels=False)
        res.append(pt(g[g.q==0],"ex")+pt(g[g.q==4],"ex"))
    out["offset low/high clv"]=pd.DataFrame(res,columns=["n_lo","m_lo","t_lo","n_hi","m_hi","t_hi"])
    # low clv interaction with day sign & range size
    G["zs"]=np.where(G.z>0,"up","dn")
    out["ex5 clvq x daysign"]=tab(G[G.clvq.isin([0,4])],["zs","clvq"],"ex")
    G["rq"]=pd.qcut(G.rngz,3,labels=["narrow","mid","wide"])
    out["ex5 lowclv x range"]=tab(G[G.clvq==0],"rq","ex")
    # big up days by agitation
    G["zb"]=pd.cut(G.z,[-99,-1.5,0,1.5,99],labels=["bigdn","dn","up","bigup"])
    out["ex5 z x agit"]=tab(G,["agit","zb"],"ex")
    # next day rebound after big down, by agitation (grid of 1 = every bar)
    D=A.dropna(subset=["z","ex1"]).copy()
    D["zb"]=pd.cut(D.z,[-99,-2,-1,0,1,2,99])
    out["ex1 z x agit"]=tab(D,["agit","zb"],"ex1")
    return out
