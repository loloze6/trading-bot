def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; posrows=[]; dayrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].values; v=b["volume"].values
            n=len(b)
            wd=ts.dt.weekday.values; hr=ts.dt.hour.values
            alloc=b["postRebalance_current_allocation"].values
            ret1=np.r_[c[1:]/c[:-1]-1,np.nan]
            posrows.append(pd.DataFrame({"wd":wd,"absalloc":np.abs(alloc),"gain":alloc*ret1}))
            idx=np.where((wd==6)&(hr==23))[0]
            for t in idx:
                if t-168<0 or t+48>=n: continue
                rwe=c[t]/c[t-48]-1
                rwk=c[t-48]/c[t-168]-1 if t-168>=0 else np.nan
                vwe=v[t-47:t+1].mean(); vwd=v[t-167:t-47].mean()
                f48=c[t+48]/c[t]-1
                f24=c[t+24]/c[t]-1
                rows.append(dict(coin=coin,w=w,year=ts[t].year,rwe=rwe,rwk=rwk,ratio=vwd/vwe if vwe>0 else np.nan,
                                 f48=f48,f24=f24,fc=b["forecast"].values[t],alloc=alloc[t]))
            # weekday-control: Thursday 23:00 48h move then next 48h
            idx2=np.where((wd==3)&(hr==23))[0]
            for t in idx2:
                if t-48<0 or t+48>=n: continue
                dayrows.append(dict(coin=coin,rwe=c[t]/c[t-48]-1,f48=c[t+48]/c[t]-1))
    d=pd.DataFrame(rows)
    sd=d.groupby("coin")["f48"].transform("std")
    d["z"]=d["rwe"]/d.groupby("coin")["rwe"].transform("std")
    d["fz"]=(d["f48"]-d.groupby("coin")["f48"].transform("mean"))/sd
    out={}
    out["n"]=len(d)
    def slope(x,y):
        m=np.isfinite(x)&np.isfinite(y); r=stats.linregress(x[m],y[m]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":m.sum()})
    out["fz_on_weekendz_all"]=slope(d["z"].values,d["fz"].values)
    d["rq"]=pd.qcut(d["ratio"],3,labels=["thickwe","mid","thinwe"])
    out["slope_by_ratio_tercile"]=d.groupby("rq").apply(lambda g:slope(g["z"].values,g["fz"].values))
    d["zq"]=pd.qcut(d["z"],5,labels=False)
    out["fwd_by_weekend_move_quintile"]=d.groupby("zq").agg(z=("z","mean"),f48=("f48","mean"),f24=("f24","mean"),n=("f48","size"))
    out["slope_by_coin"]=d.groupby("coin").apply(lambda g:slope(g["z"].values,g["fz"].values))
    out["slope_by_year"]=d.groupby("year").apply(lambda g:slope(g["z"].values,g["fz"].values))
    d["prior_z"]=d["rwk"]/d.groupby("coin")["rwk"].transform("std")
    out["fz_on_weekdayprior_z"]=slope(d["prior_z"].values,d["fz"].values)
    e=pd.DataFrame(dayrows)
    e["z"]=e["rwe"]/e.groupby("coin")["rwe"].transform("std")
    e["fz"]=(e["f48"]-e.groupby("coin")["f48"].transform("mean"))/e.groupby("coin")["f48"].transform("std")
    out["control_thu_move_next48"]=slope(e["z"].values,e["fz"].values)
    d["sig"]=np.sign(d["fc"])
    out["signal_vs_alloc_sign_agree"]=float((np.sign(d["alloc"])==d["sig"]).mean())
    p=pd.concat(posrows)
    out["book_by_weekday"]=p.groupby("wd").agg(absalloc=("absalloc","mean"),gain_bp=("gain",lambda x:x.mean()*1e4))
    return out
