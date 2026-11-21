def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"]
            r2=c/c.shift(2)-1
            r1=c/c.shift(1)-1
            scale=r2.abs().rolling(60,min_periods=20).mean().shift(1)
            z=r2/scale
            f1=c.shift(-1)/c-1
            f2b=c.shift(-2)/c.shift(-1)-1
            rv=r1.abs().rolling(168,min_periods=48).mean()
            r24=c/c.shift(24)-1
            pos=np.arange(len(b))
            rows.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"pos":pos,"z":z.values,"f1":f1.values,
                "f2b":f2b.values,"rv":rv.values,"r24":r24.values,
                "alloc":b["postRebalance_current_allocation"].values,"prev":b["previous_allocation"].values}))
    d=pd.concat(rows,ignore_index=True).dropna(subset=["z","f1","f2b","rv"])
    d["zc"]=np.clip(d["z"],-3,3)
    d["s1"]=-d["zc"]*d["f1"]; d["s2"]=-d["zc"]*d["f2b"]
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x))})
    st=d[d.hour.isin([7,15,23])]
    split={"settle_bar1":tt(st["s1"]),"settle_bar2":tt(st["s2"])}
    # all hours, non-overlap grid pos%2==0, by vol tercile and z quintile
    g=d[d.pos%2==0].copy()
    g["vt"]=g.groupby("coin")["rv"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    g["s"]=g["s1"]+g["s2"]
    allvol=g.groupby("vt")["s"].apply(tt).unstack()
    g["zq"]=pd.qcut(g["z"],5,labels=False)
    zq=g.groupby("zq").apply(lambda x: pd.Series({"z_mean":x.z.mean(),"fwd2_bp":(x.f1+x.f2b).mean()*1e4,
        "t":(x.f1+x.f2b).mean()/(x.f1+x.f2b).std()*np.sqrt(len(x)),"n":len(x)}))
    # high-vol tercile, by z quintile
    h=g[g.vt==2].copy(); h["zq"]=pd.qcut(h["z"],5,labels=False)
    zqh=h.groupby("zq").apply(lambda x: pd.Series({"z_mean":x.z.mean(),"fwd2_bp":(x.f1+x.f2b).mean()*1e4,
        "t":(x.f1+x.f2b).mean()/(x.f1+x.f2b).std()*np.sqrt(len(x)),"n":len(x)}))
    # book gross: alloc*f1 on settlement bars vs turnover
    st2=st.copy(); st2["gain"]=st2["alloc"]*st2["f1"]
    book={"settle_gross_bp":st2["gain"].mean()*1e4,"settle_gross_t":st2.gain.mean()/st2.gain.std()*np.sqrt(len(st2)),
          "mean_abs_alloc":st2["alloc"].abs().mean(),"corr_alloc_negz":np.corrcoef(st2.alloc.fillna(0),-st2.zc)[0,1]}
    return {"split":pd.DataFrame(split).T,"allhours_by_vol":allvol,"allhours_zq":zq,"highvol_zq":zqh,"book":pd.Series(book)}
