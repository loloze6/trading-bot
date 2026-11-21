def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]
    h=5
    drift={}; usual={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-h,h)
            rs+=list(cl[idx+h]/cl[idx]-1)
        drift[c]=np.mean(rs); usual[c]=np.std(rs)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            f=df["forecast"].fillna(0).values; cl=df["close"].values
            s=pd.Series(cl)
            r60=(s/s.shift(60)-1).values
            r10=(s/s.shift(10)-1).values
            ma50=(s/s.rolling(50).mean()-1).values
            vol=s.pct_change().rolling(20).std().values
            low=f[0]; bets=[]
            for i in range(len(f)):
                low=min(low,f[i])
                if f[i]>0 and f[i]-low>=2:
                    bets.append(i); low=f[i]
            seen=set()
            for i in bets:
                cell=i//5
                if cell in seen: continue
                seen.add(cell)
                if i+h>=len(cl): continue
                r=cl[i+h]/cl[i]-1
                rows.append(dict(coin=c,win=w,r60=r60[i],r10=r10[i],ma50=ma50[i],vol=vol[i],
                                 un=r-drift[c],big=(r-drift[c])>0.10,small=abs(r-drift[c])))
    d=pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g),mean=g.un.mean(),t=g.un.mean()/(g.un.std()/np.sqrt(len(g))),median=g.un.median(),hit=(g.un>0).mean()))
    out={}
    for col in ["r60","ma50","vol","r10"]:
        dd=d.dropna(subset=[col]).copy()
        dd["q"]=pd.qcut(dd[col].rank(method="first"),3,labels=False)
        out["by_"+col]=dd.groupby("q").apply(agg)
        out[col+"_qmeans"]=dd.groupby("q")[col].mean()
    dd=d.dropna(subset=["r60"]).copy()
    out["r60_sign"]=dd.groupby(dd.r60>0).apply(agg)
    out["share_from_top5pct"]=pd.Series(dict(sum_all=d.un.sum(),sum_top5=d.un[d.un>=d.un.quantile(.95)].sum(),skew=d.un.skew()))
    return out
