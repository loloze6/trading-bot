def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    out={}
    cs=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; wk=pd.to_datetime(b["timestamp"]).dt.weekday.values
            r14=pd.Series(cl).pct_change(14).values
            vol=pd.Series(cl).pct_change().rolling(20).std().values
            lo=pd.Series(b["low"].values).rolling(365,min_periods=60).min().values
            hi=pd.Series(b["high"].values).rolling(365,min_periods=60).max().values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(b)
            for i in range(0,n-2,2):
                cs.append(dict(coin=c,wn=int(w[1:]),fri=wk[i]==4,wkd=wk[i],ret2=cl[i+2]/cl[i]-1,
                    z=r14[i]/(vol[i]*np.sqrt(14)) if vol[i]>0 else np.nan,
                    pos=(cl[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,year=yr[i]))
            for i in range(n-2):
                if wk[i]==4 and i%2==1:
                    cs.append(dict(coin=c,wn=int(w[1:]),fri=True,wkd=4,ret2=cl[i+2]/cl[i]-1,
                        z=r14[i]/(vol[i]*np.sqrt(14)) if vol[i]>0 else np.nan,
                        pos=(cl[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,year=yr[i]))
    C=pd.DataFrame(cs).dropna(subset=["z"])
    def g(x): return pd.Series(dict(n=len(x),mean=x["ret2"].mean(),t=x["ret2"].mean()/(x["ret2"].std()/np.sqrt(len(x)))))
    C["up"]=C["z"]>0
    out["fri_vs_not_by_up"]=C.groupby(["fri","up"]).apply(g)
    NF=C[~C["fri"]&C["up"]].copy(); NF["q"]=pd.qcut(NF["z"],3,labels=False)
    out["nonfri_up_by_z_tercile"]=NF.groupby("q").apply(g)
    C["posq"]=pd.cut(C["pos"],[-.01,.5,.8,1.01])
    out["fri_by_pos_up"]=C[C["fri"]].groupby(["posq","up"]).apply(g)
    out["nonfri_by_pos_up"]=C[~C["fri"]].groupby(["posq","up"]).apply(g)
    out["fri_up_by_year"]=C[C["fri"]&C["up"]].groupby("year").apply(g)
    # long-only book deepest fall by year
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); d=days[c][w].reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).dt.normalize(); al=b["postRebalance_current_allocation"].values
            m=pd.DataFrame({"day":ts,"prev":np.r_[0,al[:-1]],"al":al})
            dd=pd.DataFrame({"day":pd.to_datetime(d["day"]).dt.normalize(),"br":d["book_return"].values}).merge(m,on="day",how="left")
            dd["lo"]=dd["br"].where(~((dd["prev"]<0)|(dd["al"]<0)),0.0); dd["wn"]=int(w[1:])
            rows.append(dd)
    D=pd.concat(rows); B=D.groupby(["wn","day"])["lo"].mean().dropna().reset_index().sort_values(["wn","day"])
    v=(1+B["lo"]).cumprod(); B["dd"]=(v/v.cummax()-1).values; B["year"]=pd.to_datetime(B["day"]).dt.year
    out["longonly_by_year"]=B.groupby("year").agg(sum=("lo","sum"),min_dd=("dd","min"))
    return out
