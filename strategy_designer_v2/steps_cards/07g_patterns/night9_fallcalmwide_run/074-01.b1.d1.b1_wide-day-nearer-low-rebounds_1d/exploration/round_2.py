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
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"n3":c.shift(-3)/c-1,"i":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in [1,2,3]:
        g=d[d["i"]%h==0]
        mu=g.groupby("coin")["n%d"%h].mean()
        d["x%d"%h]=d["n%d"%h]-d["coin"].map(mu)
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    d["yr"]=pd.to_datetime(d["ts"]).dt.year
    def st(s,col):
        s=s.dropna(subset=[col])
        if len(s)<5: return pd.Series({"n":len(s),"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        dev=s[col]-s[col].mean()
        gs=dev.groupby(s["day"]).sum(); G=len(gs)
        se=np.sqrt((gs**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n":len(s),"days":G,"mean%":100*s[col].mean(),"t_day":s[col].mean()/se})
    def slope(s,x,y):
        s=s.dropna(subset=[x,y])
        if len(s)<10: return pd.Series({"n":len(s),"slope":np.nan,"t":np.nan})
        X=s[x]-s[x].mean(); b=(X*s[y]).sum()/(X**2).sum()
        e=s[y]-s[y].mean()-b*X
        gs=(X*e).groupby(s["day"]).sum(); G=len(gs)
        se=np.sqrt((gs**2).sum()*G/(G-1))/(X**2).sum()
        return pd.Series({"n":len(s),"slope%":100*b,"t":b/se})
    out={}
    rc=d[d.rc]
    # down day rebound in rc, outside wide days
    rc2=rc.copy(); rc2["dn"]=rc2["rz"]<0
    out["rc_down_by_wide"]=rc2[rc2.dn].groupby(rc2["rng"]>=2).apply(lambda s:st(s,"x1")).round(3)
    out["rc_down_graded_slope_x1_on_rz"]=pd.DataFrame({"down":slope(rc2[rc2.dn],"rz","x1"),"all":slope(rc,"rz","x1")}).round(3)
    out["rc_down_by_window"]=rc2[rc2.dn].groupby("win").apply(lambda s:st(s,"x1")).round(3)
    out["rc_down_by_year"]=rc2[rc2.dn].groupby("yr").apply(lambda s:st(s,"x1")).round(3)
    # horizons in rc wide low close
    wl=rc[(rc.rng>=2)&(rc["loc"]>=0.5)]
    hz={}
    for h in [1,2,3]:
        g=wl[wl["i"]%h==0]; hz["h%d"%h]=st(g,"x%d"%h)
    out["rc_widelow_horizons_grid"]=pd.DataFrame(hz).round(3)
    g3=rc[(rc["i"]%3==0)&(rc.rng>=1.5)]
    out["rc_wide1.5_slopes_x3"]=pd.DataFrame({"loc":slope(g3,"loc","x3"),"rng":slope(g3,"rng","x3")}).round(3)
    g3w=wl[wl["i"]%3==0]
    out["rc_widelow_x3_by_window"]=g3w.groupby("win").apply(lambda s:st(s,"x3")).round(3)
    # outside rc: wide high close fade by trend
    o=d[(~d.rc)&(d.rng>=2)].copy()
    o["trend"]=np.where(o["tr60"]>0.1,"rising",np.where(o["tr60"]<-0.1,"falling",np.where(o["tr60"].notna(),"choppy","na")))
    o["close_in_upper"]=o["loc"]<0.5
    out["nonrc_wide2_by_trend_close"]=o.groupby(["trend","close_in_upper"]).apply(lambda s:st(s,"x1")).round(3)
    out["nonrc_wide2_slope_x1_on_loc"]=slope(o,"loc","x1").round(3)
    # book largest days
    bd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; bd.append(t)
    bd=pd.concat(bd)
    m=bd.groupby("day")["book_return"].mean().dropna()
    q=m.sort_values()
    out["book_tails"]=pd.Series({"days":len(m),"top10_sum%":100*q.tail(10).sum(),"bottom10_sum%":100*q.head(10).sum(),"total_sum%":100*m.sum()}).round(3)
    return out
