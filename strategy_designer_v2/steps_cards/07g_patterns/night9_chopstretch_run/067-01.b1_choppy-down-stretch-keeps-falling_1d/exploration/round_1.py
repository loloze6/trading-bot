def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c-sma)/sma/sd
            sd30=r.rolling(30).std()
            ret5b=c/c.shift(5)-1
            ret1=r
            rng=(b["high"]-b["low"])/c
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            yr=pd.to_datetime(b["timestamp"]).dt.year
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"sd30":sd30,"r1":ret1,"r5b":ret5b,"rng":rng,
                             "fwd":fwd,"fwd1":fwd1,"wd":wd,"yr":yr,"reg":b["regime"].astype(str),
                             "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"pos":np.arange(len(b)),
                             "sd20":sd})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    A["exs"]=A["ex"]/A["coin"].map(A[A.pos%H==0].groupby("coin")["fwd"].std())
    medsd=A.groupby("coin")["sd30"].median()
    A["agit"]=np.where(A["sd30"]>A["coin"].map(medsd),"agit","calm")
    A["choppy"]=np.where(A["reg"]=="unknown","choppy","trend")
    G=A[(A.pos%H==0)&A.ex.notna()&A.z.notna()].copy()
    G["zq"]=pd.qcut(G["z"],5,labels=False)
    def summ(g):
        n=len(g); m=g["ex"].mean(); t=m/(g["ex"].std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series({"n":n,"zmean":g["z"].mean(),"ex%":100*m,"t":t,"str":g["exs"].mean()})
    out={}
    out["regime counts"]=A["reg"].value_counts()
    out["z quintile x choppy"]=G.groupby(["choppy","zq"]).apply(summ)
    out["z quintile x agit (choppy)"]=G[G.choppy=="choppy"].groupby(["agit","zq"]).apply(summ)
    out["z quintile all"]=G.groupby("zq").apply(summ)
    # slopes
    res={}
    for k,g in [("all",G),("choppy",G[G.choppy=="choppy"]),("trend",G[G.choppy=="trend"]),
                ("chop_up",G[(G.choppy=="choppy")&(G.z>0)]),("chop_dn",G[(G.choppy=="choppy")&(G.z<0)]),
                ("trend_up",G[(G.choppy=="trend")&(G.z>0)]),("trend_dn",G[(G.choppy=="trend")&(G.z<0)])]:
        s=stats.linregress(g["z"],g["exs"]); res[k]=[len(g),s.slope,s.slope/s.stderr]
    out["slope exs on z"]=pd.DataFrame(res,index=["n","slope","t"]).T
    # prior 5d return and 1d range
    G["r5q"]=pd.qcut(G["r5b"],5,labels=False)
    out["prior5d quintile"]=G.groupby(["choppy","r5q"]).apply(summ)
    G["rngq"]=pd.qcut(G["rng"]/G["sd20"],5,labels=False)
    out["range/sd quintile"]=G.groupby("rngq").apply(summ)
    out["weekday all bars fwd1"]=A.groupby("wd")["fwd1"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["by window choppy dn slope"]=G[(G.choppy=="choppy")&(G.z<0)].groupby("w").apply(lambda g: pd.Series({"n":len(g),"ex%":100*g.ex.mean(),"corr":g[["z","ex"]].corr().iloc[0,1]}))
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["count","mean","sum"])
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t.assign(coin=coin,w=w))
    T=pd.concat(T)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
