def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    out={}
    cases=[]; drift={}
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): g.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=pd.Series(b["close"].values); f=b["forecast"].values
            r1=c.pct_change(); sd=r1.rolling(20).std()
            r30=c/c.shift(30)-1; r10=c/c.shift(10)-1
            hi=c.rolling(60,min_periods=30).max(); dd60=c/hi-1
            for s in range(0,len(b),H):
                for i in range(s,min(s+H,len(b))):
                    if abs(f[i])>=2:
                        if i+H<len(b):
                            ret=c[i+H]/c[i]-1
                            cases.append(dict(coin=coin,side=np.sign(f[i]),f=abs(f[i]),
                              ex=ret-drift[coin],z=r1.iloc[i]/sd.iloc[i],r30=r30.iloc[i]/(sd.iloc[i]*np.sqrt(30)),
                              r10=r10.iloc[i]/(sd.iloc[i]*np.sqrt(10)),dd=dd60.iloc[i],vol=sd.iloc[i]))
                        break
    d=pd.DataFrame(cases)
    d["sx"]=d.side*d.ex
    def agg(x):
        return pd.Series(dict(n=len(x),mean_sx=x.sx.mean(),t=x.sx.mean()/x.sx.std()*np.sqrt(len(x))))
    for col in ["r30","r10","dd","vol","z"]:
        dd=d.dropna(subset=[col]).copy()
        dd["q"]=dd.groupby("side")[col].transform(lambda x:pd.qcut(x.rank(method="first"),4,labels=False))
        out["sx_by_side_"+col+"_q"]=dd.groupby(["side","q"]).apply(agg)
        out["mean_"+col+"_by_side_q"]=dd.groupby(["side","q"])[col].mean().unstack()
    # book falls: daily book, drawdown episodes, position held
    rows=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            y=x[["day","book_return","coin_return"]].copy(); y["coin"]=coin; y["win"]=w; rows.append(y)
    D=pd.concat(rows)
    al=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            y=pd.DataFrame(dict(day=pd.to_datetime(b["timestamp"]).dt.floor("D"),a=b["postRebalance_current_allocation"].values))
            y["coin"]=coin; y["win"]=w; al.append(y)
    A=pd.concat(al)
    D["day"]=pd.to_datetime(D["day"])
    D=D.merge(A,on=["coin","win","day"],how="left")
    D["prev_a"]=D.groupby(["coin","win"]).a.shift(1)
    D["pos"]=np.sign(D.prev_a)
    D["cbin"]=pd.cut(D.coin_return,[-1,-0.05,-0.02,0,0.02,0.05,5])
    out["book_ret_by_pos_coinmove"]=D.pivot_table(index="cbin",columns="pos",values="book_return",aggfunc=["mean","size"])
    B=D.groupby(["win","day"]).book_return.mean().reset_index()
    worst=B.nsmallest(30,"book_return")
    W=D.merge(worst[["win","day"]],on=["win","day"])
    out["worst30days_pos_share"]=W.pos.value_counts(normalize=True)
    out["worst30days_mean_coinret_by_pos"]=W.groupby("pos").coin_return.mean()
    out["all_pos_share"]=D.pos.value_counts(normalize=True)
    return out
