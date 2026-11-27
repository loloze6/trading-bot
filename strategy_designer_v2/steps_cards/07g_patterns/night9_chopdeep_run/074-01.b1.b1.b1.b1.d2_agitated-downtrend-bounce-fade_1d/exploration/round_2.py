def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["ts"]=pd.to_datetime(b["timestamp"])
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            d["r0"]=c.pct_change()
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["r1b"]=c.shift(-2)/c.shift(-1)-1
            rng=(h-l)/c
            d["rr"]=rng/rng.rolling(20,min_periods=20).mean()
            d["loc"]=(c-l)/(h-l).replace(0,np.nan)
            d["tr60"]=c/c.shift(60)-1
            v=d["r0"].rolling(30).std()
            d["agi"]=v/v.expanding(30).median()
            d["inprof"]=(b["regime"]!="chop").astype(int)
            d["coin"]=coin; d["w"]=w; d["wn"]=int(w[1:])
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["day"]=A["ts"].dt.floor("D")
    for col in ["r1","r2","r1b"]:
        A["mu_"+col]=A.groupby("coin")[col].transform("mean")
    def tt(sub,col="r1"):
        x=(sub[col]-sub["mu_"+col]); ok=x.notna(); x=x[ok]; dd=sub["day"][ok]
        if len(x)<5: return pd.Series({"n":len(x),"mean":np.nan,"t":np.nan,"days":0})
        g=x.groupby(dd).sum(); D=len(g); m=g.sum()/len(x)
        se=np.sqrt((g**2).sum()*D/(D-1))/len(x)
        return pd.Series({"n":len(x),"mean":m,"t":m/se,"days":D})
    A["trend"]=np.where(A.tr60>0.1,"rising",np.where(A.tr60<-0.1,"falling",np.where(A.tr60.notna(),"choppy","na")))
    A["agt"]=np.where(A.agi>1,"agit",np.where(A.agi.notna(),"calm","na"))
    out={}
    up=A[(A.r0>0)&A.rr.notna()]
    res={}
    for (tr,ag),s in up.groupby(["trend","agt"]):
        s=s.copy(); 
        if len(s)<40: continue
        s["q"]=pd.qcut(s.rr,3,labels=False,duplicates="drop")
        for k,ss in s.groupby("q"): res[f"{tr}_{ag}_q{k}"]=tt(ss)
    out["up_days_rr_tercile_by_trend_agit"]=pd.DataFrame(res).T
    # choppy wide up: horizons
    res={}
    for tr in ["choppy","falling","rising"]:
        s=A[(A.r0>0)&(A.trend==tr)&(A.rr>=1.3)]
        res[tr+"_r1"]=tt(s,"r1"); res[tr+"_r1b(day2)"]=tt(s,"r1b"); res[tr+"_r2"]=tt(s,"r2")
    out["wideup_rr1.3_horizons"]=pd.DataFrame(res).T
    # choppy wide up by year and by close loc
    s=A[(A.r0>0)&(A.trend=="choppy")&(A.rr>=1.2)].copy()
    s["yr"]=s.ts.dt.year
    res={}
    for k,ss in s.groupby("yr"): res["y"+str(k)]=tt(ss)
    s["lq"]=pd.cut(s["loc"],[0,0.5,0.75,1.01],labels=["low","mid","high"])
    for k,ss in s.groupby("lq"): res["loc_"+str(k)]=tt(ss)
    out["choppy_wideup_by_year_loc"]=pd.DataFrame(res).T
    # correlation grading in choppy up days: rr vs dev
    s=A[(A.r0>0)&(A.trend=="choppy")].dropna(subset=["rr","r1"])
    out["choppy_up_spearman_rr_vs_r1"]=float(s[["rr","r1"]].corr("spearman").iloc[0,1])
    s=A[(A.r0>0)&(A.trend=="falling")].dropna(subset=["rr","r1"])
    out["falling_up_spearman_rr_vs_r1"]=float(s[["rr","r1"]].corr("spearman").iloc[0,1])
    s=A[(A.r0>0)&(A.trend=="rising")].dropna(subset=["rr","r1"])
    out["rising_up_spearman_rr_vs_r1"]=float(s[["rr","r1"]].corr("spearman").iloc[0,1])
    # book largest days
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=coin; dl.append(x)
    Dd=pd.concat(dl)
    act=Dd[Dd.book_return.abs()>1e-9]
    out["book_active_coin_days_by_coin"]=act.groupby("coin")["book_return"].agg(["count","mean","std"])
    return out
