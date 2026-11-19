def explore(data):
    import numpy as np, pandas as pd
    feerate=0.00108
    ev=[]; dly=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            c=b["close"].values; n=len(b)
            f=b["forecast"].fillna(0).values; a=b["postRebalance_current_allocation"].fillna(0).values
            ts=pd.to_datetime(b["timestamp"])
            pos=np.zeros(n); prev=0.0; fees=np.zeros(n)
            for i in range(0,n,72):
                p=a[i] if f[i]>0 else 0.0
                fees[i]=abs(p-prev)*feerate; prev=p
                pos[i:i+72]=p
                if i+72<n and i>=72:
                    ev.append(dict(coin=coin,f=f[i],ret=c[i+72]/c[i]-1,r72=c[i]/c[i-72]-1,
                                   r24=c[i]/c[i-24]-1))
            r1=np.append(c[1:]/c[:-1]-1,0)
            br=pos*r1-fees
            s=pd.DataFrame({"d":ts.dt.floor("D"),"br":br,"gr":pos*r1})
            dd=s.groupby("d").agg(br=("br",lambda x:(1+x).prod()-1),gr=("gr",lambda x:(1+x).prod()-1))
            dly.append(dd.assign(coin=coin,w=w).reset_index())
    D=pd.concat(dly)
    day=D.groupby(["w","d"])[["br","gr"]].mean()
    slow=pd.Series(dict(sharpe_net=day.br.mean()/day.br.std()*np.sqrt(365),
                        sharpe_gross=day.gr.mean()/day.gr.std()*np.sqrt(365),
                        mean_net=day.br.mean(),mean_gross=day.gr.mean()))
    E=pd.DataFrame(ev); E["exc"]=E.ret-E.groupby("coin").ret.transform("mean")
    A=E[E.f>0].copy()
    A["r72q"]=pd.qcut(A.r72,3,labels=["deep3d","mid3d","shallow3d"])
    A["r24q"]=pd.qcut(A.r24,3,labels=["big1d","mid1d","small1d"])
    tab=A.groupby(["r72q","r24q"],observed=True).exc.agg(["size","mean"])
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    t3=A.groupby("r72q",observed=True).exc.agg(["size","mean",tt])
    t1=A.groupby("r24q",observed=True).exc.agg(["size","mean",tt])
    return {"slow_book":slow,"by3d":t3,"by1d":t1,"cross":tab}
