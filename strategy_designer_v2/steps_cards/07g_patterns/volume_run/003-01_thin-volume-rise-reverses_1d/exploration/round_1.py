import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float); v=d["volume"].astype(float)
            r1=c.pct_change()
            vol20=r1.rolling(20,min_periods=10).std()
            vr=v/v.rolling(30,min_periods=15).mean()
            r5p=c/c.shift(5)-1
            f5=c.shift(-5)/c-1
            wd=pd.to_datetime(d["timestamp"]).dt.weekday
            idx=np.arange(len(d))
            t=pd.DataFrame({"coin":coin,"w":w,"pos":idx,"r1":r1,"z":r1/vol20,"vr":vr,"r5p":r5p/(vol20*np.sqrt(5)),
                            "vol":vol20,"f5":f5,"wd":wd,"fc":d["forecast"],"alloc":d["postRebalance_current_allocation"],
                            "nxt":c.shift(-1)/c-1})
            g.append(t)
        rows.append(pd.concat(g))
    A=pd.concat(rows)
    A["vollvl"]=A.groupby("coin")["vol"].rank(pct=True)
    grid=A[(A.pos%5==0)&A.f5.notna()].copy()
    grid["ex"]=grid.f5-grid.groupby("coin")["f5"].transform("mean")
    def summ(gb):
        s=gb["ex"].agg(["mean","std","count"])
        s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"]))
        return s.drop(columns="std")
    out={}
    grid["zq"]=pd.cut(grid.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["f5 by 1d z"]=summ(grid.groupby("zq"))
    grid["vrq"]=pd.cut(grid.vr,[0,0.5,0.75,1.0,1.5,2.5,99])
    grid["up"]=np.where(grid.z>1,"bigup",np.where(grid.z<-1,"bigdn","mid"))
    out["f5 by move x vr"]=summ(grid.groupby(["up","vrq"]))
    grid["r5q"]=pd.qcut(grid.r5p,5)
    out["f5 by prior5d scaled"]=summ(grid.groupby("r5q"))
    grid["vlq"]=pd.cut(grid.vollvl,[0,.33,.66,1])
    out["f5 by vol level"]=summ(grid.groupby("vlq"))
    out["f5 by vr all"]=summ(grid.groupby("vrq"))
    dd=A.dropna(subset=["nxt"]).copy()
    dd["ex1"]=dd.nxt-dd.groupby("coin")["nxt"].transform("mean")
    s=dd.groupby((dd.wd+1)%7)["ex1"].agg(["mean","std","count"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"]))
    out["next day by weekday of bar(+1)"]=s.drop(columns="std")
    dd["pnl"]=dd.alloc*dd.nxt
    out["pnl by coin"]=dd.groupby("coin").agg(pnl=("pnl","mean"),active=("alloc",lambda x:(x.abs()>0).mean()))
    out["f5 by coin bigup thin"]=summ(grid[(grid.z>1)&(grid.vr<=0.75)].groupby("coin"))
    return out
