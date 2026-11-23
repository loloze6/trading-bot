def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        # drift per coin: 3-bar grid returns over all windows
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            g+=list(c[3::3][:len(c[0::3])-1]/c[0::3][:len(c[3::3])]-1) if len(c)>3 else []
        drift=np.nanmean(g) if g else 0.0
        sd3=np.nanstd(g) if g else np.nan
        for w,b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r=b["close"].pct_change()
            mabs=r.abs().rolling(60,min_periods=20).mean()
            vrel=b["volume"]/b["volume"].rolling(60,min_periods=20).mean()
            r2=b["close"]/b["close"].shift(2)-1
            r20=b["close"]/b["close"].shift(20)-1
            f3=b["close"].shift(-3)/b["close"]-1
            f1=b["close"].shift(-1)/b["close"]-1
            df=pd.DataFrame({"coin":coin,"win":w,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
              "z":(r/mabs).values,"z2":(r2/mabs).values,"vrel":vrel.values,"r20":r20.values,
              "ex3":(f3-drift).values,"f1":f1.values,"u3":((f3-drift)/sd3).values})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","ex3"])
    def summ(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    bins=[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf]
    d["zb"]=pd.cut(d["z"],bins)
    out={}
    out["ex3 by weekday x zbin (mean)"]=d.pivot_table(index="zb",columns="wd",values="ex3",aggfunc="mean",observed=True).round(4)
    out["ex3 by weekday x zbin (n)"]=d.pivot_table(index="zb",columns="wd",values="ex3",aggfunc="count",observed=True)
    sl=[]
    for wd,gg in d.groupby("wd"):
        res=stats.linregress(gg["z"],gg["ex3"])
        fall=gg[gg.z<-1]["ex3"]; rise=gg[gg.z>1]["ex3"]
        sl.append({"wd":wd,"slope":res.slope,"t_slope":res.slope/res.stderr,"n":len(gg),
                   "fall>1u":fall.mean(),"t_fall":summ(fall)["t"],"rise>1u":rise.mean(),"t_rise":summ(rise)["t"]})
    out["slope ex3 on z by weekday"]=pd.DataFrame(sl).round(4)
    sun=d[(d.wd==6)&(d.z<-0.3)].copy()
    sun["vb"]=pd.qcut(sun["vrel"],3,labels=["lowvol","mid","highvol"])
    out["sunday falls by rel volume"]=sun.groupby("vb",observed=True)["ex3"].apply(summ).unstack().round(4)
    sun["tb"]=pd.qcut(sun["r20"],3,labels=["down20","mid","up20"])
    out["sunday falls by 20d trend"]=sun.groupby("tb",observed=True)["ex3"].apply(summ).unstack().round(4)
    out["sunday falls by year"]=sun.groupby("year")["ex3"].apply(summ).unstack().round(4)
    sun2=d[(d.wd==6)].copy(); sun2["z2b"]=pd.cut(sun2["z2"],bins)
    out["sunday: ex3 by sat+sun 2d z"]=sun2.groupby("z2b",observed=True)["ex3"].apply(summ).unstack().round(4)
    # all-weekday falls by trend
    allf=d[d.z<-1].copy(); allf["tb"]=pd.qcut(allf["r20"],3,labels=["down20","mid","up20"])
    out["all-day falls>1u: ex3 by trend x sunday"]=allf.groupby([allf.wd==6,"tb"],observed=True)["ex3"].apply(summ).unstack().round(4)
    # book
    br=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; x["coin"]=coin; br.append(x)
    br=pd.concat(br).dropna(subset=["book_return"])
    out["book ret by weekday"]=br.groupby("wd")["book_return"].apply(summ).unstack()
    return out
