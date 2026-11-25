def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change()
            sd30=r1.rolling(30).std()
            ret5=c/c.shift(5)-1
            ret1=r1
            ret60=c/c.shift(60)-1
            hi=b["high"].astype(float); lo=b["low"].astype(float); op=b["open"].astype(float)
            rng=(hi-lo)/c
            clpos=(c-lo)/(hi-lo).replace(0,np.nan)
            for h in (1,3,5):
                pass
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),
                "s5":ret5/sd30,"s1":ret1/sd30,"sd30":sd30,"ret60":ret60,
                "choppy":(b["regime"]=="unknown").astype(int),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "clpos":clpos,"rng_s":rng/sd30,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (1,3,5):
        m=D[D.pos%h==0].groupby("coin")["f%d"%h].mean()
        D["x%d"%h]=D["f%d"%h]-D.coin.map(m)
    def tab(g,h,key):
        sub=D[(D.pos%h==0)].dropna(subset=["x%d"%h])
        out=[]
        for k,s in sub.groupby(key):
            x=s["x%d"%h]
            dd=s.assign(dev=x-x.mean()).groupby("day")["dev"].sum()
            se=np.sqrt((dd**2).sum())/len(s)
            out.append(pd.Series({"n":len(s),"days":len(dd),"mean%":100*x.mean(),"t_day":x.mean()/se if se>0 else np.nan},name=k))
        return pd.DataFrame(out)
    D["s5q"]=D.groupby("coin")["s5"].transform(lambda v: pd.qcut(v,5,labels=False,duplicates="drop"))
    D["s1q"]=D.groupby("coin")["s1"].transform(lambda v: pd.qcut(v,5,labels=False,duplicates="drop"))
    D["volq"]=D.groupby("coin")["sd30"].transform(lambda v: pd.qcut(v,3,labels=False,duplicates="drop"))
    D["clq"]=pd.qcut(D["clpos"],5,labels=False,duplicates="drop")
    D["trend"]=np.where(D.ret60>0.1,"rise",np.where(D.ret60<-0.1,"fall",np.where(D.ret60.notna(),"chop","na")))
    res={}
    res["f3 by s5 quintile x choppy"]=tab(D,3,["choppy","s5q"])
    res["f3 by s5 quintile x trend"]=tab(D,3,["trend","s5q"])
    res["f1 by s1 quintile x choppy"]=tab(D,1,["choppy","s1q"])
    res["f3 by s1 quintile"]=tab(D,3,["s1q"])
    res["f1 by weekday"]=tab(D,1,["wd"])
    res["f3 by vol tercile"]=tab(D,3,["volq"])
    res["f1 by close position quintile"]=tab(D,1,["clq"])
    res["f3 by close position quintile x choppy"]=tab(D,3,["choppy","clq"])
    res["f5 by s5 quintile"]=tab(D,5,["s5q"])
    return res
