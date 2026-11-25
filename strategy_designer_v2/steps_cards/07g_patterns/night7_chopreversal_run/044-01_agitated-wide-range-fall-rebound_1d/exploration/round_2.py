def explore(data):
    import numpy as np, pandas as pd
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
            d = pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"r":r,"z":r/sd,"rr":rng/mrng,
                "agit":(b["regime"]!="chop").values,"fc":b["forecast"].astype(float),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r60":c/c.shift(60)-1,"n1":c.shift(-1)/c-1-mu,"n3":c.shift(-3)/c-1-3*mu})
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z","rr","n1","r60"])
    D["trend"]=np.where(D.r60>0.1,"rising",np.where(D.r60<-0.1,"falling","choppy"))
    D["prod"]=np.where(D.r<0,(-D.z)*D.rr,0.0)
    D["upprod"]=np.where(D.r>0,D.z*D.rr,0.0)
    def tday(s, ds):
        m=s.mean(); dev=(s-m).groupby(ds).sum(); se=np.sqrt((dev**2).sum())/len(s)
        return m, (m/se if se>0 else np.nan), ds.nunique()
    def slope(x,y,ds):
        x=x-x.mean(); b=(x*y).sum()/(x*x).sum(); e=y-y.mean()-b*x
        se=np.sqrt(((x*e).groupby(ds).sum()**2).sum())/(x*x).sum()
        return b, b/se
    out={}
    tab=[]
    F=D[D.r<0]
    for (a,tr),g in F.groupby(["agit","trend"]):
        b,t=slope(g["prod"],g.n1,g.day); m,tm,nd=tday(g.n1,g.day)
        tab.append(dict(agit=a,trend=tr,n=len(g),days=nd,mean_pct=m*100,t_mean=tm,slope_bp=b*1e4,t_slope=t))
    out["fall_prod_slope_by_profile"]=pd.DataFrame(tab)
    tab=[]
    for (a,tr),g in D[D.r>0].groupby(["agit","trend"]):
        b,t=slope(g["upprod"],g.n1,g.day); m,tm,nd=tday(g.n1,g.day)
        tab.append(dict(agit=a,trend=tr,n=len(g),mean_pct=m*100,t_mean=tm,slope_bp=b*1e4,t_slope=t))
    out["up_prod_slope_by_profile"]=pd.DataFrame(tab)
    # falling agitated falls: tercile of prod, by year and coin
    G=F[(F.agit)&(F.trend=="falling")].copy()
    G["pq"]=pd.qcut(G["prod"],3,labels=["lo","mid","hi"])
    tab=[]
    for pq,g in G.groupby("pq",observed=True):
        m,t,nd=tday(g.n1,g.day); m3,t3,_=tday(g.n3.dropna(),g.dropna(subset=["n3"]).day)
        tab.append(dict(pq=pq,n=len(g),n1_pct=m*100,t1=t,n3_pct=m3*100,t3=t3))
    out["fallagit_prod_terciles"]=pd.DataFrame(tab)
    tab=[]
    for y,g in G.groupby("yr"):
        b,t=slope(g["prod"],g.n1,g.day); tab.append(dict(yr=y,n=len(g),slope_bp=b*1e4,t=t,mean_pct=g.n1.mean()*100))
    out["fallagit_by_year"]=pd.DataFrame(tab)
    tab=[]
    for co,g in G.groupby("coin"):
        b,t=slope(g["prod"],g.n1,g.day); tab.append(dict(coin=co,n=len(g),slope_bp=b*1e4,t=t,mean_pct=g.n1.mean()*100))
    out["fallagit_by_coin"]=pd.DataFrame(tab)
    # calm, non-falling: by year
    H=F[(~F.agit)&(F.trend!="falling")]
    tab=[]
    for y,g in H.groupby("yr"):
        b,t=slope(g["prod"],g.n1,g.day); tab.append(dict(yr=y,n=len(g),slope_bp=b*1e4,t=t,mean_pct=g.n1.mean()*100))
    out["calm_nonfalling_by_year"]=pd.DataFrame(tab)
    # book: active bars by trend
    A=D[D.fc>0]
    tab=[]
    for tr,g in A.groupby("trend"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(trend=tr,n=len(g),mean_pct=m*100,t=t))
    out["book_active_by_trend"]=pd.DataFrame(tab)
    return out
