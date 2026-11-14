def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"].astype(float)
            nxt=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            ma200=None
            r20=c/c.shift(20)-1
            hi=c.rolling(20).max(); lo=c.rolling(20).min()
            pos=(c-lo)/(hi-lo)
            vol=np.log(c).diff().rolling(20).std()
            df=pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"alloc":a,"nxt":nxt,
                             "gain":a*nxt,"regime":b["regime"].astype(str),"fc":b["forecast"].astype(float),
                             "r20":r20,"pos":pos,"vol":vol})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["nxt"])
    out={}
    g=D.groupby("coin")
    out["by_coin"]=pd.DataFrame({"mean_gain":g.gain.mean(),"mean_alloc":g.alloc.mean(),
        "coin_drift":g.nxt.mean(),"drift_part":g.alloc.mean()*g.nxt.mean(),
        "share_sum_gain":g.gain.sum()/D.gain.sum(),"t":g.gain.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)))})
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; x["year"]=pd.to_datetime(x["day"]).dt.year; dd.append(x)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    gw=DD.groupby("w")
    out["by_window"]=pd.DataFrame({"book_mean":gw.book_return.mean(),"hold_mean":gw.coin_return.mean(),"n":gw.size()})
    gy=DD.groupby("year")
    out["by_year"]=pd.DataFrame({"book_mean":gy.book_return.mean(),"hold_mean":gy.coin_return.mean(),
        "book_sum":gy.book_return.sum(),"n":gy.size()})
    out["book_coin_mean"]=DD.groupby("coin")[["book_return","coin_return"]].mean()
    # timing decomposition overall
    act=D[D.alloc.abs()>1e-9]
    out["active_vs_flat"]=pd.DataFrame({"n":[len(act),len(D)-len(act)],
        "coin_nxt_mean":[act.nxt.mean(),D[D.alloc.abs()<=1e-9].nxt.mean()],
        "gain_mean":[act.gain.mean(),0]},index=["active","flat"])
    out["regime"]=D.groupby("regime").agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    D["fcq"]=pd.qcut(D.fc.where(D.fc>0),5,duplicates="drop")
    out["fc_bucket"]=D[D.fc>0].groupby("fcq").agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    tr=D[D.regime=="trending"].copy()
    tr["r20q"]=pd.qcut(tr.r20,5); tr["volq"]=pd.qcut(tr.vol,3)
    out["trend_by_r20"]=tr.groupby("r20q").agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    out["trend_by_vol"]=tr.groupby("volq").agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    p=T.profit_loss_percent.astype(float).sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(p),"sum":p.sum(),"top10_sum":p.head(10).sum(),"top1pct_sum":p.head(max(1,len(p)//100)).sum(),"win_rate":(p>0).mean()})
    return out
