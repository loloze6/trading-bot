def explore(data):
    import pandas as pd, numpy as np
    rows=[]; cases=[]; trd=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            gross=(a*r).fillna(0)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            rows.append(dict(coin=c,w=w,n=len(b),gross=gross.sum(),fee=fee.fillna(0).sum(),
                             turnover=(b["postRebalance_current_allocation"].fillna(0)-b["previous_allocation"].fillna(0)).abs().sum()))
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            idx=np.where(hr==15)[0]
            for i in idx:
                if i+2<len(b):
                    cases.append(dict(coin=c,f=b["forecast"].iloc[i],a=a.iloc[i],
                        r2=b["close"].iloc[i+2]/b["close"].iloc[i]-1,
                        g=gross.iloc[i]+gross.iloc[i+1],
                        fee=fee.iloc[i:i+3].fillna(0).sum()))
        for w,t in data["trades"][c].items():
            trd.append(t[["profit_loss_percent","net_profit_loss_percent","total_commission","duration_minutes"]].assign(coin=c))
    R=pd.DataFrame(rows); C=pd.DataFrame(cases); T=pd.concat(trd)
    bycoin=R.groupby("coin")[["gross","fee","turnover"]].sum()
    C["absf"]=C.f.abs()
    C["q"]=pd.qcut(C.absf.rank(method="first"),5,labels=False)
    C["sr"]=np.sign(C.f)*C.r2
    byq=C.groupby("q").agg(n=("sr","size"),absf=("absf","mean"),absa=("a",lambda x:x.abs().mean()),
        signret=("sr","mean"),gross=("g","mean"),fee=("fee","mean"))
    byq["net"]=byq.gross-byq.fee
    tsum=T.groupby("coin").agg(n=("profit_loss_percent","size"),pl=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),dur=("duration_minutes","median"))
    return {"bycoin":bycoin,"byq":byq,"trades":tsum,
            "totals":pd.Series(dict(gross=R.gross.sum(),fee=R.fee.sum(),turnover=R.turnover.sum(),
              casegross=C.g.mean(),casefee=C.fee.mean(),signret=C.sr.mean(),meanabsr2=C.r2.abs().mean()))}
