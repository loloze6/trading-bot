def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    tr=pd.concat([trades[c][w].assign(coin=c,w=w) for c in trades for w in trades[c] if len(trades[c][w])])
    tr["year"]=pd.to_datetime(tr.entry_time).dt.year
    tr["dur"]=tr.duration_minutes/1440
    out["trades_by_year"]=tr.groupby("year").agg(n=("dur","size"),gross=("profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()),dur=("dur","mean"))
    out["trades_by_side"]=tr.groupby("side").agg(n=("dur","size"),gross=("profit_loss_percent","mean"))
    tr["durq"]=pd.cut(tr.dur,[0,2,5,8,15,1000])
    out["trades_by_dur"]=tr.groupby("durq").agg(n=("dur","size"),gross=("profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()))
    tr["efq"]=pd.qcut(tr.entry_forecast.rank(method="first"),4,labels=["most_neg","q2","q3","least_neg"])
    out["trades_by_entry_forecast"]=tr.groupby("efq").agg(n=("dur","size"),ef=("entry_forecast","mean"),gross=("profit_loss_percent","mean"))
    out["trades_by_exit_forecast_zero"]=tr.groupby(tr.exit_forecast==0).agg(n=("dur","size"),gross=("profit_loss_percent","mean"),dur=("dur","mean"))
    # book daily by year, and bars-level: position gain by regime / forecast state
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            r1=b.close.shift(-1)/b.close-1
            a=b.postRebalance_current_allocation
            hi=b.high.rolling(30).max(); lo=b.low.rolling(30).min()
            ret60=b.close/b.close.shift(60)-1
            ret10=b.close/b.close.shift(10)-1
            df=pd.DataFrame(dict(g=a*r1,a=a,f=b.forecast,reg=b.regime,ret60=ret60,ret10=ret10,
                                 year=pd.to_datetime(b.timestamp).dt.year,coin=c,chg=b.allocation_change.abs() if "allocation_change" in b else np.nan))
            rows.append(df)
    B=pd.concat(rows).dropna(subset=["g"])
    B["state"]=np.where(B.a==0,"flat",np.where(B.f<0,"short_signal_on","short_signal_off"))
    out["bar_gain_by_state"]=B.groupby("state").agg(n=("g","size"),gain=("g","mean"),absal=("a",lambda x:x.abs().mean()),t=("g",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    out["bar_gain_by_regime"]=B[B.a!=0].groupby("reg").agg(n=("g","size"),gain=("g","mean"))
    S=B[B.a!=0].copy()
    S["r60q"]=pd.qcut(S.ret60.rank(method="first"),4,labels=["q1low","q2","q3","q4high"])
    out["held_gain_by_ret60"]=S.groupby("r60q").agg(n=("g","size"),gain=("g","mean"),ret60=("ret60","mean"))
    out["held_gain_by_year"]=S.groupby("year").agg(n=("g","size"),gain=("g","mean"))
    out["rebal_bars_share"]=pd.Series(dict(share_bars_trading=(B.chg>1e-9).mean(),mean_abs_change=B.chg.mean()))
    D=pd.concat([days[c][w].assign(coin=c,w=w) for c in days for w in days[c]]).dropna(subset=["book_return"])
    D["year"]=pd.to_datetime(D.day).dt.year
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    return out
