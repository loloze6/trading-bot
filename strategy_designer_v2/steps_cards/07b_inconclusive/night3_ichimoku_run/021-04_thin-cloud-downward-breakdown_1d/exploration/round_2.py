def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[]
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H):
                rs.append(c[i+H]/c[i]-1)
        drift=np.mean(rs); usual=np.std(rs)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; hi=b["high"].values; lo=b["low"].values
            f=b["forecast"].fillna(0).values
            H_=pd.Series(hi); L_=pd.Series(lo)
            ten=(H_.rolling(9).max()+L_.rolling(9).min())/2
            kij=(H_.rolling(26).max()+L_.rolling(26).min())/2
            sa=(ten+kij)/2
            sb=(H_.rolling(52).max()+L_.rolling(52).min())/2
            n=len(c); low=0.0; seen=set()
            for t in range(1,n):
                if f[t]>=0: low=0.0; continue
                if f[t] <= low-2:
                    low=f[t]; cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    if t+H>=n: continue
                    r26=c[t+H]/c[t]-1
                    un=-(r26-drift)
                    p52=c[t]/c[t-52]-1 if t>=52 else np.nan
                    p13=c[t]/c[t-13]-1 if t>=13 else np.nan
                    fut=(sa[t]-sb[t])/c[t] if not np.isnan(sb[t]) else np.nan
                    ma=np.mean(c[max(0,t-49):t+1]) if t>=49 else np.nan
                    rows.append(dict(coin=coin,un=un,str=un/usual,p52=p52,p13=p13,fut=fut,
                        below50=(c[t]/ma-1) if not np.isnan(ma) else np.nan,f=f[t],
                        dv=np.std(np.diff(np.log(c[max(0,t-20):t+1])))))
    d=pd.DataFrame(rows)
    def tt(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={"all":tt(d.un),"all_strength":tt(d.str)}
    for col in ["p52","p13","fut","below50","dv"]:
        s=d.dropna(subset=[col])
        q=pd.qcut(s[col].rank(method="first"),3,labels=["low","mid","high"])
        out["by_"+col]=s.groupby(q).un.apply(tt).unstack()
        out["spear_"+col]=stats.spearmanr(s[col],s.un)[0]
    s=d.dropna(subset=["fut"])
    out["fut_sign"]=s.groupby(np.sign(s.fut)).un.apply(tt).unstack()
    s=d.dropna(subset=["p52"])
    out["p52_sign"]=s.groupby(np.sign(s.p52)).un.apply(tt).unstack()
    neg=s[s.p52<0]
    out["thin_in_p52neg_spear"]=stats.spearmanr(neg.f,neg.un)[0] if len(neg)>5 else np.nan
    return out
