def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 70: continue
            hi = b["high"].rolling(20, min_periods=20).max()
            lo = b["low"].rolling(20, min_periods=20).min()
            b["rp"] = 2*(b["close"]-lo)/(hi-lo)-1
            b["r1"] = b["close"].pct_change()
            b["r60"] = b["close"]/b["close"].shift(60)-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["v30"] = b["r1"].rolling(30).std()
            b["v60"] = b["r1"].rolling(60).std()
            b["agit"] = (b["v30"]>b["v60"]).astype(int)
            b["f10"] = b["close"].shift(-10)/b["close"]-1
            b["f5"] = b["close"].shift(-5)/b["close"]-1
            b["inprof"] = (b["regime"]=="unknown").astype(int)
            g = b.iloc[::10].copy()
            g["coin"]=coin; g["w"]=w
            g["day"]=pd.to_datetime(g["timestamp"]).dt.floor("D")
            rows.append(g)
    G = pd.concat(rows).dropna(subset=["f10","rp","r60"])
    drift = G.groupby("coin")["f10"].mean()
    G["ex10"] = G["f10"]-G["coin"].map(drift)
    G["trend"] = np.where(G["r60"]>0.10,"rising",np.where(G["r60"]<-0.10,"falling","choppy"))
    G["sig"] = G["rp"]*G["ex10"]
    def tt(df,key,col):
        r = df.groupby(key)[col].agg(["count","mean","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"])); return r.round(4)
    out={}
    out["rp*ex10 by trend x inprof"]=tt(G,["trend","inprof"],"sig")
    out["rp*ex10 by trend x agit(proxy)"]=tt(G,["trend","agit"],"sig")
    G["rpq"]=pd.cut(G["rp"],[-1.01,-0.33,0.33,1.01])
    out["ex10 by trend x rp tercile"]=tt(G,["trend","rpq"],"ex10")
    G["s20"]=np.sign(G["r20"])*G["ex10"]
    out["sign(r20)*ex10 by trend"]=tt(G,"trend","s20")
    out["rp*ex10 by window"]=tt(G[G.inprof==1],"w","sig")
    # per-day aggregated t for out-of-profile choppy rp effect
    sub=G[(G.trend=="choppy")]
    ds=sub.groupby("day")["sig"].sum()
    out["choppy rp*ex10 per-day t"]=pd.Series({"days":len(ds),"mean":ds.mean(),"t":ds.mean()/(ds.std()/np.sqrt(len(ds)))}).round(4)
    T=[]
    for coin, ws in trades.items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median","std"]).round(3)
    T["ef"]=pd.qcut(T["entry_forecast"].abs(),3,duplicates="drop")
    out["trades by |entry forecast|"]=T.groupby(["side","ef"])["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    return out
