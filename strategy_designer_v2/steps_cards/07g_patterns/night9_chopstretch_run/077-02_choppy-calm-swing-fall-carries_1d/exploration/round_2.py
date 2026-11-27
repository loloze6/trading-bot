def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            sdy=r.rolling(30).std().rolling(365,min_periods=120).rank(pct=True)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                             "z14":(c/c.shift(14)-1)/(sd*np.sqrt(14)),
                             "z7":(c/c.shift(7)-1)/(sd*np.sqrt(7)),
                             "z30":(c/c.shift(30)-1)/(sd*np.sqrt(30)),
                             "f7":c.shift(-7)/c-1,"f1":r.shift(-1),"sd":sd,"sdy":sdy,
                             "ret60":c/c.shift(60)-1,
                             "inprof":b["regime"].isin(["unknown","mean_reversion"]).values,
                             "day":pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year.values,
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday.values})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    g=d[d.pos%7==0].dropna(subset=["f7","z14"]).copy()
    drift=g.groupby("coin").f7.mean()
    g["u"]=g.f7-g.coin.map(drift)
    g["sdq"]=g.groupby("coin").sd.rank(pct=True)
    def cl_slope(sub,x):
        sub=sub.dropna(subset=[x,"u"])
        if len(sub)<10: return (len(sub),np.nan,np.nan,np.nan)
        X=sub[x]-sub[x].mean(); y=sub.u-sub.u.mean()
        b=(X*y).sum()/(X*X).sum()
        e=y-b*X
        sc=(X*e).groupby(sub.day).sum()
        D=len(sc)
        var=(sc**2).sum()/((X*X).sum()**2)*D/(D-1)
        return (len(sub),D,b,b/np.sqrt(var))
    out={}
    res={}
    ip=g[g.inprof]
    for x in ["z7","z14","z30"]:
        res["inprof_"+x]=cl_slope(ip,x)
        res["lowvolq20_"+x]=cl_slope(g[g.sdq<=0.2],x)
        res["lowvolq20_outprof_"+x]=cl_slope(g[(g.sdq<=0.2)&(~g.inprof)],x)
        res["calm_sdy_le05_"+x]=cl_slope(g[g.sdy<=0.5],x)
        res["agit_sdy_gt05_"+x]=cl_slope(g[g.sdy>0.5],x)
    out["clustered_slopes"]=pd.DataFrame(res,index=["n","days","slope","t"]).T
    # per window sign in profile and low vol
    res={}
    for w,sub in g.groupby("w"):
        a=cl_slope(sub[sub.inprof],"z14"); bq=cl_slope(sub[sub.sdq<=0.2],"z14")
        res[w]=(a[0],a[2],bq[0],bq[2])
    out["per_window"]=pd.DataFrame(res,index=["n_in","slope_in","n_lv","slope_lv"]).T
    # sides in profile
    res={}
    res["in_up"]=cl_slope(ip[ip.z14>0],"z14"); res["in_dn"]=cl_slope(ip[ip.z14<0],"z14")
    lv=g[g.sdq<=0.2]
    res["lv_up"]=cl_slope(lv[lv.z14>0],"z14"); res["lv_dn"]=cl_slope(lv[lv.z14<0],"z14")
    out["sides"]=pd.DataFrame(res,index=["n","days","slope","t"]).T
    # signed momentum mean in profile: u*sign(z14)
    ip2=ip.copy(); ip2["m"]=ip2.u*np.sign(ip2.z14)
    out["inprof_signed_by_coin"]=ip2.groupby("coin").m.agg(["count","mean"])
    # weekday by year
    dd=d.dropna(subset=["f1"]).copy()
    dd["thfr"]=dd.wd.isin([3,4])
    out["thfr_minus_rest_by_year"]=dd.groupby("yr").apply(lambda x: pd.Series({"n":len(x),"diff":x[x.thfr].f1.mean()-x[~x.thfr].f1.mean(),
        "t":stats.ttest_ind(x[x.thfr].f1,x[~x.thfr].f1,equal_var=False).statistic}))
    return out
