def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std().shift(1)
            z=r/vol
            tr60=c/c.shift(60)-1
            tr20=c/c.shift(20)-1
            rng=(b["high"]-b["low"])/c
            pos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            hi20=c.rolling(20).max(); lo20=c.rolling(20).min()
            rpos=(c-lo20)/(hi20-lo20).replace(0,np.nan)
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"ts":pd.to_datetime(b["timestamp"]),
              "r":r,"z":z,"tr60":tr60,"tr20":tr20,"vol":vol,"rng":rng,"pos":pos,"rpos":rpos,"f1":f1,"f3":f3,
              "alloc":b["postRebalance_current_allocation"],"fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D.ts.dt.floor("D")
    D["wd"]=D.ts.dt.weekday
    mu=D.groupby("coin").r.mean(); D["x1"]=D.f1-D.coin.map(mu)
    mu3=D[D.i%3==0].groupby("coin").f3.mean(); D["x3"]=D.f3-D.coin.map(mu3)
    def tt(s,days):
        g=pd.DataFrame({"s":s,"d":days}).dropna()
        if len(g)<10: return (np.nan,np.nan,len(g))
        m=g.s.mean(); ds=(g.s-m).groupby(g.d).sum(); n=len(ds)
        se=np.sqrt((ds**2).sum())/len(g)
        return (m,m/se if se>0 else np.nan,len(g))
    out={}
    D["trb"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    D["zb"]=pd.cut(D.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    res=[]
    for (a,bq),g in D.groupby(["trb","zb"],observed=True):
        m,t,n=tt(g.x1,g.day); res.append([a,str(bq),n,m*100,t])
    out["next1_excess_by_trend_z"]=pd.DataFrame(res,columns=["trend","z","n","mean%","t"])
    g3=D[D.i%3==0]; res=[]
    for (a,bq),g in g3.groupby(["trb","zb"],observed=True):
        m,t,n=tt(g.x3,g.day); res.append([a,str(bq),n,m*100,t])
    out["next3_excess_by_trend_z_grid"]=pd.DataFrame(res,columns=["trend","z","n","mean%","t"])
    # brief: range position 20d in choppy, by vol level
    D["volq"]=D.groupby("coin").vol.transform(lambda s:s.rank(pct=True))
    D["rpb"]=pd.cut(D.rpos,[-0.01,0.1,0.3,0.7,0.9,1.01])
    res=[]
    for (a,bq),g in g3.assign(volq=D.loc[g3.index,"volq"],rpb=D.loc[g3.index,"rpb"]).groupby(["trb","rpb"],observed=True):
        m,t,n=tt(g.x3,g.day); res.append([a,str(bq),n,m*100,t])
    out["next3_by_trend_rangepos20"]=pd.DataFrame(res,columns=["trend","rpos","n","mean%","t"])
    res=[]
    for wd,g in D.groupby("wd"):
        m,t,n=tt(g.x1,g.day); res.append([wd,n,m*100,t])
    out["next1_by_weekday_of_close"]=pd.DataFrame(res,columns=["wd","n","mean%","t"])
    D["volb"]=pd.cut(D.volq,[0,0.33,0.66,1.0])
    res=[]
    for (a,bq),g in D.groupby(["volb","zb"],observed=True):
        m,t,n=tt(g.x1,g.day); res.append([str(a),str(bq),n,m*100,t])
    out["next1_by_vollevel_z"]=pd.DataFrame(res,columns=["volq","z","n","mean%","t"])
    # intrabar close position
    D["pb"]=pd.cut(D.pos,[-0.01,0.2,0.4,0.6,0.8,1.01])
    res=[]
    for (a,bq),g in D.groupby(["trb","pb"],observed=True):
        m,t,n=tt(g.x1,g.day); res.append([a,str(bq),n,m*100,t])
    out["next1_by_trend_closepos"]=pd.DataFrame(res,columns=["trend","closepos","n","mean%","t"])
    return out
