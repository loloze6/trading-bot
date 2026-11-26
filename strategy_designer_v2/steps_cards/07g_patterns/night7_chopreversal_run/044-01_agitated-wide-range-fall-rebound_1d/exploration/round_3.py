def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp"); allr.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r = c.pct_change(); sd = r.rolling(30).std()
            rng = (h-l)/c.shift(1); mrng = rng.rolling(30).mean()
            d = pd.DataFrame({"coin":coin,"win":w,"r":r,"z":r/sd,"rr":rng/mrng,
                "agit":(b["regime"]!="chop").values,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r60":c/c.shift(60)-1,"n1":c.shift(-1)/c-1-mu,"n2":c.shift(-2)/c.shift(-1)-1-mu})
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z","rr","n1","r60"])
    D["trend"]=np.where(D.r60>0.1,"rising",np.where(D.r60<-0.1,"falling","choppy"))
    D["prod"]=np.where(D.r<0,(-D.z)*D.rr,np.where(D.r>0,D.z*D.rr,0.0))
    def slope(x,y,ds):
        x=x-x.mean(); b=(x*y).sum()/(x*x).sum(); e=y-y.mean()-b*x
        se=np.sqrt(((x*e).groupby(ds).sum()**2).sum())/(x*x).sum()
        return b, b/se
    def tday(s, ds):
        m=s.mean(); dev=(s-m).groupby(ds).sum(); se=np.sqrt((dev**2).sum())/len(s)
        return m, (m/se if se>0 else np.nan), ds.nunique()
    out={}
    tab=[]
    for side,G in [("fall",D[(D.r<0)&D.agit&(D.trend=="falling")]),("rise",D[(D.r>0)&D.agit&(D.trend=="falling")])]:
        G=G.copy()
        b,t=slope(G["prod"],G.n1,G.day); tab.append(dict(side=side,test="raw",b_bp=b*1e4,t=t,n=len(G)))
        cap=G["prod"].quantile(0.95); Gc=G[G["prod"]<=cap]
        b,t=slope(Gc["prod"],Gc.n1,Gc.day); tab.append(dict(side=side,test="drop_top5pct_prod",b_bp=b*1e4,t=t,n=len(Gc)))
        lo,hi=G.n1.quantile([0.02,0.98]); y=G.n1.clip(lo,hi)
        b,t=slope(G["prod"],y,G.day); tab.append(dict(side=side,test="winsor_n1",b_bp=b*1e4,t=t,n=len(G)))
        rho,p=stats.spearmanr(G["prod"],G.n1); tab.append(dict(side=side,test="spearman",b_bp=rho,t=p,n=len(G)))
        G2=G.dropna(subset=["n2"]); m,t2,_=tday(G2.n2,G2.day); tab.append(dict(side=side,test="day2_mean_pct",b_bp=m*100,t=t2,n=len(G2)))
    out["falling_agit_robust"]=pd.DataFrame(tab)
    R=D[(D.r>0)&D.agit&(D.trend=="falling")].copy()
    R["pq"]=pd.qcut(R["prod"],3,labels=["lo","mid","hi"])
    tab=[]
    for pq,g in R.groupby("pq",observed=True):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(pq=pq,n=len(g),n1_pct=m*100,t=t,days=nd))
    out["fallingagit_rise_terciles"]=pd.DataFrame(tab)
    tab=[]
    for y,g in R.groupby("yr"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(yr=y,n=len(g),n1_pct=m*100,t=t))
    out["fallingagit_rise_by_year"]=pd.DataFrame(tab)
    tab=[]
    for co,g in R.groupby("coin"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(coin=co,n=len(g),n1_pct=m*100,t=t))
    out["fallingagit_rise_by_coin"]=pd.DataFrame(tab)
    G=D[(D.r<0)&D.agit&(D.trend=="falling")].copy()
    G["pq"]=pd.qcut(G["prod"],3,labels=["lo","mid","hi"])
    tab=[]
    for (y,pq),g in G.groupby(["yr","pq"],observed=True):
        tab.append(dict(yr=y,pq=pq,n=len(g),n1_pct=g.n1.mean()*100))
    out["fallingagit_fall_terc_by_year"]=pd.DataFrame(tab)
    return out
