def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        recs=[]
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            feat=pd.DataFrame({
                "fwd":c.shift(-H)/c-1,
                "p5":c/c.shift(5)-1,
                "p1":r1,
                "p20":c/c.shift(20)-1,
                "vol20":r1.rolling(20).std(),
                "rng":(df["high"]-df["low"])/c,
                "raw":df.get("debug_info.components.support_break.last_history_value"),
                "fc":df["forecast"],
                "hi20":c/c.rolling(20).max()-1,
                "lo20":c/c.rolling(20).min()-1,
                "wd":pd.to_datetime(df["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(df["timestamp"]).dt.year,
            })
            feat["volchg"]=feat["vol20"]/r1.rolling(60).std()
            g=feat.iloc[::H].copy(); g["coin"]=coin; g["win"]=w
            recs.append(g)
        d=pd.concat(recs)
        d=d.dropna(subset=["fwd"])
        d["u"]=d["fwd"]-d["fwd"].mean()
        d["usd"]=d["fwd"].std()
        d["s"]=d["u"]/d["usd"]
        rows.append(d)
    D=pd.concat(rows)
    out={}
    out["n_cases"]=len(D)
    def qtab(col):
        x=D.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        t=x.groupby("q")["s"].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["u_mean"]=x.groupby("q")["u"].mean()
        # per coin spearman
        cc=x.groupby("coin").apply(lambda g: stats.spearmanr(g[col],g["s"])[0])
        t["coins_pos_rho"]=(cc>0).sum()
        t["rho_pooled"]=stats.spearmanr(x[col],x["s"])[0]
        return t.drop(columns="std")
    for col in ["p1","p5","p20","vol20","rng","hi20","lo20","volchg"]:
        out["q_"+col]=qtab(col)
    x=D.copy(); x["broken"]=(x["raw"].fillna(0)>0)
    t=x.groupby("broken")["s"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["broken_vs_not"]=t
    xb=x[x.broken]
    out["broken_q_raw"]=xb.assign(q=pd.qcut(xb["raw"].rank(method="first"),4,labels=False)).groupby("q")["s"].agg(["mean","count"])
    t=D.groupby("wd")["s"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday"]=t
    out["year"]=D.groupby("yr")["s"].agg(["mean","count"])
    # book
    bk=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            bk.append(df.assign(coin=coin,win=w))
    B=pd.concat(bk)
    daily=B.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_daily"]=pd.Series({"book_mean":daily.book_return.mean(),"coin_mean":daily.coin_return.mean(),"corr":daily.corr().iloc[0,1]})
    # book by coin
    out["book_by_coin"]=B.groupby("coin")[["book_return","coin_return"]].mean()
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,df in wins.items():
            tr.append(df.assign(coin=coin))
    T=pd.concat(tr)
    out["trades"]=T.groupby(["coin","side"])["net_profit_loss_percent"].agg(["mean","count"])
    return out
