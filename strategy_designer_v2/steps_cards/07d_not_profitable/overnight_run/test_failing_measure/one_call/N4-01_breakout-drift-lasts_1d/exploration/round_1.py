def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    # book daily series per window
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c][w][["day","book_return","coin_return"]].copy()
            d["coin"] = c
            frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
        g["win"] = w
        rows.append(g)
    B = pd.concat(rows, ignore_index=True)
    B = B.dropna(subset=["book"])
    B["eq"] = (1+B["book"]).cumprod()
    B["peak"] = B["eq"].cummax()
    B["dd"] = B["eq"]/B["peak"]-1
    out["maxdd"] = float(B["dd"].min())
    ann = (B["eq"].iloc[-1])**(365/len(B))-1
    out["ann_ret"] = float(ann)
    # per window stats
    def wstat(g):
        eq=(1+g.book).cumprod(); dd=(eq/eq.cummax()-1).min()
        heq=(1+g.hold).cumprod()
        return pd.Series({"ret":eq.iloc[-1]-1,"hold":heq.iloc[-1]-1,"mdd":dd,"n":len(g)})
    out["per_window"] = B.groupby("win", sort=False).apply(wstat).round(3)
    # dd episodes: windows where global dd deepens
    B["ddnew"] = B["dd"] < B["dd"].shift(1).fillna(0)
    out["dd_by_window_min"] = B.groupby("win", sort=False)["dd"].min().round(3)
    # coin contributions to losses, per window where book window ret < 0
    contrib = {}
    for w in wins:
        contrib[w] = {c: float((1+data["days"][c][w]["book_return"].fillna(0)).prod()-1) for c in coins}
    out["coin_window_ret"] = pd.DataFrame(contrib).T.round(3)
    # trades: outcome by entry context
    T=[]
    for c in coins:
        for w in wins:
            t = data["trades"][c][w].copy()
            b = data["bars"][c][w].copy()
            if len(t)==0: continue
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["vol20"]=np.log(b["close"]).diff().rolling(20).std()
            b["r5"]=b["close"]/b["close"].shift(5)-1
            b["ma50"]=b["close"]/b["close"].rolling(50).mean()-1
            t["et"]=pd.to_datetime(t["entry_time"])
            m = pd.merge_asof(t.sort_values("et"), b[["ts","r20","vol20","r5","ma50"]].sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            m["coin"]=c; m["win"]=w
            T.append(m)
    T=pd.concat(T, ignore_index=True)
    T["pnl"]=T["net_profit_loss_percent"]
    out["trades_summary"]=pd.Series({"n":len(T),"mean":T.pnl.mean(),"median":T.pnl.median(),"win":(T.pnl>0).mean(),"dur_days_mean":T.duration_minutes.mean()/1440,"comm_mean":T.total_commission.mean(),"long_share":(T.side=="LONG").mean()})
    for col in ["r20","vol20","r5","ma50"]:
        T["q"]=pd.qcut(T[col],5,duplicates="drop")
        out["pnl_by_"+col]=T.groupby("q",observed=True)["pnl"].agg(["count","mean","median",lambda x:(x>0).mean()]).round(3)
    T["dq"]=pd.qcut(T.duration_minutes/1440,5,duplicates="drop")
    out["pnl_by_dur"]=T.groupby("dq",observed=True)["pnl"].agg(["count","mean","sum"]).round(3)
    return out
