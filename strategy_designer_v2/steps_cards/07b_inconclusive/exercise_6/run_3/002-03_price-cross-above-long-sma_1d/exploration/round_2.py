import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    blk=[]; rows=[]
    for coin, ws in bars.items():
        rets=[]
        for w, df in ws.items():
            c=df["close"].values; rets.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(rets))
        for w, df in ws.items():
            c=df["close"].values; f=df["forecast"].values; a=df["postRebalance_current_allocation"].values
            n=len(c)
            # days since forecast turned positive
            age=np.zeros(n); k=0
            for i in range(n):
                k = k+1 if f[i]>0 else 0; age[i]=k
            for s in range(0,n,20):
                v=[];vf=[]
                for i in range(s,min(s+20,n)):
                    if i+20<n:
                        e=c[i+20]/c[i]-1-20*mu; v.append(a[i]*e); vf.append(f[i]/10*e)
                if v: blk.append((coin,w,sum(v),sum(vf)))
            for i in range(0,n-20,20):
                rows.append((coin,w,f[i],age[i],a[i],c[i+20]/c[i]-1-20*mu))
    B=pd.DataFrame(blk,columns=["coin","w","s","sf"])
    R=pd.DataFrame(rows,columns=["coin","w","f","age","a","ex"])
    out={}
    s=B["s"].sort_values(ascending=False)
    out["block_dist"]=pd.Series({"mean":s.mean(),"median":s.median(),"skew":stats.skew(s),
        "sum_top10":s.head(10).sum(),"sum_all":s.sum(),"mean_wo_top10":s.iloc[10:].mean(),
        "t_wo_top10":s.iloc[10:].mean()/(s.iloc[10:].std()/np.sqrt(len(s)-10)),
        "t_forecast_weighted":B.sf.mean()/(B.sf.std()/np.sqrt(len(B))), "mean_fw":B.sf.mean()})
    A=R[R.f>0].copy()
    A["ageb"]=pd.cut(A.age,[0,20,60,120,10000],labels=["1-20","21-60","61-120",">120"])
    def tt(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"median":x.median(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"hit":(x>0).mean()})
    out["active_by_age"]=A.groupby("ageb")["ex"].apply(tt).unstack()
    out["active_quantiles"]=A["ex"].quantile([.05,.25,.5,.75,.95]).to_frame()
    # by window: block mean per window, count positive
    W=B.groupby("w")["s"].mean()
    out["windows"]=pd.Series({"n_w":len(W),"pos_w":(W>0).sum(),"t_w":W.mean()/(W.std()/np.sqrt(len(W)))})
    return out
