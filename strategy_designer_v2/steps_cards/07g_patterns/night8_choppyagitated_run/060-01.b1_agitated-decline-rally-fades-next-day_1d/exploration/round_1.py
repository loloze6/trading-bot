import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            z=r/sd
            tr60=c/c.shift(60)-1
            n1=c.shift(-1)/c-1
            n3=c.shift(-3)/c-1
            rng=(b["high"]-b["low"])/c
            clpos=(b["close"]-b["low"])/(b["high"]-b["low"])
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"r":r,"n1":n1,"n3":n3,
                "fa":(b["regime"]=="unknown"),"tr60":tr60,"clpos":clpos,
                "wd":ts.dt.weekday,"year":ts.dt.year,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "pos":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["n1"].mean()
    d["u1"]=d["n1"]-d["coin"].map(mu)
    mu3=d[d.pos%3==0].groupby("coin")["n3"].mean()
    d["u3"]=d["n3"]-d["coin"].map(mu3)
    d["tp"]=np.where(d.tr60>0.10,"rising",np.where(d.tr60<-0.10,"falling","choppy"))
    d.loc[d.tr60.isna(),"tp"]="na"
    d["zb"]=pd.cut(d.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    def agg(g,col="u1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["FA next-day unusual by z bin"]=d[d.fa].groupby("zb").apply(agg)
    out["notFA next-day unusual by z bin"]=d[~d.fa].groupby("zb").apply(agg)
    d3=d[d.pos%3==0]
    out["FA 3day unusual by z bin (grid)"]=d3[d3.fa].groupby("zb").apply(lambda g:agg(g,"u3"))
    out["notFA by trend x z bin next day"]=d[~d.fa].groupby(["tp","zb"]).apply(agg)
    out["all by weekday next day"]=d.groupby("wd").apply(agg)
    out["FA up days by close position next day"]=d[d.fa&(d.z>0.3)].groupby(pd.cut(d.clpos,[0,0.33,0.66,1.0001])).apply(agg)
    out["FA up days by year"]=d[d.fa&(d.z>0.3)].groupby("year").apply(agg)
    # book
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd)
    br=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book days summary"]=pd.Series({"n":len(br),"mean%":br.mean()*100,"share_nonzero":(br!=0).mean(),
        "top10 sum%":br.nlargest(10).sum()*100,"bot10 sum%":br.nsmallest(10).sum()*100,"total sum%":br.sum()*100})
    out["book by window sum%"]=br.groupby(level=0).sum()*100
    return out
