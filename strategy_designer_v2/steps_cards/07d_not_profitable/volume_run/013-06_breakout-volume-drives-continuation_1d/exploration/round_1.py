def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily returns pooled: mean across coins per day? compute per coin-window then pool
    rows=[]; trows=[]; brows=[]
    for c in data["bars"]:
        for w in data["bars"][c]:
            b = data["bars"][c][w].copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["ret1"]
            b["inpos"] = b["postRebalance_current_allocation"].abs()>1e-6
            b["fwd30"] = b["close"].shift(-30)/b["close"]-1
            b["fwd5"] = b["close"].shift(-5)/b["close"]-1
            b["past30"] = b["close"]/b["close"].shift(30)-1
            b["coin"]=c; b["win"]=w
            brows.append(b[["coin","win","forecast","postRebalance_current_allocation","ret1","gain","inpos","fwd30","fwd5","past30","regime"]])
            t = data["trades"][c][w].copy(); t["coin"]=c; t["win"]=w; trows.append(t)
            d = data["days"][c][w].copy(); d["coin"]=c; d["win"]=w; rows.append(d)
    B = pd.concat(brows); T = pd.concat(trows); D = pd.concat(rows)
    out["exposure share of bars"] = float(B["inpos"].mean())
    out["new-high bars share"] = float((B["regime"]=="trending").mean())
    ip = B[B["inpos"]]
    out["held bars: mean gain, mean ret1, n"] = pd.Series({"gain":ip["gain"].mean(),"ret1":ip["ret1"].mean(),"alloc":ip["postRebalance_current_allocation"].mean(),"n":len(ip)})
    out["trades summary"] = pd.Series({"n":len(T),"mean dur days":T["duration_minutes"].mean()/1440,"median dur days":T["duration_minutes"].median()/1440,
        "mean pl":T["profit_loss_percent"].mean(),"mean net":T["net_profit_loss_percent"].mean(),"win share":(T["net_profit_loss_percent"]>0).mean(),
        "mean comm":T["total_commission"].mean()})
    T["dq"]=pd.cut(T["duration_minutes"]/1440,[0,1.5,3,7,15,1000])
    out["trades by duration"]=T.groupby("dq")["net_profit_loss_percent"].agg(["count","mean","median"])
    # held bars by forecast quintile
    tr = B[B["regime"]=="trending"].copy()
    tr["fq"]=pd.qcut(tr["forecast"].rank(method="first"),4,labels=False)
    out["new-high bars by forecast quartile"]=tr.groupby("fq").agg(fc=("forecast","mean"),n=("ret1","size"),ret1=("ret1","mean"),fwd5=("fwd5","mean"),fwd30=("fwd30","mean"),alloc=("postRebalance_current_allocation","mean"))
    # past30 at new highs
    tr["pq"]=pd.qcut(tr["past30"],4,labels=False)
    out["new-high bars by past 30d return quartile"]=tr.groupby("pq").agg(p30=("past30","mean"),n=("ret1","size"),ret1=("ret1","mean"),fwd5=("fwd5","mean"),fwd30=("fwd30","mean"))
    # book daily
    D["br"]=D["book_return"]
    out["book daily by year"]=D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y")["br"].agg(["mean","std","count"])
    # worst book days: what held
    worst = D.nsmallest(15,"br")[["coin","win","br","coin_return"]]
    out["worst book days by coin"]=worst.groupby("coin")["br"].agg(["count","sum"])
    out["worst 15 mean br, coin_ret"]=pd.Series({"br":worst["br"].mean(),"coin":worst["coin_return"].mean()})
    out["by coin held gain"]=ip.groupby("coin")["gain"].agg(["mean","count"])
    return out
