def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); o=b["open"].astype(float); l=b["low"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            hh=h.rolling(20).max()
            depth=(c-hh)/hh/sd
            rng=(h-l)/c
            pos=(c-l)/(h-l)
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"r":r,"sd":sd,"depth":depth,
              "choppy":(b["regime"]=="unknown"),"f1":c.shift(-1)/c-1,"f5":c.shift(-5)/c-1,
              "r5p":c/c.shift(5)-1,"pos":pos,"rngz":rng/sd,
              "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D["f1x"]=D["f1"]-D.groupby("coin")["f1"].transform("mean")
    g5=D[D["i"]%5==0].copy()
    g5["f5x"]=g5["f5"]-g5.groupby("coin")["f5"].transform("mean")
    out={}
    def tab(df,key,col):
        a=df.dropna(subset=[key,col]).groupby(key,observed=True)[col]
        t=a.agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); return t[["mean","count","t"]]
    for nm,sub in [("choppy",g5[g5.choppy]),("trend",g5[~g5.choppy])]:
        s=sub.dropna(subset=["depth"]).copy(); s["q"]=pd.qcut(s["depth"],5,labels=False)
        out["5d excess by depth quintile "+nm]=tab(s,"q","f5x")
    s=D.dropna(subset=["depth"]).copy(); s["q"]=pd.qcut(s["depth"],5,labels=False)
    s["up"]=s["r"]>0
    out["1d excess by depth q x choppy (all bars)"]=s.groupby(["choppy","q"])["f1x"].agg(["mean","count"])
    # past 5d move scaled
    g5["m5"]=g5["r5p"]/(g5["sd"]*np.sqrt(5))
    s=g5.dropna(subset=["m5","f5x"]).copy(); s["q"]=pd.qcut(s["m5"],5,labels=False)
    out["5d excess by past 5d scaled move q, choppy"]=tab(s[s.choppy],"q","f5x")
    out["5d excess by past 5d scaled move q, trend"]=tab(s[~s.choppy],"q","f5x")
    s=g5.dropna(subset=["sd","f5x"]).copy(); s["q"]=s.groupby("coin")["sd"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["5d excess by vol tercile x choppy"]=s.groupby(["choppy","q"])["f5x"].agg(["mean","count"])
    out["1d excess by weekday"]=tab(D,"wd","f1x")
    s=D.dropna(subset=["pos","rngz","f1x"]).copy(); s["q"]=pd.qcut(s["pos"],5,labels=False)
    out["1d excess by close position in day range q"]=tab(s,"q","f1x")
    s["rq"]=pd.qcut(s["rngz"],3,labels=False)
    out["1d excess pos q x range tercile"]=s.groupby(["rq","q"])["f1x"].agg(["mean","count"])
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd=pd.concat(dd)
    bk=dd.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book by window"]=bk.groupby("w")[["book_return","coin_return"]].mean()*100
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    out["book by weekday"]=tab(bk,"wd","book_return")
    q=bk["book_return"].quantile([0.02,0.98])
    out["coin ret on book worst2%/best2% days"]=pd.Series({"worst_book":bk.loc[bk.book_return<=q.iloc[0],"coin_return"].mean(),"best_book":bk.loc[bk.book_return>=q.iloc[1],"coin_return"].mean()})
    return out
