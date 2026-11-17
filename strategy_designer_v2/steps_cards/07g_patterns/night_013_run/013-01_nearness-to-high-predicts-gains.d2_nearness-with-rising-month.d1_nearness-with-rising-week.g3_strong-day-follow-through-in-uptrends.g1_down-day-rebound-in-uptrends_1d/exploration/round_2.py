def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["win"]=w
            d["r1"]=r; d["vol"]=r.rolling(30).std(); d["z"]=r/d["vol"]
            d["ret30"]=cl/cl.shift(30)-1
            d["dist"]=cl/b["high"].rolling(30).max()-1
            d["fwd1"]=cl.shift(-1)/cl-1
            d["fwd5"]=cl.shift(-5)/cl-1
            d["vz"]=np.log(b["volume"].replace(0,np.nan)/b["volume"].rolling(30).mean())
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values; d["yr"]=ts.dt.year.values
            d["alloc"]=b["postRebalance_current_allocation"]
            d["grid5"]=(np.arange(len(b))%5==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex1"]=D["fwd1"]-D.groupby("coin")["fwd1"].transform("mean")
    D["ex5"]=D["fwd5"]-D.groupby("coin")["fwd5"].transform("mean")
    D=D.dropna(subset=["z","ret30","ex1"]).copy()
    D["up"]=np.where(D["ret30"]>0,"up30","dn30")
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.5,0,0.5,1,2,99])
    def agg(g,col="ex1"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean() if n else np.nan,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["ex1 by z bin x regime"]=D.groupby(["up","zb"],observed=True).apply(agg).round(4)
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False))
    D["zs"]=np.sign(D["z"])
    out["ex1 by volq x zsign x regime"]=D.groupby(["up","volq","zs"]).apply(agg).round(4)
    out["ex1 by weekday"]=D.groupby("wd").apply(agg).round(4)
    D["db"]=pd.qcut(D["dist"],5)
    G=D[D["grid5"]]
    out["ex5 by dist quintile (grid5)"]=G.groupby("db",observed=True).apply(lambda g:agg(g,"ex5")).round(4)
    out["ex1 by dist quintile"]=D.groupby("db",observed=True).apply(agg).round(4)
    D["vzb"]=pd.qcut(D["vz"],4)
    out["ex1 by vol-surprise x zsign"]=D.groupby(["zs","vzb"],observed=True).apply(agg).round(4)
    res=[]
    for (u,c),g in D[D.z<0].groupby(["up","coin"]):
        s=stats.linregress(-g["z"],g["ex1"]); res.append([u,c,len(g),s.slope,s.slope/s.stderr])
    out["per coin slope fall->ex1"]=pd.DataFrame(res,columns=["reg","coin","n","slope","t"]).round(4)
    res=[]
    for (u,c),g in D[D.z>0].groupby(["up","coin"]):
        s=stats.linregress(g["z"],g["ex1"]); res.append([u,c,len(g),s.slope,s.slope/s.stderr])
    out["per coin slope rise->ex1"]=pd.DataFrame(res,columns=["reg","coin","n","slope","t"]).round(4)
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["win"]=w; dd.append(x)
    B=pd.concat(dd,ignore_index=True); B["day"]=pd.to_datetime(B["day"])
    P=B.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna().reset_index()
    P["yr"]=P["day"].dt.year; P["wd"]=P["day"].dt.weekday
    out["book by year"]=P.groupby("yr").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean")).round(5)
    out["book by weekday"]=P.groupby("wd").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean")).round(5)
    out["mean alloc, share in"]=pd.Series({"mean_alloc":float(D["alloc"].mean()),"share_in":float((D["alloc"].abs()>1e-6).mean())})
    return out
