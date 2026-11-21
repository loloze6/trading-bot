def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hr=[]; rows24=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c); r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r1}))
            for i in range(0,n,72):
                if i<72 or i+72>=n: continue
                past=r1[i-71:i+1]; vv=v[i-71:i+1]
                a=np.abs(past)
                rows.append(dict(coin=coin,w=w,yr=ts.iloc[i].year,r72=c[i]/c[i-72]-1,r24=c[i]/c[i-24]-1,
                    vol=np.nanstd(past),jump=np.nanmax(a)/np.nansum(a),
                    effic=abs(c[i]/c[i-72]-1)/np.nansum(a),
                    vconc=np.nanmax(vv)/max(np.nansum(vv),1e-12),
                    vtrend=np.nansum(vv[-24:])/max(np.nansum(vv),1e-12),
                    fc=b["forecast"].iloc[i],f=c[i+72]/c[i]-1))
            for i in range(0,n,24):
                if i<24 or i+24>=n: continue
                rows24.append(dict(coin=coin,r24=c[i]/c[i-24]-1,vol=np.nanstd(r1[i-23:i+1]),f=c[i+24]/c[i]-1))
    g=pd.DataFrame(rows); g["ex"]=g["f"]-g.groupby("coin")["f"].transform("mean")
    g24=pd.DataFrame(rows24); g24["ex"]=g24["f"]-g24.groupby("coin")["f"].transform("mean")
    out={}
    def corr(df,x):
        d=df[[x,"ex"]].dropna(); 
        if len(d)<30: return (np.nan,np.nan,len(d))
        rho=stats.spearmanr(d[x],d["ex"])[0]; t=rho*np.sqrt((len(d)-2)/(1-rho**2)); return (round(rho,4),round(t,2),len(d))
    res=[]
    for reg,df in [("all",g),("down72",g[g.r72<0]),("up72",g[g.r72>0])]:
        for x in ["r72","r24","vol","jump","effic","vconc","vtrend"]:
            rho,t,n=corr(df,x); res.append(dict(reg=reg,x=x,rho=rho,t=t,n=n))
    out["grid72 spearman feature vs fwd72 excess"]=pd.DataFrame(res)
    # signed move x efficiency: does efficient move continue?
    g["sm"]=np.sign(g.r72)*g.ex
    out["sign-aligned fwd by effic tercile"]=g.groupby(pd.qcut(g.effic,3,labels=False))["sm"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["fwd72 ex by r72 quintile"]=g.groupby(pd.qcut(g.r72,5,labels=False))["ex"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["fwd72 ex by vol quintile"]=g.groupby(pd.qcut(g.vol,5,labels=False))["ex"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["fwd24 ex by r24 quintile"]=g24.groupby(pd.qcut(g24.r24,5,labels=False))["ex"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["fwd72 ex by year"]=g.groupby("yr")["ex"].agg(["mean","count"])
    out["down72 r72 vs fwd by coin"]=g[g.r72<0].groupby("coin").apply(lambda d: pd.Series(corr(d,"r72"),index=["rho","t","n"]))
    H=pd.concat(hr)
    out["hourly ret by hour (bp)"]=H.groupby("hour")["r"].agg(lambda s:s.mean()*1e4).to_frame("bp").join(H.groupby("hour")["r"].agg(lambda s:s.mean()/s.std()*np.sqrt(s.count())).rename("t"))
    out["hourly ret by weekday"]=H.groupby("wd")["r"].agg(lambda s:s.mean()*1e4).to_frame("bp").join(H.groupby("wd")["r"].agg(lambda s:s.mean()/s.std()*np.sqrt(s.count())).rename("t"))
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book by coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin_=("coin_return","mean"))
    bd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book by window"]=bd.groupby("w")[["book_return","coin_return"]].mean().assign(sh=bd.groupby("w")["book_return"].apply(lambda s:s.mean()/s.std()*np.sqrt(365)))
    return out
