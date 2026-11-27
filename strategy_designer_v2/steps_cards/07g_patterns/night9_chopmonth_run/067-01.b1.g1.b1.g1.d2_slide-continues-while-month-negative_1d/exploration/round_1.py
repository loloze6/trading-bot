def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            df["ret30"]=c/c.shift(30)-1; df["ret60"]=c/c.shift(60)-1
            df["ret5"]=c/c.shift(5)-1
            df["vol30"]=r1.rolling(30).std()
            df["r1"]=r1
            df["z1"]=r1/r1.rolling(30).std().shift(1)
            df["clv"]=(c-l)/(h-l).replace(0,np.nan)
            df["rng"]=(h-l)/c/df["vol30"]
            for k in (1,5,10): df[f"f{k}"]=c.shift(-k)/c-1
            df["alloc"]=b["postRebalance_current_allocation"].astype(float)
            df["fc"]=b["forecast"].astype(float)
            df["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            df["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["drift10"]=A.groupby("coin")["f10"].transform(lambda s: s[A.loc[s.index,"pos"]%10==0].mean())
    A["drift1"]=A.groupby("coin")["f1"].transform("mean")
    A["x10"]=A["f10"]-A["drift10"]; A["x1"]=A["f1"]-A["drift1"]
    G=A[(A.pos%10==0)].dropna(subset=["ret30","ret60","x10"])
    G["chop"]=G.ret60.abs()<=0.10
    G["trend"]=np.where(G.ret60>0.10,"rise",np.where(G.ret60<-0.10,"fall","chop"))
    G["q30"]=pd.qcut(G.ret30,5,labels=False)
    def summ(g,col="x10"):
        x=g[col].dropna(); 
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["x10 by trend x ret30 quintile"]=G.groupby(["trend","q30"]).apply(summ).round(3)
    # slopes of x10 on ret30 / vol per trend
    sl=[]
    for t,g in G.groupby("trend"):
        z=g.ret30/g.vol30/np.sqrt(30)
        res=stats.linregress(z,g.x10); sl.append([t,len(g),res.slope,res.slope/res.stderr])
    out["slope x10 on scaled ret30 by trend"]=pd.DataFrame(sl,columns=["trend","n","slope","t"])
    # daily: next-day after large z1 moves
    D=A.dropna(subset=["z1","x1"]).copy()
    D["zq"]=pd.qcut(D.z1,10,labels=False)
    out["next-day x1 by today's scaled move decile"]=D.groupby("zq").apply(summ,col="x1").round(3)
    D["cq"]=pd.qcut(D.clv,5,labels=False)
    out["next-day x1 by close location"]=D.groupby("cq").apply(summ,col="x1").round(3)
    out["x1 by weekday"]=D.groupby("wd").apply(summ,col="x1").round(3)
    # vol level
    G2=G.dropna(subset=["vol30"]).copy(); G2["vq"]=G2.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["x10 by vol tercile (within coin)"]=G2.groupby("vq").apply(summ).round(3)
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    DD=pd.concat(dd); DD["wd"]=pd.to_datetime(DD["day"]).dt.dayofweek
    out["book daily return by window (bp)"]=DD.groupby("w")["book_return"].agg(lambda s:1e4*s.mean()).round(2)
    out["book by weekday (bp)"]=DD.groupby("wd")["book_return"].agg(lambda s:1e4*s.mean()).round(2)
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades"]=pd.Series({"n":len(T),"mean pl%":T.profit_loss_percent.mean(),"net%":T.net_profit_loss_percent.mean(),"win":(T.net_profit_loss_percent>0).mean(),"med dur d":T.duration_minutes.median()/1440})
    return out
