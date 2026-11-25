def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; pc=c.shift(1)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["ret"]=c/pc-1
            hl=(b["high"]-b["low"]).replace(0,np.nan)
            d["rng"]=(b["high"]-b["low"])/pc
            d["clv"]=(c-b["low"])/hl
            d["upwick"]=(b["high"]-np.maximum(b["open"],c))/pc
            d["lowick"]=(np.minimum(b["open"],c)-b["low"])/pc
            d["r1"]=c.shift(-1)/c-1
            d["ret5"]=c/c.shift(5)-1
            d["ret30"]=c/c.shift(30)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["rngrel"]=d["rng"]/d["rng"].rolling(20).mean().shift(1)
            d["lwv"]=d["lowick"]/d["vol20"]
            d["uwv"]=d["upwick"]/d["vol20"]
            d["fc"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["ret"].mean()
    D["u1"]=D["r1"]-D["coin"].map(drift)
    D["day"]=D["ts"].dt.floor("D")
    def tday(s, days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).dropna()
        g=x.groupby("d")["v"].sum(); n=len(g)
        t=g.mean()/(g.std()/np.sqrt(n)) if n>2 and g.std()>0 else np.nan
        return x["v"].mean(), t, n, len(x)
    def tab(df,key,col="u1"):
        r=[]
        for k,g in df.groupby(key):
            m,t,n,nc=tday(g[col],g["day"]); r.append((str(k),round(m*100,3),round(t,2),nc,n))
        return pd.DataFrame(r,columns=["grp","mean%","t_day","n","days"])
    def q(df,col,k):
        return df.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),k,labels=False))
    out={}
    D["retq"]=q(D,"ret",10)
    out["u1 by ret decile"]=tab(D,"retq")
    down=D[D["ret"]<0].copy()
    down["fallq"]=q(down,"ret",3)  # 0 = deepest fall
    down["rngq"]=q(down.dropna(subset=["rngrel"]),"rngrel",3)
    down["clvq"]=q(down.dropna(subset=["clv"]),"clv",3)
    out["down: fall(0=deep) x rngrel"]=tab(down,["fallq","rngq"])
    out["down: fall(0=deep) x clv"]=tab(down,["fallq","clvq"])
    up=D[D["ret"]>0].copy()
    up["riseq"]=q(up,"ret",3)
    up["clvq"]=q(up.dropna(subset=["clv"]),"clv",3)
    out["up: rise(2=big) x clv"]=tab(up,["riseq","clvq"])
    D["wd"]=D["ts"].dt.dayofweek
    out["u1 by weekday"]=tab(D,"wd")
    D["vq"]=q(D.dropna(subset=["vol20"]),"vol20",3)
    D["t30"]=np.where(D["ret30"]>0.1,"rise",np.where(D["ret30"]<-0.1,"fall","chop"))
    D.loc[D["ret30"].isna(),"t30"]="na"
    fc=D[D["fc"]>0].copy()
    fc["fq"]=q(fc,"fc",4)
    out["fc>0 by fc quartile"]=tab(fc,"fq")
    out["fc>0 by t30"]=tab(fc,"t30")
    out["fc>0 by vol tercile"]=tab(fc,"vq")
    out["fc==0 by t30"]=tab(D[D["fc"]==0],"t30")
    out["all by t30"]=tab(D,"t30")
    out["all by vol tercile"]=tab(D,"vq")
    D["r5q"]=q(D.dropna(subset=["ret5"]),"ret5",5)
    out["u1 by 5d ret quintile"]=tab(D,"r5q")
    D["lwq"]=q(D.dropna(subset=["lwv"]),"lwv",5)
    out["u1 by lower wick/vol quintile"]=tab(D,"lwq")
    D["uwq"]=q(D.dropna(subset=["uwv"]),"uwv",5)
    out["u1 by upper wick/vol quintile"]=tab(D,"uwq")
    br=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["coin"]=coin; x["win"]=w; br.append(x)
    B=pd.concat(br,ignore_index=True)
    bd=B.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window %"]=(bd.groupby(level=0).mean()*100).round(3)
    qq=bd["book_return"]
    top=bd[qq>=qq.quantile(0.98)]; bot=bd[qq<=qq.quantile(0.02)]
    out["book extremes"]=pd.DataFrame({"n":[len(top),len(bot)],"book%":[top.book_return.mean()*100,bot.book_return.mean()*100],"coin%":[top.coin_return.mean()*100,bot.coin_return.mean()*100]},index=["top2%","bot2%"])
    return out
