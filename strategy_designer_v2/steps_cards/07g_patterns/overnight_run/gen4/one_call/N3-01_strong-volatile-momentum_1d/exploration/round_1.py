def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            c = d["close"].astype(float)
            r = np.log(c).diff()
            d["r1"] = r
            d["f1"] = r.shift(-1)
            d["f5"] = np.log(c.shift(-5) / c)
            d["ret20"] = c / c.shift(20) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol20"] = r.rolling(20).std()
            d["z"] = r / d["vol20"].shift(1)
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(d))
            d["alloc"] = d["postRebalance_current_allocation"].astype(float)
            rows.append(d[["coin","win","pos","r1","f1","f5","ret20","ret60","vol20","z","wd","forecast","regime","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    cm1 = A.groupby("coin")["r1"].mean()
    A["xf1"] = A["f1"] - A["coin"].map(cm1)
    G = A[A["pos"] % 5 == 0].copy()
    cm5 = G.groupby("coin")["f5"].mean()
    G["xf5"] = G["f5"] - G["coin"].map(cm5)
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # forecast buckets
    G["fb"] = pd.cut(G["forecast"], [-1,0,1e-9,2,10,20.1], labels=["0","tiny","0-2","2-10","10+"], include_lowest=True)
    out["xf5 by forecast bucket"] = G.groupby("fb")["xf5"].apply(summ).unstack()
    out["xf5 by regime"] = G.groupby("regime")["xf5"].apply(summ).unstack()
    # regimes by ret20/ret60 sign combos
    G["combo"] = np.sign(G["ret20"]).astype(str) + "/" + np.sign(G["ret60"]).astype(str)
    out["xf5 by ret20/ret60 sign"] = G.groupby("combo")["xf5"].apply(summ).unstack()
    # vol tercile within coin
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["xf5 by vol tercile"] = G.groupby("vq")["xf5"].apply(summ).unstack()
    out["xf5 by vol tercile x ret20 up"] = G.groupby(["vq", G["ret20"]>0])["xf5"].apply(summ).unstack()
    # large moves -> next day
    A["zb"] = pd.cut(A["z"], [-99,-2.5,-1.5,1.5,2.5,99])
    out["next-day excess by shock z"] = A.groupby("zb")["xf1"].apply(summ).unstack()
    # large moves -> next 5 (non overlap by shock events: take shock bars, keep spacing)
    ev = []
    for (coin,w), g in A.groupby(["coin","win"]):
        last = -10
        for i,row in g[g["z"].abs()>2].iterrows():
            if row["pos"]-last>=5:
                ev.append((coin, np.sign(row["z"]), row["f5"]- cm5[coin])); last=row["pos"]
    E = pd.DataFrame(ev, columns=["coin","sgn","x5"])
    out["5d excess after |z|>2 shock by sign"] = E.groupby("sgn")["x5"].apply(summ).unstack()
    out["weekday next-day excess"] = A.groupby("wd")["xf1"].apply(summ).unstack()
    # per coin forecast>=10
    out["10+ by coin"] = G[G["forecast"]>=10].groupby("coin")["xf5"].apply(summ).unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["days"] = T["duration_minutes"]/1440
    T["eb"] = pd.cut(T["entry_forecast"], [0,2,10,20.1])
    out["trades by entry fc"] = T.groupby("eb")["net_profit_loss_percent"].agg(["count","mean","median",lambda s:(s>0).mean()])
    out["trades by duration"] = T.groupby(pd.cut(T["days"],[0,2,5,10,30,999]))["net_profit_loss_percent"].agg(["count","mean",lambda s:(s>0).mean()])
    # book largest daily gains/losses: coin return prior 20d sign
    D = pd.concat([d.assign(coin=c) for c,ws in data["days"].items() for d in ws.values()], ignore_index=True)
    D = D.dropna(subset=["book_return"])
    act = D[D["book_return"].abs()>1e-9]
    q = act["book_return"].quantile([0.02,0.98])
    out["book extreme days: coin ret same day"] = pd.Series({"top_n": (act["book_return"]>q[0.98]).sum(),
        "top_coin_mean": act.loc[act["book_return"]>q[0.98],"coin_return"].mean(),
        "bot_coin_mean": act.loc[act["book_return"]<q[0.02],"coin_return"].mean(),
        "share_active_days": len(act)/len(D)})
    return out
