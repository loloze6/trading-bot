def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30).std()
            mx5=c.rolling(5).max()
            dip=(c-mx5)/mx5/sd30
            r60=c/c.shift(60)-1
            r5p=c/c.shift(5)-1
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"dip":dip,"sd30":sd30,
                "r60":r60,"r5p":r5p,"r1":r1,"fwd5":fwd5,"fwd1":fwd1,"regime":b["regime"].values,
                "wd":ts.dt.weekday,"yr":ts.dt.year,"alloc":b["postRebalance_current_allocation"].values})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    # drift per coin
    G=A[A.pos%5==0].dropna(subset=["fwd5"]).copy()
    drift=G.groupby("coin")["fwd5"].mean()
    G["ex5"]=G["fwd5"]-G["coin"].map(drift)
    # vol level relative to coin median
    G["volhi"]=G["sd30"]>G["coin"].map(A.groupby("coin")["sd30"].median())
    G["rising"]=G["regime"]!="chop"
    G["trend"]=np.where(G.r60>0.1,"rising",np.where(G.r60<-0.1,"falling",np.where(G.r60.notna(),"choppy","na")))
    def summ(g):
        x=g["ex5"].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    G["dipq"]=pd.qcut(G["dip"],5,labels=False,duplicates="drop")
    out["dip quintile x rising (regime col)"]=G.groupby(["rising","dipq"]).apply(summ)
    out["dip quintile x rising x volhi"]=G[G.rising].groupby(["volhi","dipq"]).apply(summ)
    out["trend60 x dipq"]=G[G.trend!="na"].groupby(["trend","dipq"]).apply(summ)
    G["r5q"]=pd.qcut(G["r5p"],5,labels=False)
    out["past5 return quintile x trend"]=G[G.trend!="na"].groupby(["trend","r5q"]).apply(summ)
    # large 1-day moves scaled
    G["z1"]=G["r1"]/G["sd30"]
    G["z1b"]=pd.cut(G["z1"],[-99,-2,-1,0,1,2,99])
    out["1d scaled move bin x volhi"]=G.groupby(["volhi","z1b"]).apply(summ)
    out["vol high/low overall"]=G.groupby(["volhi","rising"]).apply(summ)
    # weekday on daily returns
    D=A.dropna(subset=["fwd1"]).copy()
    D["ex1"]=D["fwd1"]-D["coin"].map(D.groupby("coin")["fwd1"].mean())
    out["weekday next-day excess"]=D.groupby("wd")["ex1"].agg(lambda x: pd.Series([len(x),100*x.mean(),x.mean()/(x.std()/np.sqrt(len(x)))]).round(3).tolist()).astype(str)
    out["year x rising"]=G.groupby(["yr","rising"]).apply(summ)
    # book daily
    days=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;days.append(d)
    Dd=pd.concat(days)
    bk=Dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["mean","std","count"]).mul(1).round(5)
    q=bk["book_return"]
    top=bk[q>=q.quantile(0.95)];bot=bk[q<=q.quantile(0.05)]
    out["book extremes coin_return"]=pd.DataFrame({"top5%":top.mean(),"bot5%":bot.mean(),"corr":[bk.corr().iloc[0,1]]*2},index=["book_return","coin_return"])
    return out
