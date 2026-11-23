def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,5,10]
    rows=[]
    for coin,ws in data["bars"].items():
        g={h:[] for h in H}
        for w,b in ws.items():
            c=b["close"].values
            for h in H:
                idx=np.arange(0,len(c)-h,h); g[h]+=list(c[idx+h]/c[idx]-1)
        dr={h:np.mean(g[h]) for h in H}; sd={h:np.std(g[h],ddof=1) for h in H}
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            o,hi,lo,c,v=[b[k].values.astype(float) for k in ["open","high","low","close","volume"]]
            volr=v/pd.Series(v).shift(1).rolling(20).mean().values
            rng=hi-lo; clv=np.where(rng>0,(c-lo)/rng,np.nan)
            ret20=c/pd.Series(c).shift(20).values-1
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            for t in range(0,n,10):
                if not np.isfinite(volr[t]): continue
                r={"coin":coin,"w":w,"year":yr[t],"volr":volr[t],"clv":clv[t],"ret20":ret20[t],"body":abs(c[t]-o[t])/o[t]*100}
                for h in H:
                    r[f"u{h}"]=(c[t+h]/c[t]-1-dr[h])*100 if t+h<n else np.nan
                    r[f"s{h}"]=(c[t+h]/c[t]-1-dr[h])/sd[h] if t+h<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows).dropna(subset=["u10","clv"])
    d["vgrp"]=pd.cut(d["volr"],[0,1,2,3,1e9],labels=["<1","1-2","2-3",">=3"])
    out={}
    def hl(x,col):
        a=x[x.clv>2/3][col]; bb=x[x.clv<1/3][col]
        tt=stats.ttest_ind(a,bb,equal_var=False).statistic if len(a)>2 and len(bb)>2 else np.nan
        return pd.Series({"n":len(x),"n_hi":len(a),"hi_mean":a.mean(),"lo_mean":bb.mean(),"hi_minus_lo":a.mean()-bb.mean(),"welch_t":tt,"corr_clv":x[["clv",col]].corr().iloc[0,1]})
    for h in [5,10]:
        out[f"10-day grid: by volume group, u{h} high vs low clv"]=d.groupby("vgrp").apply(lambda x:hl(x,f"u{h}"))
    hv=d[d.volr>=2]
    out["heavy (>=2) 10d grid by coin u10"]=hv.groupby("coin").apply(lambda x:hl(x,"u10"))
    out["heavy (>=2) 10d grid by year u10"]=hv.groupby("year").apply(lambda x:hl(x,"u10"))
    hv=hv.copy(); hv["cs"]=hv["clv"]-0.5
    out["heavy: graded clv-0.5 x u10 strength"]=pd.Series({"n":len(hv),"mean_signed_s10":(np.sign(hv.cs)*hv.s10).mean(),"corr_clv_u10":hv[["clv","u10"]].corr().iloc[0,1],"corr_clvxvolr_u10":pd.Series(hv.cs*hv.volr).corr(hv.u10)})
    return out
