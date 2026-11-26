def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["nxt"] = b["close"].shift(-1)/b["close"] - 1
            b["ret"] = b["close"].pct_change()
            b["r20"] = b["close"]/b["close"].shift(20) - 1
            b["r5"] = b["close"]/b["close"].shift(5) - 1
            b["s20"] = b["ret"].rolling(20).std()
            b["s5"] = b["ret"].rolling(5).std()
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["win"] = w; b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    order = {f"w{i}":i for i in range(1,40)}
    d["o"] = d["win"].map(order)
    cost = 0.0019/2
    def book(pos):
        x = d[["coin","win","o","day","nxt"]].copy()
        x["p"] = pos.values
        x["turn"] = x.groupby(["coin","win"])["p"].diff().abs().fillna(x["p"].abs())
        x["g"] = x["p"]*x["nxt"].fillna(0) - x["turn"]*cost
        bk = x.groupby(["o","day"])["g"].mean().sort_index()
        v = (1+bk).cumprod(); ddn = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(bk))-1
        return pd.Series({"mean":bk.mean(),"sharpe":bk.mean()/bk.std()*np.sqrt(365),
                          "yr":yr,"maxdd":ddn,"calmar":yr/-ddn,"inpos":(x["p"]>0).mean(),
                          "turn":x["turn"].mean()})
    f = d["forecast"]; a = d["alloc"]
    vt = (0.382/np.sqrt(365))/d["s20"].replace(0,np.nan)
    vt = vt.clip(upper=2).fillna(0)
    res = {}
    res["actual alloc"] = book(a)
    res["fc>=10, actual alloc"] = book(a.where(f>=10,0))
    res["fc>=14, actual alloc"] = book(a.where(f>=14,0))
    res["fc>=18, actual alloc"] = book(a.where(f>=18,0))
    res["alloc*(fc-10)+/10"] = book(a*((f-10).clip(lower=0)/10))
    res["fc>=10 and r20<0"] = book(a.where((f>=10)&(d["r20"]<0),0))
    res["fc>=10 and r20>0"] = book(a.where((f>=10)&(d["r20"]>0),0))
    res["fc>=10 and r5<0"] = book(a.where((f>=10)&(d["r5"]<0),0))
    res["fc>=10 and r5>0"] = book(a.where((f>=10)&(d["r5"]>0),0))
    out["variant books (approx, cost 0.095%/unit turnover)"] = pd.DataFrame(res).T
    # condition alone vs with signal
    d["top"] = f>=10
    d["r5s"] = np.sign(d["r5"])
    d["ret_s"] = np.sign(d["ret"])
    out["nxt by top x sign r5"] = d.groupby(["top","r5s"]).agg(n=("nxt","size"),nxt=("nxt","mean"),sd=("nxt","std"))
    out["nxt by top x sign today ret"] = d.groupby(["top","ret_s"]).agg(n=("nxt","size"),nxt=("nxt","mean"),sd=("nxt","std"))
    # deepest fall days: book loss days in w14
    x = d.copy(); x["g"]=x["alloc"]*x["nxt"]
    bk = x.groupby(["o","day"]).agg(g=("g","mean"),h=("nxt","mean"),fc=("forecast","mean"),al=("alloc","mean")).sort_index()
    v=(1+bk["g"]).cumprod(); bk["dd"]=v/v.cummax()-1
    bk["indd"] = bk["dd"]<-0.15
    out["days in deep fall vs not"] = bk.groupby("indd").agg(n=("g","size"),g=("g","mean"),h=("h","mean"),fc=("fc","mean"),al=("al","mean"))
    # forecast fifth contribution to losses on worst hold days
    bk["hq"]=pd.qcut(bk["h"],5,labels=False)
    x = x.merge(bk[["hq"]].reset_index(), on=["o","day"])
    x["fq"]=pd.cut(x["forecast"],[-1,5,10,15,21],labels=["0-5","5-10","10-15","15-20"])
    out["gain by fc band x hold-day fifth"] = x.pivot_table(index="fq",columns="hq",values="g",aggfunc="sum")
    # nxt by forecast bands, t
    gg = x.groupby("fq")["nxt"]
    out["nxt by fc band"] = pd.DataFrame({"n":gg.size(),"mean":gg.mean(),"t":gg.mean()/(gg.std()/np.sqrt(gg.size()))})
    return out
