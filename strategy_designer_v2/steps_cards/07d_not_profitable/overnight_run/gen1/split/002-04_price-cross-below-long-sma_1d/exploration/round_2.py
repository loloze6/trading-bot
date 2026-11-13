def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            r=b["close"].pct_change()
            a=b["postRebalance_current_allocation"].shift(1)
            raw=b["debug_info.components.below_ma.last_history_value"].shift(1)
            f=b["forecast"].shift(1)
            act=(b["forecast"]<0).astype(int)
            # bars since short began (run length)
            grp=(act!=act.shift()).cumsum()
            run=act.groupby(grp).cumsum().shift(1)
            ret5=(b["close"]/b["close"].shift(5)-1).shift(1)
            vol=r.rolling(20).std().shift(1)
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"a":a,"f":f,"raw":raw,"run":run,"ret5":ret5,"vol":vol,"gross":a*r})
            rows.append(d.iloc[1:])
    D=pd.concat(rows,ignore_index=True)
    A=D[D["a"].abs()>1e-9].copy()
    out={}
    A["rawbin"]=pd.qcut(A["raw"],5)
    out["by_raw_distance_quintile"]=A.groupby("rawbin").agg(n=("r","size"),coin_ret=("r","mean"),gross=("gross","mean"),alloc=("a","mean"),vol=("vol","mean"))
    A["runbin"]=pd.cut(A["run"],[0,5,20,60,150,1e5],labels=["1-5","6-20","21-60","61-150",">150"])
    out["by_bars_since_short_start"]=A.groupby("runbin").agg(n=("r","size"),coin_ret=("r","mean"),gross=("gross","mean"),alloc=("a","mean"))
    A["r5"]=np.where(A["ret5"]<-0.1,"fell>10%",np.where(A["ret5"]<0,"fell0-10%",np.where(A["ret5"]<0.1,"rose0-10%","rose>10%")))
    out["by_prior5d_move"]=A.groupby("r5").agg(n=("r","size"),coin_ret=("r","mean"),gross=("gross","mean"),alloc=("a","mean"))
    # gross pnl contribution share
    A["fb"]=pd.cut(A["f"],[-20.1,-15,-10,-5,-1e-9])
    g=A.groupby("fb")["gross"].sum()
    out["sum_gross_by_forecast"]=g
    out["sum_gross_total_active"]=float(A["gross"].sum())
    # equal-weight short (sign only)
    A["unit"]=-A["r"]
    out["unit_short_by_forecast"]=A.groupby("fb").agg(unit=("unit","mean"),t=("unit",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["unit_short_all"]=pd.Series({"mean":A["unit"].mean(),"t":A["unit"].mean()/A["unit"].std()*np.sqrt(len(A))})
    return out
