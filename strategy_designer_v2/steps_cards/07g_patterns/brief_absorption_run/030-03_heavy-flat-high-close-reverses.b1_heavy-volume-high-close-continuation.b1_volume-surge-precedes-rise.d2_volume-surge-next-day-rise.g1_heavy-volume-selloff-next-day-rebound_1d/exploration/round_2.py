def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float);o=b["open"].astype(float);h=b["high"].astype(float);l=b["low"].astype(float);v=b["volume"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin;d["win"]=w
            d["ret1"]=c.pct_change()
            d["ret3"]=c/c.shift(3)-1
            d["vr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            rng=(h-l).replace(0,np.nan)
            d["clv"]=(c-l)/rng
            d["lwick"]=(np.minimum(o,c)-l)/rng
            d["vol20"]=d["ret1"].rolling(20,min_periods=20).std()
            d["nxt"]=c.shift(-1)/c-1
            d["nxt2"]=c.shift(-2)/c.shift(-1)-1
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["yr"]=ts.dt.year.values
            d["fc"]=b["forecast"].astype(float)
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["ret1"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D["ex2"]=D["nxt2"]-D["coin"].map(mu)
    D=D.dropna(subset=["ex","ret1","vr","vol20"]).copy()
    def st1(x):
        x=pd.Series(x).dropna();n=len(x)
        t=x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan
        return {"n":n,"mean%":round(100*x.mean(),4),"t":round(t,2)}
    def grp(df,keys,col="ex"):
        res=[]
        for k,g in df.groupby(keys,observed=True):
            r=st1(g[col]);k=k if isinstance(k,tuple) else (k,)
            res.append(dict(zip(keys if isinstance(keys,list) else [keys],k),**r))
        return pd.DataFrame(res)
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err "+str(e)[:80]
    D["rq"]=pd.qcut(D.groupby("coin")["ret1"].rank(pct=True),5,labels=["r1low","r2","r3","r4","r5high"])
    D["heavy"]=np.where(D["vr"]>=1,"heavy","light")
    D["clvb"]=pd.cut(D.clv,[-0.001,0.33,0.66,1.001],labels=["lowclose","mid","highclose"])
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
    safe("ret quintile x volume",lambda:grp(D,["rq","heavy"]))
    safe("down days clv x volume",lambda:grp(D[D.ret1<0],["clvb","heavy"]))
    safe("up days clv x volume",lambda:grp(D[D.ret1>=0],["clvb","heavy"]))
    safe("bottom ret quintile vol tercile x volume",lambda:grp(D[D.rq=="r1low"],["volq","heavy"]))
    safe("top ret quintile vol tercile x volume",lambda:grp(D[D.rq=="r5high"],["volq","heavy"]))
    safe("active day2 excess",lambda:pd.DataFrame([st1(D[D.fc>0]["ex2"])]))
    safe("active by weekday",lambda:grp(D[D.fc>0],["wd"]))
    safe("all by weekday",lambda:grp(D,["wd"]))
    safe("3d ret quintile",lambda:grp(D.assign(r3q=pd.qcut(D.groupby("coin")["ret3"].rank(pct=True),5,labels=False)),["r3q"]))
    safe("active by coin",lambda:grp(D[D.fc>0],["coin"]))
    safe("active by year",lambda:grp(D[D.fc>0],["yr"]))
    safe("active clv tercile",lambda:grp(D[D.fc>0],["clvb"]))
    def vrq():
        dd=D[D.rq=="r1low"].copy()
        dd["vrq"]=pd.qcut(dd.vr.rank(method="first"),4,labels=False)
        return grp(dd,["vrq"])
    safe("bottom ret quintile by volume-ratio quartile",vrq)
    def lw():
        dd=D[D.ret1<0].copy();dd["lw"]=pd.qcut(dd.lwick.rank(method="first"),3,labels=False)
        return grp(dd,["lw","heavy"])
    safe("down days lower-wick tercile x volume",lw)
    # book days
    def book():
        bd=[]
        for coin,wins in data["days"].items():
            for w,d in wins.items():
                d=d.copy();d["coin"]=coin;d["win"]=w
                d["nb"]=d["book_return"].shift(-1);d["pb"]=d["book_return"].shift(1)
                d["nc"]=d["coin_return"].shift(-1)
                bd.append(d)
        B=pd.concat(bd,ignore_index=True).dropna(subset=["book_return"])
        B=B[B.book_return!=0]
        q=B.book_return.quantile([0.05,0.95])
        r=[]
        for nm,g in [("worst5%",B[B.book_return<=q.iloc[0]]),("best5%",B[B.book_return>=q.iloc[1]])]:
            r.append(dict(grp=nm,n=len(g),book_mean=100*g.book_return.mean(),coin_same=100*g.coin_return.mean(),coin_next=100*g.nc.mean(),book_next=100*g.nb.mean()))
        return pd.DataFrame(r)
    safe("book extreme days",book)
    return out
