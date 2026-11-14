def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","close","forecast","postRebalance_current_allocation","postRebalance_total_value"]].copy()
            d["dist"]=df["debug_info.components.above_ma.last_history_value"]
            d["coin"]=c
            d["r1"]=d.close.pct_change()
            d["f1"]=d.close.shift(-1)/d.close-1
            d["f5"]=d.close.shift(-5)/d.close-1
            d["f20"]=d.close.shift(-20)/d.close-1
            d["vol20"]=d.r1.rolling(20).std()
            d["mom20"]=d.close/d.close.shift(20)-1
            d["bk"]=d.postRebalance_total_value.pct_change().shift(-1)
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["ts"]=pd.to_datetime(A.timestamp)
    out={}
    fb=pd.cut(A.forecast,[-0.01,0,5,10,15,20.01],labels=["0","0-5","5-10","10-15","15-20"])
    out["fwd by forecast"]=A.groupby(fb).agg(n=("f20","count"),f5=("f5","mean"),f20=("f20","mean"),f20med=("f20","median"),hit=("f20",lambda x:(x>0).mean()))
    A["dq"]=A.groupby("coin").dist.transform(lambda x:pd.qcut(x,10,labels=False,duplicates="drop"))
    out["fwd by raw dist decile"]=A.groupby("dq").agg(dist=("dist","mean"),f20=("f20","mean"),f20med=("f20","median"),hit=("f20",lambda x:(x>0).mean()),vol=("vol20","mean"))
    A["z"]=A.r1/A.vol20.shift(0)
    A["zb"]=pd.cut(A.r1/A.groupby("coin").r1.transform("std"),[-99,-2,-1,1,2,99])
    out["after daily move (sd units)"]=A.groupby("zb").agg(n=("f1","count"),f1=("f1","mean"),f5=("f5","mean"),f20=("f20","mean"))
    A["vq"]=A.groupby("coin").vol20.transform(lambda x:pd.qcut(x,3,labels=["lo","mid","hi"]))
    out["by vol tercile"]=A.groupby(["vq",A.forecast>0]).agg(n=("f20","count"),f1=("f1","mean"),f20=("f20","mean"),bk=("bk","mean"))
    out["weekday"]=A.groupby(A.ts.dt.weekday).agg(r1=("r1","mean"),t=("r1",lambda x:x.mean()/x.std()*np.sqrt(x.count())),bk=("bk","mean"))
    out["by coin"]=A.groupby("coin").agg(on=("forecast",lambda x:(x>0).mean()),f20_on=("f20",lambda x:np.nan),bk=("bk","mean"),r1=("r1","mean"))
    out["coin x on f20"]=A.groupby(["coin",A.forecast>0]).f20.mean().unstack()
    out["year"]=A.groupby([A.ts.dt.year,A.forecast>0]).f20.mean().unstack()
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    T["days"]=T.duration_minutes/1440
    T["db"]=pd.cut(T.days,[0,1,3,10,30,1e9])
    out["trades by duration"]=T.groupby("db").agg(n=("net_profit_loss_percent","count"),mean=("net_profit_loss_percent","mean"),sum=("net_profit_loss_percent","sum"),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    out["trades summary"]=pd.Series({"n":len(T),"side_long":(T.side=="LONG").mean(),"comm_sum":T.total_commission.sum(),"pnl_sum":T.net_profit_loss_percent.sum()})
    return out
