def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"]
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            to=(a-b["previous_allocation"]).abs()
            lr=np.log(b["close"]).diff()
            vol=lr.rolling(168).std()
            d=pd.DataFrame({"coin":c,"w":w,"gross":a*r,"fee":fee,"to":to,"f":b["forecast"],
                            "hour":pd.to_datetime(b["timestamp"]).dt.hour,"vol":vol,"absa":a.abs(),
                            "r1":r,"lag1":lr,"lag2":lr.shift(1)})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    out["per-bar means"]=pd.Series({"gross":D.gross.mean(),"fee":D.fee.mean(),"turnover":D.to.mean(),
        "abs alloc":D.absa.mean(),"gross t":D.gross.mean()/D.gross.std()*np.sqrt(D.gross.count()),
        "gross per day":D.gross.mean()*24,"fee per day":D.fee.mean()*24,
        "fee per unit turnover":D.fee.sum()/D.to.sum()})
    out["by coin"]=D.groupby("coin").agg(gross=("gross","mean"),fee=("fee","mean"),to=("to","mean"))*24
    D["fq"]=pd.qcut(D.f.abs().rank(method="first"),5,labels=False)
    out["by |f| quintile, per bar"]=D.groupby("fq").agg(gross=("gross","mean"),fee=("fee","mean"),to=("to","mean"),n=("gross","count"))
    D["vq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by vol quintile, per bar"]=D.groupby("vq").agg(gross=("gross","mean"),fee=("fee","mean"),to=("to","mean"))
    out["by hour gross x1e5"]=(D.groupby("hour")["gross"].mean()*1e5).round(2)
    # autocorr of hourly returns at lags
    ac={}
    for L in [1,2,3,4,6,12,24]:
        x=D.groupby(["coin","w"])["lag1"].apply(lambda s: s.autocorr(L))
        ac[L]=x.mean()
    out["mean hourly-return autocorr by lag"]=pd.Series(ac)
    return out
