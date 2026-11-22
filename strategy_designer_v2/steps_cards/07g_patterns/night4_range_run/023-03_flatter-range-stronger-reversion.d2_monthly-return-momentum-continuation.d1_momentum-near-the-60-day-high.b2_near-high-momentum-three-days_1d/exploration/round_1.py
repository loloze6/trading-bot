def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=10).std()
            ret30=c/c.shift(30)-1
            ret7=c/c.shift(7)-1
            ret3=c/c.shift(3)-1
            hi=c.rolling(40,min_periods=20).max()
            dist=c/hi-1
            fwd=c.shift(-H)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.dayofweek
            yr=pd.to_datetime(b["timestamp"]).dt.year
            df=pd.DataFrame({"coin":coin,"w":w,"fc":b["forecast"],"pos":b["postRebalance_current_allocation"],
                "r1":r1,"vol":vol,"ret30":ret30,"ret7":ret7,"ret3":ret3,"dist":dist,"fwd":fwd,"wd":wd,"yr":yr})
            df=df.iloc[::H]
            rows.append(df)
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["z"]=g["ex"]/g.groupby("coin")["fwd"].transform("std")
    out={}
    def tab(col,q=5):
        d=g.dropna(subset=[col]).copy()
        d["b"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        t=d.groupby("b")["ex"].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["mean_"+col]=d.groupby("b")[col].mean()
        return t.round(5)
    for col in ["fc","ret30","ret7","ret3","r1","dist","vol"]:
        out["ex by quintile of "+col]=tab(col)
    # interaction: ret3 reversal by vol tercile
    d=g.dropna(subset=["ret3","vol"]).copy()
    d["vt"]=d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    d["s"]=d.groupby("coin")["ret3"].transform(lambda x:(x-x.mean())/x.std())
    res={}
    for v,dd in d.groupby("vt"):
        s=stats.linregress(dd["s"],dd["z"]); res[v]=[s.slope,s.slope/s.stderr,len(dd)]
    out["z on ret3 std, by vol tercile (slope,t,n)"]=pd.DataFrame(res,index=["slope","t","n"]).T.round(4)
    # dist x ret30
    d=g.dropna(subset=["ret30","dist"]).copy()
    d["rq"]=d.groupby("coin")["ret30"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    d["dq"]=d.groupby("coin")["dist"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["ex mean ret30 tercile x dist tercile"]=d.pivot_table(index="rq",columns="dq",values="ex",aggfunc="mean").round(4)
    out["ex count ret30 x dist"]=d.pivot_table(index="rq",columns="dq",values="ex",aggfunc="count")
    out["ex by weekday"]=g.groupby("wd")["ex"].agg(["mean","count"]).round(4)
    # book daily
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=coin; x["w"]=w; x["i"]=np.arange(len(x)); dl.append(x)
    D=pd.concat(dl)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    bk=D.groupby(["w","i"]).agg(br=("book_return","mean"),cr=("coin_return","mean"),yr=("yr","first")).dropna()
    by=bk.groupby("yr").agg(book=("br","mean"),hold=("cr","mean"),n=("br","count"),bsd=("br","std"))
    by["sharpe"]=by["book"]/by["bsd"]*np.sqrt(365)
    out["book by year"]=by.round(5)
    bw=bk.groupby("w").agg(book=("br","sum"),hold=("cr","sum"))
    out["book sum by window"]=bw.round(4)
    # positions vs coin return: long vs short
    pl=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            nx=b["close"].shift(-1)/b["close"]-1
            p=b["postRebalance_current_allocation"]
            pl.append(pd.DataFrame({"g":p*nx,"side":np.sign(p),"absp":p.abs()}))
    P=pd.concat(pl).dropna()
    out["bar gain by side"]=P.groupby("side")["g"].agg(["mean","sum","count"]).round(6)
    tr=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades by side"]=tr.groupby("side")["net_profit_loss_percent"].agg(["mean","median","count"]).round(3)
    return out
