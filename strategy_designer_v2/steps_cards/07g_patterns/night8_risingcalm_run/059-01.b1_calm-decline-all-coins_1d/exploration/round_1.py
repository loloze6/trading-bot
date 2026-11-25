def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30,min_periods=20).std()
            s14=(c/c.shift(14)-1)/(sd30*np.sqrt(14))
            s1=r1/sd30
            tr60=c/c.shift(60)-1 if len(c)>70 else pd.Series(np.nan,index=c.index)
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            rng=(b["high"]-b["low"])/c/sd30
            clo=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"s14":s14,"s1":s1,"tr60":tr60,
                "f5":f5,"f1":f1,"agit":(b["regime"]=="chop"),"fc":b["forecast"],"rng":rng,"clo":clo,
                "wd":ts.dt.weekday,"yr":ts.dt.year,"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%5==0)&D.f5.notna()].copy()
    drift=G.groupby("coin").f5.mean()
    G["x5"]=G.f5-G.coin.map(drift)
    def summ(g,col="x5"):
        v=g[col].dropna()
        return pd.Series({"n":len(v),"mean%":100*v.mean(),"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
    out={}
    G["q14"]=pd.qcut(G.s14,5,labels=False)
    out["s14 quintile x agit -> excess 5d"]=G.dropna(subset=["q14"]).groupby(["agit","q14"]).apply(summ).round(3)
    G["q1"]=pd.qcut(G.s1,5,labels=False)
    out["1d scaled move quintile x agit -> excess 5d"]=G.dropna(subset=["q1"]).groupby(["agit","q1"]).apply(summ).round(3)
    G["trend"]=pd.cut(G.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["trend x agit x s14 neg/pos -> excess 5d"]=G.dropna(subset=["trend","s14"]).assign(neg=lambda x:x.s14<0).groupby(["trend","agit","neg"]).apply(summ).round(3)
    G["qr"]=pd.qcut(G.rng,4,labels=False)
    out["range quartile x lowclose -> excess 5d"]=G.dropna(subset=["qr","clo"]).assign(low=lambda x:x.clo<0.33).groupby(["qr","low"]).apply(summ).round(3)
    D1=D[D.f1.notna()].copy()
    d1=D1.groupby("coin").f1.mean(); D1["x1"]=D1.f1-D1.coin.map(d1)
    out["weekday -> excess next day"]=D1.groupby("wd").apply(lambda g:summ(g,"x1")).round(3)
    # book days
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    DD=pd.concat(dd,ignore_index=True)
    book=DD.groupby(["w","day"]).agg(b=("book_return","mean"),c=("coin_return","mean")).dropna()
    out["book by window"]=book.groupby("w").agg(meanb=("b",lambda x:100*x.mean()),meanc=("c",lambda x:100*x.mean()),n=("b","size")).round(3)
    q=book.b.quantile([0.02,0.98])
    out["coin ret on book extreme days"]=pd.DataFrame({"worst2%":[100*book[book.b<=q.iloc[0]].c.mean(),(book.b<=q.iloc[0]).sum()],"best2%":[100*book[book.b>=q.iloc[1]].c.mean(),(book.b>=q.iloc[1]).sum()]},index=["coin mean%","n"]).round(3)
    return out
