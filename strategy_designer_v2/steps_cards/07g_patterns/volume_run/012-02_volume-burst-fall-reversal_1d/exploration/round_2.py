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
            r20=c/c.shift(20)-1
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1; f7=c.shift(-7)/c-1
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame(dict(coin=coin,w=w,wn=int(w[1:]),pos=np.arange(len(b)),z=z,r1=r1,vr=vr,r20=r20,vol20=vol20,
                        f1=f1,f3=f3,f7=f7,wd=ts.dt.weekday,yr=ts.dt.year)))
    D=pd.concat(rows,ignore_index=True)
    m3=D[D.pos%3==0].groupby("coin").f3.mean(); D["x3"]=D.f3-D.coin.map(m3)
    m7=D[D.pos%7==0].groupby("coin").f7.mean(); D["x7"]=D.f7-D.coin.map(m7)
    m1=D.groupby("coin").f1.mean(); D["x1"]=D.f1-D.coin.map(m1)
    G=D[D.pos%3==0].dropna(subset=["x3","vr","z"]).copy()
    G7=D[D.pos%7==0].dropna(subset=["x7","r20"]).copy()
    out={}
    def reg(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<10: return pd.Series(dict(slope=np.nan,t=np.nan,n=len(df)))
        s=stats.linregress(df[x],df[y]); return pd.Series(dict(slope=s.slope,t=s.slope/s.stderr,n=len(df)))
    out["vr->x3 per coin"]=G.groupby("coin").apply(lambda d:reg(d,"vr","x3"))
    out["vr->x3 by year"]=G.groupby("yr").apply(lambda d:reg(d,"vr","x3"))
    G["vrq"]=G.groupby("coin").vr.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["x3 by vr quintile"]=G.groupby("vrq").x3.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    G["dn"]=(G.r1<0).astype(int)
    out["vr->x3 by bar direction (dn=1)"]=G.groupby("dn").apply(lambda d:reg(d,"vr","x3"))
    G["lvr"]=np.log(G.vr)
    out["logvr->x3 all"]=reg(G,"lvr","x3")
    out["logvr->x3 by vol tercile"]=G.groupby(G.groupby("coin").vol20.transform(lambda s:pd.qcut(s,3,labels=False))).apply(lambda d:reg(d,"lvr","x3"))
    out["r20->x7 per coin"]=G7.groupby("coin").apply(lambda d:reg(d,"r20","x7"))
    out["r20->x7 by year"]=G7.groupby("yr").apply(lambda d:reg(d,"r20","x7"))
    # weekday by year: Thu+Fri minus Mon+Wed
    D2=D.dropna(subset=["x1"]).copy()
    D2["grp"]=np.where(D2.wd.isin([3,4]),"ThuFri",np.where(D2.wd.isin([0,2]),"MonWed","other"))
    out["weekday grp by year"]=D2[D2.grp!="other"].groupby(["yr","grp"]).x1.mean().unstack()
    out["weekday x1 per coin ThuFri-MonWed"]=D2.groupby("coin").apply(lambda d:d[d.grp=="ThuFri"].x1.mean()-d[d.grp=="MonWed"].x1.mean())
    # extreme falls by year
    F=D[D.z<=-3].dropna(subset=["x3"])
    out["z<=-3 x3 by coin"]=F.groupby("coin").x3.agg(["mean","count"])
    out["z<=-3 x3 by year"]=F.groupby("yr").x3.agg(["mean","count"])
    return out
