def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            st=(c/sma-1)/sd
            sd5=r.rolling(5).std(); sdlong=r.rolling(60,min_periods=40).std()
            tr60=c/c.shift(60)-1
            ret5=c.shift(-5)/c-1
            ret10=c.shift(-10)/c-1
            r1=r
            for i in range(0,len(b),5):
                if pd.isna(ret5.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,i=i,day=str(b["timestamp"].iloc[i])[:10],
                    st=st.iloc[i],ret5=ret5.iloc[i],ret10=ret10.iloc[i],r1=r1.iloc[i],
                    volratio=(r.rolling(30).std().iloc[i]/sdlong.iloc[i]) if sdlong.iloc[i]>0 else np.nan,
                    tr60=tr60.iloc[i],inprof=(b["regime"].iloc[i]=="unknown"),
                    wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                    yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["ret5"].transform("mean")
    d["ab5"]=d["ret5"]-drift
    d["ab10"]=d["ret10"]-d.groupby("coin")["ret10"].transform("mean")
    def summ(g,col="ab5"):
        x=g[col].dropna()
        n=len(x); m=x.mean()
        # day-clustered t
        dd=g.dropna(subset=[col]).groupby("day")[col].sum()
        D=len(dd); se=np.sqrt((dd**2).sum())/n*np.sqrt(D/(D-1)) if D>1 else np.nan
        dd2=g.dropna(subset=[col]).groupby("day")[col].apply(lambda v:(v-m).sum())
        se=np.sqrt((dd2**2).sum()*D/(D-1))/n if D>1 else np.nan
        return pd.Series(dict(n=n,days=D,mean=m,t=m/se if se else np.nan))
    out={}
    d["stq"]=pd.qcut(d["st"],5,labels=False)
    out["stretch_quintile_all_ab5"]=d.dropna(subset=["st"]).groupby("stq").apply(summ)
    d["agit"]=np.where(d["volratio"]>1,"agit","calm")
    d["trend"]=np.where(d["tr60"]>0.1,"rising",np.where(d["tr60"]<-0.1,"falling",np.where(d["tr60"].notna(),"choppy","na")))
    out["stq_by_agit_ab5"]=d.dropna(subset=["st","volratio"]).groupby(["agit","stq"]).apply(summ)
    out["stq_by_trend_ab5"]=d.dropna(subset=["st"]).query("trend!='na'").groupby(["trend","stq"]).apply(summ)
    out["inprof_stq_ab5"]=d.dropna(subset=["st"]).groupby(["inprof","stq"]).apply(summ)
    d["r1q"]=pd.qcut(d["r1"],5,labels=False)
    out["r1_quintile_ab5"]=d.dropna(subset=["r1"]).groupby("r1q").apply(summ)
    out["weekday_ab5"]=d.groupby("wd").apply(summ)
    out["year_ab5"]=d.groupby("yr").apply(summ)
    # correlations
    x=d.dropna(subset=["st","ab5"])
    out["spearman_st_ab5"]=pd.Series(dict(all=stats.spearmanr(x.st,x.ab5)[0],
        agit=stats.spearmanr(x[x.agit=="agit"].st,x[x.agit=="agit"].ab5)[0],
        calm=stats.spearmanr(x[x.agit=="calm"].st,x[x.agit=="calm"].ab5)[0]))
    return out
