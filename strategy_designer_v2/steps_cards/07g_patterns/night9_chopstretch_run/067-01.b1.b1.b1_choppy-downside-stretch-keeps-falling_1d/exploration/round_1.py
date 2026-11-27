import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean()
            sd=r.rolling(20).std()
            z=((c-sma)/sma)/sd
            tr60=c/c.shift(60)-1
            sd90=r.rolling(90).std()
            rng=(b["high"]-b["low"])/c
            pos=np.arange(len(b))
            df=pd.DataFrame({"coin":coin,"w":w,"pos":pos,"z":z,"r1":r,"r5b":c/c.shift(5)-1,
                "tr60":tr60,"volrel":sd/sd90,"rng":rng,
                "f5":c.shift(-5)/c-1,"f1":c.shift(-1)/c-1,
                "choppy":(b["regime"]=="unknown"),"fc":b["forecast"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    m5=D[D.pos%5==0].groupby("coin")["f5"].mean()
    m1=D.groupby("coin")["f1"].mean()
    D["x5"]=D["f5"]-D["coin"].map(m5)
    D["x1"]=D["f1"]-D["coin"].map(m1)
    G=D[(D.pos%5==0)&D.x5.notna()]
    def tab(g,col,val="x5"):
        o=g.groupby(col)[val].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o.drop(columns="std").round(4)
    out={}
    G=G.copy()
    G["zq"]=pd.qcut(G.z,5,labels=False)
    out["z quint all"]=tab(G,"zq")
    out["z quint choppy"]=tab(G[G.choppy],"zq")
    out["z quint notchoppy"]=tab(G[~G.choppy],"zq")
    G["trd"]=np.where(G.tr60>0.1,"rise",np.where(G.tr60<-0.1,"fall",np.where(G.tr60.notna(),"chop","na")))
    G["agit"]=np.where(G.volrel>1,"agit","calm")
    out["z quint x trend"]=G.groupby(["trd","zq"])["x5"].agg(["mean","count"]).round(4).unstack()
    G["r5q"]=pd.qcut(G.r5b,5,labels=False)
    out["past5 quint"]=tab(G,"r5q")
    out["past5 quint x trend"]=G.groupby(["trd","r5q"])["x5"].mean().round(4).unstack()
    G["vq"]=pd.qcut(G.volrel,4,labels=False)
    out["volrel quart"]=tab(G,"vq")
    D1=D[D.x1.notna()].copy()
    D1["r1q"]=pd.qcut(D1.r1,5,labels=False)
    out["r1 quint next day"]=tab(D1,"r1q","x1")
    out["weekday next day"]=tab(D1,"wd","x1")
    D1["rq"]=pd.qcut(D1.rng,5,labels=False)
    out["range quint next day"]=tab(D1,"rq","x1")
    out["z quint by year choppy"]=G[G.choppy].groupby(["yr","zq"])["x5"].mean().round(4).unstack()
    out["regime share"]=D.choppy.mean()
    return out
