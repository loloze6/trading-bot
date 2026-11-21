def explore(data):
    import numpy as np, pandas as pd
    H=120
    rows=[]
    out={}
    for coin,ws in data["bars"].items():
        fr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            if len(idx): fr+=list(c[idx+H]/c[idx]-1)
        fr=np.array(fr)
        if len(fr)<5: continue
        dr=fr.mean(); us=fr.std()
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            v=b["volume"].astype(float).reset_index(drop=True)
            r24=c/c.shift(24)-1
            mabs=r24.abs().rolling(720,min_periods=200).mean()
            surge=r24/mabs
            r1=c.pct_change()
            vol=r1.rolling(720,min_periods=200).std()*np.sqrt(168)
            pw=(c.shift(24)/c.shift(192)-1)/vol
            m30=(c/c.shift(720)-1)/(r1.rolling(720,min_periods=200).std()*np.sqrt(720))
            vr=v.rolling(24).sum()/v.rolling(720,min_periods=200).mean()/24
            f={h:c.shift(-h)/c-1 for h in (24,72,120,240)}
            alloc=b["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            n=len(c)
            for start in range(0,n-H,H):
                s=surge.iloc[start:start+H]
                hit=s[s>=3]
                if len(hit)==0: continue
                k=hit.index[0]
                rows.append(dict(coin=coin,win=w,surge=surge.iloc[k],pw=pw.iloc[k],m30=m30.iloc[k],vr=vr.iloc[k],
                    f24=f[24].iloc[k],f72=f[72].iloc[k],f120=f[120].iloc[k]-dr,f120raw=f[120].iloc[k],f240=f[240].iloc[k],
                    st=(f[120].iloc[k]-dr)/us,alloc=alloc.iloc[k],dr=dr,year=pd.Timestamp(b["timestamp"].iloc[k]).year))
    d=pd.DataFrame(rows).dropna(subset=["f120","pw"])
    def agg(g,col="f120"):
        x=g[col].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,strength=g.st.mean()))
    out["all_first_surge3"]=agg(d)
    out["by_priorweek"]=d.groupby(pd.cut(d.pw,[-99,-2,-1,0,1,2,99])).apply(agg)
    out["by_surge_size"]=d.groupby(pd.cut(d.surge,[3,4,5,7,99])).apply(agg)
    out["by_30d_trend"]=d.groupby(pd.cut(d.m30,[-99,-1,-0.3,0,0.3,1,99])).apply(agg)
    out["by_volume_ratio"]=d.groupby(pd.qcut(d.vr,4)).apply(agg)
    neg=d[d.pw<0]
    out["fall_cases_horizons_raw"]=pd.DataFrame({h:agg(neg,h) for h in ["f24","f72","f120raw","f240"]})
    out["fall_cases_by_30d_trend"]=neg.groupby(pd.cut(neg.m30,[-99,-1,-0.3,0,0.3,1,99])).apply(agg)
    out["fall_cases_by_year"]=neg.groupby("year").apply(agg)
    # book: drift vs timing
    dd=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).values
            a=b["postRebalance_current_allocation"].astype(float).values
            g=a[:-1]*(c[1:]/c[:-1]-1)
            dd.append(pd.DataFrame(dict(g=g,a=a[:-1],r=c[1:]/c[:-1]-1,coin=coin)))
    dd=pd.concat(dd)
    mr=dd.groupby("coin").r.mean()
    dd["drift_part"]=dd.a*dd.coin.map(mr)
    out["book_hourly_parts_bps"]=pd.Series(dict(total=dd.g.mean()*1e4,from_drift=dd.drift_part.mean()*1e4,timing=(dd.g-dd.drift_part).mean()*1e4,share_short=(dd.a<0).mean(),mean_abs_alloc_when_in=dd.a[dd.a!=0].abs().mean()))
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades_pl_quantiles"]=tr.net_profit_loss_percent.quantile([.05,.25,.5,.75,.95])
    return out
