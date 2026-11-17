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
            ts=pd.to_datetime(d["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"wn":int(w[1:]),"pos":np.arange(len(d)),"z":r1/vol20,"vr":vr,
                "f5":c.shift(-5)/c-1,"f2":c.shift(-2)/c-1,"yr":ts.dt.year,
                "z3":(c/c.shift(3)-1)/(vol20*np.sqrt(3))}))
    A=pd.concat(rows)
    out={}
    def summ(g,col="ex"):
        s=g[col].agg(["mean","std","count"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"])); return s.drop(columns="std")
    grid=A[(A.pos%5==0)&A.f5.notna()&A.z.notna()].copy()
    grid["ex"]=grid.f5-grid.groupby("coin")["f5"].transform("mean")
    up=grid[grid.z>1]
    out["bigup by coin"]=summ(up.groupby("coin"))
    up=up.assign(half=np.where(up.wn<=12,"w1-12","w13-24"))
    out["bigup by half"]=summ(up.groupby("half"))
    out["bigup by year"]=summ(up.groupby("yr"))
    pz=grid[grid.z>0]
    r,p=stats.spearmanr(pz.z,pz.ex); out["spearman z vs ex5 on up days"]=f"rho={r:.3f} p={p:.4f} n={len(pz)}"
    r,p=stats.spearmanr(grid.z,grid.ex); out["spearman z vs ex5 all"]=f"rho={r:.3f} p={p:.4f} n={len(grid)}"
    r,p=stats.spearmanr(grid.vr.dropna(),grid.loc[grid.vr.notna(),"ex"]); out["spearman vr vs ex5 all"]=f"rho={r:.3f} p={p:.4f}"
    # 3-day scaled move continuation
    grid["z3q"]=pd.qcut(grid.z3,5)
    out["ex5 by 3d scaled move"]=summ(grid.groupby("z3q"))
    # bigup: high vs low vr within up days
    up2=grid[grid.z>1].copy(); up2["thin"]=np.where(up2.vr<=1,"vr<=1","vr>1")
    out["bigup thin vs heavy"]=summ(up2.groupby("thin"))
    # 2-day grid
    g2=A[(A.pos%2==0)&A.f2.notna()&A.z.notna()].copy(); g2["ex"]=g2.f2-g2.groupby("coin")["f2"].transform("mean")
    g2["zq"]=pd.cut(g2.z,[-99,-2,-1,1,2,99]); out["ex2 by z"]=summ(g2.groupby("zq"))
    # book extremes
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            D.append(df.assign(coin=coin))
    D=pd.concat(D).dropna(subset=["book_return"])
    q=D.book_return.quantile([0.01,0.99])
    out["book tail share"]=pd.Series({"top1%sum":D.book_return[D.book_return>=q[0.99]].sum(),"bot1%sum":D.book_return[D.book_return<=q[0.01]].sum(),"total":D.book_return.sum()})
    return out
