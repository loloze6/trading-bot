def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; trs=[]; dys=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["fwd1"]=b["close"].shift(-1)/b["close"]-1
            b["fwd10"]=b["close"].shift(-10)/b["close"]-1
            r=b["close"].pct_change()
            b["vol20"]=r.rolling(20).std()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["bookret_next"]=b["postRebalance_total_value"].shift(-1)/b["postRebalance_total_value"]-1
            b["coin"]=coin; b["w"]=w; b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["raw"]=b["debug_info.components.sma_cross.last_history_value"]
            rows.append(b[["coin","w","year","forecast","pos","fwd1","fwd10","vol20","ret20","bookret_next","raw"]])
            t=data["trades"][coin][w].copy(); t["coin"]=coin; t["w"]=w; trs.append(t)
            d=data["days"][coin][w].copy(); d["coin"]=coin; d["w"]=w; dys.append(d)
    B=pd.concat(rows); T=pd.concat(trs); D=pd.concat(dys)
    out={}
    B["fb"]=pd.cut(B["forecast"],[-0.1,0,5,10,15,19.99,20.1],labels=["0","0-5","5-10","10-15","15-20","20cap"])
    out["by_forecast_bucket"]=B.groupby("fb").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"),pos=("pos","mean"),vol=("vol20","mean"))
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby("coin").agg(n=("side","size"),longs=("side",lambda s:(s=="LONG").mean()),dur=("dur_d","median"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),comm=("total_commission","mean"),win=("profit_loss_percent",lambda s:(s>0).mean()))
    out["trades_all"]=pd.Series({"n":len(T),"gross_mean":T.profit_loss_percent.mean(),"gross_median":T.profit_loss_percent.median(),"net_mean":T.net_profit_loss_percent.mean(),"dur_med":T.dur_d.median(),"dur_mean":T.dur_d.mean(),"share_dur<=3d":(T.dur_d<=3).mean(),"gross_sum":T.profit_loss_percent.sum(),"net_sum":T.net_profit_loss_percent.sum()})
    T["db"]=pd.cut(T["dur_d"],[0,2,5,15,40,1e5])
    out["trades_by_dur"]=T.groupby("db").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),sumnet=("net_profit_loss_percent","sum"))
    act=B["pos"].abs()>1e-9
    out["exposure"]=pd.Series({"share_active":act.mean(),"mean_pos_active":B.loc[act,"pos"].mean(),"book_next_active":B.loc[act,"bookret_next"].mean(),"book_next_flat":B.loc[~act,"bookret_next"].mean(),"coin_fwd1_active":B.loc[act,"fwd1"].mean(),"coin_fwd1_flat":B.loc[~act,"fwd1"].mean(),"coin_fwd1_all":B.fwd1.mean()})
    out["by_coin"]=B.groupby("coin").apply(lambda g:pd.Series({"act":(g.pos.abs()>0).mean(),"fwd1_act":g.loc[g.pos.abs()>0,"fwd1"].mean(),"fwd1_flat":g.loc[g.pos.abs()==0,"fwd1"].mean(),"book":g.bookret_next.mean()}))
    out["by_year"]=B.groupby("year").apply(lambda g:pd.Series({"act":(g.pos.abs()>0).mean(),"fwd1_act":g.loc[g.pos.abs()>0,"fwd1"].mean(),"fwd1_flat":g.loc[g.pos.abs()==0,"fwd1"].mean(),"book":g.bookret_next.mean(),"coin":g.fwd1.mean()}))
    B["vt"]=B.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["by_vol_active"]=B[act].groupby("vt").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"),book=("bookret_next","mean"))
    B["mt"]=B.groupby("coin")["ret20"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["by_ret20_active"]=B[act].groupby("mt").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"),book=("bookret_next","mean"))
    out["by_ret20_flat"]=B[~act].groupby("mt").agg(n=("fwd1","size"),fwd1=("fwd1","mean"),fwd10=("fwd10","mean"))
    out["days_up_down"]=D.assign(up=D.coin_return>0).groupby("up").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    out["by_window"]=D.groupby("w").agg(book=("book_return","sum"),coin=("coin_return","sum"))
    return out
