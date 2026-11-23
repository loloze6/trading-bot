def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"]; allr.append((c.shift(-1)/c-1).dropna())
        cm=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r0=c/c.shift(1)-1
            d=pd.DataFrame({"coin":coin,"w":w})
            d["r1"]=c.shift(-1)/c-1-cm
            d["r3"]=c.shift(-3)/c-1-3*cm
            d["pos"]=np.arange(len(b))
            d["r0"]=r0
            v20=r0.rolling(20).std()
            d["z"]=r0/v20
            d["v20"]=v20
            d["vr"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rg=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(2*c-b["high"]-b["low"])/rg
            d["rng"]=rg/c/v20
            d["r5"]=c/c.shift(5)-1
            d["z5"]=d["r5"]/(v20*np.sqrt(5))
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"]=b["postRebalance_current_allocation"]
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,col,key="r1"):
        x=df.dropna(subset=[col,key]).groupby(col,observed=True)[key]
        o=x.agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        o["mean"]*=100; return o[["mean","t","count"]].round(3)
    out={}
    out["by_weekday"]=g(D,"wd")
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["by_z_day"]=g(D,"zb")
    D["we"]=D["wd"].isin([5,6])
    out["z_x_weekend"]=D.dropna(subset=["zb","r1"]).groupby(["zb","we"],observed=True)["r1"].agg(lambda s:f"{100*s.mean():.3f}|t{s.mean()/(s.std()/np.sqrt(len(s))):.2f}|n{len(s)}").unstack()
    D["vrb"]=pd.qcut(D["vr"],3,labels=["lowV","midV","highV"])
    D["clvb"]=pd.cut(D["clv"],[-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out["clv_x_vol"]=D.dropna(subset=["clvb","vrb","r1"]).groupby(["clvb","vrb"],observed=True)["r1"].agg(lambda s:f"{100*s.mean():.3f}|t{s.mean()/(s.std()/np.sqrt(len(s))):.2f}|n{len(s)}").unstack()
    D["rngb"]=pd.qcut(D["rng"],5)
    out["by_range_norm"]=g(D,"rngb")
    D["z5b"]=pd.cut(D["z5"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["by_z5"]=g(D,"z5b")
    D["v20b"]=D.groupby("coin")["v20"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["by_vol_tercile"]=g(D,"v20b")
    N3=D[D["pos"]%3==0]
    out["r3_by_z"]=g(N3,"zb","r3")
    out["r3_by_z5"]=g(N3,"z5b","r3")
    # book
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday; dd["w"]=w; br.append(dd)
    B=pd.concat(br)
    out["book_by_weekday"]=g(B.rename(columns={"book_return":"r1"}),"wd")
    out["coin_by_weekday"]=g(B.rename(columns={"coin_return":"r1"}),"wd")
    return out
