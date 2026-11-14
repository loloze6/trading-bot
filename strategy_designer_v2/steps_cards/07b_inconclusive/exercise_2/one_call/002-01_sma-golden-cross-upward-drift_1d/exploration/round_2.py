def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            raw=b["debug_info.components.sma_cross.last_history_value"].values
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(0,n-10,10):
                r=c[i+10]/c[i]-1
                past=c[i]/c[i-10]-1 if i>=10 else np.nan
                past20=c[i]/c[i-20]-1 if i>=20 else np.nan
                hi20=c[i]>=np.max(c[i-19:i+1]) if i>=19 else np.nan
                rows.append(dict(coin=coin,w=w,i=i,year=ts[i].year,f=f[i],raw=raw[i],r=r,past=past,past20=past20,hi20=hi20))
    d=pd.DataFrame(rows)
    d["ex"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    # market-relative: subtract mean return of all coins on same window/block
    d["mkt"]=d.groupby(["w","i"])["r"].transform("mean")
    d["rel"]=d["r"]-d["mkt"]
    def summ(g,col="ex"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,"hit":(g.r>0).mean()})
    out={}
    pq=d.past.quantile([.25,.5,.75]).values
    d["pastq"]=pd.cut(d.past,[-9,pq[0],pq[1],pq[2],9],labels=["q1","q2","q3","q4"])
    d["state"]=np.where(d.f>0,"up","flat")
    out["past10_x_state_ex"]=d.groupby(["state","pastq"]).apply(summ)
    out["past10_x_state_rel"]=d.groupby(["state","pastq"]).apply(lambda g:summ(g,"rel"))
    d["p20pos"]=np.where(d.past20>0,"p20_up","p20_down")
    out["past20_x_state"]=d[d.past20.notna()].groupby(["state","p20pos"]).apply(summ)
    out["hi20_x_state"]=d[d.hi20.notna()].groupby(["state","hi20"]).apply(summ)
    p=d[(d.f>0)&(d.past.notna())]
    s=stats.linregress(p.past,p.ex); out["up_slope_ex_on_past10"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(p)})
    s=stats.linregress(p.past,p.rel); out["up_slope_rel_on_past10"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr})
    z=d[(d.f==0)&(d.past.notna())]
    s=stats.linregress(z.past,z.ex); out["flat_slope_ex_on_past10"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(z)})
    s=stats.linregress(d.f,d.rel); out["f_slope_rel"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr})
    top=p[p.pastq=="q4"]
    out["up_q4_by_coin"]=top.groupby("coin").apply(summ)
    out["up_q4_by_year"]=top.groupby("year").apply(summ)
    out["share_var_market"]=pd.Series({"var_r":d.r.var(),"var_mkt":d.mkt.var(),"corr_r_mkt":d[["r","mkt"]].corr().iloc[0,1]})
    return out
