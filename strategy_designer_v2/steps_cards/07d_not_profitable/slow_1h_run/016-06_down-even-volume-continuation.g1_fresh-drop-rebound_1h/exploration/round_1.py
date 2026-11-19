def explore(data):
    import numpy as np, pandas as pd
    rows=[]; binrows=[]; days=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.copy()
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            gross=(a*r)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            turn=(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs()
            rows.append(dict(coin=coin,w=w,n=len(b),gross=gross.sum(),fee=fee.sum(),turn=turn.sum(),
                             meanalloc=a.mean(),inpos=(a.abs()>1e-6).mean(),mr=(b["regime"]=="mean_reversion").mean()))
            # forward 72 on grid
            f72=b["close"].shift(-72)/b["close"]-1
            g=b.iloc[::72].copy(); g["f72"]=f72.iloc[::72]; g["a"]=a.iloc[::72]
            g["coin"]=coin
            binrows.append(g[["coin","forecast","a","f72","regime"]])
            d=data["days"][coin][w]; days.append(d.assign(coin=coin,w=w))
    R=pd.DataFrame(rows)
    by_coin=R.groupby("coin")[["gross","fee","turn","meanalloc","inpos","mr"]].agg({"gross":"sum","fee":"sum","turn":"sum","meanalloc":"mean","inpos":"mean","mr":"mean"})
    G=pd.concat(binrows).dropna(subset=["f72"])
    G["exc"]=G["f72"]-G.groupby("coin")["f72"].transform("mean")
    G["fb"]=pd.cut(G["forecast"],[-0.01,0.001,2,4,8,21])
    fb=G.groupby("fb",observed=True).agg(n=("f72","size"),f72=("f72","mean"),exc=("exc","mean"),alloc=("a","mean"))
    D=pd.concat(days)
    tot=pd.Series(dict(gross_total=R.gross.sum(),fee_total=R.fee.sum(),turn_total=R.turn.sum(),
                       bars=R.n.sum(),book_daily_mean=D.book_return.mean(),coin_daily_mean=D.coin_return.mean()))
    # hold durations
    T=pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c]])
    tr=pd.Series(dict(ntr=len(T),dur_h_med=T.duration_minutes.median()/60,pl_mean=T.profit_loss_percent.mean(),
                      net_mean=T.net_profit_loss_percent.mean(),comm_mean=T.total_commission.mean()))
    return {"totals":tot,"by_coin":by_coin,"fc_bins":fb,"trades":tr}
