def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            rng=(h-l).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            d["clv"]=(c-l)/rng
            d["r1"]=c.pct_change()
            d["r5p"]=c.shift(1)/c.shift(6)-1
            d["mad"]=d["r1"].abs().rolling(20).mean()
            d["z1"]=d["r1"]/d["mad"]
            d["tr60"]=c/c.shift(60)-1
            d["vol30"]=d["r1"].rolling(30).std()
            d["rngz"]=(rng/c)/( (rng/c).rolling(20).mean())
            for k in (1,2,5):
                d[f"f{k}"]=c.shift(-k)/c-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year
            d["fc"]=b["forecast"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in (1,2,5):
        g=D[D.pos%k==0]
        dr=g.groupby("coin")[f"f{k}"].mean()
        D[f"x{k}"]=D[f"f{k}"]-D.coin.map(dr)
    D["volhi"]=D.groupby("coin")["vol30"].transform(lambda s: s>s.median())
    D["trend"]=np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling",np.where(D.tr60.notna(),"choppy",None)))
    def summ(df,k,by):
        g=df[(df.pos%k==0)].dropna(subset=[f"x{k}"])
        def f(s):
            n=len(s); m=s.mean(); t=m/(s.std()/np.sqrt(n)) if n>2 else np.nan
            return pd.Series({"n":n,"mean":m,"t":t})
        return g.groupby(by)[f"x{k}"].apply(f).unstack()
    out={}
    D["clvq"]=pd.cut(D.clv,[-0.01,0.2,0.4,0.6,0.8,1.01],labels=["q1","q2","q3","q4","q5"])
    out["clv->x2"]=summ(D,2,"clvq")
    out["clv->x5"]=summ(D,5,"clvq")
    D["tv"]=D.trend.astype(str)+"_"+np.where(D.volhi,"agi","calm")
    D["top"]=np.where(D.clv>=0.75,"hi",np.where(D.clv<=0.25,"lo","mid"))
    out["profile x clv -> x2"]=summ(D[D.trend.notna()],2,["tv","top"])
    D["r5q"]=pd.qcut(D.r5p,5,labels=False)
    out["past5 quint->x5"]=summ(D,5,"r5q")
    D["z1q"]=pd.qcut(D.z1,7,labels=False)
    out["z1 sept->x1"]=summ(D,1,"z1q")
    out["z1 sept->x5"]=summ(D,5,"z1q")
    out["wd->x1"]=summ(D,1,"wd")
    D["rzq"]=pd.qcut(D.rngz,5,labels=False)
    out["rangez->x2"]=summ(D,2,["rzq"])
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["w"]=w;dd.append(t)
    Dy=pd.concat(dd)
    out["book by window"]=Dy.groupby("w")[["book_return","coin_return"]].mean()
    out["book by coin"]=Dy.groupby("coin")["book_return"].agg(["mean","count"])
    return out
