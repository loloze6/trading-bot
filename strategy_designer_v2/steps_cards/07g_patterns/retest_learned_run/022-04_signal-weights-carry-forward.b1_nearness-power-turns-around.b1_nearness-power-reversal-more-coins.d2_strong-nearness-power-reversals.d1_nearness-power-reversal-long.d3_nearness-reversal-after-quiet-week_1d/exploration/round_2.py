def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            f=pd.DataFrame(index=b.index)
            f["coin"]=coin; f["w"]=w
            ts=pd.to_datetime(b["timestamp"])
            f["year"]=ts.dt.year.values
            f["wd"]=ts.dt.weekday.values
            f["fwd"]=c.shift(-H)/c-1
            f["fwd1"]=c.shift(-1)/c-1
            f["r1"]=c/c.shift(1)-1
            f["r5"]=c/c.shift(5)-1
            f["r20"]=c/c.shift(20)-1
            f["r60"]=c/c.shift(60)-1
            f["near"]=c/b["high"].astype(float).rolling(60,min_periods=30).max()-1
            f["vol20"]=f["r1"].rolling(20,min_periods=15).std()
            f["volratio"]=f["vol20"]/f["r1"].rolling(60,min_periods=40).std()
            f["rng"]=(b["high"].astype(float)-b["low"].astype(float))/c
            f["fc"]=b["forecast"].astype(float)
            f["alloc"]=b["postRebalance_current_allocation"].astype(float)
            f["grid"]=(np.arange(len(b))%H==0)
            g.append(f)
        g=pd.concat(g,ignore_index=True)
        m5=g.loc[g.grid,"fwd"].mean(); m1=g["fwd1"].mean()
        g["ex"]=g["fwd"]-m5; g["ex1"]=g["fwd1"]-m1
        g["r1z"]=g["r1"]/g["vol20"]; g["r5z"]=g["r5"]/(g["vol20"]*np.sqrt(5))
        g["r20z"]=g["r20"]/(g["vol20"]*np.sqrt(20))
        g["r60z"]=g["r60"]/(g["vol20"]*np.sqrt(60))
        g["volrank"]=g["vol20"].rank(pct=True)
        g["exz"]=g["ex"]/(g.loc[g.grid,"fwd"].std())
        rows.append(g)
    A=pd.concat(rows,ignore_index=True)
    G=A[A.grid & A.ex.notna()]
    out={}
    def qtab(df,col,y="ex",q=5):
        d=df[[col,y]].dropna().copy()
        d["q"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        t=d.groupby("q")[y].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        rho=stats.spearmanr(d[col],d[y])
        t.loc["rho"]=[rho[0],len(d),np.nan,rho[0]*np.sqrt(len(d))]
        return t.round(4)
    for col in ["r1z","r5z","r20z","r60z","near","volrank","volratio","rng"]:
        try: out["grid5 ex by "+col]=qtab(G,col)
        except Exception as e: out["err "+col]=str(e)
    try:
        Gp=G[G.fc>0]
        out["fc>0 by fc quint"]=qtab(Gp,"fc")
        out["fc>0 vs fc=0"]=G.groupby(G.fc>0)["ex"].agg(["mean","count","std"]).round(4)
        out["fc>0 by r5z"]=qtab(Gp,"r5z")
        out["fc=0 by r5z"]=qtab(G[G.fc<=0],"r5z")
    except Exception as e: out["err fc"]=str(e)
    try:
        # r5z effect split by trend regime (sign of 60d return)
        for s,lab in [(1,"r60>0"),(0,"r60<=0")]:
            sub=G[(G.r60>0)==bool(s)]
            out["r5z in "+lab]=qtab(sub,"r5z")
        for lab,sub in [("hi vol",G[G.volrank>0.5]),("lo vol",G[G.volrank<=0.5])]:
            out["r5z in "+lab]=qtab(sub,"r5z")
    except Exception as e: out["err reg"]=str(e)
    try:
        D=A[A.ex1.notna()]
        t=D.groupby("wd")["ex1"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        out["next-day excess by weekday"]=t.round(5)
        out["next-day ex by r1z dec"]=qtab(D,"r1z","ex1",q=10)
        # per coin rho of r5z vs 5d ex
        pc=[]
        for coin,sub in G.groupby("coin"):
            d=sub[["r5z","ex","near"]].dropna()
            if len(d)>30:
                pc.append([coin,len(d),stats.spearmanr(d.r5z,d.ex)[0],stats.spearmanr(d.near,d.ex)[0]])
        out["per coin rho r5z, near vs ex5"]=pd.DataFrame(pc,columns=["coin","n","rho_r5z","rho_near"]).set_index("coin").round(3)
        yr=[]
        for y,sub in G.groupby("year"):
            d=sub[["r5z","ex","near"]].dropna()
            if len(d)>30:
                yr.append([y,len(d),stats.spearmanr(d.r5z,d.ex)[0],stats.spearmanr(d.near,d.ex)[0]])
        out["per year rho r5z, near vs ex5"]=pd.DataFrame(yr,columns=["year","n","rho_r5z","rho_near"]).set_index("year").round(3)
    except Exception as e: out["err daily"]=str(e)
    try:
        bd=[]
        for coin,ws in data["days"].items():
            for w,d in ws.items():
                d=d.copy(); d["coin"]=coin; d["w"]=w; bd.append(d)
        bd=pd.concat(bd,ignore_index=True)
        bd["year"]=pd.to_datetime(bd["day"]).dt.year
        out["book vs coin ann. mean by year"]=(bd.groupby("year")[["book_return","coin_return"]].mean()*365).round(3)
        out["book vs coin ann. mean by coin"]=(bd.groupby("coin")[["book_return","coin_return"]].mean()*365).round(3)
        B=bd.groupby("day")[["book_return","coin_return"]].mean().dropna()
        q=B.book_return.quantile([0.02,0.98])
        out["coin ret on book's worst/best 2% days"]=pd.DataFrame({
            "worst":B[B.book_return<=q.iloc[0]].mean(),"best":B[B.book_return>=q.iloc[1]].mean(),
            "all":B.mean()}).round(4)
    except Exception as e: out["err book"]=str(e)
    try:
        trs=[]
        for coin,ws in data["trades"].items():
            for w,t in ws.items():
                if len(t): trs.append(t.assign(coin=coin))
        T=pd.concat(trs,ignore_index=True)
        T["dur_d"]=T.duration_minutes/1440
        T["fq"]=pd.qcut(T.entry_forecast.rank(method="first"),4,labels=False)
        out["trades by entry fc quartile"]=T.groupby("fq")[["net_profit_loss_percent","dur_d","entry_forecast"]].agg(["mean","count"]).round(3)
    except Exception as e: out["err trades"]=str(e)
    return out
