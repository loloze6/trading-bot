def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    drows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            f=pd.DataFrame({"coin":coin,"w":w})
            f=pd.DataFrame(index=b.index)
            f["coin"]=coin; f["w"]=w
            f["year"]=pd.to_datetime(b["timestamp"]).dt.year
            f["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            f["fwd"]=c.shift(-H)/c-1
            f["fwd1"]=c.shift(-1)/c-1
            f["r1"]=c/c.shift(1)-1
            f["r5"]=c/c.shift(5)-1
            f["r20"]=c/c.shift(20)-1
            f["r60"]=c/c.shift(60)-1
            f["near"]=c/b["high"].astype(float).rolling(60,min_periods=30).max()-1
            f["vol20"]=f["r1"].rolling(20,min_periods=15).std()
            f["volratio"]=f["vol20"]/f["r1"].rolling(60,min_periods=40).std()
            f["rng"]=(b["high"]-b["low"])/c
            f["fc"]=b["forecast"].astype(float)
            f["alloc"]=b["postRebalance_current_allocation"].astype(float)
            f["grid"]=(np.arange(len(b))%H==0)
            g.append(f)
        g=pd.concat(g)
        m5=g.loc[g.grid,"fwd"].mean(); m1=g["fwd1"].mean()
        g["ex"]=g["fwd"]-m5; g["ex1"]=g["fwd1"]-m1
        g["r1z"]=g["r1"]/g["vol20"]; g["r5z"]=g["r5"]/(g["vol20"]*np.sqrt(5))
        g["r20z"]=g["r20"]/(g["vol20"]*np.sqrt(20))
        # coin-relative vol level rank
        g["volrank"]=g["vol20"].rank(pct=True)
        rows.append(g)
    A=pd.concat(rows)
    G=A[A.grid & A.ex.notna()]
    out={}
    def qtab(df,col,y="ex",q=5):
        d=df[[col,y]].dropna()
        d["q"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        t=d.groupby("q")[y].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        rho=stats.spearmanr(d[col],d[y])
        t.loc["rho"]=[rho[0],len(d),np.nan,rho[0]*np.sqrt(len(d))]
        return t.round(4)
    for col in ["r1z","r5z","r20z","r60","near","volrank","volratio","rng"]:
        out["grid5 by "+col]=qtab(G,col)
    Gp=G[G.fc>0]
    out["fc>0 by fc quint"]=qtab(Gp,"fc")
    out["fc>0 vs fc=0"]=G.groupby(G.fc>0)["ex"].agg(["mean","count","std"]).round(4)
    out["fc>0 by r5z"]=qtab(Gp,"r5z")
    # daily: next-day by weekday
    D=A[A.ex1.notna()]
    t=D.groupby("wd")["ex1"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["next-day excess by weekday"]=t.round(5)
    out["next-day by r1z"]=qtab(D,"r1z","ex1",q=10)
    # book
    bd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; bd.append(d)
    bd=pd.concat(bd)
    bd["year"]=pd.to_datetime(bd["day"]).dt.year
    yt=bd.groupby("year")[["book_return","coin_return"]].mean()*365
    out["book vs coin annualised mean by year"]=yt.round(3)
    ct=bd.groupby("coin")[["book_return","coin_return"]].mean()*365
    out["book vs coin by coin"]=ct.round(3)
    return out
