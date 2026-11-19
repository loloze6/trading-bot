def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[];hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"hour":ts.dt.hour.values,"year":ts.dt.year.values,"r":np.r_[c[1:]/c[:-1]-1,np.nan],"coin":coin,"w":w}))
            n=len(c)
            for t in range(H,n-H,H):
                rr=r[t-H+1:t+1]; lr=np.log1p(rr); net=lr.sum()
                eff=net/np.abs(lr).sum()
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,past=c[t]/c[t-H]-1,fwd=c[t+H]/c[t]-1,seff=eff,vol=np.nanstd(rr)))
    d=pd.DataFrame(rows).dropna()
    out={}
    f=lambda x: pd.Series({"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"n":len(x)})
    d["sq"]=d.groupby("coin")["seff"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["fwd by signed eff quintile"]=d.groupby("sq")["fwd"].apply(f).unstack()
    # eff vs past in regression, per coin standardised
    d["z_eff"]=d.groupby("coin")["seff"].transform(lambda x:(x-x.mean())/x.std())
    d["z_past"]=d.groupby("coin")["past"].transform(lambda x:(x-x.mean())/x.std())
    d["z_absp"]=d.groupby("coin")["past"].transform(lambda x:(x.abs()-x.abs().mean())/x.abs().std())
    X=np.c_[np.ones(len(d)),d.z_eff,d.z_past,d.z_absp]; y=d.fwd.values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-4))
    out["reg fwd ~ eff+past+|past|"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","eff","past","abspast"])
    # per coin: top minus bottom eff quintile
    pc=[]
    for coin,g in d.groupby("coin"):
        a=g[g.sq==4].fwd;bb=g[g.sq==0].fwd
        pc.append([coin,a.mean()-bb.mean(),stats.ttest_ind(a,bb,equal_var=False).statistic,len(a)])
    out["eff top-bottom per coin"]=pd.DataFrame(pc,columns=["coin","diff","t","n"])
    py=[]
    for yr,g in d.groupby("year"):
        a=g[g.sq==4].fwd;bb=g[g.sq==0].fwd
        py.append([yr,a.mean()-bb.mean(),stats.ttest_ind(a,bb,equal_var=False).statistic,len(a)])
    out["eff top-bottom per year"]=pd.DataFrame(py,columns=["year","diff","t","n"])
    # |past| extremes: both tails within up and down
    d["aq"]=d.groupby("coin")["z_absp"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["fwd by sign x |past| tercile"]=d.groupby([np.sign(d.past),"aq"])["fwd"].apply(f).unstack()
    # hour 20-21 consistency, cross-coin averaged per hour bar
    h=pd.concat(hr).dropna()
    h["h2021"]=h.hour.isin([20,21])
    out["h20-21 minus other per coin"]=h.groupby("coin").apply(lambda g: pd.Series({"diff":g[g.h2021].r.mean()-g[~g.h2021].r.mean(),"t":stats.ttest_ind(g[g.h2021].r,g[~g.h2021].r,equal_var=False).statistic}))
    out["h20-21 minus other per year"]=h.groupby("year").apply(lambda g: pd.Series({"diff":g[g.h2021].r.mean()-g[~g.h2021].r.mean(),"t":stats.ttest_ind(g[g.h2021].r,g[~g.h2021].r,equal_var=False).statistic,"n":g.h2021.sum()}))
    # book: market part vs timing
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd)
    out["book mean, coin mean"]=pd.Series({"book":D.book_return.mean(),"coin":D.coin_return.mean(),"corr":D[["book_return","coin_return"]].corr().iloc[0,1]})
    return out
