import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        cm=pd.concat([b["close"].astype(float).pct_change().dropna() for b in ws.values()]).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change(); sd=r.rolling(20).std()
            pct=sd.rolling(100,min_periods=20).apply(lambda x:(x<=x[-1]).mean(),raw=True).rolling(5).mean()
            rows.append(pd.DataFrame({"coin":coin,"vsr":r/sd,"pct":pct,"fc":b["forecast"].astype(float),
                "reg":b["regime"],"nx":c.shift(-1)/c-1-cm,"yr":pd.to_datetime(b["timestamp"]).dt.year}))
    d=pd.concat(rows).dropna(subset=["vsr","pct","nx"])
    d["fall"]=(-d["vsr"]).clip(lower=0)
    def sl(g,x):
        g=g.dropna(subset=[x])
        if len(g)<10 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        s=stats.linregress(g[x],g["nx"]); return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out={}
    d["pbin"]=pd.cut(d["pct"],[-0.01,0.2,0.4,0.6,0.8,0.9,1.01]).astype(str)
    out["fall slope by vol pct bin, all bars"]=d.groupby("pbin").apply(lambda g:sl(g,"fall"))
    reg=d[d["reg"]=="mean_reversion"]
    out["fc slope by coin, regime"]=reg.groupby("coin").apply(lambda g:sl(g,"fc"))
    out["fc slope by year, regime"]=reg.groupby("yr").apply(lambda g:sl(g,"fc"))
    pos=reg[reg["fc"]>0].copy()
    pos["q"]=pd.qcut(pos["fc"],5,labels=False,duplicates="drop")
    out["regime fc>0 quintiles"]=pos.groupby("q").agg(n=("nx","size"),fc=("fc","mean"),nx=("nx","mean"),
        t=("nx",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    z=reg[reg["fc"]==0]["nx"]
    out["regime fc==0"]=pd.Series({"n":len(z),"mean":z.mean(),"t":z.mean()/z.std()*np.sqrt(len(z))})
    out["non-regime fall slope"]=sl(d[d["reg"]!="mean_reversion"],"fall")
    d["dq"]=pd.qcut(d["vsr"],10,labels=False)
    out["all bars vsr decile next-day"]=d.groupby("dq").agg(n=("nx","size"),vsr=("vsr","mean"),nx=("nx","mean"),
        t=("nx",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    return out
