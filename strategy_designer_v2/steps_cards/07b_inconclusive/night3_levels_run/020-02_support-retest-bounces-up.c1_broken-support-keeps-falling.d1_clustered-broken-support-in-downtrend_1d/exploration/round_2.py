def explore(data):
    import numpy as np, pandas as pd
    H=[1,2,3,5,7,10,15]
    rows=[]; base=[]
    for coin, wins in data["bars"].items():
        drift={}; sd={}
        for h in H:
            rr=[]
            for w,b in wins.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rr+=list(c[idx+h]/c[idx]-1)
            drift[h]=np.mean(rr); sd[h]=np.std(rr)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            rc=b.get("debug_info.components.low_cluster.last_history_value")
            raw=rc.values if rc is not None else np.full(len(c),np.nan)
            sma=pd.Series(c).rolling(50,min_periods=20).mean().values
            dist=c/sma-1
            r1=pd.Series(c).pct_change(1).values
            r3=pd.Series(c).pct_change(3).values
            low=0; bets=np.zeros(len(c),bool)
            for i in range(len(c)):
                m=-f[i] if f[i]<0 else 0
                if m==0: low=0; continue
                if m-low>=2: bets[i]=True; low=m
                else: low=min(low,m)
            n=len(c)
            for cell in range(0,n,10):
                js=[j for j in range(cell,min(cell+10,n)) if bets[j]]
                if not js: continue
                j=js[0]
                d={"coin":coin,"wn":int(w[1:]),"raw":raw[j],"dist":dist[j],"r1":-r1[j],"r3":-r3[j]}
                for h in H:
                    if j+h<n:
                        d[f"u{h}"]=-(c[j+h]/c[j]-1-drift[h]); d[f"tot{h}"]=-(c[j+h]/c[j]-1)
                rows.append(d)
            for j in range(0,n-10,10):
                if dist[j]<0:
                    base.append({"coin":coin,"u10":-(c[j+10]/c[j]-1-drift[10]),"r1":-r1[j]})
    df=pd.DataFrame(rows); bs=pd.DataFrame(base)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["grid10_by_h_unusual"]=pd.DataFrame({h:tt(df[f"u{h}"]) for h in H}).T
    out["grid10_by_h_total"]=pd.DataFrame({h:tt(df[f"tot{h}"]) for h in H}).T
    out["u10_by_coin"]=df.groupby("coin")["u10"].apply(tt).unstack()
    df["third"]=pd.cut(df["wn"],[0,8,16,24],labels=["w1-8","w9-16","w17-24"])
    out["u10_by_third"]=df.groupby("third")["u10"].apply(tt).unstack()
    df["rawq"]=pd.qcut(df["raw"].rank(method="first"),4,labels=False)
    out["u10_by_rawq"]=df.groupby("rawq")["u10"].apply(tt).unstack()
    df["r1q"]=pd.qcut(df["r1"].rank(method="first"),4,labels=False)
    out["by_signalbar_drop_q"]=df.groupby("r1q").agg(drop=("r1","mean"),n=("u10","size"),u1=("u1","mean"),u3=("u3","mean"),u10=("u10","mean"))
    out["u10_by_r1q_t"]=df.groupby("r1q")["u10"].apply(tt).unstack()
    out["corr_raw_u10"]=float(df[["raw","u10"]].corr(method="spearman").iloc[0,1])
    out["corr_r1_u10"]=float(df[["r1","u10"]].corr(method="spearman").iloc[0,1])
    out["baseline_below_sma_u10"]=tt(bs["u10"])
    bs["r1q"]=pd.qcut(bs["r1"].rank(method="first"),4,labels=False)
    out["baseline_by_r1q"]=bs.groupby("r1q")["u10"].apply(tt).unstack()
    return out
