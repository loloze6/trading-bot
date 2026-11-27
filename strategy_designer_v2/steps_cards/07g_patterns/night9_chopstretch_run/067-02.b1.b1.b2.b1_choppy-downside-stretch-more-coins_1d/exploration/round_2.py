def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sma=c.rolling(20).mean()
            sd=r1.rolling(20).std()
            sd30=r1.rolling(30).std()
            st=(c/sma-1)/sd
            ret5=c.shift(-H)/c-1
            ret10=c.shift(-10)/c-1
            tr60=c/c.shift(60)-1
            tr40=c/c.shift(40)-1
            ts=pd.to_datetime(b["timestamp"])
            chop=(b["regime"]=="unknown")
            for i in range(0,len(b),H):
                if i+H>=len(b) or np.isnan(st.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,yr=ts.iloc[i].year,day=ts.iloc[i].normalize(),
                    st=st.iloc[i],chop=bool(chop.iloc[i]),r5=ret5.iloc[i],r10=ret10.iloc[i] if i+10<len(b) else np.nan,
                    tr60=tr60.iloc[i],tr40=tr40.iloc[i],sd30=sd30.iloc[i]))
    d=pd.DataFrame(rows)
    for col in ["r5","r10"]:
        dr=d.groupby("coin")[col].mean(); us=d.groupby("coin")[col].std()
        d["z"+col]=(d[col]-d["coin"].map(dr))/d["coin"].map(us)
    d["agit"]=d["sd30"]>d.groupby("coin")["sd30"].transform("median")
    tr=d["tr60"].fillna(d["tr40"])
    d["trend"]=np.where(d.chop,"choppy",np.where(tr>0,"rising",np.where(tr<0,"falling","na")))
    d["q"]=pd.qcut(d["st"],5,labels=False)
    def tday(x,col="zr5"):
        x=x.dropna(subset=[col]); n=len(x)
        if n<3: return pd.Series(dict(n=n,days=np.nan,mean_z=np.nan,t=np.nan))
        m=x[col].mean()
        dev=x.groupby("day")[col].apply(lambda s:(s-m).sum())
        se=np.sqrt((dev**2).sum())/n
        return pd.Series(dict(n=n,days=x["day"].nunique(),mean_z=m,t=m/se))
    def slope(x,col="zr5"):
        x=x.dropna(subset=["st",col])
        if len(x)<20: return pd.Series(dict(n=len(x),rho=np.nan,p=np.nan))
        r,p=stats.spearmanr(x["st"],x[col]); return pd.Series(dict(n=len(x),rho=r,p=p))
    out={}
    out["trend_q"]=d.groupby(["trend","q"]).apply(tday)
    out["slope_by_trend"]=d.groupby("trend").apply(slope)
    out["slope_by_trend_agit"]=d.groupby(["trend","agit"]).apply(slope)
    out["slope_by_trend_10d"]=d.groupby("trend").apply(lambda x:slope(x,"zr10"))
    out["trend_q_10d"]=d.groupby(["trend","q"]).apply(lambda x:tday(x,"zr10"))
    nc=d[~d.chop]
    out["nonchop_slope_by_year"]=nc.groupby("yr").apply(slope)
    out["nonchop_slope_by_coin"]=nc.groupby("coin").apply(slope)
    # signed stretch times outcome, day-pooled t, non-chop
    nc=nc.dropna(subset=["zr5"]).copy()
    nc["s"]=np.sign(nc["st"])*nc["zr5"]
    m=nc["s"].mean(); dev=nc.groupby("day")["s"].apply(lambda s:(s-m).sum())
    out["nonchop_signed_follow_t"]=f"mean {m:.4f} t {m/(np.sqrt((dev**2).sum())/len(nc)):.2f} n {len(nc)} days {nc.day.nunique()}"
    return out
