def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drifts={}
    H=[1,3,5,10]
    for coin,ws in data["bars"].items():
        g={h:[] for h in H}
        for w,b in ws.items():
            c=b["close"].values
            for h in H:
                idx=np.arange(0,len(c)-h,h)
                g[h]+=list(c[idx+h]/c[idx]-1)
        drifts[coin]={h:np.mean(g[h]) for h in H}
        sd5=np.std(g[5],ddof=1)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            o,hi,lo,c,v=[b[k].values.astype(float) for k in ["open","high","low","close","volume"]]
            mv=pd.Series(v).shift(1).rolling(20).mean().values
            volr=v/mv; body=np.abs(c-o)/o*100
            rng=hi-lo; clv=np.where(rng>0,(c-lo)/rng,np.nan)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            for t in range(n):
                if not (volr[t]>=2): continue
                flat=body[t]<=1
                r={"coin":coin,"w":w,"t":t,"year":yr[t],"volr":volr[t],"clv":clv[t],"flat":flat,"body":body[t]}
                for h in H:
                    r[f"u{h}"]=(c[t+h]/c[t]-1-drifts[coin][h])*100 if t+h<n else np.nan
                r["s5"]=r["u5"]/100/sd5 if t+5<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    # one per 5-grid cell per window, separately flat/nonflat
    d["cell"]=d["t"]//5
    def first(x): return x.sort_values("t").groupby(["coin","w","cell"]).head(1)
    out={}
    def summ(x,col="u5"):
        x=x.dropna(subset=[col]); m=x[col].mean(); s=x[col].std(ddof=1)
        return pd.Series({"n":len(x),"mean%":m,"t":m/(s/np.sqrt(len(x))) if len(x)>1 else np.nan})
    for flat in [True,False]:
        f=first(d[d.flat==flat]).copy()
        f["clvbin"]=pd.cut(f["clv"],[-0.01,1/3,2/3,1.01],labels=["low","mid","high"])
        out[f"flat={flat} by clv bin, u1/u3/u5/u10"]=pd.concat({h:f.groupby("clvbin").apply(lambda x:summ(x,f"u{h}")) for h in H},axis=1)
        out[f"flat={flat} corr clv vs u"]=pd.Series({h:f[["clv",f"u{h}"]].dropna().corr().iloc[0,1] for h in H})
        if flat:
            ff=f
    ff["signed"]=ff["u5"]*np.sign(ff["clv"]-0.5)
    out["flat by coin: corr clv,u5 and high-bin u5"]=ff.groupby("coin").apply(lambda x:pd.Series({"n":len(x),"corr":x[["clv","u5"]].corr().iloc[0,1],"high_u5":x[x.clv>2/3]["u5"].mean(),"low_u5":x[x.clv<1/3]["u5"].mean()}))
    out["flat by year"]=ff.groupby("year").apply(lambda x:pd.Series({"n":len(x),"corr":x[["clv","u5"]].corr().iloc[0,1],"signed_u5":x["signed"].mean()}))
    ff["vbin"]=pd.qcut(ff["volr"],3,labels=["v_lo","v_mid","v_hi"])
    out["flat by volr tercile"]=ff.groupby("vbin").apply(lambda x:pd.Series({"n":len(x),"corr":x[["clv","u5"]].corr().iloc[0,1],"signed_u5":x["signed"].mean(),"t":x["signed"].mean()/(x["signed"].std()/np.sqrt(len(x)))}))
    out["flat high clv (>2/3) by volr tercile u5"]=ff[ff.clv>2/3].groupby("vbin")["u5"].agg(["count","mean"])
    return out
