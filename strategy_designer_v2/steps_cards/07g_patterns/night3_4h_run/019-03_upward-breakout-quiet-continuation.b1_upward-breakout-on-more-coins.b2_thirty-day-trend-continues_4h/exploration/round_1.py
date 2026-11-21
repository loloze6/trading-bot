def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]
    hb=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            n=len(df)
            rng=(hi-lo)/c
            r1=c.pct_change()
            feat=pd.DataFrame({
                "coin":coin,"win":w,
                "fc":df["forecast"].astype(float),
                "fwd":c.shift(-H)/c-1,
                "r6":c/c.shift(6)-1,
                "r18":c/c.shift(18)-1,
                "r180":c/c.shift(180)-1,
                "r360":c/c.shift(360)-1,
                "comp":rng.rolling(30).mean()/rng.rolling(180).mean(),
                "vol":r1.rolling(30).std(),
                "vol180":r1.rolling(180).std(),
                "lastbar":r1,
                "lastrng":rng/rng.rolling(30).mean(),
            })
            feat=feat.iloc[::H]
            rows.append(feat)
            ts=pd.to_datetime(df["timestamp"])
            nxt=c.shift(-1)/c-1
            hb.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"nxt":nxt,
                                    "pos":df["postRebalance_current_allocation"].astype(float)}))
    g=pd.concat(rows,ignore_index=True).dropna(subset=["fwd"])
    st=g.groupby("coin")["fwd"].agg(["mean","std"])
    g["ex"]=g["fwd"]-g["coin"].map(st["mean"])
    g["s"]=g["ex"]/g["coin"].map(st["std"])
    g["absz"]=g["fwd"].abs()/g["coin"].map(st["std"])
    out={}
    def tab(col,q=5,val="s"):
        d=g.dropna(subset=[col]).copy()
        d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        a=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=(val,"size"),mean=(val,"mean"),sd=(val,"std"),
                              ex_pct=("ex","mean"),absz=("absz","mean"))
        a["t"]=a["mean"]/(a["sd"]/np.sqrt(a["n"]))
        return a.drop(columns="sd").round(4)
    d=g.copy(); d["fb"]=pd.cut(d["fc"],[-1,0,5,10,15,21],labels=["0","0-5","5-10","10-15","15-20"])
    a=d.groupby("fb").agg(n=("s","size"),s=("s","mean"),sd=("s","std"),ex=("ex","mean"))
    a["t"]=a["s"]/(a["sd"]/np.sqrt(a["n"])); out["fc_bins"]=a.round(4)
    for col in ["r180","r360","r6","r18","comp","vol","lastrng"]:
        out["q_"+col]=tab(col)
    # breakout direction after compression: sign of 6-bar return x excess, by comp quintile
    d=g.dropna(subset=["comp","r6"]).copy()
    d["b"]=pd.qcut(d["comp"].rank(method="first"),5,labels=False)
    d["dir"]=np.sign(d["r6"])*d["s"]
    a=d.groupby("b").agg(n=("dir","size"),m=("dir","mean"),sd=("dir","std"))
    a["t"]=a["m"]/(a["sd"]/np.sqrt(a["n"])); out["comp_dir6"]=a.round(4)
    # forecast>0 split by vol relative
    d=g[g.fc>0].dropna(subset=["vol","vol180"]).copy()
    d["vr"]=d["vol"]/d["vol180"]
    d["b"]=pd.qcut(d["vr"].rank(method="first"),3,labels=False)
    a=d.groupby("b").agg(n=("s","size"),m=("s","mean"),sd=("s","std"))
    a["t"]=a["m"]/(a["sd"]/np.sqrt(a["n"])); out["fcpos_by_volratio"]=a.round(4)
    h=pd.concat(hb,ignore_index=True).dropna(subset=["nxt"])
    h["z"]=h["nxt"]/h["coin"].map(h.groupby("coin")["nxt"].std())
    for k in ["hour","wd"]:
        a=h.groupby(k).agg(n=("z","size"),bps=("nxt",lambda x:x.mean()*1e4),m=("z","mean"),sd=("z","std"))
        a["t"]=a["m"]/(a["sd"]/np.sqrt(a["n"])); out["bar_"+k]=a.drop(columns="sd").round(3)
    return out
