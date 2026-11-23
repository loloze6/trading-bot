def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    tr=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            b=data["bars"][c][w].reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            t=t.copy()
            et=pd.to_datetime(t["entry_time"])
            idx=np.searchsorted(ts.values,et.values,side="right")-1
            dep=b.get("debug_info.components.depth.last_history_value",pd.Series(np.nan,index=b.index))
            cl=b["close"]; r20=cl/cl.shift(20)-1
            vol=np.log(cl).diff().rolling(30,min_periods=20).std()
            t["depth"]=[dep.iloc[i] if i>=0 else np.nan for i in idx]
            t["r20"]=[r20.iloc[i] if i>=0 else np.nan for i in idx]
            t["vol"]=[vol.iloc[i] if i>=0 else np.nan for i in idx]
            t["days"]=t.duration_minutes/1440
            t["coin"]=c; t["win"]=w
            tr.append(t)
    T=pd.concat(tr)
    T["dur_b"]=pd.cut(T.days,[-0.1,1.5,3.5,7.5,8.5,100])
    out["trades_by_duration"]=T.groupby("dur_b").agg(n=("days","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda v:(v>0).mean()))
    for col in ["depth","r20","vol"]:
        x=T.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],4,labels=False,duplicates="drop")
        out["trades_by_"+col]=x.groupby("q").agg(lo=(col,"min"),hi=(col,"max"),n=(col,"size"),gross=("profit_loss_percent","mean"),
            t=("profit_loss_percent",lambda v:v.mean()/v.std()*np.sqrt(len(v))))
    out["trades_side"]=T.groupby("side").agg(n=("days","size"),gross=("profit_loss_percent","mean"),comm=("total_commission","mean"))
    # book daily on short days vs coin
    br=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            b=data["bars"][c][w]
            al=b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last().shift(1)
            dd=dd.copy(); dd["al"]=al.reindex(pd.to_datetime(dd["day"])).values
            dd["coin"]=c; dd["win"]=w; br.append(dd)
    D=pd.concat(br).dropna(subset=["book_return"])
    S=D[D.al<-1e-6]
    out["short_days"]=pd.Series({"n":len(S),"mean_book":S.book_return.mean(),"mean_coin":S.coin_return.mean(),
        "all_coin_mean":D.coin_return.mean(),"mean_alloc":S.al.mean(),"share_days":len(S)/len(D)})
    W=D.groupby("win").book_return.sum()
    out["book_sum_by_window_worst5"]=W.sort_values().head(5)
    out["book_sum_by_window_best5"]=W.sort_values().tail(5)
    return out
