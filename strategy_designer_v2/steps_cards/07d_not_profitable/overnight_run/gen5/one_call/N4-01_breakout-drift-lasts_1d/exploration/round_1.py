def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tr_rows=[]; bar_rows=[]; day_rows=[]; win_rows=[]
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"]=coin; b["win"]=w
            # 20d vol, 20d trend
            r = b["close"].pct_change()
            b["vol20"] = r.rolling(20).std()
            b["tr20"] = b["close"]/b["close"].shift(20)-1
            bar_rows.append(b[["coin","win","forecast","regime","pos","ret1","vol20","tr20"]])
            t = data["trades"][coin][w].copy(); t["coin"]=coin; t["win"]=w
            tr_rows.append(t)
            d = data["days"][coin][w].copy(); d["coin"]=coin; d["win"]=w
            day_rows.append(d)
            bv = d["book_value"].dropna()
            if len(bv)>1:
                dd = (bv/bv.cummax()-1).min()
                win_rows.append({"coin":coin,"win":w,"book":bv.iloc[-1]/bv.iloc[0]-1,
                                 "coin_ret":d["close"].iloc[-1]/d["close"].iloc[0]-1,"maxdd":dd})
    B = pd.concat(bar_rows); T = pd.concat(tr_rows); D = pd.concat(day_rows); W = pd.DataFrame(win_rows)
    out["forecast_desc"] = B["forecast"].describe()
    out["pos_share_nonzero"] = float((B["pos"].abs()>1e-9).mean())
    # trades
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades"] = pd.Series({"n":len(T),"long_share":(T.side=="LONG").mean(),
        "dur_mean_d":T.dur_d.mean(),"dur_median_d":T.dur_d.median(),
        "gross_mean":T.profit_loss_percent.mean(),"net_mean":T.net_profit_loss_percent.mean(),
        "comm_mean":T.total_commission.mean(),"gross_median":T.profit_loss_percent.median(),
        "win_rate_gross":(T.profit_loss_percent>0).mean(),
        "t_gross":T.profit_loss_percent.mean()/T.profit_loss_percent.std()*np.sqrt(len(T))})
    T["durb"]=pd.cut(T.dur_d,[0,1.5,3.5,7.5,15,1000])
    out["trades_by_dur"]=T.groupby("durb").agg(n=("dur_d","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),sumnet=("net_profit_loss_percent","sum"))
    # forecast buckets on active bars, next-day return
    A = B[B.forecast!=0].dropna(subset=["ret1"])
    A["fb"]=pd.qcut(A.forecast,5,duplicates="drop")
    out["fc_bucket_ret1"]=A.groupby("fb").ret1.agg(["count","mean","std"])
    # book days: position active
    D["active"]=None
    out["book_by_year"]=D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["windows"]=W.groupby("win").agg(book=("book","mean"),coin=("coin_ret","mean"),dd=("maxdd","mean")).round(3)
    out["by_coin"]=W.groupby("coin").agg(book=("book","mean"),coin=("coin_ret","mean"),dd=("maxdd","min")).round(3)
    # regime / vol / trend on active bars: pos*ret1
    A2 = B[B.pos.abs()>1e-9].dropna(subset=["ret1"]).copy()
    A2["pnl"]=A2.pos*A2.ret1
    out["by_regime"]=A2.groupby("regime").pnl.agg(["count","mean","sum"])
    A2["vb"]=pd.qcut(A2.vol20,3,duplicates="drop")
    out["by_vol"]=A2.groupby("vb").pnl.agg(["count","mean","sum","std"])
    A2["tb"]=pd.qcut(A2.tr20,4,duplicates="drop")
    out["by_trend20"]=A2.groupby("tb").pnl.agg(["count","mean","sum"])
    return out
