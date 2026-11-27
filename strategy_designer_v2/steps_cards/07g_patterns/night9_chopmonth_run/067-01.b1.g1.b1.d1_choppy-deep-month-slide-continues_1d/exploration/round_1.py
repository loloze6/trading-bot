def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["regime"]=b["regime"].values
            d["r30"]=c/c.shift(30)-1
            d["r60"]=c/c.shift(60)-1
            d["r5"]=c/c.shift(5)-1
            d["r1"]=c.pct_change()
            lr=np.log(c).diff()
            d["v30"]=lr.rolling(30).std()
            d["v10"]=lr.rolling(10).std()
            d["f10"]=c.shift(-10)/c-1
            d["pos"]=np.arange(len(b))
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    g=D[D.pos%10==0].dropna(subset=["f10"]).copy()
    drift=g.groupby("coin")["f10"].mean()
    usd=g.groupby("coin")["f10"].std()
    g["u"]=g["f10"]-g["coin"].map(drift)
    g["z30"]=g["r30"]/(g["v30"]*np.sqrt(30))
    g["day"]=g["ts"].dt.floor("D")
    g["year"]=g["ts"].dt.year
    g["chop"]=(g["regime"]=="chop")
    g["vr"]=g["v10"]/g["v30"]
    def summ(x,col="u"):
        x=x.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x)})
        s=x.groupby("day")[col].sum(); G=len(s)
        se=np.sqrt((s-x[col].mean()*x.groupby("day")[col].size()).pow(2).sum()*G/(G-1))/len(x)
        return pd.Series({"n":len(x),"days":G,"mean":x[col].mean(),"t":x[col].mean()/se if se>0 else np.nan})
    out={}
    ch=g[g.chop].dropna(subset=["r30"]).copy()
    ch["q"]=pd.qcut(ch["r30"],5,labels=False)
    out["chop_by_r30_quintile"]=ch.groupby("q").apply(summ).join(ch.groupby("q")["r30"].mean().rename("r30mean"))
    ch["qz"]=pd.qcut(ch["z30"],5,labels=False)
    out["chop_by_z30_quintile"]=ch.groupby("qz").apply(summ)
    ch5=ch.dropna(subset=["r5"]).copy(); ch5["q5"]=pd.qcut(ch5["r5"],5,labels=False)
    out["chop_by_r5_quintile"]=ch5.groupby("q5").apply(summ)
    nc=g[~g.chop].dropna(subset=["r30","r60"]).copy()
    nc["tr"]=np.where(nc.r60>0.1,"rising",np.where(nc.r60<-0.1,"falling","other"))
    nc["q"]=nc.groupby("tr")["r30"].transform(lambda s: pd.qcut(s,3,labels=False))
    out["nonchop_trend_r30_tercile"]=nc.groupby(["tr","q"]).apply(summ)
    gv=g.dropna(subset=["vr"]).copy(); gv["qv"]=pd.qcut(gv["vr"],5,labels=False)
    out["all_by_v10_over_v30"]=gv.groupby("qv").apply(summ)
    g1=g.dropna(subset=["r1","v30"]).copy(); g1["z1"]=g1.r1/g1.v30; g1["q1"]=pd.qcut(g1["z1"],5,labels=False)
    out["all_by_1day_z"]=g1.groupby("q1").apply(summ)
    g["wd"]=g.ts.dt.dayofweek
    # chop rise vs fall by year
    ch["side"]=np.sign(ch.r30)
    ch["su"]=ch["u"]*ch["side"]
    out["chop_signed_by_side_year"]=ch.groupby(["side","year"]).apply(summ,col="su")
    # book
    bd=[]
    for coin,wd in data["days"].items():
        for w,d in wd.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; bd.append(x)
    B=pd.concat(bd); B["year"]=pd.to_datetime(B["day"]).dt.year
    out["book_by_window"]=B.groupby("w").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    out["usual_move_mean"]=float(usd.mean())
    return out
