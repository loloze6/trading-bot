def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(b)-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift=np.mean(allr); sd=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            lvr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            r1=c/c.shift(1)-1
            vol30=r1.rolling(30).std()
            vrel=vol30/vol30.expanding(min_periods=20).median()
            yr=pd.to_datetime(b["timestamp"]).dt.year
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            for i in range(0,len(b)-H,H):
                fr=c[i+H]/c[i]-1
                rows.append(dict(coin=coin,w=w,yr=yr[i],day=day[i],fc=b["forecast"][i],
                    r20=r20[i],r60=r60[i],lvr=lvr[i],vrel=vrel[i],ex=fr-drift,z=(fr-drift)/sd))
    d=pd.DataFrame(rows)
    out={}
    def tday(x,col):
        x=x.dropna(subset=[col])
        s=x.groupby("day")[col].sum()
        return pd.Series({"n":len(x),"days":len(s),"mean":x[col].mean(),"t_day":s.mean()/(s.std()/np.sqrt(len(s)))})
    a=d[d.fc!=0].copy(); a["sx"]=np.sign(a.fc)*a.ex; a["s"]=np.sign(a.fc)
    out["active_deep_r20_le_-10_signed"]=tday(a[a.r20<=-0.10],"sx")
    out["active_shallow_r20_gt_-10_signed"]=tday(a[a.r20>-0.10],"sx")
    out["active_short_side_ex"]=tday(a[a.s<0],"ex")
    out["active_long_side_ex"]=tday(a[a.s>0],"ex")
    a["ag"]=np.where(a.vrel>1,"agitated",np.where(a.vrel<=1,"calm","na"))
    out["active_signed_by_ag"]=a.groupby("ag").apply(lambda x:tday(x,"sx"))
    a["deep"]=a.r20<=-0.10
    out["active_deep_by_year"]=a[a.deep].groupby("yr").sx.agg(["count","mean"])
    out["active_deep_by_coin"]=a[a.deep].groupby("coin").sx.agg(["count","mean"])
    # falling, moderate fall: graded slope of z on lvr in deep vs shallow
    f=d[(d.r60<-0.10)&(d.r20<0)&(d.r20>=-0.2)].dropna(subset=["lvr","z"])
    res={}
    for nm,x in [("deep",f[f.r20<=-0.10]),("shallow",f[f.r20>-0.10])]:
        sl=stats.linregress(x.lvr,x.z); res[nm]=pd.Series({"n":len(x),"slope":sl.slope,"t":sl.slope/sl.stderr})
    out["falling_mod_slope_lvr_deep_vs_shallow"]=pd.DataFrame(res)
    # interaction: lvr * |r20| graded
    f=f.copy(); f["inter"]=f.lvr*(-f.r20)
    sl=stats.linregress(f.inter,f.z); out["falling_mod_slope_lvr_x_depth"]=pd.Series({"n":len(f),"slope":sl.slope,"t":sl.slope/sl.stderr})
    # falling shrink x depth by year
    f["sx"]=-np.sign(f.lvr)*0  # placeholder
    fd=f[f.r20<=-0.10]; fd=fd.assign(sx=np.sign(fd.lvr)*fd.ex)
    out["falling_deep_signed_lvr_by_year"]=fd.groupby("yr").sx.agg(["count","mean"])
    out["falling_deep_signed_lvr_tday"]=tday(fd,"sx")
    return out
