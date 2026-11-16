def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            lo=c.rolling(20).min(); hi=c.rolling(20).max()
            rp=(c-lo)/(hi-lo)
            rpz=(rp-rp.rolling(60,min_periods=20).mean())/rp.rolling(60,min_periods=20).std()
            r30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            fwd=c.shift(-10)/c-1
            for i in range(0,len(b),10):
                if i+10<len(b):
                    rows.append(dict(coin=coin,w=w,year=int(yr[i]),reg=b["regime"].iloc[i],
                        fc=b["forecast"].iloc[i],rp=rp[i],rpz=rpz[i],r30=r30[i],fwd=fwd[i]))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    tr=d[d.reg=="trending"].dropna(subset=["rp","ex"]).copy()
    def slope(g,x):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<10 or g[x].std()==0: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[x],g["ex"]); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    out={}
    out["rp_by_coin"]=tr.groupby("coin").apply(lambda g:slope(g,"rp"))
    out["rp_by_year"]=tr.groupby("year").apply(lambda g:slope(g,"rp"))
    out["rpz_vs_rp"]=pd.DataFrame({"rp":slope(tr,"rp"),"rpz":slope(tr,"rpz"),"fc":slope(tr.assign(fc=tr.fc.astype(float)),"fc")})
    out["fc_saturated_share"]=float((tr.fc.astype(float).abs()>=19.99).mean())
    tr["r30q"]=pd.qcut(tr["r30"].rank(method="first"),3,labels=False)
    out["rp_by_r30tercile"]=tr.groupby("r30q").apply(lambda g:pd.concat([slope(g,"rp"),pd.Series(dict(r30=g.r30.mean()))]))
    X=np.column_stack([np.ones(len(tr)),tr.rp,tr.r30.clip(lower=0)])
    beta,res,_,_=np.linalg.lstsq(X,tr.ex.values,rcond=None)
    e=tr.ex.values-X@beta; s2=e@e/(len(tr)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["multi_rp_r30pos"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","rp","r30pos"])
    out["rp_up_vs_low_t"]=pd.Series(dict(top=tr[tr.rp>=0.8].ex.mean(),low=tr[tr.rp<0.8].ex.mean(),
        t=stats.ttest_ind(tr[tr.rp>=0.8].ex,tr[tr.rp<0.8].ex,equal_var=False).statistic))
    return out
