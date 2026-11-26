def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; hi=b["high"].rolling(20).max(); lo=b["low"].rolling(20).min()
            b["rp"]=(c-lo)/(hi-lo)
            r1=c.pct_change()
            b["r1"]=r1
            b["vol20"]=r1.rolling(20).std()
            b["z1"]=r1/b["vol20"].shift(1)
            b["r5p"]=c/c.shift(5)-1
            b["z5"]=b["r5p"]/(b["vol20"].shift(5)*np.sqrt(5))
            b["ret20"]=c/c.shift(20)-1
            b["fwd"]=c.shift(-H)/c-1
            b["fwd1"]=c.shift(-1)/c-1
            b["inprof"]=(b["regime"]=="unknown").astype(int)
            b["vrank"]=b["vol20"].rolling(60,min_periods=30).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            rows.append(b[["coin","w","pos","rp","z1","z5","ret20","fwd","fwd1","inprof","vrank","wd","r1"]])
    d=pd.concat(rows)
    g=d[(d.pos%H==0)].dropna(subset=["fwd"]).copy()
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    def tab(df,col,q=5):
        df=df.dropna(subset=[col]).copy()
        df["b"]=pd.qcut(df[col],q,labels=False,duplicates="drop")
        a=df.groupby("b")["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.round(4)
    out={}
    for p in [1,0]:
        s=g[g.inprof==p]
        out[f"rangepos_q prof{p}"]=tab(s,"rp")
        out[f"z1_q prof{p}"]=tab(s,"z1")
        out[f"z5_q prof{p}"]=tab(s,"z5")
        out[f"ret20_q prof{p}"]=tab(s,"ret20")
        out[f"vrank_q prof{p}"]=tab(s,"vrank")
    # daily weekday effect (all bars)
    d2=d.dropna(subset=["fwd1"]).copy()
    d2["ex1"]=d2["fwd1"]-d2.groupby("coin")["fwd1"].transform("mean")
    wdt=d2.groupby("wd")["ex1"].agg(["mean","count","std"]); wdt["t"]=wdt["mean"]/(wdt["std"]/np.sqrt(wdt["count"]))
    out["weekday next-day excess (decision weekday)"]=wdt.round(5)
    # book by weekday and by window
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=coin; x["w"]=w; bk.append(x)
    bk=pd.concat(bk).dropna(subset=["book_return"])
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    out["book by window"]=bk.groupby("w")["book_return"].agg(["mean","count"]).round(5)
    out["book by coin"]=bk.groupby("coin")["book_return"].agg(["mean","count"]).round(5)
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades by side"]=tr.groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].agg(["mean","count"]).round(3)
    out["prof share"]=float(d.inprof.mean())
    return out
