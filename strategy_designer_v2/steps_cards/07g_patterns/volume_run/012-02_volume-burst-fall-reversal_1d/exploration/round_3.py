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
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1; f7=c.shift(-7)/c-1
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),z=z,r1=r1,vr=vr,vol20=vol20,
                        f1=f1,f3=f3,f7=f7,wd=ts.dt.weekday,yr=ts.dt.year)))
    D=pd.concat(rows,ignore_index=True)
    m3=D[D.pos%3==0].groupby("coin").f3.mean(); D["x3"]=D.f3-D.coin.map(m3)
    m7=D[D.pos%7==0].groupby("coin").f7.mean(); D["x7"]=D.f7-D.coin.map(m7)
    m1=D.groupby("coin").f1.mean(); D["x1"]=D.f1-D.coin.map(m1)
    D["lvr"]=np.log(D.vr)
    out={}
    def reg(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<10: return pd.Series(dict(slope=np.nan,t=np.nan,n=len(df)))
        s=stats.linregress(df[x],df[y]); return pd.Series(dict(slope=s.slope,t=s.slope/s.stderr,n=len(df)))
    G=D[D.pos%3==0].dropna(subset=["x3","lvr","z"]).copy()
    Dn=G[G.r1<0].copy(); Up=G[G.r1>0].copy()
    out["down bars logvr->x3 per coin"]=Dn.groupby("coin").apply(lambda d:reg(d,"lvr","x3"))
    out["down bars logvr->x3 by year"]=Dn.groupby("yr").apply(lambda d:reg(d,"lvr","x3"))
    Dn["zb"]=pd.cut(Dn.z,[-99,-2,-1,0])
    out["down bars logvr->x3 by fall size"]=Dn.groupby("zb").apply(lambda d:reg(d,"lvr","x3"))
    Dn["vq"]=Dn.groupby("coin").lvr.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["down bars x3 by vr quintile"]=Dn.groupby("vq").x3.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    Up["vq"]=Up.groupby("coin").lvr.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["up bars x3 by vr quintile"]=Up.groupby("vq").x3.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # multivariate on down bars: x3 ~ lvr + z
    X=np.column_stack([np.ones(len(Dn)),Dn.lvr,Dn.z]); y=Dn.x3.values
    b,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
    cov=np.linalg.inv(X.T@X)*(e@e)/(len(y)-3)
    out["down x3 ~ lvr + z (coef,t)"]=pd.DataFrame(dict(coef=b,t=b/np.sqrt(np.diag(cov))),index=["const","lvr","z"])
    # signed volume: lvr*sign
    G["sv"]=-np.sign(G.r1)*G.lvr
    out["all x3 ~ -sign(r)*logvr"]=reg(G,"sv","x3")
    G1=D.dropna(subset=["x1","lvr"]); G1=G1[G1.r1<0]
    out["down bars logvr->x1 (all bars)"]=reg(G1,"lvr","x1")
    G7=D[(D.pos%7==0)&(D.r1<0)].dropna(subset=["x7","lvr"])
    out["down bars logvr->x7 grid7"]=reg(G7,"lvr","x7")
    # weekday ThuFri vs MonWed welch t per coin
    D2=D.dropna(subset=["x1"])
    out["weekday welch per coin"]=D2.groupby("coin").apply(lambda d:pd.Series(dict(diff=d[d.wd.isin([3,4])].x1.mean()-d[d.wd.isin([0,2])].x1.mean(),
        t=stats.ttest_ind(d[d.wd.isin([3,4])].x1,d[d.wd.isin([0,2])].x1,equal_var=False).statistic)))
    return out
