def explore(data):
    import pandas as pd, numpy as np
    bars, days = data["bars"], data["days"]
    coins = list(days.keys())
    wins = list(days[coins[0]].keys())
    out = {}
    # book daily
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        b = df.groupby("day")["book_return"].mean().dropna()
        h = df.groupby("day")["coin_return"].mean().dropna()
        for i,(dd,v) in enumerate(b.items()):
            rows.append((w, dd, v, h.get(dd, np.nan)))
    bk = pd.DataFrame(rows, columns=["w","day","r","h"])
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    # per-window stats
    def ws(g):
        eq = (1+g["r"]).cumprod()
        dd = (eq/eq.cummax()-1).min()
        heq=(1+g["h"].fillna(0)).cumprod(); hdd=(heq/heq.cummax()-1).min()
        return pd.Series({"n":len(g),"ret":eq.iloc[-1]-1,"maxdd":dd,"hold_ret":heq.iloc[-1]-1,"hold_dd":hdd,"year":g["year"].iloc[0]})
    out["windows"] = bk.groupby("w", sort=False).apply(ws).round(4)
    # whole book equity in window order
    eq = (1+bk["r"]).cumprod(); ddser = eq/eq.cummax()-1
    bk["dd"]=ddser.values
    out["overall"] = pd.Series({"maxdd":ddser.min(),"ann_ret":(eq.iloc[-1])**(365/len(bk))-1,"worst_day":bk["r"].min(),"share_days_lt_-3pct":(bk["r"]<-0.03).mean()})
    # bar-level features per coin
    feats=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            cl=b["close"]
            b["sma"]=cl.rolling(20).mean()
            b["dist"]=cl/b["sma"]-1
            b["ret20"]=cl.pct_change(20)
            b["ret5"]=cl.pct_change(5)
            b["vol20"]=cl.pct_change().rolling(20).std()
            b["vol_ratio"]=b["vol20"]/cl.pct_change().rolling(60).std()
            b["next"]=cl.shift(-1)/cl-1
            b["active"]=b["forecast"]>0
            b["coin"]=c; b["w"]=w
            feats.append(b[["coin","w","forecast","dist","ret20","ret5","vol20","vol_ratio","next","active"]])
    F=pd.concat(feats).dropna(subset=["next","dist","ret20","vol20"])
    A=F[F["active"]]
    res={}
    for f in ["dist","ret20","ret5","vol20","vol_ratio","forecast"]:
        q=pd.qcut(A[f].rank(method="first"),5,labels=False)
        g=A.groupby(q)["next"]
        res[f]=g.mean()
    tab=pd.DataFrame(res); tab.index.name="quintile"
    out["active_next1_by_feature_quintile"]=(tab*1e4).round(1)
    q=pd.qcut(A["ret20"].rank(method="first"),5,labels=False)
    out["ret20_quintile_bounds"]=A.groupby(q)["ret20"].agg(["min","max","count"]).round(3)
    qv=pd.qcut(A["dist"].rank(method="first"),5,labels=False)
    out["dist_quintile_bounds"]=A.groupby(qv)["dist"].agg(["min","max"]).round(3)
    out["active_share"]=F["active"].mean()
    return out
