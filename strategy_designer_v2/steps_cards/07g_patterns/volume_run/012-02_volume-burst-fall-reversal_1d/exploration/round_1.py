import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol20=r1.rolling(20,min_periods=20).std().shift(1)
            z=r1/vol20
            vr=b["volume"]/b["volume"].rolling(30,min_periods=30).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            wick=(np.minimum(b["open"],c)-b["low"])/rng
            uwick=(b["high"]-np.maximum(b["open"],c))/rng
            r5=c/c.shift(5)-1
            r20=c/c.shift(20)-1
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1; f7=c.shift(-7)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),z=z,vr=vr,wick=wick,uwick=uwick,r5=r5,r20=r20,vol20=vol20,
                                f1=f1,f3=f3,f7=f7,wd=ts.dt.weekday,yr=ts.dt.year,alloc=b["postRebalance_current_allocation"]))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin mean 3-bar return on grid
    g3=D[D.pos%3==0]
    m3=g3.groupby("coin").f3.mean()
    D["x3"]=D.f3-D.coin.map(m3)
    g7=D[D.pos%7==0]; m7=g7.groupby("coin").f7.mean(); D["x7"]=D.f7-D.coin.map(m7)
    G=D[D.pos%3==0].dropna(subset=["x3","z"]).copy()
    out={}
    def reg(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<10: return (np.nan,np.nan,len(df))
        s=stats.linregress(df[x],df[y]); return (s.slope,s.slope/s.stderr,len(df))
    # z buckets
    G["zb"]=pd.cut(G.z,[-99,-3,-2,-1,0,1,2,3,99])
    out["x3 by z bucket (grid3)"]=G.groupby("zb").x3.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # events: greedy thinning of sharp falls
    ev=[]
    for (c_,w_),d in D.groupby(["coin","w"]):
        last=-99
        for i,rw in d[d.z<=-2].iterrows():
            if rw.pos-last>=3: ev.append(i); last=rw.pos
    E=D.loc[ev].dropna(subset=["x3"])
    out["falls n"]=len(E)
    out["falls x3 ~ wick (slope,t,n)"]=str(reg(E,"wick","x3"))
    out["falls x3 ~ vr"]=str(reg(E,"vr","x3"))
    out["falls x3 ~ z"]=str(reg(E,"z","x3"))
    out["falls x3 ~ r20"]=str(reg(E,"r20","x3"))
    out["falls x7 ~ wick"]=str(reg(E,"wick","x7"))
    E["wq"]=pd.qcut(E.wick,3,labels=False)
    out["falls x3 by wick tercile"]=E.groupby("wq").x3.agg(["mean","count"])
    # up shocks
    up=[]
    for (c_,w_),d in D.groupby(["coin","w"]):
        last=-99
        for i,rw in d[d.z>=2].iterrows():
            if rw.pos-last>=3: up.append(i); last=rw.pos
    U=D.loc[up].dropna(subset=["x3"])
    out["ups x3 mean,t,n"]=str((U.x3.mean(),U.x3.mean()/U.x3.std()*np.sqrt(len(U)),len(U)))
    out["ups x3 ~ vr"]=str(reg(U,"vr","x3")); out["ups x3 ~ uwick"]=str(reg(U,"uwick","x3"))
    # all bars grid regressions
    out["grid x3 ~ z"]=str(reg(G,"z","x3")); out["grid x3 ~ r20"]=str(reg(G,"r20","x3"))
    out["grid x3 ~ vr"]=str(reg(G,"vr","x3")); out["grid x3 ~ wick"]=str(reg(G,"wick","x3"))
    G7=D[D.pos%7==0].dropna(subset=["x7"])
    out["grid7 x7 ~ r20"]=str(reg(G7,"r20","x7")); out["grid7 x7 ~ r5"]=str(reg(G7,"r5","x7"))
    # vol level
    G["vq"]=G.groupby("coin").vol20.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["x3 by vol quintile"]=G.groupby("vq").x3.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # weekday
    m1=D.groupby("coin").f1.mean(); D["x1"]=D.f1-D.coin.map(m1)
    out["x1 by weekday"]=D.dropna(subset=["x1"]).groupby("wd").x1.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # per coin regression x3~z on grid
    out["per coin grid x3~z"]=pd.DataFrame({c:reg(d,"z","x3") for c,d in G.groupby("coin")},index=["slope","t","n"]).T
    # book
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            br.append(d.assign(coin=coin,w=w))
    B=pd.concat(br)
    dm=B.groupby("day")[["book_return","coin_return"]].mean().dropna()
    out["book daily mean,std,sharpe"]=str((dm.book_return.mean(),dm.book_return.std(),dm.book_return.mean()/dm.book_return.std()*np.sqrt(365)))
    out["share days active"]=float((D.alloc.abs()>1e-6).mean())
    return out
