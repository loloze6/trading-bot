def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"r":r,
                "rng":(h-l)/c/sd,"rs":r/sd,"clv":(c-l)/(h-l).replace(0,np.nan),
                "body":(c-o)/(h-l).replace(0,np.nan),
                "vol":b["volume"]/b["volume"].rolling(30,min_periods=20).mean().shift(1),
                "tr60":c/c.shift(60)-1,"sdx":sd,
                "n1":c.shift(-1)/c-1,"n3":c.shift(-3)/c-1,
                "pos":b["postRebalance_current_allocation"],
                "r_prev":r.shift(1)})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["x1"]=D["n1"]-D["coin"].map(mu)
    D["x3"]=D["n3"]-3*D["coin"].map(mu)
    D["side"]=np.where(D["r"]<0,"down","up")
    D=D.dropna(subset=["rng","x1"])
    def tab(g,col="x1"):
        a=g[col].dropna(); 
        return pd.Series({"n":len(a),"mean%":100*a.mean(),"t":a.mean()/a.std()*np.sqrt(len(a)) if len(a)>2 else np.nan})
    out={}
    D["rq"]=D.groupby("coin")["rng"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["side x range quintile x1"]=D.groupby(["side","rq"]).apply(tab).round(3)
    out["side x range quintile x3 (all bars, overlapping)"]=D.groupby(["side","rq"]).apply(lambda g:tab(g,"x3")).round(3)
    # close location on down days
    dn=D[D.side=="down"].copy()
    dn["clvq"]=pd.qcut(dn["clv"],5,labels=False,duplicates="drop")
    out["down: close-location quintile"]=dn.groupby("clvq").apply(tab).round(3)
    up=D[D.side=="up"].copy()
    up["clvq"]=pd.qcut(up["clv"],5,labels=False,duplicates="drop")
    out["up: close-location quintile"]=up.groupby("clvq").apply(tab).round(3)
    # return size in swing units vs range
    D["rsq"]=D.groupby("coin")["rs"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    out["rs decile (signed return in swing units)"]=D.groupby("rsq").apply(tab).round(3)
    # regression within down days: x1 on rng and |rs|
    import numpy.linalg as la
    for nm,g in [("down",dn),("up",up),("all",D)]:
        g=g.dropna(subset=["rng","rs","x1","clv"])
        X=np.column_stack([np.ones(len(g)),g["rng"],g["rs"],g["clv"]])
        y=g["x1"].values; bta,res,_,_=la.lstsq(X,y,rcond=None)
        e=y-X@bta; s2=e@e/(len(y)-4); se=np.sqrt(np.diag(s2*la.inv(X.T@X)))
        out["ols x1 ~ rng+rs+clv "+nm]=pd.DataFrame({"coef":bta,"t":bta/se},index=["c","rng","rs","clv"]).round(4)
    # volume
    dn["vq"]=pd.qcut(dn["vol"],5,labels=False,duplicates="drop")
    out["down: vol ratio quintile"]=dn.groupby("vq").apply(tab).round(3)
    # trend / agitation
    D["trend"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["side x trend"]=D.groupby(["side","trend"]).apply(tab).round(3)
    D["wd"]=D["ts"].dt.weekday
    out["weekday all"]=D.groupby("wd").apply(tab).round(3)
    out["by coin down top2 quintiles"]=D[(D.side=="down")&(D.rq>=3)].groupby("coin").apply(tab).round(3)
    out["by window down top2 quintiles"]=D[(D.side=="down")&(D.rq>=3)].groupby("w").apply(tab).round(3)
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    B=pd.concat(dd)
    bk=B.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book corr with coins"]=float(bk.corr().iloc[0,1])
    q=bk["book_return"].quantile([0.02,0.98])
    out["book worst 2% days: coin mean%"]=100*bk[bk.book_return<=q.iloc[0]]["coin_return"].mean()
    out["book best 2% days: coin mean%"]=100*bk[bk.book_return>=q.iloc[1]]["coin_return"].mean()
    return out
