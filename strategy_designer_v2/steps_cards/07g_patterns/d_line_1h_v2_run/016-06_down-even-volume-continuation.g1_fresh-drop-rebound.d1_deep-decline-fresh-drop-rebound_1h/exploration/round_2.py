def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; rows24=[]; hr=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c); r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"yr":ts.dt.year.values,"wd":ts.dt.weekday.values,"r":r1}))
            for i in range(0,n,72):
                if i<72 or i+72>=n: continue
                past=r1[i-71:i+1]; vv=v[i-71:i+1]; a=np.abs(past)
                rows.append(dict(coin=coin,yr=ts.iloc[i].year,r72=c[i]/c[i-72]-1,
                    effic=abs(c[i]/c[i-72]-1)/np.nansum(a),
                    vtrend=np.nansum(vv[-24:])/max(np.nansum(vv),1e-12),f=c[i+72]/c[i]-1))
            for i in range(0,n,24):
                if i<72 or i+72>=n: continue
                rv=np.nanstd(r1[i-71:i+1])
                rows24.append(dict(coin=coin,yr=ts.iloc[i].year,r24=c[i]/c[i-24]-1,z24=(c[i]/c[i-24]-1)/(rv*np.sqrt(24)),
                    f24=c[i+24]/c[i]-1))
    g=pd.DataFrame(rows); g["ex"]=g.f-g.groupby("coin").f.transform("mean")
    g["sm"]=np.sign(g.r72)*g.ex
    g24=pd.DataFrame(rows24); g24["ex"]=g24.f24-g24.groupby("coin").f24.transform("mean")
    def sp(d,x,y):
        d=d[[x,y]].dropna(); rho=stats.spearmanr(d[x],d[y])[0]; return pd.Series({"rho":round(rho,4),"t":round(rho*np.sqrt((len(d)-2)/(1-rho**2)),2),"n":len(d)})
    out={}
    out["r24 vs fwd24 by coin"]=g24.groupby("coin").apply(lambda d:sp(d,"r24","ex"))
    out["r24 vs fwd24 by year"]=g24.groupby("yr").apply(lambda d:sp(d,"r24","ex"))
    out["z24 vs fwd24 all"]=sp(g24,"z24","ex").to_frame("v")
    out["fwd24 by z24 quintile"]=g24.groupby(pd.qcut(g24.z24,5,labels=False)).ex.agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["effic vs sign-aligned fwd72 by coin"]=g.groupby("coin").apply(lambda d:sp(d,"effic","sm"))
    out["effic vs sign-aligned by year"]=g.groupby("yr").apply(lambda d:sp(d,"effic","sm"))
    out["vtrend vs fwd72 by coin"]=g.groupby("coin").apply(lambda d:sp(d,"vtrend","ex"))
    H=pd.concat(hr)
    H["late"]=H.hour.isin([21,22])
    L=H[H.late]
    out["hour21-22 bp by coin"]=L.groupby("coin").r.agg(bp=lambda s:s.mean()*1e4,t=lambda s:s.mean()/s.std()*np.sqrt(s.count()))
    out["hour21-22 bp by year"]=L.groupby("yr").r.agg(bp=lambda s:s.mean()*1e4,t=lambda s:s.mean()/s.std()*np.sqrt(s.count()))
    out["hour21-22 by weekday"]=L.groupby("wd").r.agg(bp=lambda s:s.mean()*1e4,t=lambda s:s.mean()/s.std()*np.sqrt(s.count()))
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items(): D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    bd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book vs coin corr"]=pd.Series({"corr":bd[["book_return","coin_return"]].corr().iloc[0,1],"book_sh":bd.book_return.mean()/bd.book_return.std()*np.sqrt(365),"hold_sh":bd.coin_return.mean()/bd.coin_return.std()*np.sqrt(365)}).to_frame("v")
    return out
