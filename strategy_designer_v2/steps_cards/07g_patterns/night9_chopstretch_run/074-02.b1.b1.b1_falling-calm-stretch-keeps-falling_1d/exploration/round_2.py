def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            st=(c/sma-1)/sd
            ret5=c.shift(-5)/c-1; ret10=c.shift(-10)/c-1
            tr60=c/c.shift(60)-1
            vr=r.rolling(30).std()/r.rolling(60,min_periods=40).std()
            for i in range(0,len(b),5):
                if pd.isna(ret5.iloc[i]) or pd.isna(st.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,day=str(b["timestamp"].iloc[i])[:10],
                    yr=pd.Timestamp(b["timestamp"].iloc[i]).year,st=st.iloc[i],
                    ret5=ret5.iloc[i],ret10=ret10.iloc[i],tr60=tr60.iloc[i],vr=vr.iloc[i],
                    inprof=(b["regime"].iloc[i]=="unknown")))
    d=pd.DataFrame(rows)
    d["ab5"]=d["ret5"]-d.groupby("coin")["ret5"].transform("mean")
    d["ab10"]=d["ret10"]-d.groupby("coin")["ret10"].transform("mean")
    def summ(g,col="ab5"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<3: return pd.Series(dict(n=n,days=np.nan,mean=np.nan,t=np.nan))
        m=g[col].mean(); dd=g.groupby("day")[col].apply(lambda v:(v-m).sum()); D=len(dd)
        se=np.sqrt((dd**2).sum()*D/(D-1))/n if D>1 else np.nan
        return pd.Series(dict(n=n,days=D,mean=m,t=m/se))
    out={}
    p=d[d.inprof].copy()
    p["side"]=np.where(p.st>0,"above","below")
    p["q"]=p.groupby("side")["st"].transform(lambda s:pd.qcut(s.abs(),3,labels=False))
    out["inprof_side_tercile_ab5"]=p.groupby(["side","q"]).apply(summ)
    out["inprof_side_tercile_ab10"]=p.groupby(["side","q"]).apply(lambda g:summ(g,"ab10"))
    out["inprof_side_year_ab5"]=p.groupby(["side","yr"]).apply(summ)
    out["inprof_side_coin_ab5"]=p.groupby(["side","coin"]).apply(summ)
    a=p[p.st>0]; b_=p[p.st<0]
    out["spearman_inprof"]=pd.Series(dict(above_st_ab5=stats.spearmanr(a.st,a.ab5)[0],n_above=len(a),
        below_st_ab5=stats.spearmanr(b_.st,b_.ab5)[0],n_below=len(b_)))
    f=d[(d.tr60<-0.1)&d.vr.notna()].copy()
    f["ag"]=np.where(f.vr>1,"agit","calm"); f["side"]=np.where(f.st>0,"above","below")
    out["falling_ag_side_ab5"]=f.groupby(["ag","side"]).apply(summ)
    return out
