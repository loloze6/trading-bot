import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            mabs=r1.abs().rolling(720,min_periods=240).mean().shift(1)
            z=r1/mabs
            vr=v/v.rolling(720,min_periods=240).mean().shift(1)
            r24p=c/c.shift(24)-1
            sd24=r1.rolling(720,min_periods=240).std().shift(1)*np.sqrt(24)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"tr24":r24p/sd24,
                            "hour":pd.to_datetime(b["timestamp"]).dt.hour,
                            "pos":np.arange(len(b)),
                            "alloc":b["postRebalance_current_allocation"]})
            for h in [2,6,12,24]:
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # drift per coin, 6h grid
    g6=D[D.pos%6==0]
    drift={h:D[D.pos%h==0].groupby("coin")[f"f{h}"].mean() for h in [2,6,12,24]}
    for h in [2,6,12,24]:
        D[f"u{h}"]=D[f"f{h}"]-D.coin.map(drift[h])
    S=D[(D.pos%6==0)].dropna(subset=["z","vr","u6"]).copy()
    S["zb"]=pd.cut(S.z,[-99,-4,-3,-2,-1.5,-1,0,1,1.5,2,3,4,99])
    S["vb"]=pd.cut(S.vr,[0,0.667,1.5,3,99])
    def agg(x,col):
        return pd.Series({"n":len(x),"mean%":x[col].mean()*100,"t":x[col].mean()/(x[col].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["u6 by zbin x volbin (mean%)"]=S.groupby(["zb","vb"],observed=True)["u6"].mean().unstack()*100
    out["n by zbin x volbin"]=S.groupby(["zb","vb"],observed=True)["u6"].size().unstack()
    out["t by zbin x volbin"]=S.groupby(["zb","vb"],observed=True)["u6"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan).unstack()
    # falls z<-2 with normal vol: horizons
    F=D[(D.z<-2)&(D.vr.between(0.667,1.5))]
    hz={}
    for h in [2,6,12,24]:
        x=F[F.pos%h==0][f"u{h}"].dropna()
        x2=F[f"u{h}"].dropna()
        hz[h]={"n_grid":len(x),"mean%_grid":x.mean()*100,"n_all":len(x2),"mean%_all":x2.mean()*100}
    out["fall z<-2 normal vol, by horizon"]=pd.DataFrame(hz).T
    # by prior 24h trend for z<-2 normal vol (all bars, 6h)
    F=F.copy(); F["tb"]=pd.qcut(F.tr24,4)
    out["fall z<-2 nv by prior 24h trend"]=F.groupby("tb",observed=True)["u6"].agg(["size","mean"])
    # strategy allocation activity
    act=D[D.alloc.abs()>0]
    out["share bars in position"]=len(act)/len(D)
    out["mean |alloc| when in"]=act.alloc.abs().mean()
    return out
