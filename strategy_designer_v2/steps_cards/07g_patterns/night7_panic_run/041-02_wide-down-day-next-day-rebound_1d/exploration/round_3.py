def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            v=b["volume"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),"r":r,
                "rng":(h-l)/c/sd,"rs":r/sd,"clv":(c-l)/(h-l).replace(0,np.nan),
                "lvol":np.log(v.replace(0,np.nan)/v.rolling(30,min_periods=20).mean().shift(1)),
                "tr60":c/c.shift(60)-1,"n1":c.shift(-1)/c-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["x1"]=D["n1"]-D["coin"].map(mu)
    D=D.replace([np.inf,-np.inf],np.nan).dropna(subset=["rng","x1","rs"])
    D["side"]=np.where(D["r"]<0,"down","up")
    D["trend"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"]).astype(str)
    def ct(g,col="x1"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<5: return pd.Series({"n":n,"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        s=g.groupby("day")[col].apply(lambda a:(a-g[col].mean()).sum())
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"days":g["day"].nunique(),"mean%":100*g[col].mean(),"t_day":g[col].mean()/se})
    def cols(g,xs,col="x1"):
        try:
            g=g.dropna(subset=xs+[col]).reset_index(drop=True)
            if len(g)<30: return pd.DataFrame({"coef":[np.nan],"t_day":[np.nan]},index=["few"])
            X=np.column_stack([np.ones(len(g))]+[g[x].values for x in xs]); y=g[col].values
            XtX=np.linalg.pinv(X.T@X); b=XtX@X.T@y; e=y-X@b
            S=np.zeros((X.shape[1],X.shape[1]))
            for _,idx in g.groupby("day").indices.items():
                s=(X[idx]*e[idx,None]).sum(0); S+=np.outer(s,s)
            se=np.sqrt(np.diag(XtX@S@XtX))
            return pd.DataFrame({"n":len(g),"coef":b,"t_day":b/se},index=["c"]+xs).round(4)
        except Exception as ex:
            return str(ex)[:80]
    out={}
    dn=D[D.side=="down"]; up=D[D.side=="up"]
    out["down ols rng"]=cols(dn,["rng"])
    out["down ols rng rs clv lvol"]=cols(dn,["rng","rs","clv","lvol"])
    out["up ols rng"]=cols(up,["rng"])
    out["up ols rng rs"]=cols(up,["rng","rs"])
    out["up ols rng rs clv lvol"]=cols(up,["rng","rs","clv","lvol"])
    out["all ols rs"]=cols(D,["rs"])
    out["all ols signed rng (rng*sign)"]=cols(D.assign(srng=D["rng"]*np.sign(D["r"])),["srng"])
    for t in ["fall","chop","rise"]:
        out["up ols rng, trend "+t]=cols(up[up.trend==t],["rng"])
        out["down ols rng, trend "+t]=cols(dn[dn.trend==t],["rng"])
    out["side x trend day t"]=D.groupby(["side","trend"]).apply(ct).round(3)
    D["rq"]=D.groupby("coin")["rng"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["side x range quintile day t"]=D.groupby(["side","rq"]).apply(ct).round(3)
    dv=dn.dropna(subset=["lvol"]).copy(); dv["vq"]=pd.qcut(dv["lvol"],5,labels=False,duplicates="drop")
    out["down vol quintile day t"]=dv.groupby("vq").apply(ct).round(3)
    out["down ols lvol only"]=cols(dn,["lvol"])
    out["weekday day t"]=D.assign(wd=D.day.dt.weekday).groupby("wd").apply(ct).round(3)
    return out
