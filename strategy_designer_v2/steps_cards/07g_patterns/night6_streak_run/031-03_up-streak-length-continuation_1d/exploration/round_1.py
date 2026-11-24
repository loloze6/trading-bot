def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            up=(r>0).astype(int); dn=(r<0).astype(int)
            us=up.groupby((up!=up.shift()).cumsum()).cumsum()*up
            ds=dn.groupby((dn!=dn.shift()).cumsum()).cumsum()*dn
            vol=r.rolling(20,min_periods=10).std()
            p5=c/c.shift(5)-1; p20=c/c.shift(20)-1
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(c-b["low"])/rng
            f5=c.shift(-5)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "us":us,"ds":ds,"r1z":r/vol,"p5z":p5/(vol*np.sqrt(5)),"p20z":p20/(vol*np.sqrt(20)),
                "vol":vol,"cl":cl,"f5":f5,"fc":b["forecast"],"pos":np.arange(len(b))})
            df=df[df.pos%5==0]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["f5"])
    d["ex"]=d["f5"]-d.groupby("coin")["f5"].transform("mean")
    d["volq"]=d.groupby("coin")["vol"].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
    d["wd"]=d["day"].dt.weekday; d["yr"]=d["day"].dt.year
    def tab(key, bins=None):
        x=d.dropna(subset=[key]).copy()
        g=pd.cut(x[key],bins) if bins is not None else x[key]
        x["g"]=g.astype(str)
        out=[]
        for k,s in x.groupby("g"):
            pdm=s.groupby("day")["ex"].mean()
            t=pdm.mean()/(pdm.std(ddof=1)/np.sqrt(len(pdm))) if len(pdm)>2 else np.nan
            out.append([k,len(s),len(pdm),s["ex"].mean()*100,t])
        return pd.DataFrame(out,columns=["g","n","days","ex%","t"]).set_index("g")
    res={}
    res["down streak"]=tab("ds",[-1,0,1,2,3,4,30])
    res["up streak"]=tab("us",[-1,0,1,2,3,4,30])
    res["past5 z"]=tab("p5z",[-99,-2,-1,-0.3,0.3,1,2,99])
    res["past20 z"]=tab("p20z",[-99,-2,-1,-0.3,0.3,1,2,99])
    res["1d z"]=tab("r1z",[-99,-2,-1,0,1,2,99])
    res["vol tercile"]=tab("volq")
    res["close loc"]=tab("cl",[-0.01,0.2,0.4,0.6,0.8,1.01])
    res["weekday"]=tab("wd")
    res["year"]=tab("yr")
    # down streak by coin: slope
    sl=[]
    for coin,s in d.groupby("coin"):
        s=s.dropna(subset=["p5z"])
        sl.append([coin,np.corrcoef(s["ds"],s["ex"])[0,1],np.corrcoef(s["p5z"],s["ex"])[0,1],np.corrcoef(s["p20z"],s["ex"])[0,1],len(s)])
    res["corr by coin"]=pd.DataFrame(sl,columns=["coin","ds","p5z","p20z","n"])
    # book by weekday
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd); D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    bk["wd"]=bk.index.weekday
    res["book by weekday"]=bk.groupby("wd").agg(["mean","count"])*[100,1,100,1]
    return res
