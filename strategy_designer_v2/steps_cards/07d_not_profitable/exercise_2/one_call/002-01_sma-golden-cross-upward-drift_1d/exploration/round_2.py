def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["fwd1"]=b["close"].shift(-1)/b["close"]-1
            b["fwd10"]=b["close"].shift(-10)/b["close"]-1
            r=b["close"].pct_change()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ret60"]=b["close"]/b["close"].shift(60)-1
            b["raw"]=b["debug_info.components.sma_cross.last_history_value"]
            b["pos"]=b["postRebalance_current_allocation"]
            on=(b["raw"]>0).astype(int)
            grp=(on!=on.shift()).cumsum()
            b["age"]=on.groupby(grp).cumcount()
            b["on"]=on
            v=b["postRebalance_total_value"]
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","forecast","pos","raw","on","age","fwd1","fwd10","ret20","ret60"]])
            t=data["trades"][coin][w].copy(); t["coin"]=coin; t["w"]=w; trs.append(t)
    B=pd.concat(rows); T=pd.concat(trs)
    out={}
    out["raw_vs_fc"]=pd.Series({"raw>0":(B.raw>0).mean(),"fc>0":(B.forecast>0).mean(),"raw>0&fc==0":((B.raw>0)&(B.forecast==0)).mean(),"raw<=0&fc>0":((B.raw<=0)&(B.forecast>0)).mean()})
    A=B[B.on==1].copy()
    A["ab"]=pd.cut(A.age,[-1,20,60,120,250,1e5])
    out["by_age_on"]=A.groupby("ab").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"),fc=("forecast","mean"))
    Z=B[B.on==0].copy(); Z["ab"]=pd.cut(Z.age,[-1,20,60,120,250,1e5])
    out["by_age_off"]=Z.groupby("ab").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"))
    A["r60"]=pd.qcut(A.ret60,3,labels=False)
    out["on_by_ret60"]=A.groupby("r60").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"),fc=("forecast","mean"))
    # trades: entry forecast, exit forecast
    T["dur_d"]=T.duration_minutes/1440
    T["short"]=T.dur_d<=40
    out["trade_exit"]=T.groupby("short").agg(n=("side","size"),efc=("entry_forecast","mean"),xfc=("exit_forecast","mean"),share_xfc0=("exit_forecast",lambda s:(s==0).mean()),gross=("profit_loss_percent","mean"))
    # flips: how many trades per on-episode
    ep=B.groupby(["coin","w"]).apply(lambda g:pd.Series({"episodes_on":((g.on==1)&(g.on.shift()!=1)).sum(),"fc_entries":((g.forecast>0)&(g.forecast.shift().fillna(0)==0)).sum()})).sum()
    out["episodes_vs_entries"]=ep
    # drawdown of book per coin-window
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            v=d.book_value; c=d.close
            dd.append({"coin":coin,"w":w,"bookdd":(v/v.cummax()-1).min(),"coindd":(c/c.cummax()-1).min(),"bookret":v.iloc[-1]/v.iloc[0]-1})
    DD=pd.DataFrame(dd)
    out["dd_by_coin"]=DD.groupby("coin").agg(bookdd_mean=("bookdd","mean"),bookdd_min=("bookdd","min"),coindd_mean=("coindd","mean"),bookret_mean=("bookret","mean"))
    out["share_fc_change_days"]=((B.groupby(["coin","w"]).pos.diff().abs()>0.05).mean())
    return out
