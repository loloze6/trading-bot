def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(b["high"]-c)/rng
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r":r,"z":r/sd,"cl":cl,"agit":(b["regime"]!="chop"),
                "f":b["forecast"],"pos":b["postRebalance_current_allocation"],
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"n3":c.shift(-3)/c-1,
                "r5":c/c.shift(5)-1,"r20":c/c.shift(20)-1})
            d["n2g"]=np.arange(len(d))%2==0; d["n3g"]=np.arange(len(d))%3==0
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["n1"].transform("mean"); D["x1"]=D["n1"]-mu
    mu2=D[D.n2g].groupby("coin")["n2"].mean(); D["x2"]=D["n2"]-D["coin"].map(mu2)
    mu3=D[D.n3g].groupby("coin")["n3"].mean(); D["x3"]=D["n3"]-D["coin"].map(mu3)
    D["year"]=D.ts.dt.year; D["wd"]=D.ts.dt.weekday
    def summ(g,col="x1"):
        v=g[col].dropna(); n=len(v)
        return pd.Series({"n":n,"mean%":100*v.mean(),"t":v.mean()/(v.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["zb"]=pd.cut(D.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    D["clb"]=pd.cut(D.cl,[-0.01,0.2,0.5,0.8,1.01])
    out["z bin x agit next1"]=D.groupby(["agit","zb"]).apply(summ)
    out["down days: cl bin x agit next1"]=D[D.r<0].groupby(["agit","clb"]).apply(summ)
    out["up days: cl bin x agit next1"]=D[D.r>0].groupby(["agit","clb"]).apply(summ)
    dn=D[(D.r<0)&D.agit].copy(); dn["fq"]=pd.qcut(dn.z*-1*dn.cl,5,labels=False,duplicates="drop")
    out["agit down: fall*cl quintile, n1,n2,n3"]=pd.concat({h:dn[dn[g] if g else slice(None)].groupby("fq").apply(lambda q:summ(q,h)) if g else dn.groupby("fq").apply(lambda q:summ(q,h)) for h,g in [("x1",None),("x2","n2g"),("x3","n3g")]},axis=1)
    cd=D[(D.r<0)&~D.agit].copy(); cd["fq"]=pd.qcut(cd.z*-1*cd.cl,5,labels=False,duplicates="drop")
    out["calm down: fall*cl quintile n1"]=cd.groupby("fq").apply(summ)
    D["r5b"]=pd.qcut(D.r5,5,labels=False); D["r20b"]=pd.qcut(D.r20,5,labels=False)
    out["agit r5 quintile n1"]=D[D.agit].groupby("r5b").apply(summ)
    out["calm r5 quintile n1"]=D[~D.agit].groupby("r5b").apply(summ)
    out["agit r20 quintile n1"]=D[D.agit].groupby("r20b").apply(summ)
    out["weekday x agit n1"]=D.groupby(["wd"]).apply(summ)
    out["signal (f>0) by year n1"]=D[D.f>0].groupby("year").apply(summ)
    out["signal by coin"]=D[D.f>0].groupby("coin").apply(summ)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    DD=pd.concat(dd); DD["day"]=pd.to_datetime(DD["day"])
    bk=DD.groupby("day").agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    bk["year"]=bk.index.year
    out["book by year"]=bk.groupby("year").agg(mean=("br","mean"),sd=("br","std"),n=("br","size"),coin=("cr","mean"))
    q=bk.br.quantile([0.01,0.99])
    out["coin ret on book worst1%/best1% days"]=pd.Series({"worst n":(bk.br<=q.iloc[0]).sum(),"worst coin mean%":100*bk.cr[bk.br<=q.iloc[0]].mean(),"best coin mean%":100*bk.cr[bk.br>=q.iloc[1]].mean(),"share sum gain from best1%":bk.br[bk.br>=q.iloc[1]].sum()/bk.br.sum(),"share loss worst1%":bk.br[bk.br<=q.iloc[0]].sum()/bk.br.sum()})
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    tr["dur_d"]=tr.duration_minutes/1440
    out["trades"]=pd.Series({"n":len(tr),"mean pl%":tr.profit_loss_percent.mean(),"mean net%":tr.net_profit_loss_percent.mean(),"median dur d":tr.dur_d.median(),"mean dur d":tr.dur_d.mean(),"win share":(tr.profit_loss_percent>0).mean()})
    return out
