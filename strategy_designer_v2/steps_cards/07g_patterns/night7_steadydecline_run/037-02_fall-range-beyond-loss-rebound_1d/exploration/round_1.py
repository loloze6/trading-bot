def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; pc=c.shift(1)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["ret"]=c/pc-1
            d["rng"]=(b["high"]-b["low"])/pc
            d["clv"]=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d["upwick"]=(b["high"]-np.maximum(b["open"],c))/pc
            d["lowick"]=(np.minimum(b["open"],c)-b["low"])/pc
            d["r1"]=c.shift(-1)/c-1
            d["r3"]=c.shift(-3)/c-1
            d["ret5"]=c/c.shift(5)-1
            d["ret30"]=c/c.shift(30)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["rngrel"]=d["rng"]/d["rng"].rolling(20).mean().shift(1)
            d["fc"]=b["forecast"]
            d["alloc"]=b["postRebalance_current_allocation"]
            d["pos"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["ret"].mean()
    D["u1"]=D["r1"]-D["coin"].map(drift)
    D["day"]=D["ts"].dt.floor("D")
    def tday(s, days):
        g=pd.DataFrame({"v":s,"d":days}).dropna().groupby("d")["v"].sum()
        n=len(g); 
        m=s.dropna().mean()
        return m, (g.mean()/(g.std()/np.sqrt(n)) if n>2 else np.nan), n
    out={}
    def tab(df, key, col="u1"):
        r=[]
        for k,g in df.groupby(key, observed=True):
            m,t,n=tday(g[col],g["day"]); r.append((k,round(m*100,3),round(t,2),len(g[col].dropna()),n))
        return pd.DataFrame(r,columns=["grp","mean%","t_day","n","days"])
    D["absret_q"]=D.groupby("coin")["ret"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    out["u1 by ret decile"]=tab(D,"absret_q")
    down=D[D["ret"]<0].copy()
    down["fallq"]=down.groupby("coin")["ret"].transform(lambda s: pd.qcut(-s,3,labels=False))
    down["rngq"]=down.groupby("coin")["rngrel"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    down["clvq"]=down.groupby("coin")["clv"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["down: fall x rngrel"]=tab(down,["fallq","rngq"])
    out["down: fall x clv"]=tab(down,["fallq","clvq"])
    up=D[D["ret"]>0].copy()
    up["riseq"]=up.groupby("coin")["ret"].transform(lambda s: pd.qcut(s,3,labels=False))
    up["clvq"]=up.groupby("coin")["clv"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["up: rise x clv"]=tab(up,["riseq","clvq"])
    D["wd"]=D["ts"].dt.dayofweek
    out["u1 by weekday"]=tab(D,"wd")
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    D["t30"]=np.where(D["ret30"]>0.1,"rise",np.where(D["ret30"]<-0.1,"fall","chop"))
    D.loc[D["ret30"].isna(),"t30"]=np.nan
    fc=D[D["fc"]>0].copy()
    fc["fq"]=fc.groupby("coin")["fc"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["fc>0 by fc quartile"]=tab(fc,"fq")
    out["fc>0 by t30 trend"]=tab(fc,"t30")
    out["fc>0 by vol tercile"]=tab(fc,"vq")
    out["fc==0 baseline by t30"]=tab(D[D["fc"]==0],"t30")
    D["r5q"]=D.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["u1 by 5d ret quintile"]=tab(D,"r5q")
    D["lwq"]=D.groupby("coin")["lowick"].transform(lambda s: pd.qcut(s/ D.loc[s.index,"vol20"],5,labels=False,duplicates="drop"))
    out["u1 by lower wick/vol quintile"]=tab(D,"lwq")
    D["uwq"]=D.groupby("coin")["upwick"].transform(lambda s: pd.qcut(s/ D.loc[s.index,"vol20"],5,labels=False,duplicates="drop"))
    out["u1 by upper wick/vol quintile"]=tab(D,"uwq")
    # book
    br=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["coin"]=coin; x["win"]=w; br.append(x)
    B=pd.concat(br); bd=B.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window"]=B.groupby("win")[["book_return","coin_return"]].mean()*100
    q=bd["book_return"]
    top=bd[q>=q.quantile(0.98)]; bot=bd[q<=q.quantile(0.02)]
    out["book extremes"]=pd.DataFrame({"n":[len(top),len(bot)],"book%":[top.book_return.mean()*100,bot.book_return.mean()*100],"coin%":[top.coin_return.mean()*100,bot.coin_return.mean()*100]},index=["top2%","bot2%"])
    return out
