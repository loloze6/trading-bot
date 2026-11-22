def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]
    for coin,ws in data["bars"].items():
        for wi,(w,b) in enumerate(ws.items()):
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=10).std()
            volrel=vol/vol.rolling(120,min_periods=40).median()
            ret3=c/c.shift(3)-1
            ret30=c/c.shift(30)-1
            mx=c.rolling(30,min_periods=20).max(); mn=c.rolling(30,min_periods=20).min()
            mid=(mx+mn)/2
            rpos=(c-mid)/(mx-mn)
            dev=(c/c.rolling(20,min_periods=10).mean()-1)/vol
            flat=(ret30.abs())/(vol*np.sqrt(30))
            fwd=c.shift(-H)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"wn":int(w[1:]),"ret3":ret3,"ret30":ret30,"vol":vol,"volrel":volrel,
                "rpos":rpos,"dev":dev,"flat":flat,"fwd":fwd,"pos":b["postRebalance_current_allocation"]})
            rows.append(df.iloc[::H])
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["z"]=g["ex"]/g.groupby("coin")["fwd"].transform("std")
    g["s3"]=g["ret3"]/(g["vol"]*np.sqrt(3))
    out={}
    def reg(d,x):
        d=d.dropna(subset=[x,"z"])
        if len(d)<30: return [np.nan,np.nan,len(d)]
        s=stats.linregress(d[x],d["z"]); return [round(s.slope,4),round(s.slope/s.stderr,2),len(d)]
    g["vt"]=g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    for x in ["s3","ret3","dev","rpos"]:
        out["z on %s by own-vol tercile"%x]=pd.DataFrame({v:reg(dd,x) for v,dd in g.groupby("vt")},index=["slope","t","n"]).T
    d=g.dropna(subset=["volrel"]).copy()
    d["vr"]=d.groupby("coin")["volrel"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["z on s3 by rel-vol tercile"]=pd.DataFrame({v:reg(dd,"s3") for v,dd in d.groupby("vr")},index=["slope","t","n"]).T
    d=g.dropna(subset=["flat"]).copy()
    d["ft"]=d.groupby("coin")["flat"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["z on rpos by flatness tercile (0=flattest)"]=pd.DataFrame({v:reg(dd,"rpos") for v,dd in d.groupby("ft")},index=["slope","t","n"]).T
    out["z on s3 by flatness tercile"]=pd.DataFrame({v:reg(dd,"s3") for v,dd in d.groupby("ft")},index=["slope","t","n"]).T
    lo=g[g["vt"]==0]
    out["low-vol: z on s3 by coin"]=pd.DataFrame({c:reg(dd,"s3") for c,dd in lo.groupby("coin")},index=["slope","t","n"]).T
    lo=lo.assign(half=np.where(lo["wn"]<=12,"w1-w12","w13-w24"))
    out["low-vol: z on s3 by window half"]=pd.DataFrame({c:reg(dd,"s3") for c,dd in lo.groupby("half")},index=["slope","t","n"]).T
    lo=lo.copy(); lo["q"]=lo.groupby("coin")["s3"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    t=lo.groupby("q")["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["low-vol: ex by s3 quintile"]=t.round(5)
    # all-bar slope of z on s3
    out["all: z on s3"]=pd.Series(reg(g,"s3"),index=["slope","t","n"])
    # shorts by ret30 sign
    g["side"]=np.sign(g["pos"])
    g["up30"]=np.sign(g["ret30"])
    out["ex*side by side & ret30 sign"]=g.assign(gx=g["side"]*g["fwd"]).groupby(["side","up30"])["gx"].agg(["mean","count"]).round(5)
    return out
