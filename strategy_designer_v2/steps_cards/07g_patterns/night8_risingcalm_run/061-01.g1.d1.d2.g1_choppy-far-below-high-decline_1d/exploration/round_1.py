def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            fwd=c.shift(-H)/c-1
            gap=c/c.rolling(20).max()-1
            sd20=r.rolling(20).std().shift(1)
            z=r/sd20
            r5=c/c.shift(5)-1
            vol=b["sizing_realised_vol"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"fwd":fwd,"gap":gap,"z":z,"r1":r,
                             "r5":r5,"regime":b["regime"],"fc":b["forecast"].astype(float),
                             "alloc":b["postRebalance_current_allocation"].astype(float),"vol":vol,
                             "wd":ts.dt.weekday})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["choppy"]=(A["regime"]=="unknown")
    mu=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(mu)
    A["volhi"]=A.groupby("coin")["vol"].transform(lambda s: s>s.median())
    G=A[(A.pos%H==0)&A.ex.notna()].copy()
    def summ(g,col="ex"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    # gap quintiles by trend regime
    G["gapq"]=pd.qcut(G["gap"].rank(method="first"),5,labels=False)
    out["gap quintile x choppy (ex 5d)"]=G.groupby(["choppy","gapq"]).apply(summ).reset_index()
    # big day in swing units, signed continuation
    G["zs"]=np.sign(G["z"])*G["ex"]
    G["zq"]=pd.qcut(G["z"].rank(method="first"),6,labels=False)
    out["z sextile x choppy (ex 5d)"]=G.groupby(["choppy","zq"]).apply(summ).reset_index()
    out["z sextile x volhi (ex 5d)"]=G.groupby(["volhi","zq"]).apply(summ).reset_index()
    G["r5q"]=pd.qcut(G["r5"].rank(method="first"),5,labels=False)
    out["5d past ret quintile x volhi"]=G.groupby(["volhi","r5q"]).apply(summ).reset_index()
    # weekday next-day return
    A["fwd1"]=A.groupby(["coin","w"])["r1"].shift(-1)
    out["weekday next-day ret"]=A.groupby("wd").apply(lambda g: summ(g,"fwd1")).reset_index()
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window (mean% , sum%)"]=bk.groupby(level=0).agg(lambda s:100*s.mean()).to_frame("mean%").join(bk.groupby(level=0).sum().mul(100).rename("sum%"))
    # trades
    trs=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; trs.append(t)
    T=pd.concat(trs)
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
