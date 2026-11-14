def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"])
            cl=b["close"].astype(float)
            b["r1"]=cl.pct_change()
            b["f1"]=cl.shift(-1)/cl-1
            b["f10"]=cl.shift(-10)/cl-1
            b["p10"]=cl/cl.shift(10)-1
            b["vol20"]=b["r1"].rolling(20).std()
            b["dist"]=b["debug_info.components.below_ma.last_history_value"].astype(float)
            b["coin"]=c; b["win"]=w
            b["alloc"]=b["postRebalance_current_allocation"].astype(float)
            b["bv"]=b["postRebalance_total_value"].astype(float)
            b["br"]=b["bv"].pct_change()
            rows.append(b[["coin","win","ts","r1","f1","f10","p10","vol20","dist","forecast","alloc","br"]])
    d=pd.concat(rows,ignore_index=True)
    out={}
    def agg(g,col):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"up_share":(x>0).mean()})
    d["fb"]=pd.cut(d["forecast"],[-20.01,-15,-10,-5,-2,-1e-9,0.01],labels=["<=-15","-15..-10","-10..-5","-5..-2","-2..0","0"])
    out["f10_by_forecast_bucket"]=d.groupby("fb").apply(lambda g:agg(g,"f10"))
    out["f1_by_forecast_bucket"]=d.groupby("fb").apply(lambda g:agg(g,"f1"))
    d["db"]=pd.qcut(d["dist"],10,duplicates="drop")
    out["f10_by_raw_dist_decile"]=d.groupby("db").apply(lambda g:agg(g,"f10"))
    # forecast vs raw distance mismatch
    out["share_below_but_forecast0"]=float(((d["dist"]<0)&(d["forecast"]==0)).mean())
    out["share_above_but_forecast_neg"]=float(((d["dist"]>0)&(d["forecast"]<0)).mean())
    out["alloc_vs_forecast_corr"]=float(d[["alloc","forecast"]].corr().iloc[0,1])
    # past 10d return
    d["pb"]=pd.qcut(d["p10"],5)
    out["f10_by_past10_quintile"]=d.groupby("pb").apply(lambda g:agg(g,"f10"))
    # large daily moves
    d["z"]=d["r1"]/d["vol20"]
    d["zb"]=pd.cut(d["z"],[-99,-2.5,-1.5,1.5,2.5,99])
    out["f1_by_zmove"]=d.groupby("zb").apply(lambda g:agg(g,"f1"))
    out["f10_by_zmove"]=d.groupby("zb").apply(lambda g:agg(g,"f10"))
    d["vb"]=d.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x,3,labels=["lo","mid","hi"]))
    out["f1_by_vol_tercile"]=d.groupby("vb").apply(lambda g:agg(g,"f1"))
    out["book_by_vol_tercile"]=d.groupby("vb").apply(lambda g:agg(g,"br"))
    d["wd"]=d["ts"].dt.dayofweek
    out["f1_by_weekday"]=d.groupby("wd").apply(lambda g:agg(g,"f1"))
    out["book_by_coin"]=d.groupby("coin").apply(lambda g:agg(g,"br"))
    out["book_by_year"]=d.groupby(d["ts"].dt.year).apply(lambda g:agg(g,"br"))
    out["f1_by_year_short_vs_flat"]=d.assign(sh=d["alloc"]<0).groupby([d["ts"].dt.year,"sh"]).apply(lambda g:agg(g,"f1"))
    tr=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=c; tr.append(t)
    t=pd.concat(tr,ignore_index=True)
    t["days"]=t["duration_minutes"]/1440
    t["db"]=pd.cut(t["days"],[0,1.5,3,7,20,1e5])
    out["trades_by_duration"]=t.groupby(["side","db"]).agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),comm=("total_commission","mean"))
    return out
