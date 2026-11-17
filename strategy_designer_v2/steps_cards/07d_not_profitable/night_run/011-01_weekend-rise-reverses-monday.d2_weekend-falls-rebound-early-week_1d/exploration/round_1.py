def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; trows = []; drows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["wd"] = b["ts"].dt.dayofweek
            b["r1"] = b["close"].shift(-1)/b["close"] - 1
            b["r2"] = b["close"].shift(-2)/b["close"] - 1
            b["r3"] = b["close"].shift(-3)/b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["vol20"] = (b["close"].pct_change()).rolling(20).std()
            b["ret"] = b["close"].pct_change()
            b["z"] = b["ret"]/b["vol20"]
            b["ret7"] = b["close"]/b["close"].shift(7)-1
            b["ret30"] = b["close"]/b["close"].shift(30)-1
            b["coin"] = coin; b["win"] = w
            rows.append(b)
        t = data["trades"][coin]
        for w, tt in t.items():
            tt = tt.copy(); tt["coin"]=coin; trows.append(tt)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; drows.append(d)
    B = pd.concat(rows, ignore_index=True)
    T = pd.concat(trows, ignore_index=True)
    D = pd.concat(drows, ignore_index=True)
    # exposure by weekday
    out["pos_by_weekday"] = B.groupby("wd").agg(meanpos=("pos","mean"), share_in=("pos", lambda x:(x.abs()>1e-6).mean()), gain=("gain","mean"), r1=("r1","mean"))
    out["trade_duration_hours"] = T["duration_minutes"].describe()/60
    out["trades_pnl"] = pd.Series({"n":len(T),"mean_gross":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),"fee_mean":T["total_commission"].mean()})
    # sunday bars with forecast>0: forward returns by day
    S = B[(B["wd"]==6)]
    S = S.assign(fpos=S["forecast"]>0)
    out["sunday_fwd"] = S.groupby("fpos").agg(n=("r1","count"), r1=("r1","mean"), r2=("r2","mean"), r3=("r3","mean"))
    # incremental day returns after sunday fall
    S2 = S[S.fpos].copy()
    S2["d1"]=S2["r1"]; S2["d2"]=(1+S2["r2"])/(1+S2["r1"])-1; S2["d3"]=(1+S2["r3"])/(1+S2["r2"])-1
    out["after_fall_daily"] = S2[["d1","d2","d3"]].agg(["mean","std","count"])
    out["coin_mean_daily"] = B["ret"].mean()
    # by forecast tercile and 30d trend
    S2["fq"] = pd.qcut(S2["forecast"],3,labels=False,duplicates="drop")
    out["by_fq"] = S2.groupby("fq").agg(n=("r3","count"), r1=("r1","mean"), r3=("r3","mean"), fc=("forecast","mean"))
    S2["trend"] = np.sign(S2["ret30"])
    out["by_trend30"] = S2.groupby("trend").agg(n=("r3","count"), r1=("r1","mean"), r3=("r3","mean"))
    S2["vq"] = S2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["by_vol"] = S2.groupby("vq").agg(n=("r3","count"), r1=("r1","mean"), r3=("r3","mean"))
    # book daily
    out["book_daily"] = pd.Series({"book_mean":D["book_return"].mean(),"coin_mean":D["coin_return"].mean(),
        "book_sharpe":D["book_return"].mean()/D["book_return"].std()*np.sqrt(365),
        "coin_sharpe":D["coin_return"].mean()/D["coin_return"].std()*np.sqrt(365)})
    out["by_coin"] = S2.groupby("coin").agg(n=("r3","count"), r1=("r1","mean"), r3=("r3","mean"))
    return out
