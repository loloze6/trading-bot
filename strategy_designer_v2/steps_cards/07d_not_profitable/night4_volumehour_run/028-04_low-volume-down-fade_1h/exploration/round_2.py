import numpy as np, pandas as pd

def explore(data):
    out={}
    # book daily: gross vs fees, market part vs timing
    rows=[]
    for coin, ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"].astype(float)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            rows.append(pd.DataFrame({"coin":coin,"w":w,"g":a*r,"a":a,"r":r,"fee":fee,
                "turn":(a-b["previous_allocation"].astype(float)).abs(),
                "fc":b["forecast"].astype(float)}))
    B=pd.concat(rows,ignore_index=True)
    mr=B.groupby("coin")["r"].mean()
    B["mkt"]=B.a*B.coin.map(mr)
    s=B.groupby("coin")[["g","fee","mkt","turn"]].sum()
    nb=B.groupby("coin").size()
    out["per-bar sums %/bar (gross, fee, market part, turnover)"]=(s.div(nb,axis=0)*100)
    out["per-day x24 %: gross, fee, mkt"]=(s.div(nb,axis=0)*2400)[["g","fee","mkt"]]
    # gain by forecast size while in position
    I=B[B.a.abs()>0].copy()
    I["fb"]=pd.cut(I.fc,[-0.01,0.5,2,5,10,20.01])
    out["gross gain by forecast bin (bars in position)"]=I.groupby("fb",observed=True).agg(n=("g","size"),gain_bp=("g",lambda x:x.mean()*1e4),fee_bp=("fee",lambda x:x.mean()*1e4),alloc=("a","mean"))
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    T["dur_h"]=T.duration_minutes/60
    T["eb"]=pd.cut(T.entry_forecast.astype(float),[-0.01,2,5,10,20.01])
    out["trades by entry forecast"]=T.groupby("eb",observed=True).agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("dur_h","median"))
    out["trades overall"]=pd.Series({"n":len(T),"gross%":T.profit_loss_percent.mean(),"net%":T.net_profit_loss_percent.mean(),"dur_h_med":T.dur_h.median(),"dur_h_mean":T.dur_h.mean()})
    # book daily Sharpe by year
    Dd=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    Dd["year"]=pd.to_datetime(Dd.day).dt.year
    out["book & coin mean daily % by year"]=Dd.groupby("year")[["book_return","coin_return"]].mean()*100
    return out
