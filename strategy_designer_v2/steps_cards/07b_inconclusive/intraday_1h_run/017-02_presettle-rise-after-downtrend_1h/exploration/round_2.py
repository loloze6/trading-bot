def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        g={2:[],8:[],24:[]}
        for w,df in ws.items():
            c=df["close"].values.astype(float)
            for h in g:
                idx=np.arange(0,len(c)-h,h); g[h].append(c[idx+h]/c[idx]-1)
        m={h:np.nanmean(np.concatenate(v)) for h,v in g.items()}
        for w,df in ws.items():
            d=pd.DataFrame({"ts":pd.to_datetime(df["timestamp"]),"c":df["close"].astype(float)})
            for h in (2,8,24):
                d[f"r{h}"]=d.c.shift(-h)/d.c-1-m[h]
            d["fall"]=d.c/d.c.shift(72)-1
            vol=np.log(d.c).diff().rolling(72,min_periods=40).std()*np.sqrt(72)
            d["fz"]=d.fall/vol
            d["hour"]=d.ts.dt.hour; d["coin"]=coin; d["win"]=w; d["year"]=d.ts.dt.year
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r2","fall","fz"])
    D["q"]=D.groupby("coin").fall.transform(lambda s:pd.qcut(s,10,labels=False))
    def tm(s): s=s.dropna(); return s.mean()/(s.std()/np.sqrt(len(s)))
    out={}
    # all bars, unconditional mean 2h excess by hour (time-of-day seasonality)
    out["all bars 2h excess by hour"]=D.groupby("hour").r2.agg(n="size",mean_bp=lambda s:s.mean()*1e4,t=tm)
    # deepest decile, 2h excess by hour
    deep=D[D.q==0]
    out["deepest 3d-fall decile 2h by hour"]=deep.groupby("hour").r2.agg(n="size",mean_bp=lambda s:s.mean()*1e4,t=tm)
    # settlement vs other hours, deepest decile, diff
    S=deep[deep.hour.isin([5,13,21])].r2; O=deep[~deep.hour.isin([5,13,21])].r2
    out["deep decile settle minus other (bp,t)"]=pd.Series({"settle_bp":S.mean()*1e4,"other_bp":O.mean()*1e4,"diff_t":stats.ttest_ind(S,O,equal_var=False).statistic})
    # longer horizons after deep fall, non-overlapping: hour 5,13,21 bars only, deciles
    C=D[D.hour.isin([5,13,21])]
    out["settle bars by fall decile, 2h/8h/24h"]=C.groupby("q").agg(n=("r2","size"),fall=("fall","mean"),r2_bp=("r2",lambda s:s.mean()*1e4),t2=("r2",tm),r8_bp=("r8",lambda s:s.mean()*1e4),t8=("r8",tm))
    # 24h on non-overlapping grid (hour 5 only, one per day), by decile
    G=D[D.hour==5]
    out["daily grid (hour5) 24h excess by fall decile"]=G.groupby("q").agg(n=("r24","size"),r24_bp=("r24",lambda s:s.mean()*1e4),t=("r24",tm))
    # deepest decile settlement cases by coin, year
    dS=deep[deep.hour.isin([5,13,21])]
    out["deep settle by coin"]=dS.groupby("coin").r2.agg(n="size",mean_bp=lambda s:s.mean()*1e4,t=tm)
    out["deep settle by year"]=dS.groupby("year").r2.agg(n="size",mean_bp=lambda s:s.mean()*1e4,t=tm)
    # slope on raw fall in falls
    F=C[C.fall<0]
    sl=stats.linregress(-F.fall,F.r2); out["settle slope on raw fall size (bp per 1.0, t, n)"]=pd.Series({"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr,"n":len(F)})
    sl=stats.linregress(-D[D.fall<0].fall,D[D.fall<0].r2); out["all hours slope on raw fall size"]=pd.Series({"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr,"n":(D.fall<0).sum()})
    return out
