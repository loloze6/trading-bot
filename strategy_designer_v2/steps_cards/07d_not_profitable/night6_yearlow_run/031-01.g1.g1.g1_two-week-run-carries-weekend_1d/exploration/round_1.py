def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    # book daily returns: mean across coins per (window, day)
    rows=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D=pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    B=D.groupby(["wn","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index().dropna().sort_values(["wn","day"])
    v=(1+B["br"]).cumprod(); dd=v/v.cummax()-1
    B["dd"]=dd.values
    out["deepest_dd"]=float(dd.min())
    # drawdown episodes: by window, min dd reached and book sum
    B["year"]=pd.to_datetime(B["day"]).dt.year
    B["wd"]=pd.to_datetime(B["day"]).dt.weekday
    out["book_by_year"]=B.groupby("year").agg(mean_br=("br","mean"),sum_br=("br","sum"),min_dd=("dd","min"),n=("br","size"))
    out["book_by_weekday"]=B.groupby("wd").agg(mean_br=("br","mean"),std=("br","std"),n=("br","size"))
    # cases
    cs=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            ts=pd.to_datetime(b["timestamp"])
            r1=pd.Series(cl).pct_change()
            vol20=r1.rolling(20).std()
            r14=pd.Series(cl).pct_change(14)
            lo365=pd.Series(b["low"].values).rolling(365,min_periods=60).min()
            hi=pd.Series(b["high"].values).rolling(365,min_periods=60).max()
            r60=pd.Series(cl).pct_change(60)
            for i in range(len(b)-2):
                if b["regime"].iat[i]!="trending": continue
                f=b["forecast"].iat[i]
                if not np.isfinite(f) or f==0: continue
                cs.append(dict(coin=c,w=w,day=ts.iat[i].normalize(),f=f,ret2=cl[i+2]/cl[i]-1,
                  ret1=cl[i+1]/cl[i]-1, alloc=b["postRebalance_current_allocation"].iat[i],
                  vol=vol20.iat[i],r14=r14.iat[i],r60=r60.iat[i],
                  pos=(cl[i]-lo365.iat[i])/(hi.iat[i]-lo365.iat[i]) if np.isfinite(lo365.iat[i]) else np.nan,
                  wkd=ts.iat[i].weekday()))
    C=pd.DataFrame(cs)
    C["sg"]=np.sign(C["f"]); C["dirret"]=C["sg"]*C["ret2"]; C["pnl"]=C["alloc"]*C["ret2"]
    C["year"]=C["day"].dt.year
    out["case_weekday"]=C["wkd"].value_counts()
    def g(x): return pd.Series(dict(n=len(x),dirret=x["dirret"].mean(),t=x["dirret"].mean()/(x["dirret"].std()/np.sqrt(len(x))),pnl=x["pnl"].mean(),absalloc=x["alloc"].abs().mean()))
    out["by_side"]=C.groupby("sg").apply(g)
    C["fq"]=pd.qcut(C["f"].abs(),5,labels=False)
    out["by_absf_q"]=C.groupby("fq").apply(g)
    C["vq"]=C.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["by_volq"]=C.groupby("vq").apply(g)
    out["by_year_side"]=C.groupby(["year","sg"]).apply(g)
    C["r60s"]=np.sign(C["r60"])==C["sg"]
    out["by_r60_agree"]=C.groupby("r60s").apply(g)
    C["posq"]=pd.cut(C["pos"],[-.01,.2,.5,.8,1.01])
    out["by_pos_side"]=C.groupby(["posq","sg"]).apply(g)
    # positions held on which weekdays
    hold=[]
    for c in bars:
        for w,b in bars[c].items():
            ts=pd.to_datetime(b["timestamp"])
            hold.append(pd.DataFrame({"wd":ts.dt.weekday,"inpos":b["postRebalance_current_allocation"].abs()>1e-9}))
    H=pd.concat(hold)
    out["inpos_by_weekday"]=H.groupby("wd")["inpos"].mean()
    return out
