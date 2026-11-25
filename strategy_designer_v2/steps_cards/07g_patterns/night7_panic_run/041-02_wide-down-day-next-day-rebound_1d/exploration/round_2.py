def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            sd30=r.rolling(30,min_periods=20).std()
            pct=sd30.rolling(365,min_periods=120).apply(lambda a:(a<=a[-1]).mean(),raw=True)
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),"r":r,
                "rng":(h-l)/c/sd,"rs":r/sd,"clv":(c-l)/(h-l).replace(0,np.nan),
                "lvol":np.log(b["volume"]/b["volume"].rolling(30,min_periods=20).mean().shift(1)),
                "tr60":c/c.shift(60)-1,"ag":pct,"n1":c.shift(-1)/c-1,
                "r5":c/c.shift(5)-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["x1"]=D["n1"]-D["coin"].map(mu)
    D=D.dropna(subset=["rng","x1","rs"])
    D["side"]=np.where(D["r"]<0,"down","up")
    D["trend"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    D["agit"]=np.where(D["ag"]>0.5,"agit",np.where(D["ag"].notna(),"calm","na"))
    def ct(g,col="x1"):
        g=g.dropna(subset=[col]); s=g.groupby("day")[col].apply(lambda a:(a-g[col].mean()).sum())
        n=len(g); se=np.sqrt((s**2).sum())/n if n>2 else np.nan
        return pd.Series({"n":n,"days":g["day"].nunique(),"mean%":100*g[col].mean(),"t_day":g[col].mean()/se})
    def cols(g,xs,col="x1"):
        g=g.dropna(subset=xs+[col]); X=np.column_stack([np.ones(len(g))]+[g[x] for x in xs]); y=g[col].values
        XtX=np.linalg.inv(X.T@X); b=XtX@X.T@y; e=y-X@b
        S=np.zeros((X.shape[1],X.shape[1]))
        for _,idx in g.reset_index(drop=True).groupby("day").groups.items():
            s=(X[idx]*e[idx,None]).sum(0); S+=np.outer(s,s)
        se=np.sqrt(np.diag(XtX@S@XtX))
        return pd.DataFrame({"coef":b,"t_day":b/se},index=["c"]+xs).round(4)
    out={}
    dn=D[D.side=="down"]; up=D[D.side=="up"]
    out["down ols rng rs clv lvol"]=cols(dn,["rng","rs","clv","lvol"])
    out["up ols rng rs clv lvol"]=cols(up,["rng","rs","clv","lvol"])
    out["all ols rs"]=cols(D,["rs"])
    out["down ols rng by trend"]=pd.concat({t:cols(dn[dn.trend==t],["rng"]) for t in ["fall","chop","rise"]})
    out["up ols rng by trend"]=pd.concat({t:cols(up[up.trend==t],["rng"]) for t in ["fall","chop","rise"]})
    out["up ols rs by trend"]=pd.concat({t:cols(up[up.trend==t],["rs"]) for t in ["fall","chop","rise"]})
    out["side x trend x agit"]=D.groupby(["side","trend","agit"]).apply(ct).round(3)
    out["down ols rng by agit"]=pd.concat({a:cols(dn[dn.agit==a],["rng"]) for a in ["calm","agit"]})
    D["r5q"]=D.groupby("coin")["r5"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["5d return quintile"]=D.groupby("r5q").apply(ct).round(3)
    out["all ols r5 (in day units)"]=cols(D.assign(r5s=D["r5"]/(D["rs"].abs()*0+1)),["r5"])
    lq=dn.copy(); lq["vq"]=pd.qcut(lq["lvol"],5,labels=False,duplicates="drop")
    out["down vol quintile day t"]=lq.groupby("vq").apply(ct).round(3)
    out["weekday day t"]=D.assign(wd=D.day.dt.weekday).groupby("wd").apply(ct).round(3)
    return out
