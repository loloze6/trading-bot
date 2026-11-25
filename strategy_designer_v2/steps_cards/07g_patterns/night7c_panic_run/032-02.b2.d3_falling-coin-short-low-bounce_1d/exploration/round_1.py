import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["r1"]=c.shift(-1)/c-1
            d["r3"]=c.shift(-3)/c-1
            d["pos"]=np.arange(len(b))
            d["prev1"]=c/c.shift(1)-1
            d["ret30"]=c/c.shift(30)-1
            d["ret7"]=c/c.shift(7)-1
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std()
            d["volr"]=d["vol20"]/lr.rolling(120,min_periods=60).std()
            low10=b["low"].shift(1).rolling(10).min()
            d["depth"]=c/low10-1
            hi30=b["high"].shift(1).rolling(30).max()
            d["dhi30"]=c/hi30-1
            d["range"]=(b["high"]-b["low"])/c
            d["alloc"]=b["postRebalance_current_allocation"]
            d["wd"]=d["ts"].dt.weekday
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean(); D["x1"]=D["r1"]-D["coin"].map(mu)
    D["day"]=D["ts"].dt.floor("D")
    def tstat(sub,col="x1"):
        s=sub.dropna(subset=[col])
        g=s.groupby("day")[col].sum(); n=len(s)
        if n<5: return (n,np.nan,np.nan)
        m=s[col].mean()
        se=np.sqrt(((g-0)**2).sum()- 0) # placeholder
        dev=s[col]-m; gd=dev.groupby(s["day"]).sum()
        se=np.sqrt((gd**2).sum())/n
        return (n,m,m/se)
    def grp(key,bins=None,q=None,sub=None):
        S=D if sub is None else sub
        k=pd.qcut(S[key],q,duplicates="drop") if q else S[key]
        out=[]
        for lab,s in S.groupby(k,observed=True):
            n,m,t=tstat(s); out.append((str(lab),n,m,t))
        return pd.DataFrame(out,columns=["grp","n","mean_x1","t"])
    res={}
    res["by_prev1_decile"]=grp("prev1",q=10)
    res["by_volratio_q5"]=grp("volr",q=5)
    res["by_range_q5"]=grp("range",q=5)
    res["by_weekday"]=grp("wd")
    res["by_ret7_decile"]=grp("ret7",q=10)
    res["by_dhi30_decile"]=grp("dhi30",q=10)
    fall=D[(D.ret30<0)&(D.depth<0)]
    res["falling_break_depth_q5"]=grp("depth",q=5,sub=fall)
    res["falling_break_prev1_q5"]=grp("prev1",q=5,sub=fall)
    rise=D[(D.ret30>0)&(D.depth<0)]
    res["rising30_break_depth_q3"]=grp("depth",q=3,sub=rise)
    # 3-day horizon non-overlap
    G=D[D.pos%3==0].copy(); mu3=G.groupby("coin")["r3"].mean(); G["x3"]=G["r3"]-G["coin"].map(mu3)
    out=[]
    for lab,s in G.groupby(pd.qcut(G["prev1"],5),observed=True):
        n,m,t=tstat(s,"x3"); out.append((str(lab),n,m,t))
    res["h3_by_prev1_q5"]=pd.DataFrame(out,columns=["grp","n","mean_x3","t"])
    # corr of prev1 and r1 by coin
    res["corr_prev1_r1_by_coin"]=D.groupby("coin").apply(lambda s:s[["prev1","r1"]].corr().iloc[0,1])
    return res
