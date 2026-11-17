import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r1=c/c.shift(1)-1
            vol=r1.rolling(20,min_periods=15).std()
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"year":ts.dt.year,
                "r1":r1,"z":r1/vol,"vol":vol,
                "vr":b["volume"]/b["volume"].rolling(20,min_periods=15).mean(),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f7":c.shift(-7)/c-1,
                "z3":(c/c.shift(3)-1)/(vol*np.sqrt(3)),"z7":(c/c.shift(7)-1)/(vol*np.sqrt(7)),
                "fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin means of 3-bar return non-overlapping grid
    D["pos_in_w"]=D.groupby(["coin","w"]).cumcount()
    m3=D[D.pos_in_w%3==0].groupby("coin")["f3"].mean()
    m1=D.groupby("coin")["f1"].mean()
    D["x3"]=D["f3"]-D["coin"].map(m3); D["x1"]=D["f1"]-D["coin"].map(m1)
    out={}
    # slope of x3 on z by weekday (each weekday 7 apart -> nonoverlapping)
    res=[]
    for wd,g in D.dropna(subset=["z","x3"]).groupby("wd"):
        s=stats.linregress(g["z"],g["x3"]); 
        neg=g[g.z<0]; s2=stats.linregress(neg["z"],neg["x3"])
        pos=g[g.z>0]; s3=stats.linregress(pos["z"],pos["x3"])
        res.append([wd,len(g),s.slope,s.slope/s.stderr,s2.slope/s2.stderr,s3.slope/s3.stderr])
    out["x3 on z by weekday (0=Mon)"]=pd.DataFrame(res,columns=["wd","n","slope","t","t_negz","t_posz"])
    # 1-day mean by weekday
    g=D.dropna(subset=["x1"]).groupby("wd")["x1"]
    out["next-day excess by weekday of bar"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # 1-day reversal x1 on z by weekday
    res=[]
    for wd,g in D.dropna(subset=["z","x1"]).groupby("wd"):
        s=stats.linregress(g["z"],g["x1"]); res.append([wd,s.slope,s.slope/s.stderr])
    out["x1 on z by weekday"]=pd.DataFrame(res,columns=["wd","slope","t"])
    # Sunday: interaction with volume ratio
    S=D[(D.wd==6)].dropna(subset=["z","x3","vr"])
    S["zv"]=S["z"]*S["vr"]
    X=np.column_stack([np.ones(len(S)),S.z,S.vr,S.zv]); y=S.x3.values
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-4))
    out["sunday x3 ~ z + vr + z*vr (coef,t)"]=pd.DataFrame({"coef":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z","vr","z*vr"])
    # longer-horizon: z7 -> f7 on Sunday grid per window 7-day nonoverlap (sundays)
    S7=D[D.wd==6].dropna(subset=["z7","f7"])
    s=stats.linregress(S7.z7,S7.f7); out["sunday 7d z -> next 7d slope,t,n"]=f"{s.slope:.5f},{s.slope/s.stderr:.2f},{len(S7)}"
    # by coin sunday slope
    res=[]
    for coin,g in D[D.wd==6].dropna(subset=["z","x3"]).groupby("coin"):
        s=stats.linregress(g.z,g.x3); res.append([coin,len(g),s.slope/s.stderr])
    out["sunday slope t by coin"]=pd.DataFrame(res,columns=["coin","n","t"])
    # vol regime: sunday z effect by vol tercile
    S=D[D.wd==6].dropna(subset=["z","x3","vol"]).copy()
    S["vq"]=S.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    res=[]
    for q,g in S.groupby("vq"):
        s=stats.linregress(g.z,g.x3); res.append([q,len(g),s.slope,s.slope/s.stderr])
    out["sunday slope by vol tercile"]=pd.DataFrame(res,columns=["vq","n","slope","t"])
    return out
