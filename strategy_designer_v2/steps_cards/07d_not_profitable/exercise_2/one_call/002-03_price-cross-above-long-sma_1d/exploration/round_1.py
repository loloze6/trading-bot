import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars, trades, days = data["bars"], data["trades"], data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["ret1"] = b["close"].pct_change().shift(-1)
            b["fwd20"] = b["close"].shift(-20)/b["close"]-1
            b["bookret1"] = b["postRebalance_total_value"].pct_change().shift(-1)
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            b["mom20"] = b["close"]/b["close"].shift(20)-1
            b["coin"]=c; b["win"]=w
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["alloc"]=B["postRebalance_current_allocation"]
    B["dist"]=B["debug_info.components.above_ma.last_history_value"]
    B["fb"]=pd.cut(B["forecast"],[-0.01,0,5,10,15,19.99,20.01],labels=["0","0-5","5-10","10-15","15-20","20"])
    out["by_forecast_bucket"]=B.groupby("fb",observed=True).agg(n=("ret1","size"),alloc=("alloc","mean"),ret1=("ret1","mean"),fwd20=("fwd20","mean"),hit20=("fwd20",lambda s:(s>0).mean()),book1=("bookret1","mean"))
    B["db"]=pd.qcut(B["dist"],8,duplicates="drop")
    out["by_raw_distance"]=B.groupby("db",observed=True).agg(n=("ret1","size"),fc=("forecast","mean"),ret1=("ret1","mean"),fwd20=("fwd20","mean"),vol=("vol20","mean"))
    B["volq"]=B.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=["calm","mid","wild"]))
    B["active"]=B["alloc"].abs()>0
    out["by_vol_active"]=B.groupby(["volq","active"],observed=True).agg(n=("ret1","size"),ret1=("ret1","mean"),book1=("bookret1","mean"),fwd20=("fwd20","mean"))
    B["mstate"]=np.where(B["mom20"]>0,"up20","down20")
    out["by_mom_active"]=B.groupby(["mstate","active"]).agg(n=("ret1","size"),ret1=("ret1","mean"),book1=("bookret1","mean"))
    out["by_year"]=B.groupby("year").agg(active=("active","mean"),coin1=("ret1","mean"),book1=("bookret1","mean"))
    out["by_coin"]=B.groupby("coin").agg(active=("active","mean"),coin1=("ret1","mean"),book1=("bookret1","mean"),alloc_when_on=("alloc",lambda s:s[s>0].mean()))
    T=pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()],ignore_index=True)
    T["days"]=T["duration_minutes"]/1440
    out["trades"]=pd.Series({"n":len(T),"side_long_share":(T["side"]=="LONG").mean(),"med_days":T["days"].median(),"mean_days":T["days"].mean(),
        "mean_gross":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),"mean_comm":T["total_commission"].mean(),
        "win_gross":(T["profit_loss_percent"]>0).mean(),"sum_gross":T["profit_loss_percent"].sum(),"sum_net":T["net_profit_loss_percent"].sum()})
    T["db"]=pd.cut(T["days"],[0,1.5,5,20,60,1e5])
    out["trades_by_dur"]=T.groupby("db",observed=True).agg(n=("days","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),sumnet=("net_profit_loss_percent","sum"))
    # allocation changes
    out["alloc_change_stats"]=pd.Series({"mean_abs_change_per_bar":B["alloc"].groupby([B.coin,B.win]).diff().abs().mean(),"share_bars_changed":(B["alloc"].groupby([B.coin,B.win]).diff().abs()>1e-6).mean(),"alloc_max":B["alloc"].max(),"alloc_mean_on":B.loc[B.active,"alloc"].mean()})
    return out
