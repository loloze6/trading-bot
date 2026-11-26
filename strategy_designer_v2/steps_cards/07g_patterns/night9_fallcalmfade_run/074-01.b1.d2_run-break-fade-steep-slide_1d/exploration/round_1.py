def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            n=len(d)
            tr60=c/c.shift(60)-1
            ret20=c/c.shift(20)-1
            sd30=r.shift(1).rolling(30).std()
            # down run before today, up run before today
            dn=(r<0).astype(int); up=(r>0).astype(int)
            drun=np.zeros(n); urun=np.zeros(n)
            for i in range(1,n):
                drun[i]=drun[i-1]+1 if dn.iloc[i] else 0
                urun[i]=urun[i-1]+1 if up.iloc[i] else 0
            prev_drun=pd.Series(drun).shift(1); prev_urun=pd.Series(urun).shift(1)
            rng=(d["high"]-d["low"])/c
            clv=(c-d["low"])/(d["high"]-d["low"]).replace(0,np.nan)
            x=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(d["timestamp"]).dt.floor("D"),
                "wd":pd.to_datetime(d["timestamp"]).dt.weekday,"year":pd.to_datetime(d["timestamp"]).dt.year,
                "r":r,"nxt":nxt,"tr60":tr60,"ret20":ret20,"sd30":sd30,"prev_drun":prev_drun.values,
                "prev_urun":prev_urun.values,"rng":rng,"clv":clv,"fc":d["forecast"]})
            rows.append(x)
    X=pd.concat(rows,ignore_index=True)
    X=X.dropna(subset=["nxt","r","tr60","sd30"])
    X["cmean"]=X.groupby("coin")["nxt"].transform("mean")
    X["ex"]=X["nxt"]-X["cmean"]
    X["z"]=X["ex"]/X["sd30"]
    X["trend"]=np.where(X.tr60>0.10,"rising",np.where(X.tr60<-0.10,"falling","choppy"))
    med=X.groupby("coin")["sd30"].transform("median")
    X["agit"]=np.where(X.sd30>med,"agit","calm")
    def ct(s,days):
        g=s.groupby(days).sum(); G=len(g)
        if G<3: return np.nan
        se=np.sqrt((g**2).sum()*G/(G-1))/len(s)*1.0
        return s.mean()/se if se>0 else np.nan
    def summ(m,col="ex"):
        out={}
        for k,sub in m:
            s=sub[col]-sub[col].mean()+sub[col].mean()
            dev=sub[col]-0
            out[k]={"n":len(sub),"mean%":100*sub[col].mean(),"t_day":ct(sub[col],sub["day"]),"days":sub["day"].nunique()}
        return pd.DataFrame(out).T
    res={}
    upbr=X[(X.r>0)&(X.prev_drun>=1)].copy()
    upbr["runb"]=upbr.prev_drun.clip(upper=5).astype(int)
    res["upbreak_by_trend_run_nextex"]=summ(upbr.groupby(["trend","runb"]))
    res["upbreak_by_trend_agit_run2plus"]=summ(upbr[upbr.prev_drun>=2].groupby(["trend","agit"]))
    res["all_days_by_trend_nextex"]=summ(X.groupby(["trend","agit"]))
    # mirror: first down day after an up run
    dnbr=X[(X.r<0)&(X.prev_urun>=1)].copy()
    dnbr["runb"]=dnbr.prev_urun.clip(upper=5).astype(int)
    res["downbreak_by_trend_run_nextex"]=summ(dnbr.groupby(["trend","runb"]))
    # all up days / down days by trend and size of move in sd units
    X["rz"]=X.r/X.sd30
    X["rzb"]=pd.cut(X.rz,[-99,-2,-1,-0.3,0.3,1,2,99])
    res["by_trend_rz_nextex"]=summ(X.groupby(["trend","rzb"],observed=True))
    return res
