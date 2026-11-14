def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            raw=b["debug_info.components.sma_cross.last_history_value"].values
            n=len(b)
            # bars since forecast became >0
            since=np.full(n,np.nan); cnt=np.nan
            for i in range(n):
                if f[i]>0:
                    cnt = (cnt+1) if (i>0 and f[i-1]>0 and not np.isnan(cnt)) else (0 if i>0 and f[i-1]<=0 else np.nan)
                else: cnt=np.nan
                since[i]=cnt
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-10,10):
                r=c[i+10]/c[i]-1
                past=c[i]/c[i-10]-1 if i>=10 else np.nan
                vol=np.std(np.diff(np.log(c[max(0,i-20):i+1]))) if i>=5 else np.nan
                draw=raw[i]-raw[i-10] if i>=10 else np.nan
                rows.append(dict(coin=coin,w=w,year=ts[i].year,f=f[i],raw=raw[i],r=r,past=past,vol=vol,dspread=draw,since=since[i]))
    d=pd.DataFrame(rows)
    d["ex"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    out={}
    out["n"]=pd.Series({"blocks":len(d),"pos":(d.f>0).sum()})
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex":g.ex.mean(),"sd":g.ex.std(),"t":g.ex.mean()/g.ex.std()*np.sqrt(len(g)) if len(g)>2 else np.nan,"hit":(g.r>0).mean()})
    d["fb"]=pd.cut(d.f,[-0.1,0,5,10,15,20.1],labels=["0","0-5","5-10","10-15","15-20"])
    out["by_fbucket"]=d.groupby("fb").apply(summ)
    p=d[d.f>0]
    out["pos_by_coin"]=p.groupby("coin").apply(summ)
    out["zero_by_coin"]=d[d.f==0].groupby("coin").apply(summ)
    out["pos_by_year"]=p.groupby("year").apply(summ)
    p=p.copy()
    p["fresh"]=pd.cut(p.since,[-1,20,60,150,10000],labels=["<=20","21-60","61-150",">150"])
    out["pos_by_freshness"]=p.groupby("fresh").apply(summ)
    p["dsp"]=np.where(p.dspread>0,"spread_rising","spread_falling")
    out["pos_by_spreadchange"]=p.groupby("dsp").apply(summ)
    p["pastq"]=pd.qcut(p.past,4,labels=False)
    out["pos_by_past10"]=p.groupby("pastq").apply(summ)
    p["volq"]=pd.qcut(p.vol,3,labels=False)
    out["pos_by_vol"]=p.groupby("volq").apply(summ)
    out["sd_ratio"]=pd.Series({"sd_ex_all":d.ex.std(),"slope_t":stats.linregress(d.f,d.ex).rvalue*np.sqrt(len(d)-2)/np.sqrt(1-stats.linregress(d.f,d.ex).rvalue**2)})
    return out
