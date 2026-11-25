import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            ag=(b["regime"]!="chop").astype(int)
            tr=c/c.shift(60)-1
            n=len(b)
            for t in range(n):
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[t]).year,t=t,z=z.iloc[t],ag=ag.iloc[t],tr=tr.iloc[t],
                    f1=c.iloc[t+1]/c.iloc[t]-1 if t+1<n else np.nan,
                    f23=c.iloc[t+3]/c.iloc[t+1]-1 if t+3<n else np.nan,
                    f3=c.iloc[t+3]/c.iloc[t]-1 if t+3<n else np.nan,
                    f5=c.iloc[t+5]/c.iloc[t]-1 if t+5<n else np.nan,
                    fc=b["forecast"].iloc[t]))
    d=pd.DataFrame(rows)
    out={}
    res=[]
    for name,col,h in [("d1","f1",1),("d2-3","f23",2),("d1-3","f3",3),("d1-5","f5",5)]:
        g=d[d.t%h==0].copy()
        g[col+"x"]=g[col]-g.groupby("coin")[col].transform("mean")
        for ag in [1,0]:
            s=g[(g.ag==ag)&(g.z<0)].dropna(subset=["z",col])
            x=-s["z"];y=s[col+"x"]
            lr=stats.linregress(x,y)
            big=s[s.z<-1.5]
            res.append(dict(h=name,ag=ag,n=len(s),slope=lr.slope,t=lr.slope/lr.stderr,mean_ex=y.mean(),
                            n_big=len(big),big_ex=big[col+"x"].mean(),
                            big_t=big[col+"x"].mean()/(big[col+"x"].std()/np.sqrt(len(big)))))
    out["slope_by_h_ag"]=pd.DataFrame(res)
    # d1-3 agitated by groups
    g=d[d.t%3==0].copy(); g["x"]=g["f3"]-g.groupby("coin")["f3"].transform("mean")
    s=g[(g.ag==1)&(g.z<0)].dropna(subset=["z","x"]).copy()
    s["trend"]=np.where(s.tr>0.1,"rising",np.where(s.tr<-0.1,"falling","choppy"))
    s.loc[s.tr.isna(),"trend"]="na"
    def grp(k):
        o=[]
        for key,q in s.groupby(k):
            if len(q)<10: continue
            lr=stats.linregress(-q.z,q.x)
            o.append(dict(key=key,n=len(q),slope=lr.slope,t=lr.slope/lr.stderr,mean_ex=q.x.mean()))
        return pd.DataFrame(o)
    out["d13_ag_by_coin"]=grp("coin"); out["d13_ag_by_year"]=grp("year"); out["d13_ag_by_trend"]=grp("trend")
    s["zb"]=pd.cut(-s.z,[0,0.5,1,1.5,2,3,20])
    out["d13_ag_by_zbin"]=s.groupby("zb")["x"].agg(["count","mean"])
    # same for d2-3
    g2=d[d.t%2==0].copy(); g2["x"]=g2["f23"]-g2.groupby("coin")["f23"].transform("mean")
    s2=g2[(g2.ag==1)&(g2.z<0)].dropna(subset=["z","x"]).copy()
    s2["zb"]=pd.cut(-s2.z,[0,0.5,1,1.5,2,3,20])
    out["d23_ag_by_zbin"]=s2.groupby("zb")["x"].agg(["count","mean"])
    g1=d.copy(); g1["x"]=g1["f1"]-g1.groupby("coin")["f1"].transform("mean")
    s1=g1[(g1.ag==1)&(g1.z<0)].dropna(subset=["z","x"]).copy()
    s1["zb"]=pd.cut(-s1.z,[0,0.5,1,1.5,2,3,20])
    out["d1_ag_by_zbin"]=s1.groupby("zb")["x"].agg(["count","mean"])
    return out
