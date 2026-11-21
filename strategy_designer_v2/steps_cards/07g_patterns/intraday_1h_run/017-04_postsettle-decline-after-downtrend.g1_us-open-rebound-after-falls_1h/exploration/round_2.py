def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"].values.astype(float)
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            r2=np.r_[cl[2:]/cl[:-2]-1,np.nan,np.nan]
            f72=pd.Series(cl).pct_change(72).values
            vol=pd.Series(r1).shift(1).rolling(72).std().values
            df=pd.DataFrame({"coin":c,"w":w,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"yr":ts.dt.year.values,
                             "r2":r2,"f72":f72,"vol":vol})
            rows.append(df)
    B=pd.concat(rows,ignore_index=True)
    allm=B.dropna(subset=["r2"])
    out={}
    # A: 20:00-22:00 drift (r2 at bar 19)
    A=B[B.hour==19].dropna(subset=["r2"]).copy()
    # excess vs every-hour mean of r2 for the coin (grid approx by hour 19 vs other hours)
    def tm(s): return pd.Series({"mean_bp":s.mean()*1e4,"t":s.mean()/(s.std()/np.sqrt(len(s))),"n":len(s)})
    out["A_19_by_coin"]=A.groupby("coin")["r2"].apply(tm).unstack()
    out["A_19_by_year"]=A.groupby("yr")["r2"].apply(tm).unstack()
    out["A_19_by_wd"]=A.groupby("wd")["r2"].apply(tm).unstack()
    A["vq"]=A.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["A_19_by_volq"]=A.groupby("vq")["r2"].apply(tm).unstack()
    # B: afternoon momentum, r2 at bar 15 (bars 16,17) on signed 72h return
    res=[]
    Bq=B[B.hour==15].dropna(subset=["r2","f72"])
    for key,g in list(Bq.groupby("coin"))+[("ALL",Bq)]:
        sl=stats.linregress(g.f72,g.r2); res.append([key,sl.slope,sl.slope/sl.stderr,len(g)])
    for key,g in Bq.groupby("yr"):
        sl=stats.linregress(g.f72,g.r2); res.append([str(key),sl.slope,sl.slope/sl.stderr,len(g)])
    out["B_15_slope_on_f72"]=pd.DataFrame(res,columns=["grp","slope","t","n"]).set_index("grp")
    # quintiles of f72 at bar 15
    Bq=Bq.copy(); Bq["q"]=Bq.groupby("coin")["f72"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["B_15_by_f72_quintile"]=Bq.groupby("q")["r2"].apply(tm).unstack()
    # compare same slope at all hours with signed f72 (placebo spread)
    res=[]
    for h in range(24):
        g=B[B.hour==h].dropna(subset=["r2","f72"]); sl=stats.linregress(g.f72,g.r2); res.append([h,sl.slope,sl.slope/sl.stderr])
    out["slope_signed_by_hour"]=pd.DataFrame(res,columns=["hour","slope","t"]).set_index("hour")
    return out
