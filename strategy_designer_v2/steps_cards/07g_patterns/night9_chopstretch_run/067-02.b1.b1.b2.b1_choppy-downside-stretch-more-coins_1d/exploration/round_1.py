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
            st=(c/sma-1)/sd
            sd5=r1.rolling(30).std()
            # agitation proxy: 30d sd vs its rolling median within window (limited)
            ret5=c.shift(-H)/c-1
            ret1=r1.shift(-1)
            past5=c/c.shift(5)-1
            past1=r1
            ts=pd.to_datetime(b["timestamp"])
            chop=(b["regime"]=="unknown")
            idx=np.arange(0,len(b),H)
            for i in idx:
                if i+H>=len(b) or np.isnan(st.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,yr=ts.iloc[i].year,wd=ts.iloc[i].weekday(),day=ts.iloc[i].normalize(),
                    st=st.iloc[i],chop=bool(chop.iloc[i]),r5=ret5.iloc[i],p5=past5.iloc[i]/ (sd.iloc[i]*np.sqrt(5)) if sd.iloc[i]>0 else np.nan,
                    p1=past1.iloc[i]/sd.iloc[i] if sd.iloc[i]>0 else np.nan,
                    vol=sd.iloc[i],fc=b["forecast"].iloc[i],alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["r5"].mean()
    usual=d.groupby("coin")["r5"].std()
    d["ex"]=d["r5"]-d["coin"].map(drift)
    d["z"]=d["ex"]/d["coin"].map(usual)
    def tday(x):
        g=x.groupby("day")["z"].sum()
        n=len(x); m=x["z"].mean()
        se=np.sqrt((g-g.count()*0+0).pow(2).sum())/n if n>1 else np.nan
        dev=x.groupby("day")["z"].apply(lambda s:(s-m).sum())
        se=np.sqrt((dev**2).sum())/n
        return pd.Series(dict(n=n,days=x["day"].nunique(),mean_z=m,mean_ex=x["ex"].mean(),t=m/se if se>0 else np.nan))
    out={}
    d["q"]=pd.qcut(d["st"],5,labels=False)
    out["stretch_quintile_by_chop"]=d.groupby(["chop","q"]).apply(tday)
    out["stretch_q_mean"]=d.groupby("q")["st"].mean()
    d["pq"]=pd.qcut(d["p5"],5,labels=False)
    out["past5_scaled_quintile_by_chop"]=d.groupby(["chop","pq"]).apply(tday)
    d["vq"]=d.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["stretch_q_by_volterc_chop"]=d[d.chop].groupby(["vq","q"]).apply(tday)[["n","mean_z","t"]]
    out["weekday"]=d.groupby("wd").apply(tday)
    out["year_low_stretch_chop"]=d[d.chop&(d.q==0)].groupby("yr").apply(tday)
    out["year_high_stretch_chop"]=d[d.chop&(d.q==4)].groupby("yr").apply(tday)
    # correlation st vs z in chop and not
    for k,g in d.groupby("chop"):
        g=g.dropna(subset=["st","z"])
        rr,p=stats.spearmanr(g["st"],g["z"]); out[f"spearman_st_z_chop{k}"]=f"{rr:.3f} p {p:.3g} n {len(g)}"
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    bk["wd"]=bk.index.weekday
    out["book_by_weekday"]=bk.groupby("wd")["book_return"].agg(["mean","count"])
    out["book_by_year"]=bk.groupby(bk.index.year)["book_return"].agg(["mean","std","count"])
    return out
