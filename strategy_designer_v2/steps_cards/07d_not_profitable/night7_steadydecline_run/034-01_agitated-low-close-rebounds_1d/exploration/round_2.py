def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l)
            b["clv"]=np.where(rng>0,(h-c)/rng,np.nan)
            b["rngpct"]=rng/c
            b["r1"]=c.shift(-1)/c-1
            b["tr60"]=c/c.shift(60)-1
            b["pos"]=b["postRebalance_current_allocation"].astype(float)
            b["gain"]=b["pos"]*b["r1"]
            b["coin"]=coin; b["w"]=w; b["wn"]=int(w[1:])
            b["agit"]=b["regime"]!="chop"
            b["fc"]=b["forecast"].astype(float)
            # range vs own past 60-day median range
            b["rrel"]=b["rngpct"]/b["rngpct"].rolling(60,min_periods=20).median().shift(1)
            rows.append(b[["coin","w","wn","clv","rngpct","rrel","r1","tr60","pos","gain","agit","fc"]])
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["r1"].mean(); d["x1"]=d["r1"]-d["coin"].map(mu)
    a=d[d.agit].dropna(subset=["clv","x1"]).copy()
    a["s"]=np.sign(a["clv"]-0.5); a["sx"]=a["s"]*a["x1"]
    a["rq"]=pd.qcut(a["rrel"],3,labels=["small","mid","big"])
    a["trend"]=pd.cut(a["tr60"],[-np.inf,-0.1,0.1,np.inf],labels=["falling","choppy","rising"])
    a["half"]=np.where(a.wn<=12,"w7-12","w13-18")
    def summ(g,col):
        s=g[col].dropna(); return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/s.std()*np.sqrt(len(s))})
    out={}
    out["signed x1 by rel-range tercile x half"]=a.groupby(["rq","half"]).apply(lambda g:summ(g,"sx"))
    # condition alone: unsigned x1 on big range days (any close), and long-only on big range
    out["condition alone: raw x1 by rel-range tercile"]=a.groupby("rq").apply(lambda g:summ(g,"x1"))
    a["side"]=np.where(a.s>0,"lowclose_long","highclose_short")
    out["signed x1 by rel-range x side"]=a.groupby(["rq","side"]).apply(lambda g:summ(g,"sx"))
    out["signed x1 by trend x side"]=a.groupby(["trend","side"]).apply(lambda g:summ(g,"sx"))
    out["condition alone: raw x1 by trend"]=a.groupby("trend").apply(lambda g:summ(g,"x1"))
    # graded: clv strength x range: strength = (clv-0.5)*rrel
    a["str"]=(a["clv"]-0.5)*a["rrel"]
    a["sq"]=pd.qcut(a["str"],5)
    out["x1 by quintile of (clv-0.5)*rel-range"]=a.groupby("sq").apply(lambda g:summ(g,"x1"))
    # book gross by rq and |pos|
    out["book gross% and mean|pos| by rel-range"]=a.groupby("rq").agg(gross=("gain",lambda s:s.mean()*100),abspos=("pos",lambda s:s.abs().mean()))
    out["mean |pos| by |forecast| bin"]=a.groupby(pd.cut(a.fc.abs(),[0,1,2,3,5,20]))["pos"].agg(lambda s:s.abs().mean())
    out["share of agitated bars by |forecast| bin"]=pd.cut(a.fc.abs(),[-0.01,1,2,3,5,20]).value_counts(normalize=True).sort_index()
    return out
