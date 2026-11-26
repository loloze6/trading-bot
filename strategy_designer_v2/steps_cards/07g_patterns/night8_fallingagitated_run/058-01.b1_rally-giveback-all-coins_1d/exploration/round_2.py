import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"prof":(b["regime"]=="unknown").values,
                "z3":(c/c.shift(3)-1)/sd,"z10":(c/c.shift(10)-1)/sd,"z5":(c/c.shift(5)-1)/sd,
                "r60":c/c.shift(60)-1,"sd":sd,"f5":c.shift(-5)/c-1,"f3":c.shift(-3)/c-1,
                "pos":np.arange(len(b)),"day":ts.dt.floor("D"),"yr":ts.dt.year}))
    D=pd.concat(rows,ignore_index=True)
    D["sdrank"]=D.groupby("coin")["sd"].rank(pct=True)
    out={}
    def prep(h,fc):
        g=D[D.pos%h==0].copy()
        dr=g.groupby("coin")[fc].mean(); us=g.groupby("coin")[fc].std()
        g["u"]=g[fc]-g.coin.map(dr); g["s"]=g["u"]/g.coin.map(us); return g
    def clus(x,col):
        x=x.dropna(subset=[col,"u"])
        sg=np.sign(x[col]); su=(x.u*sg); dd=su.groupby(x.day).sum()
        return pd.Series({"n":len(x),"days":len(dd),"signed_u":su.mean(),"strength":(x.s*sg).mean(),
                          "t_day":dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan})
    g=prep(5,"f5")
    for col in ["z3","z5","z10"]:
        x=g[~g.prof].dropna(subset=[col,"u"]).copy()
        x["b"]=pd.qcut(x[col],5,labels=False)
        out[f"{col} outside profile, quintile, raw u5 (continuation if sign follows)"]=x.groupby("b").apply(lambda y: pd.Series({"n":len(y),"mean_u":y.u.mean(),"t_day":(lambda dd: dd.mean()/(dd.std()/np.sqrt(len(dd))))(y.u.groupby(y.day).sum())}))
    x=g[~g.prof].dropna(subset=["z10","u","r60"]).copy()
    x["trend"]=np.where(x.r60>0.10,"rising",np.where(x.r60<-0.10,"falling","choppy"))
    x["agit"]=np.where(x.sdrank>0.5,"agit","calm")
    x["side"]=np.where(x.z10>0,"up","down")
    x["big"]=x.z10.abs()>x.z10.abs().median()
    out["z10 sign-continuation outside profile by trend/agit/side (big moves)"]=x[x.big].groupby(["trend","agit","side"]).apply(lambda y: clus(y,"z10"))
    out["z10 sign-continuation outside profile by side and year (big)"]=x[x.big].groupby(["side","yr"]).apply(lambda y: clus(y,"z10"))
    # graded: slope of u on z10, day-clustered via binned by |z10| tercile, by side
    x["mag"]=pd.qcut(x.z10.abs(),3,labels=False)
    out["z10 graded by magnitude tercile and side"]=x.groupby(["side","mag"]).apply(lambda y: clus(y,"z10"))
    # coin breadth of down-continuation
    out["down big continuation by coin"]=x[x.big&(x.side=="down")].groupby("coin").apply(lambda y: clus(y,"z10"))
    # inside profile, z10 low -> rebound, at 3d horizon
    g3=prep(3,"f3")
    y=g3[g3.prof].dropna(subset=["z10","u"]).copy(); y["b"]=pd.qcut(y.z10,4,labels=False)
    out["in profile z10 quartile raw u3"]=y.groupby("b").apply(lambda q: pd.Series({"n":len(q),"mean_u":q.u.mean(),"t_day":(lambda dd: dd.mean()/(dd.std()/np.sqrt(len(dd))))(q.u.groupby(q.day).sum())}))
    return out
