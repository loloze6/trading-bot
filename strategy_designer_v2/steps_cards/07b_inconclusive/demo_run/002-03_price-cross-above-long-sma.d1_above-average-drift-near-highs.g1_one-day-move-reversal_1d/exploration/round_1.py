import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            d["nxt"]=d["close"].shift(-1)/d["close"]-1
            d["ret1"]=d["close"].pct_change()
            d["coin"]=coin; d["win"]=w; d["year"]=pd.to_datetime(d["timestamp"]).dt.year
            d["raw"]=d["debug_info.components.vsr.last_history_value"]
            d["pos"]=d["postRebalance_current_allocation"]
            rows.append(d[["coin","win","year","forecast","raw","nxt","ret1","pos"]])
    a=pd.concat(rows,ignore_index=True)
    a=a.dropna(subset=["nxt","forecast"])
    a["ex"]=a["nxt"]-a.groupby("coin")["nxt"].transform("mean")
    def slope(g):
        if len(g)<30: return pd.Series({"n":len(g)})
        r=stats.linregress(g["forecast"],g["ex"])
        return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["by_coin"]=a.groupby("coin").apply(slope)
    out["by_year"]=a.groupby("year").apply(slope)
    a["side"]=np.where(a["forecast"]>0,"long(after fall)","short(after rise)")
    out["by_side"]=a.groupby("side").apply(slope)
    a["q"]=pd.qcut(a["forecast"],10,labels=False,duplicates="drop")
    out["deciles"]=a.groupby("q").agg(n=("ex","size"),fc=("forecast","mean"),ex_mean=("ex","mean"),
        t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))),pos=("pos","mean"))
    # position gain decomposition
    a["gain"]=a["pos"]*a["nxt"]
    mu=a.groupby("coin")["nxt"].transform("mean")
    a["mkt"]=a["pos"]*mu
    a["timing"]=a["gain"]-a["mkt"]
    out["timing_by_coin"]=a.groupby("coin")[["gain","mkt","timing"]].mean()
    out["timing_by_side"]=a.groupby("side")[["gain","mkt","timing"]].mean()
    out["timing_by_decile"]=a.groupby("q")[["timing","pos"]].mean()
    out["corr_pos_forecast"]=float(a[["pos","forecast"]].corr().iloc[0,1])
    # raw-z based slope (unstandardised)
    b=a.dropna(subset=["raw"])
    r=stats.linregress(-b["raw"],b["ex"]); out["slope_negraw_t"]=float(r.slope/r.stderr)
    return out
