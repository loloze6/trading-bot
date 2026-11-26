def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=30).std()
            rng=(b["high"]-b["low"])/c/sd
            loc=(b["high"]-c)/(b["high"]-b["low"]).replace(0,np.nan)
            tr60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"win":w,"ts":b["timestamp"],"r":r,"rz":r/sd,"rng":rng,"loc":loc,
                "rc":(b["regime"]!="chop"),"tr60":tr60,"pos":b["postRebalance_current_allocation"],
                "n1":c.shift(-1)/c-1,"n3":c.shift(-3)/c-1,"i":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    mu1=d.groupby("coin")["n1"].transform("mean")
    d["x1"]=d["n1"]-mu1
    g3=d[d["i"]%3==0]
    mu3=g3.groupby("coin")["n3"].mean()
    d["x3"]=d["n3"]-d["coin"].map(mu3)
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    d["wd"]=pd.to_datetime(d["ts"]).dt.weekday
    def st(s,col):
        s=s.dropna(subset=[col])
        if len(s)<5: return pd.Series({"n":len(s),"mean%":np.nan,"t_day":np.nan})
        dev=s[col]-s[col].mean()
        gs=dev.groupby(s["day"]).sum(); G=len(gs)
        se=np.sqrt((gs**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n":len(s),"days":G,"mean%":100*s[col].mean(),"t_day":s[col].mean()/se})
    d["wide"]=pd.cut(d["rng"],[0,1,1.5,2,3,99],labels=["<1","1-1.5","1.5-2","2-3","3+"])
    d["lowc"]=np.where(d["loc"]>=0.5,"low","high")
    d["trend"]=np.where(d["tr60"]>0.1,"rising",np.where(d["tr60"]<-0.1,"falling",np.where(d["tr60"].notna(),"choppy","na")))
    out={}
    out["rc_x_width_x_close_next1"]=d.groupby(["rc","wide","lowc"],observed=True).apply(lambda s:st(s,"x1")).round(3)
    out["trend_wide2_close_next1"]=d[d.rng>=2].groupby(["trend","lowc"]).apply(lambda s:st(s,"x1")).round(3)
    d["rzb"]=pd.cut(d["rz"],[-99,-2,-1,0,1,2,99])
    out["rc_dayret_z_next1"]=d.groupby(["rc","rzb"],observed=True).apply(lambda s:st(s,"x1")).round(3)
    g=d[d["i"]%3==0]
    out["wide2_close_next3_grid"]=g[g.rng>=2].groupby(["rc","lowc"]).apply(lambda s:st(s,"x3")).round(3)
    out["weekday_next1_all"]=d.groupby("wd").apply(lambda s:st(s,"x1")).round(3)
    out["rc_weekday_next1"]=d[d.rc].groupby("wd").apply(lambda s:st(s,"x1")).round(3)
    return out
