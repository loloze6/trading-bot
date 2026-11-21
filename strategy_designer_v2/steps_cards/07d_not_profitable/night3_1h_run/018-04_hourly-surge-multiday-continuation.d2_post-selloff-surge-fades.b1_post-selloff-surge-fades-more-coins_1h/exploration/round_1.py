def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=120
    rows=[]
    drift={}
    usual={}
    for coin,ws in data["bars"].items():
        fr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            fr+=list(c[idx+H]/c[idx]-1)
        fr=np.array(fr); drift[coin]=fr.mean() if len(fr) else 0; usual[coin]=fr.std() if len(fr)>1 else np.nan
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            r24=c/c.shift(24)-1
            mabs=r24.abs().rolling(720,min_periods=200).mean()
            surge=r24/mabs
            r1=c.pct_change()
            vol=r1.rolling(720,min_periods=200).std()*np.sqrt(168)
            pw=(c.shift(24)/c.shift(192)-1)/vol
            fwd=c.shift(-H)/c-1
            n=len(c)
            for start in range(0,n-H,H):
                seg=slice(start,start+H)
                s=surge.iloc[seg]
                if s.isna().all(): continue
                k=s.idxmax()
                rows.append(dict(coin=coin,win=w,surge=s.max(),pw=pw.iloc[k],
                    fwd=fwd.iloc[k]-drift[coin],std=(fwd.iloc[k]-drift[coin])/usual[coin],
                    alloc=b["postRebalance_current_allocation"].iloc[k],year=pd.Timestamp(b["timestamp"].iloc[k]).year))
    d=pd.DataFrame(rows).dropna(subset=["fwd","surge","pw"])
    d["sb"]=pd.cut(d.surge,[-99,0,1,2,3,4,6,99])
    def agg(g):
        return pd.Series(dict(n=len(g),mean=g.fwd.mean(),t=g.fwd.mean()/(g.fwd.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,strength=g["std"].mean()))
    out={}
    out["by_surge_max_in_cell"]=d.groupby("sb").apply(agg)
    hi=d[d.surge>=3]
    hi=hi.assign(pwb=pd.cut(hi.pw,[-99,-2,-1,0,1,2,99]))
    out["surge3_by_priorweek"]=hi.groupby("pwb").apply(agg)
    out["surge3_by_year"]=hi.groupby("year").apply(agg)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            x=t[["book_return","coin_return"]].copy(); x["win"]=w; x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd).dropna()
    out["book_by_window"]=dd.groupby("win").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr=pd.concat(tr)
    out["trades"]=pd.Series(dict(n=len(tr),mean_gross=tr.profit_loss_percent.mean(),mean_net=tr.net_profit_loss_percent.mean(),win=(tr.net_profit_loss_percent>0).mean(),dur_h=tr.duration_minutes.mean()/60))
    return out
