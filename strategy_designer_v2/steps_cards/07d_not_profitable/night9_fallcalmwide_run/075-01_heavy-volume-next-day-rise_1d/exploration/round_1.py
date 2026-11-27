import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "f":b["forecast"].astype(float),"vr":vr,
                "dayret":c/c.shift(1)-1,"ret5":c/c.shift(5)-1,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "chg":(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs().astype(float)})
            for h in (1,2,3,5,10):
                d[f"r{h}"]=c.shift(-h)/c-1
            d["tr20"]=c/c.shift(20)-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # drift per coin per h
    for h in (1,2,3,5,10):
        g=D[D.pos%h==0]
        dr=g.groupby("coin")[f"r{h}"].mean()
        D[f"x{h}"]=D[f"r{h}"]-D.coin.map(dr)
    D["q"]=pd.qcut(D.f.rank(method="first"),5,labels=False)
    D["up"]=np.where(D.dayret>0,"up","down")
    # 1) quintile x direction, next-day excess, all bars
    t=D.groupby(["q","up"]).agg(n=("x1","count"),mx1=("x1","mean"),mdayret=("dayret","mean"))
    out["q_by_dir_next1"]=t
    # 2) horizons, non-overlapping grid, by quintile and dir
    res=[]
    for h in (1,2,3,5,10):
        g=D[(D.pos%h==0)&D[f"x{h}"].notna()]
        for (q,u),s in g.groupby(["q","up"]):
            x=s[f"x{h}"]
            res.append({"h":h,"q":q,"dir":u,"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["horizons"]=pd.DataFrame(res).pivot_table(index=["q","dir"],columns="h",values=["mean","t"])
    # 3) book gain by side, gross and cost
    D["gain"]=D.alloc*D.r1
    D["cost"]=D.chg*0.0011
    D["side"]=np.sign(D.alloc)
    out["by_side"]=D.groupby("side").agg(n=("gain","count"),gross=("gain","mean"),cost=("cost","mean"),absalloc=("alloc",lambda a:a.abs().mean()))
    out["total_gross_cost"]=pd.Series({"gross_per_coinbar":D.gain.mean(),"cost_per_coinbar":D.cost.mean(),"turnover":D.chg.mean()})
    # 4) heavy volume down days by size of day's fall and trend
    hv=D[D.q==4]
    hv["fallq"]=pd.qcut(hv.dayret,4,labels=False)
    out["top_q_by_dayret_quart"]=hv.groupby("fallq").agg(n=("x1","count"),dr=("dayret","mean"),x1=("x1","mean"),x3=("x3","mean"))
    # condition alone: big down days without heavy volume
    D["dq"]=pd.qcut(D.dayret.rank(method="first"),5,labels=False)
    out["dayret_quint_by_heavy"]=D.groupby(["dq",D.q==4]).agg(n=("x1","count"),x1=("x1","mean"),x3=("x3","mean"))
    # by window
    out["by_window_top_minus_bottom"]=D.groupby("w").apply(lambda s:s[s.q==4].x1.mean()-s[s.q==0].x1.mean())
    return out
