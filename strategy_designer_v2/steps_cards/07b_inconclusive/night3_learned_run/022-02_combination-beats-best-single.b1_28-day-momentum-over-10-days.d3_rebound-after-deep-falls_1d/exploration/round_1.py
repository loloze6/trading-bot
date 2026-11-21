import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(b)
            f=b["forecast"].fillna(0).values
            f1=b.get("debug_info.components.fall28.post_pipeline_value",pd.Series(np.nan,index=b.index)).values
            f2=b.get("debug_info.components.near_low60.post_pipeline_value",pd.Series(np.nan,index=b.index)).values
            r28=b.get("debug_info.components.fall28.last_history_value",pd.Series(np.nan,index=b.index)).values
            cs=pd.Series(c)
            tr90=(cs/cs.shift(90)-1).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0,n,10):
                rec={"coin":coin,"w":w,"yr":yr[i],"f":f[i],"f1":f1[i],"f2":f2[i],"r28":r28[i],"tr90":tr90[i]}
                for h in (5,10,20):
                    rec[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    for h in (5,10,20):
        d[f"u{h}"]=d[f"r{h}"]-d.groupby("coin")[f"r{h}"].transform("mean")
    def slope(g,y="u10",x="f"):
        g=g[[x,y]].dropna()
        if len(g)<10 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["all_by_h"]=pd.DataFrame({h:slope(d,f"u{h}") for h in (5,10,20)}).T
    out["by_coin"]=d.groupby("coin").apply(slope)
    out["by_year"]=d.groupby("yr").apply(slope)
    pos=d[d.f>0].copy()
    pos["q"]=pd.qcut(pos.f.rank(method="first"),4,labels=False)
    out["pos_quartile"]=pos.groupby("q").agg(n=("u10","count"),f=("f","mean"),u10=("u10","mean"),u20=("u20","mean"),r10=("r10","mean"))
    out["zero_vs_pos"]=d.assign(p=d.f>0).groupby("p").agg(n=("u10","count"),u10=("u10","mean"),u20=("u20","mean"))
    d["trend"]=np.where(d.tr90.isna(),"na",np.where(d.tr90>0,"up90","down90"))
    out["by_trend"]=d.groupby("trend").apply(slope)
    out["trend_pos_mean"]=pos.assign(trend=np.where(pos.tr90.isna(),"na",np.where(pos.tr90>0,"up90","down90"))).groupby("trend").agg(n=("u10","count"),u10=("u10","mean"),u20=("u20","mean"))
    out["comp_fall28"]=slope(d,x="f1"); out["comp_low60"]=slope(d,x="f2")
    out["raw_r28_slope"]=slope(d,x="r28")
    return out
