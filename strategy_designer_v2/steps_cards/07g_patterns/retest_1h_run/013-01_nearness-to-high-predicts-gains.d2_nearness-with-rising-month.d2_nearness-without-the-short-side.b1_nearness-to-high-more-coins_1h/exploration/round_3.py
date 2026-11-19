def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=168
    out={}
    rows=[]; hrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            s=pd.Series(b["close"].astype(float).values); n=len(s)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            lr=np.log(s).diff()
            r720=s/s.shift(720)-1; r168=s/s.shift(168)-1; r24=s/s.shift(24)-1
            vol=lr.rolling(168,min_periods=120).std()
            hrs=ts.dt.hour.values
            # evening return 21->23 close: from close of hour 20 bar to close of hour 22 bar
            idx=np.where(hrs==20)[0]
            for i in idx:
                if i+2<n and hrs[i+2]==22:
                    hrows.append(dict(coin=coin,yr=ts.iloc[i].year,eve=s.iloc[i+2]/s.iloc[i]-1,r24=r24.iloc[i],vol=vol.iloc[i],r720=r720.iloc[i]))
            if n<2*H: continue
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,yr=ts.iloc[i].year,fwd=s.iloc[i+H]/s.iloc[i]-1,r720=r720.iloc[i],r168=r168.iloc[i],r24=r24.iloc[i]))
    g=pd.DataFrame(rows); g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    dn=g[g.r720<=0].dropna(subset=["ex","r720","r168"]).copy()
    def tab(d,col,q=5):
        d=d.copy(); d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        r=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean=("ex","mean"),sd=("ex","std"))
        r["t"]=r["mean"]/(r["sd"]/np.sqrt(r["n"])); return r.drop(columns="sd")
    out["dn_r720"]=tab(dn,"r720")
    out["dn_by_year"]=dn.groupby("yr")["ex"].agg(["size","mean"])
    cm=dn.groupby("coin")["ex"].mean()
    out["dn_coins_neg"]=f"{(cm<0).sum()} of {len(cm)}"
    dn["mid"]=dn.r168>dn.r168.quantile(0.2)
    out["dn_excl_deepfall"]=dn[dn.mid].groupby("yr")["ex"].mean()
    e=pd.DataFrame(hrows).dropna()
    e["exe"]=e["eve"]-e.groupby("coin")["eve"].transform("mean")
    def tab2(col):
        d=e.copy(); d["b"]=pd.qcut(d[col].rank(method="first"),5,labels=False)
        r=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("eve","size"),mean=("eve","mean"),sd=("eve","std"))
        r["t"]=r["mean"]/(r["sd"]/np.sqrt(r["n"])); return r.drop(columns="sd")
    out["eve_by_vol"]=tab2("vol"); out["eve_by_r24"]=tab2("r24")
    e["up"]=e.r720>0
    out["eve_by_regime"]=e.groupby("up")["eve"].agg(["size","mean","std"])
    tt=stats.ttest_1samp(e["eve"],0); out["eve_all_t"]=f"n={len(e)} mean={e['eve'].mean():.6f} t={tt.statistic:.2f}"
    return out
