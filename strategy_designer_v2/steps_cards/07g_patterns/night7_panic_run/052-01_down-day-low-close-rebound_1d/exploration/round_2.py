def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            d=pd.DataFrame({"ts":pd.to_datetime(b["timestamp"])})
            d["coin"]=coin; d["win"]=w
            d["pos"]=np.arange(len(d))
            d["ret"]=c/c.shift(1)-1
            d["nxt"]=c.shift(-1)/c-1
            d["nxt3"]=c.shift(-3)/c-1
            rng=(h-l)
            d["nearlow"]=np.where(rng>0,(h-c)/rng,np.nan)
            d["rngpct"]=rng/c
            d["body"]=np.where(rng>0,(c-o)/rng,np.nan)
            d["ret5"]=c/c.shift(5)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["tr60"]=c/c.shift(60)-1
            d["alloc"]=b["postRebalance_current_allocation"].astype(float).values
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["gain"]=D["alloc"]*D["nxt"]
    hold=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(hold)
    hold3=D[D.pos%3==0].groupby("coin")["nxt3"].mean()
    D["ex3"]=D["nxt3"]-D["coin"].map(hold3)
    def summ(g,col="ex"):
        x=g[col].dropna()
        n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean() if n else np.nan,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    def q(s,k):
        return pd.qcut(s.rank(method="first"),k,labels=False)
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err "+str(e)[:80]
    D["down"]=D["ret"]<0
    D["rq"]=D.groupby("coin")["ret"].transform(lambda s:q(s,10))
    safe("next ex by day-return decile",lambda: D.groupby("rq").apply(summ))
    D["nlq"]=D.groupby(["coin","down"])["nearlow"].transform(lambda s:q(s,5))
    safe("next ex by down x nearlow quintile",lambda: D.groupby(["down","nlq"]).apply(summ))
    D["rgq"]=D.groupby("coin")["rngpct"].transform(lambda s:q(s,5))
    safe("down days next ex by range quintile",lambda: D[D.down].groupby("rgq").apply(summ))
    safe("up days next ex by range quintile",lambda: D[~D.down].groupby("rgq").apply(summ))
    safe("down days nearlow top quintile x range quintile",lambda: D[D.down&(D.nlq==4)].groupby("rgq").apply(summ))
    safe("down days ex3 (grid) by nearlow q",lambda: D[D.down&(D.pos%3==0)].groupby("nlq").apply(lambda g:summ(g,"ex3")))
    safe("next ex by weekday",lambda: D.groupby("wd").apply(summ))
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda s:q(s,3))
    safe("down nlq0/4 by vol tercile",lambda: D[D.down&D.nlq.isin([0,4])].groupby(["vq","nlq"]).apply(summ))
    D["tr"]=pd.cut(D["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    safe("down nlq0/4 by trend",lambda: D[D.down&D.nlq.isin([0,4])].groupby(["tr","nlq"]).apply(summ))
    D["r5q"]=D.groupby("coin")["ret5"].transform(lambda s:q(s,5))
    safe("next ex by 5d return quintile (all days)",lambda: D.groupby("r5q").apply(summ))
    safe("by coin down nlq top-bot mean%",lambda: D[D.down&D.nlq.isin([0,4])].groupby(["coin","nlq"])["ex"].mean().unstack()*100)
    safe("by year down top quintile",lambda: D[D.down&(D.nlq==4)].groupby("year").apply(summ))
    safe("by window down top quintile",lambda: D[D.down&(D.nlq==4)].groupby("win").apply(summ))
    # book: gain by profile and by allocation bucket
    safe("book gain% by trend (in position)",lambda: D[D.alloc>0].groupby("tr").apply(lambda g:summ(g,"gain")))
    safe("book gain% by vol tercile",lambda: D[D.alloc>0].groupby("vq").apply(lambda g:summ(g,"gain")))
    # largest book gains/losses: what preceded
    G=D[D.alloc>0].dropna(subset=["gain"])
    lo=G.gain.quantile(0.05); hi=G.gain.quantile(0.95)
    safe("before worst/best 5% book bars",lambda: pd.DataFrame({
        "worst":G[G.gain<=lo][["ret","nearlow","rngpct","ret5","tr60","alloc"]].mean(),
        "best":G[G.gain>=hi][["ret","nearlow","rngpct","ret5","tr60","alloc"]].mean(),
        "all":G[["ret","nearlow","rngpct","ret5","tr60","alloc"]].mean()}))
    # up days: close near high continuation?
    D["nhq"]=D["nlq"]
    safe("up days by close location q (0=near high)",lambda: D[~D.down].groupby("nlq").apply(summ))
    return out
