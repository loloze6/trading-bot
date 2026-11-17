import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float); v=d["volume"].astype(float)
            r1=c.pct_change(); vol20=r1.rolling(20,min_periods=10).std()
            vr=v/v.rolling(30,min_periods=15).mean()
            rows.append(pd.DataFrame({"coin":coin,"wn":int(w[1:]),"pos":np.arange(len(d)),"z":r1/vol20,"vr":vr,
                "f5":c.shift(-5)/c-1}))
    A=pd.concat(rows)
    grid=A[(A.pos%5==0)&A.f5.notna()&A.z.notna()&A.vr.notna()].copy()
    grid["ex"]=grid.f5-grid.groupby("coin")["f5"].transform("mean")
    grid["half"]=np.where(grid.wn<=12,"w1-12","w13-24")
    def summ(g):
        s=g["ex"].agg(["mean","std","count"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"])); return s.drop(columns="std")
    out={}
    grid["lvr"]=np.log(grid.vr)
    res={}
    for k,g in grid.groupby("coin"):
        r,p=stats.spearmanr(g.lvr,g.ex); res[k]=(r,p,len(g))
    for k,g in grid.groupby("half"):
        r,p=stats.spearmanr(g.lvr,g.ex); res[k]=(r,p,len(g))
    out["spearman vr vs ex5 by coin/half"]=pd.DataFrame(res,index=["rho","p","n"]).T
    up=grid[grid.z>0].copy()
    up["sig"]=up.z*up.lvr
    res={}
    for k,g in [("all",up)]+list(up.groupby("half")):
        r,p=stats.spearmanr(g.z,g.ex); r2,p2=stats.spearmanr(g.z*g.vr,g.ex); res[k]=(r,p,r2,p2,len(g))
    out["up days: rho z / rho z*vr vs ex5"]=pd.DataFrame(res,index=["rho_z","p_z","rho_zvr","p_zvr","n"]).T
    up["zvq"]=pd.qcut(up.z*up.vr,5)
    out["up days ex5 by z*vr quintile"]=summ(up.groupby("zvq"))
    dn=grid[grid.z<0].copy(); dn["zvq"]=pd.qcut(dn.z*dn.vr,5)
    out["down days ex5 by z*vr quintile"]=summ(dn.groupby("zvq"))
    grid["vq"]=pd.qcut(grid.vr,5)
    out["ex5 by vr quintile x half"]=summ(grid.groupby(["half","vq"]))
    return out
