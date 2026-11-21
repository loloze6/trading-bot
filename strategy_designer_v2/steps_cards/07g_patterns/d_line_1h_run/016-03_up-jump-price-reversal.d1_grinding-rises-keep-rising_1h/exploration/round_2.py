def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows24 = []; rows72 = []; hr = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(c)
            hr.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"hour":ts.dt.hour.values,"r":r1}))
            for t in range(168, n-24, 24):
                seg = r1[t-23:t+1]; sd = np.nanstd(r1[t-167:t+1])
                p24 = c[t]/c[t-24]-1
                eff24 = abs(np.log(c[t]/c[t-24]))/np.nansum(np.abs(np.log1p(seg)))
                rows24.append(dict(coin=coin,w=w,year=ts.iloc[t].year,past=p24,pz=p24/(sd*np.sqrt(24)),
                                   eff=eff24,sd=sd,fwd=c[t+24]/c[t]-1))
            for t in range(72, n-72, 72):
                seg = r1[t-71:t+1]; p = c[t]/c[t-72]-1
                eff = abs(np.log(c[t]/c[t-72]))/np.nansum(np.abs(np.log1p(seg)))
                rows72.append(dict(coin=coin,w=w,past=p,eff=eff,seff=np.sign(p)*eff,fwd=c[t+72]/c[t]-1))
    d = pd.DataFrame(rows24); d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    g = pd.DataFrame(rows72); g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    def reg(df,x,y="ex"):
        s=df[[x,y,"coin"]].dropna(); xs=s[x]-s.groupby("coin")[x].transform("mean")
        r=stats.linregress(xs,s[y]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(s)})
    out={}
    out["rev24_coin"]=pd.DataFrame({k:reg(s,"pz") for k,s in d.groupby("coin")}).T
    out["rev24_year"]=pd.DataFrame({k:reg(s,"pz") for k,s in d.groupby("year")}).T
    d["sdq"]=d.groupby("coin")["sd"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["rev24_volterc"]=pd.DataFrame({k:reg(s,"pz") for k,s in d.groupby("sdq")}).T
    d["pq"]=d.groupby("coin")["pz"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["rev24_quint"]=d.groupby("pq")["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["rev24_up_down"]=pd.DataFrame({"up":reg(d[d.past>0],"pz"),"down":reg(d[d.past<0],"pz")}).T
    # multivariate on 72: past and signed eff
    s=g.dropna(subset=["past","seff","ex"]).copy()
    for x in ["past","seff"]: s[x+"_d"]=s[x]-s.groupby("coin")[x].transform("mean")
    X=np.c_[np.ones(len(s)),s["past_d"],s["seff_d"]]; y=s["ex"].values
    b,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; s2=e@e/(len(y)-3)
    se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["mv72"]=pd.Series({"b_past":b[1],"t_past":b[1]/se[1],"b_seff":b[2],"t_seff":b[2]/se[2],"n":len(y)})
    out["seff_coin"]=pd.DataFrame({k:reg(x,"seff") for k,x in g.groupby("coin")}).T
    H=pd.concat(hr); H["late"]=H.hour.isin([21,22])
    hy=H.groupby(["year","late"])["r"].agg(["mean","std","count"]); hy["t"]=hy["mean"]/hy["std"]*np.sqrt(hy["count"])
    out["late_by_year"]=hy[["mean","t","count"]]
    hc=H.groupby(["coin","late"])["r"].agg(["mean","std","count"]); hc["t"]=hc["mean"]/hc["std"]*np.sqrt(hc["count"])
    out["late_by_coin"]=hc[["mean","t"]]
    return out
