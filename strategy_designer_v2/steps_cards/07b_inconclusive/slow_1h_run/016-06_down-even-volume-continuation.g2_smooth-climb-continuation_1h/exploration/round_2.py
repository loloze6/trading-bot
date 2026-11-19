import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].astype(float).values
            n=len(c)
            ts=pd.to_datetime(df["timestamp"])
            ad=np.abs(np.diff(c,prepend=np.nan))
            s=pd.Series(ad).rolling(72).sum().values
            past=np.full(n,np.nan); past[72:]=c[72:]/c[:-72]-1
            net=np.full(n,np.nan); net[72:]=c[72:]-c[:-72]
            er=np.abs(net)/s
            fc=df["debug_info.components.er72.post_pipeline_value"].values
            pos=df["postRebalance_current_allocation"].values
            for i in range(0,n-72,72):
                rows.append(dict(coin=coin,w=w,year=ts.iloc[i].year,past=past[i],er=er[i],fc=fc[i],pos=pos[i],
                                 fwd=c[i+72]/c[i]-1))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    u=d[d.past>0].dropna(subset=["er","ex"]).copy()
    out={}
    g=u.dropna(subset=["fc"])
    out["corr raw er vs forecast"]=pd.Series(dict(pearson=np.corrcoef(g.er,g.fc)[0,1],spearman=stats.spearmanr(g.er,g.fc)[0],n=len(g)))
    X=np.column_stack([np.ones(len(g)),g.er,g.fc]); b=np.linalg.lstsq(X,g.ex,rcond=None)[0]
    e=g.ex-X@b; se=np.sqrt(np.diag(np.sum(e**2)/(len(g)-3)*np.linalg.inv(X.T@X)))
    out["multi er + forecast"]=pd.DataFrame(dict(b=b,t=b/se),index=["c","er","fc"])
    u["top"]=u.er>=u.er.quantile(0.8)
    def tt(x):
        a=x[x.top].ex; bb=x[~x.top].ex
        r=stats.ttest_ind(a,bb,equal_var=False)
        return pd.Series(dict(n_top=len(a),top=a.mean(),rest=bb.mean(),diff=a.mean()-bb.mean(),t=r.statistic))
    out["top quintile er vs rest, all"]=tt(u)
    out["top quintile by coin"]=u.groupby("coin").apply(tt)
    out["top quintile by year"]=u.groupby("year").apply(tt)
    # ER quintile within forecast quintiles: is forecast carrying raw er?
    g=g.copy(); g["fq"]=pd.qcut(g.fc,5,labels=False,duplicates="drop")
    out["ex by forecast quintile"]=g.groupby("fq").agg(n=("ex","size"),ex=("ex","mean"),er=("er","mean"))
    # mean ex for all up bars vs coin mean
    out["up bars mean ex"]=pd.Series(dict(n=len(u),mean=u.ex.mean(),t=u.ex.mean()/(u.ex.std()/np.sqrt(len(u)))))
    return out
