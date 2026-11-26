def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 5d return over all windows, grid
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-5,5):
                allr.append(c[i+5]/c[i]-1)
        mu=np.mean(allr) if allr else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            tr=c/c.shift(60)-1
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            for h in (1,3,5,10,20):
                pass
            for i in range(0,len(b)-5,5):
                r={}
                for h in (3,5,10,20):
                    r[f"f{h}"]=c.iloc[i+h]/c.iloc[i]-1 if i+h<len(b) else np.nan
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    inprof=b["regime"].iloc[i]=="unknown",fc=b["forecast"].iloc[i],
                    tr=tr.iloc[i],vr=vr.iloc[i],ex5=r["f5"]-mu,**r))
    d=pd.DataFrame(rows)
    p=d[d.inprof].copy()
    out={}
    def slope(df,x,y):
        df=df[[x,y]].dropna()
        if len(df)<10 or df[x].std()==0: return (len(df),np.nan,np.nan)
        s=stats.linregress(df[x],df[y]); return (len(df),s.slope,s.slope/s.stderr)
    out["prof_slope_fc_ex5"]=pd.Series(slope(p,"fc","ex5"),index=["n","slope","t"])
    for h in (3,5,10,20):
        out[f"prof_slope_negvr_f{h}"]=pd.Series(slope(p.assign(nv=-p.vr),"nv",f"f{h}"),index=["n","slope","t"])
    out["by_coin"]=pd.DataFrame({c:slope(g,"fc","ex5") for c,g in p.groupby("coin")},index=["n","slope","t"]).T
    out["by_window"]=pd.DataFrame({c:slope(g,"fc","ex5") for c,g in p.groupby("w")},index=["n","slope","t"]).T
    out["by_year"]=pd.DataFrame({c:slope(g,"fc","ex5") for c,g in p.groupby("year")},index=["n","slope","t"]).T
    p["q"]=pd.qcut(p.vr,5,labels=False,duplicates="drop")
    out["prof_by_vr_quintile"]=p.groupby("q").agg(n=("ex5","size"),vr=("vr","mean"),ex5=("ex5","mean"),f10=("f10","mean"),f20=("f20","mean"))
    out["prof_fc_pos_vs_zero"]=p.groupby(p.fc>0).agg(n=("ex5","size"),ex5=("ex5","mean"),sd=("ex5","std"),f10=("f10","mean"))
    # rising but not in profile (approx rising calm)
    rc=d[(~d.inprof)&(d.tr>0.10)].copy()
    out["rising_calm_negvr_f5"]=pd.Series(slope(rc.assign(nv=-rc.vr),"nv","ex5"),index=["n","slope","t"])
    out["all_negvr_f5"]=pd.Series(slope(d.assign(nv=-d.vr),"nv","ex5"),index=["n","slope","t"])
    rc["q"]=pd.qcut(rc.vr,5,labels=False,duplicates="drop")
    out["risingcalm_by_vr_q"]=rc.groupby("q").agg(n=("ex5","size"),vr=("vr","mean"),ex5=("ex5","mean"))
    return out
