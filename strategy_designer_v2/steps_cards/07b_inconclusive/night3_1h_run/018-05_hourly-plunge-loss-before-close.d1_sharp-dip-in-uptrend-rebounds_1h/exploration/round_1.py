def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    bars=data["bars"]
    fc="forecast"; rawc="debug_info.components.dip_in_rise.last_history_value"
    rows=[]; driftd={}; sdd={}
    for coin,ws in bars.items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        driftd[coin]=np.mean(allr); sdd[coin]=np.std(allr,ddof=1)
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; f=df[fc].fillna(0).values
            raw=df[rawc].values if rawc in df else np.full(len(c),np.nan)
            r24=pd.Series(c).pct_change(24)
            ma=r24.abs().rolling(720,min_periods=200).mean()
            fallz=(-r24/ma).values
            r720=pd.Series(c).pct_change(720).values
            ts=pd.to_datetime(df["timestamp"])
            low=0.0; seen=set()
            for t in range(len(c)):
                if f[t]<=0: low=0.0; continue
                if f[t]-low>=2:
                    low=f[t]; cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    rec=dict(coin=coin,win=w,year=ts.iloc[t].year,hour=ts.iloc[t].hour,fc=f[t],raw=raw[t],fallz=fallz[t],r720=r720[t])
                    for h in (12,24,72,168):
                        if t+h<len(c): rec[f"u{h}"]=c[t+h]/c[t]-1-driftd[coin]*h/H
                    rows.append(rec)
                else:
                    low=min(low,f[t])
    d=pd.DataFrame(rows)
    d=d[d["u72"].notna()]
    def summ(g,col="u72"):
        x=g[col].dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    out["n_cases"]=len(d)
    out["fc_quantiles"]=d["fc"].quantile([0,.1,.25,.5,.75,.9,1]).to_frame()
    out["share_fc_ge_19.99"]=float((d["fc"]>=19.99).mean())
    out["fc_value_counts_top"]=d["fc"].round(2).value_counts().head(8).to_frame()
    out["by_horizon"]=pd.DataFrame({h:summ(d,f"u{h}") for h in (12,24,72,168)}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    for col in ("raw","fallz","r720"):
        x=d[d[col].notna()].copy()
        if len(x)>50:
            x["q"]=pd.qcut(x[col].rank(method="first"),5,labels=False)
            out[f"by_{col}_quintile"]=x.groupby("q").apply(lambda g: pd.concat([summ(g),pd.Series({"med":g[col].median()})]))
    x=d.dropna(subset=["raw"])
    m=x["raw"].median(); a=x[x.raw>m]["u72"]; b=x[x.raw<=m]["u72"]
    out["raw_median_split"]=pd.Series(dict(diff=a.mean()-b.mean(),t=stats.ttest_ind(a,b,equal_var=False).statistic,na=len(a),nb=len(b)))
    return out
