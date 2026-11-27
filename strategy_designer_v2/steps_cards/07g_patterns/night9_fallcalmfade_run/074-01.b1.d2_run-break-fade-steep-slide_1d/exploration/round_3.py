def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float)
            r=c.pct_change(); nxt=c.shift(-1)/c-1; nxt2=c.shift(-2)/c-1
            n=len(d)
            tr60=c/c.shift(60)-1
            sd30=r.shift(1).rolling(30).std()
            up=(r>0).astype(int).values
            urun=np.zeros(n); ugain=np.zeros(n)
            for i in range(1,n):
                if up[i]:
                    urun[i]=urun[i-1]+1; ugain[i]=ugain[i-1]+np.log1p(r.iloc[i])
                else:
                    urun[i]=0; ugain[i]=0
            ts=pd.to_datetime(d["timestamp"])
            x=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"year":ts.dt.year,
                "r":r,"nxt":nxt,"nxt2":nxt2,"tr60":tr60,"sd30":sd30,
                "prev_urun":pd.Series(urun).shift(1).values,"prev_ugain":pd.Series(ugain).shift(1).values})
            rows.append(x)
    X=pd.concat(rows,ignore_index=True).dropna(subset=["nxt","r","tr60","sd30"])
    X["cmean"]=X.groupby("coin")["nxt"].transform("mean")
    X["ex"]=X["nxt"]-X["cmean"]
    X["cmean2"]=X.groupby("coin")["nxt2"].transform("mean")
    X["ex2"]=X["nxt2"]-X["cmean2"]
    X["trend"]=np.where(X.tr60>0.10,"rising",np.where(X.tr60<-0.10,"falling","choppy"))
    X["agit"]=np.where(X.sd30>X.groupby("coin")["sd30"].transform("median"),"agit","calm")
    X["gz"]=X.prev_ugain/X.sd30
    def ct(s,days):
        g=s.groupby(days).sum(); G=len(g)
        if G<3: return np.nan
        se=np.sqrt((g**2).sum()*G/(G-1))/len(s)
        return s.mean()/se if se>0 else np.nan
    def summ(gb,col="ex"):
        out={}
        for k,sub in gb:
            sub=sub.dropna(subset=[col])
            out[k]={"n":len(sub),"mean%":100*sub[col].mean(),"t_day":ct(sub[col],sub["day"]),"days":sub["day"].nunique()}
        return pd.DataFrame(out).T
    res={}
    D=X[(X.r<0)&(X.prev_urun>=2)].copy()
    D["nf"]=np.where(D.trend=="rising","rising","notrising")
    D["gzb"]=pd.cut(D.gz,[0,1.5,2.5,4,99])
    res["downbreak_by_nf_gz"]=summ(D.groupby(["nf","gzb"],observed=True))
    res["downbreak_by_nf_gz_2day"]=summ(D.groupby(["nf","gzb"],observed=True),"ex2")
    res["downbreak_by_trend_agit"]=summ(D.groupby(["trend","agit"]))
    res["downbreak_notrising_by_year"]=summ(D[D.nf=="notrising"].groupby("year"))
    NR=D[D.nf=="notrising"].dropna(subset=["ex"])
    sl=stats.linregress(NR.gz.clip(upper=8),NR.ex/NR.sd30)
    res["notrising_slope_exz_on_gz"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(NR)})
    RR=D[D.nf=="rising"].dropna(subset=["ex"])
    s2=stats.linregress(RR.gz.clip(upper=8),RR.ex/RR.sd30)
    res["rising_slope_exz_on_gz"]=pd.Series({"slope":s2.slope,"t":s2.slope/s2.stderr,"n":len(RR)})
    return res
