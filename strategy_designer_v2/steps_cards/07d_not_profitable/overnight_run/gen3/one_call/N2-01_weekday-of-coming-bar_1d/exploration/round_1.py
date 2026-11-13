def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            nxt=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"].astype(float)
            pv=b["postRebalance_total_value"].astype(float)
            bookret=pv.shift(-1)/pv-1
            r20=c/c.shift(20)-1
            vol=c.pct_change().rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.dayofweek,"year":ts.dt.year,
                "nxt":nxt,"a":a,"f":b["forecast"].astype(float),"gross":a*nxt,"book":bookret,
                "r20":r20,"vol":vol,"dalloc":a.diff().abs()})
            rows.append(d)
            t=data["trades"].get(coin,{}).get(w)
            if t is not None and len(t): trs.append(t.assign(coin=coin))
    D=pd.concat(rows).dropna(subset=["nxt"])
    T=pd.concat(trs)
    out={}
    def st(g):
        x=g.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>1 else np.nan})
    out["by_weekday_of_bar_t: share active, mean alloc, gross"]=D.groupby("wd").apply(lambda g: pd.Series({"active":(g.a.abs()>1e-9).mean(),"meanalloc":g.a.mean(),"gross_mean":g.gross.mean(),"nxt_mean":g.nxt.mean(),"book_mean":g.book.mean()}))
    D["fz"]=np.sign(D.f)*np.minimum(np.abs(D.f)//5,3)
    out["by_forecast_bucket"]=D.groupby("fz").apply(lambda g: pd.concat([st(g.gross).add_prefix("g_"),st(g.nxt).add_prefix("r_")]))
    act=D[D.a.abs()>1e-9].copy()
    act["side"]=np.where(act.a>0,"long","short")
    out["active_by_side"]=act.groupby("side").apply(lambda g: st(g.gross))
    act["trend"]=np.where(act.r20>0,"up20","down20")
    out["active_by_trend"]=act.groupby("trend").apply(lambda g: st(g.gross))
    act["volq"]=pd.qcut(act.vol,3,labels=["calm","mid","wild"])
    out["active_by_vol"]=act.groupby("volq").apply(lambda g: st(g.gross))
    out["active_by_year"]=act.groupby("year").apply(lambda g: st(g.gross))
    out["active_by_coin"]=act.groupby("coin").apply(lambda g: st(g.gross))
    out["total_gross_vs_book"]=pd.Series({"sum_gross_all":D.gross.sum(),"sum_book_all":D.book.sum(),"mean_book":D.book.mean(),"mean_turnover":D.dalloc.mean(),"mean_absalloc":D.a.abs().mean()})
    T=T.copy()
    out["trades"]=T.groupby("side").apply(lambda g: pd.Series({"n":len(g),"dur_days":g.duration_minutes.mean()/1440,"gross_mean":g.profit_loss_percent.mean(),"net_mean":g.net_profit_loss_percent.mean(),"comm_mean":g.total_commission.mean(),"win":(g.profit_loss_percent>0).mean()}))
    out["entry_weekday"]=pd.to_datetime(T.entry_time).dt.dayofweek.value_counts().sort_index()
    out["holding_mean_daily_coin"]=D.nxt.mean()
    return out
