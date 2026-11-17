def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=7
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            vr=v/v.rolling(20,min_periods=10).mean()
            sd=r1.rolling(20,min_periods=10).std()
            hi20=b["high"].astype(float).rolling(20,min_periods=10).max()
            near=c/hi20-1
            r3=c/c.shift(3)-1
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b),H):
                if i+H>=len(b): break
                rows.append(dict(coin=coin,w=w,vr=vr.iloc[i],r1=r1.iloc[i],z1=r1.iloc[i]/sd.iloc[i] if sd.iloc[i]>0 else np.nan,
                    near=near.iloc[i],r3=r3.iloc[i],fwd=fwd.iloc[i],yr=ts.iloc[i].year,
                    lvr=np.log(vr.iloc[i]) if vr.iloc[i]>0 else np.nan))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["sv"]=np.sign(d["r1"])*d["vr"]
    d["z1v"]=d["z1"]*d["vr"]
    out={}
    def tslope(x,col):
        x=x.dropna(subset=[col,"ex"])
        if len(x)<20: return np.nan
        s=stats.linregress(x[col],x["ex"]); return round(s.slope/s.stderr,2)
    cols=["r1","z1","r3","near","sv","z1v"]
    out["pooled_and_coin_t"]=pd.DataFrame({c:pd.concat([d.groupby("coin").apply(lambda g:tslope(g,c)),pd.Series({"pooled":tslope(d,c),"n":d[c].notna().sum()})]) for c in cols})
    out["year_t"]=pd.DataFrame({c:d.groupby("yr").apply(lambda g:tslope(g,c)) for c in ["r1","z1","near","sv"]})
    # multiple regression: r1-z and log volume ratio and interaction
    x=d.dropna(subset=["z1","lvr","near","ex"]).copy()
    for c in ["z1","lvr","near"]:
        x[c+"s"]=(x[c]-x[c].mean())/x[c].std()
    x["int"]=x["z1s"]*x["lvrs"]
    X=np.column_stack([np.ones(len(x)),x["z1s"],x["lvrs"],x["nears"],x["int"]])
    y=x["ex"].values
    beta,res,rk,sv=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-X.shape[1]); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["multireg_t"]=pd.Series(np.round(beta/se,2),index=["const","z1","logvr","near","z1xlogvr"])
    out["multireg_n"]=len(y)
    # thin volume x sign
    x["thin"]=x.groupby("coin")["vr"].transform(lambda s:s<s.quantile(0.2))
    x["up"]=x["r1"]>0
    g=x.groupby(["thin","up"])["ex"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["thin_x_up"]=g.round(4)
    # z1 quintiles by volume half
    x["hv"]=x.groupby("coin")["vr"].transform(lambda s:s>s.median())
    x["qz"]=x.groupby("coin")["z1"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["z1q_by_hv"]=x.pivot_table(index="qz",columns="hv",values="ex",aggfunc="mean").round(4)
    # book: largest days, coin return before/after
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dd=dd.copy().reset_index(drop=True); dd["coin"]=coin
            dd["prev"]=dd["coin_return"].shift(1); dd["next"]=dd["coin_return"].shift(-1)
            dl.append(dd)
    D=pd.concat(dl).dropna(subset=["book_return"])
    D["bq"]=pd.qcut(D["book_return"].rank(method="first"),10,labels=False)
    out["book_decile_prev_next"]=D.groupby("bq")[["book_return","coin_return","prev","next"]].mean().round(5)
    return out
