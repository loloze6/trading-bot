def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["nxt"] = b["close"].shift(-1)/b["close"] - 1
            b["ret"] = b["close"].pct_change()
            b["r60"] = b["close"]/b["close"].shift(60) - 1
            b["r20"] = b["close"]/b["close"].shift(20) - 1
            b["r5"] = b["close"]/b["close"].shift(5) - 1
            b["s20"] = b["ret"].rolling(20).std()
            b["rng"] = (b["high"]-b["low"])/b["close"]/b["s20"]
            b["loc"] = (b["high"]-b["close"])/(b["high"]-b["low"]).replace(0,np.nan)
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"]*b["nxt"]
            b["coin"] = c; b["win"] = w
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - mu
    d["q"] = d.groupby("coin")["forecast"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    g = d.groupby("q").agg(n=("ex","size"), fc=("forecast","mean"), ex=("ex","mean"), nxt=("nxt","mean"),
                           alloc=("alloc","mean"), gain=("gain","mean"), sd=("nxt","std"))
    out["by forecast fifth"] = g
    d["tr"] = pd.cut(d["r60"], [-9,-0.1,0.1,99], labels=["falling","choppy","rising"])
    d["tr20"] = pd.cut(d["r20"], [-9,-0.1,0.1,99], labels=["down20","flat20","up20"])
    d["top"] = d["q"]>=3
    out["by trend60 x top2fifths"] = d.groupby(["tr","top"]).agg(n=("ex","size"), nxt=("nxt","mean"), gain=("gain","mean"), alloc=("alloc","mean"))
    out["by trend20 x top2fifths"] = d.groupby(["tr20","top"]).agg(n=("ex","size"), nxt=("nxt","mean"), gain=("gain","mean"), alloc=("alloc","mean"))
    # book daily, drawdown
    dd = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"]=c; x["win"]=w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
    order = {f"w{i}":i for i in range(1,40)}
    bk["o"] = bk["win"].map(order); bk = bk.sort_values(["o","day"]).dropna()
    v = (1+bk["b"]).cumprod(); hv = (1+bk["h"]).cumprod()
    bk["dd"] = v/v.cummax()-1
    out["window summary"] = bk.groupby("win").agg(n=("b","size"), book=("b","mean"), hold=("h","mean"),
                    bsd=("b","std"), worst=("dd","min")).sort_values("worst")
    out["max dd"] = float(bk["dd"].min())
    # book on days when hold falls hard
    bk["hq"] = pd.qcut(bk["h"], 5, labels=False)
    out["book vs hold fifth"] = bk.groupby("hq").agg(h=("h","mean"), b=("b","mean"))
    out["alloc mean"] = float(d["alloc"].mean())
    out["share forecast>0"] = float((d["forecast"]>0).mean())
    # range alone vs loc alone
    d["rq"] = d.groupby("coin")["rng"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    d["lq"] = pd.cut(d["loc"], [-0.01,0.33,0.67,1.01], labels=["nearHigh","mid","nearLow"])
    out["range fifth x loc"] = d.pivot_table(index="rq", columns="lq", values="ex", aggfunc="mean")
    out["range fifth x loc n"] = d.pivot_table(index="rq", columns="lq", values="ex", aggfunc="size")
    return out
