def explore(data):
    import pandas as pd, numpy as np
    H=18
    out={}
    # book decomposition: market rise vs timing, daily
    rows=[]
    allc=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items(): allc.append(dd["coin_return"].dropna())
    for coin,wins in data["bars"].items():
        cm=pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).mean()
        for w,b in wins.items():
            b=b.copy(); b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            c=b["close"]; b["ret30"]=c.pct_change(180)
            g=b.groupby("day").agg(alloc=("postRebalance_current_allocation","mean"),ret30=("ret30","last"))
            dd=data["days"][coin][w].copy(); dd["day"]=pd.to_datetime(dd["day"]).dt.floor("D")
            m=dd.merge(g,left_on="day",right_index=True,how="left")
            m["alloc_prev"]=m["alloc"].shift(1)
            m["mkt"]=m["alloc_prev"]*cm; m["coin"]=coin; m["w"]=w
            rows.append(m)
    D=pd.concat(rows).dropna(subset=["book_return"])
    out["decomp"]=pd.Series({"book_mean":D.book_return.mean(),"from_market_rise":D.mkt.mean(),
        "timing":D.book_return.mean()-D.mkt.mean(),"share_days_short":(D.alloc_prev<-0.01).mean(),
        "mean_alloc_when_short":D.loc[D.alloc_prev<-0.01,"alloc_prev"].mean()})
    x=D.dropna(subset=["ret30"]).copy()
    x["b"]=pd.cut(x["ret30"],[-1,-0.25,-0.15,-0.07,0,0.1,0.3,5])
    out["book_by_ret30_day"]=x.groupby("b").agg(n=("book_return","size"),book=("book_return","mean"),
        coin=("coin_return","mean"),alloc=("alloc_prev","mean"))
    # forward coin return by ret30 bucket on non-overlapping grid (all bars), long side
    rr=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values; r30=pd.Series(c).pct_change(180).values
            for i in range(0,len(c)-H,H):
                rr.append(dict(r30=r30[i],f=c[i+H]/c[i]-1))
    R=pd.DataFrame(rr).dropna()
    R["b"]=pd.cut(R["r30"],[-1,-0.25,-0.15,-0.07,0,0.1,0.3,5])
    out["grid_fwd18_by_ret30"]=R.groupby("b").agg(n=("f","size"),mean=("f","mean"),
        t=("f",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))))
    # trades: duration buckets
    T=pd.concat([t for wins in data["trades"].values() for t in wins.values() if len(t)])
    T["d"]=pd.cut(T["duration_minutes"]/60/24,[0,3,6,12,30,400])
    out["trades_by_days"]=T.groupby("d").agg(n=("net_profit_loss_percent","size"),
        net=("net_profit_loss_percent","mean"),sum_net=("net_profit_loss_percent","sum"))
    return out
