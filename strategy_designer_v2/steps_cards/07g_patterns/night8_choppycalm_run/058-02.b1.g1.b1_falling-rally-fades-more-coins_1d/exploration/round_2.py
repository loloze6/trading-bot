def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std().shift(1)
            v30=r.rolling(30,min_periods=20).std()
            z=r/vol
            tr60=c/c.shift(60)-1
            hi20=c.rolling(20).max(); lo20=c.rolling(20).min()
            rpos=(c-lo20)/(hi20-lo20).replace(0,np.nan)
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"ts":pd.to_datetime(b["timestamp"]),
              "r":r,"z":z,"tr60":tr60,"v30":v30,"rpos":rpos,"f1":f1,"f3":f3})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D.ts.dt.floor("D"); D["yr"]=D.ts.dt.year
    mu=D.groupby("coin").r.mean(); D["x1"]=D.f1-D.coin.map(mu)
    mu3=D[D.i%3==0].groupby("coin").f3.mean(); D["x3"]=D.f3-D.coin.map(mu3)
    med=D.groupby("coin").v30.transform("median")
    D["agit"]=np.where(D.v30>med,"agit","calm")
    D["trb"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    def tt(s,days):
        g=pd.DataFrame({"s":s,"d":days}).dropna()
        if len(g)<10: return (np.nan,np.nan,len(g),0)
        m=g.s.mean(); ds=(g.s-m).groupby(g.d).sum()
        se=np.sqrt((ds**2).sum())/len(g)
        return (m,m/se if se>0 else np.nan,len(g),len(ds))
    out={}
    D["zb"]=pd.cut(D.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    res=[]
    for (a,b_),g in D.groupby(["agit","zb"],observed=True):
        m,t,n,nd=tt(g.x1,g.day); res.append([a,str(b_),n,nd,m*100,t])
    out["next1_by_agit_z"]=pd.DataFrame(res,columns=["agit","z","n","days","mean%","t"])
    # up-day fade in agitated: per trend, per year
    A=D[(D.agit=="agit")&(D.z>0)]
    res=[]
    for a,g in A.groupby("trb",observed=True):
        m,t,n,nd=tt(g.x1*-1,g.day)
        sl=np.polyfit(g.dropna(subset=["x1","z"]).z.clip(upper=5),g.dropna(subset=["x1","z"]).x1,1)[0]
        res.append([a,n,nd,m*100,t,sl*100])
    out["agit_up_short_by_trend"]=pd.DataFrame(res,columns=["trend","n","days","short_mean%","t","slope%perz"])
    res=[]
    for a,g in A.groupby("yr"):
        m,t,n,nd=tt(g.x1*-1,g.day); res.append([a,n,m*100,t])
    out["agit_up_short_by_year"]=pd.DataFrame(res,columns=["yr","n","short_mean%","t"])
    res=[]
    for a,g in A.groupby("w"):
        m,t,n,nd=tt(g.x1*-1,g.day); res.append([a,n,m*100,t])
    out["agit_up_short_by_window"]=pd.DataFrame(res,columns=["w","n","short_mean%","t"])
    # weighted by z clipped
    g=A.dropna(subset=["x1","z"]); wz=g.z.clip(upper=5)
    out["agit_up_weighted_short_mean%"]=float(-(g.x1*wz).sum()/wz.sum()*100)
    # choppy range-bottom continuation
    G=D[(D.i%3==0)&(D.trb=="chop")]
    G["rpb"]=pd.cut(G.rpos,[-0.01,0.1,0.3,0.7,0.9,1.01])
    res=[]
    for (a,b_),g in G.groupby(["agit","rpb"],observed=True):
        m,t,n,nd=tt(g.x3,g.day); res.append([a,str(b_),n,m*100,t])
    out["chop_next3_by_agit_rpos"]=pd.DataFrame(res,columns=["agit","rpos","n","mean%","t"])
    # big down in agitated by trend
    B=D[(D.agit=="agit")&(D.z<-1)]
    res=[]
    for a,g in B.groupby("trb",observed=True):
        m,t,n,nd=tt(g.x1,g.day); res.append([a,n,nd,m*100,t])
    out["agit_bigdown_next1_by_trend"]=pd.DataFrame(res,columns=["trend","n","days","mean%","t"])
    return out
