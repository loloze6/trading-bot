def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days=data["days"]
    out = {}
    # 1) recorded signal: forward returns at several horizons, every active bar (first bar of each episode)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df["close"].values; f=df["forecast"].fillna(0).values; n=len(cl)
            a=df["postRebalance_current_allocation"].fillna(0).values
            for t in range(1,n):
                if f[t]<0 and f[t-1]>=0:
                    r={}
                    for h in [1,3,5,10]:
                        r[f"r{h}"]=cl[t+h]/cl[t]-1 if t+h<n else np.nan
                    r["prior20"]=cl[t]/cl[t-20]-1 if t>=20 else np.nan
                    r["alloc"]=a[t]; r["fc"]=f[t]; r["coin"]=c
                    rows.append(r)
    E=pd.DataFrame(rows)
    out["episodes_fwd_mean"]=E[["r1","r3","r5","r10","alloc","fc"]].agg(["count","mean","median"])
    # 2) broad situation: close back below prior-20d high within 10 days of a breakout, graded by state
    res=[]
    for c in bars:
        grs=[]
        for w,df in bars[c].items():
            cl=df["close"].values; idx=np.arange(0,len(cl)-5,5); grs.append(cl[idx+5]/cl[idx]-1)
        g=np.concatenate(grs); drift=g.mean(); sd=g.std()
        for w,df in bars[c].items():
            hi=df["high"]; cl=df["close"].values; n=len(cl)
            ph=hi.rolling(20).max().shift(1).values
            bo=cl>ph
            ret1=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            vol20=pd.Series(ret1).rolling(20).std().values
            for i in range(0,n-5,5):
                if i<60: continue
                b=None
                for k in range(1,11):
                    if bo[i-k]: b=i-k; break
                if b is None or cl[i]>=ph[b]: continue
                res.append(dict(coin=c,depth=ph[b]/cl[i]-1,prior60=cl[i]/cl[i-60]-1,
                     runup=cl[b]/cl[b-20]-1, vol=vol20[i],
                     un=-(cl[i+5]/cl[i]-1-drift), total=-(cl[i+5]/cl[i]-1)))
    R=pd.DataFrame(res).dropna()
    out["broad_n"]=len(R)
    for col in ["prior60","runup","vol","depth"]:
        R["q"]=pd.qcut(R[col],3,labels=["low","mid","high"])
        g=R.groupby("q",observed=True).un.agg(["count","mean","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["spearman_all"]=stats.spearmanr(R[col],R.un)[0]
        out[f"broad_by_{col}"]=g
    # 3) book days in position vs coin
    D=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); D.append(d)
    D=pd.concat(D)
    out["book_daily"]=pd.Series(dict(mean_book=D.book_return.mean(),mean_coin=D.coin_return.mean(),
        share_days_nonzero=(D.book_return.abs()>1e-12).mean()))
    return out
