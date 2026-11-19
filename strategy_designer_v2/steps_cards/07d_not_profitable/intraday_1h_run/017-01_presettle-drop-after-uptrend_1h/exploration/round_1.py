import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            b["gross"]=a*r
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["hour"]=b["ts"].dt.hour
            b["day"]=b["ts"].dt.floor("D")
            b["absA"]=a.abs()
            b["turn"]=(a-b["previous_allocation"].fillna(0)).abs()
            b["r"]=r
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","hour","gross","fee","absA","turn","r","forecast","close"]])
            d=b.groupby("day").agg(gross=("gross","sum"),fee=("fee","sum"))
            d["coin"]=coin; d["w"]=w
            daily.append(d)
    B=pd.concat(rows); D=pd.concat(daily)
    out={}
    dd=D.groupby(level=0).agg(gross=("gross","mean"),fee=("fee","mean"))
    out["daily gross vs fee"]=pd.Series({"mean gross daily":dd.gross.mean(),"mean fee daily":dd.fee.mean(),
        "t gross":dd.gross.mean()/(dd.gross.std()/np.sqrt(len(dd))),"n days":len(dd)})
    byh=B.groupby("hour").agg(meanAbsA=("absA","mean"),gross=("gross","mean"),fee=("fee","mean"),turn=("turn","mean"),r=("r","mean"))
    out["by hour"]=byh
    act=B[B.absA>0]
    out["active"]=pd.Series({"share active bars":(B.absA>0).mean(),"mean |alloc| active":act.absA.mean(),
        "gross per active bar":act.gross.mean(),"fee per bar with trade":B.loc[B.turn>0,"fee"].mean(),
        "fee/turnover":B.fee.sum()/B.turn.sum(),"mean |r| active":act.r.abs().mean()})
    out["by coin"]=B.groupby("coin").agg(gross=("gross","sum"),fee=("fee","sum"))
    # gross per active bar by forecast tercile
    act=act.copy(); act["q"]=pd.qcut(act.forecast.abs().rank(method="first"),3,labels=["low","mid","high"])
    out["active by |fc| third"]=act.groupby("q").agg(gross=("gross","mean"),r=("r","mean"),n=("r","size"),absA=("absA","mean"))
    return out
