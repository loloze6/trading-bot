def explore(data):
    import numpy as np, pandas as pd
    res={}
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin,w=w))
    T=pd.concat(tr)
    T["days"]=T["duration_minutes"]/1440
    T["dq"]=pd.cut(T["days"],[0,1.5,3.5,5.5,10.5,1e9],labels=["<=1","2-3","4-5","6-10",">10"])
    res["trades by duration"]=T.groupby("dq").agg(n=("days","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    res["trades by entry_regime"]=T.groupby("entry_regime").agg(n=("days","size"),gross=("profit_loss_percent","mean"),med_days=("days","median"))
    T["efq"]=pd.qcut(T["entry_forecast"].rank(method="first"),3,labels=["most neg","mid","least neg"])
    res["trades by entry forecast tercile"]=T.groupby("efq").agg(n=("days","size"),fc=("entry_forecast","mean"),gross=("profit_loss_percent","mean"))
    res["gross loss share of worst 10 trades"]=float(T["profit_loss_percent"].nsmallest(10).sum()/T["profit_loss_percent"].sum())
    # bar-level: where the short positions are and what they earn
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change(); vol=r1.rolling(20).std(); jump=r1/vol
            r90=c/c.shift(90)-1; r30=c/c.shift(30)-1
            sit=((r90<0)&(jump>=2)).astype(int)
            since=np.full(len(c),np.nan); last=-10**9
            for i in range(len(c)):
                if sit.iloc[i]==1: last=i
                since[i]=i-last if last>-10**8 else np.nan
            a=b["postRebalance_current_allocation"].astype(float)
            g=a*(c.shift(-1)/c-1)
            rows.append(pd.DataFrame(dict(coin=coin,w=w,a=a,g=g,since=since,r30=r30,r90=r90,reg=b["regime"],fc=b["forecast"])))
    B=pd.concat(rows)
    S=B[B.a<0].copy()
    S["sinceb"]=pd.cut(S.since,[-1,0,1,2,4,9,1e9],labels=["0","1","2","3-4","5-9",">=10"])
    res["short bars by days since situation"]=S.groupby("sinceb").agg(n=("g","size"),mean_gain_pct=("g",lambda x:100*x.mean()),t=("g",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))),mean_alloc=("a","mean"))
    S["r30s"]=np.where(S.r30<0,"r30neg","r30pos")
    res["short bars by r30 sign"]=S.groupby("r30s").agg(n=("g","size"),mean_gain_pct=("g",lambda x:100*x.mean()),t=("g",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    S["r90s"]=np.where(S.r90<0,"r90neg","r90pos")
    res["short bars by r90 sign"]=S.groupby("r90s").agg(n=("g","size"),mean_gain_pct=("g",lambda x:100*x.mean()))
    res["share of bars short"]=float((B.a<0).mean())
    res["mean |alloc| when short"]=float(S.a.abs().mean())
    return res
