def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[1,3,5,10,20]
    rows=[]; base=[]
    for coin, wins in data["bars"].items():
        # drift per horizon over all windows, non-overlapping
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
            raw=b.get("debug_info.components.low_cluster.last_history_value")
            raw=raw.values if raw is not None else np.full(len(c),np.nan)
            sma=pd.Series(c).rolling(50,min_periods=20).mean().values
            dist=c/sma-1
            r20=pd.Series(c).pct_change(20).values
            sigret=pd.Series(c).pct_change(1).values
            # bets
            low=0; bets=np.zeros(len(c),bool)
            for i in range(len(c)):
                m=-f[i] if f[i]<0 else 0
                if m==0: low=0; continue
                if m-low>=2: bets[i]=True; low=m
                else: low=min(low,m)
            n=len(c)
            for cell in range(0,n,5):
                js=[j for j in range(cell,min(cell+5,n)) if bets[j]]
                if not js: continue
                j=js[0]
                d={"coin":coin,"w":w,"raw":raw[j],"fc":f[j],"dist":dist[j],"r20":r20[j],"sig":-sigret[j]}
                for h in H:
                    if j+h<n:
                        d[f"u{h}"]=-(c[j+h]/c[j]-1-drift[h]); d[f"s{h}"]=d[f"u{h}"]/sd[h]
                rows.append(d)
            # baseline: all below-sma bars on 5-grid
            for j in range(0,n-5,5):
                if dist[j]<0:
                    base.append({"coin":coin,"u5":-(c[j+5]/c[j]-1-drift[5]),"cluster":raw[j]>0 if not np.isnan(raw[j]) else False})
    df=pd.DataFrame(rows); bs=pd.DataFrame(base)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["by_horizon"]=pd.DataFrame({h:tt(df[f"u{h}"]) for h in H}).T
    out["strength_by_h"]=pd.DataFrame({h:tt(df[f"s{h}"]) for h in H}).T
    out["fc_desc"]=df["fc"].describe()
    out["raw_desc"]=df["raw"].describe()
    out["by_coin"]=df.groupby("coin")["u5"].apply(tt).unstack()
    df["wn"]=df["w"].str[1:].astype(int)
    out["by_window"]=df.groupby("wn")["u5"].apply(tt).unstack()
    df["rawq"]=pd.qcut(df["raw"].rank(method="first"),4,labels=False)
    out["by_rawq"]=df.groupby("rawq").agg(raw=("raw","mean"),n=("u5","size"),u5=("u5","mean"),u10=("u10","mean"))
    df["distq"]=pd.qcut(df["dist"],4,labels=False)
    out["by_distq"]=df.groupby("distq").agg(dist=("dist","mean"),n=("u5","size"),u5=("u5","mean"),u10=("u10","mean"),u20=("u20","mean"))
    df["r20q"]=pd.qcut(df["r20"],4,labels=False)
    out["by_r20q"]=df.groupby("r20q").agg(r20=("r20","mean"),n=("u5","size"),u5=("u5","mean"),u10=("u10","mean"))
    out["signal_bar_move_short"]=tt(df["sig"])
    out["baseline_below_sma"]=bs.groupby("cluster")["u5"].apply(tt).unstack()
    return out
