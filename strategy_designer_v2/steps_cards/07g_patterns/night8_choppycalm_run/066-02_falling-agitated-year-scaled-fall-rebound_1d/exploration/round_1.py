def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<5: continue
            c=b["close"]
            r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "ret":r,"nxt":c.shift(-1)/c-1,"nxt2":c.shift(-2)/c.shift(-1)-1,
                "reg":b["regime"].astype(str),"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"],
                "sd30":r.rolling(30,min_periods=20).std(),
                "tr60":c/c.shift(60)-1,
                "cl":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "rng":(b["high"]-b["low"])/c.shift(1)})
            d["pos"]=np.arange(len(d))
            rows.append(d)
    P=pd.concat(rows,ignore_index=True)
    drift=P.groupby("coin")["ret"].mean()
    P["ex"]=P["nxt"]-P["coin"].map(drift)
    P["ex2"]=P["nxt2"]-P["coin"].map(drift)
    P["z30"]=P["ret"]/P["sd30"]
    P["day"]=P["ts"].dt.floor("D")
    P["wd"]=P["ts"].dt.dayofweek
    def ct(df,col):
        df=df.dropna(subset=[col])
        n=len(df)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan,"days":0})
        m=df[col].mean()
        g=(df[col]-m).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan,"days":df["day"].nunique()})
    out={}
    out["regime counts"]=P["reg"].value_counts()
    inn=P[P["reg"]=="unknown"]; outp=P[P["reg"]!="unknown"]
    # A: next-day excess by z30 bin, in and out of profile
    bins=[-99,-2,-1,-0.5,0,0.5,1,2,99]
    for nm,df in [("in",inn),("out",outp)]:
        df=df.dropna(subset=["z30"]).copy()
        df["b"]=pd.cut(df["z30"],bins)
        out[f"A {nm}: next ex by z30"]=df.groupby("b",observed=True).apply(lambda g:ct(g,"ex"))
    # day2 after falls in profile
    df=inn.dropna(subset=["z30"]).copy(); df["b"]=pd.cut(df["z30"],bins)
    out["B in: day-2 ex by z30"]=df.groupby("b",observed=True).apply(lambda g:ct(g,"ex2"))
    # out of profile split by trend proxy, up days
    o=outp.dropna(subset=["z30","tr60"]).copy()
    o["trend"]=np.where(o["tr60"]>0.1,"rising",np.where(o["tr60"]<-0.1,"falling","choppy"))
    o["b"]=pd.cut(o["z30"],[-99,-1,0,1,99])
    out["C out: ex by trend x z30"]=o.groupby(["trend","b"],observed=True).apply(lambda g:ct(g,"ex"))
    # close location on fall days in profile
    f=inn[inn["ret"]<0].dropna(subset=["cl"]).copy()
    f["clb"]=pd.cut(f["cl"],[0,0.25,0.5,0.75,1.0001],include_lowest=True)
    out["D in falls: ex by close loc"]=f.groupby("clb",observed=True).apply(lambda g:ct(g,"ex"))
    # weekday on in-profile falls
    out["E in falls: ex by weekday"]=f.groupby("wd").apply(lambda g:ct(g,"ex"))
    # book: positions and largest days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    D=pd.concat(dd,ignore_index=True)
    bk=D.groupby(["win","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["count","mean","std","sum"])
    act=D[D["book_return"].abs()>1e-9].dropna(subset=["book_return"])
    out["active coin-days by coin"]=act.groupby("coin")["book_return"].agg(["count","mean","sum"])
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)],ignore_index=True)
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby(pd.cut(T["entry_forecast"],[0,1,3,6,10,21]),observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trade duration"]=T["dur_d"].describe()
    return out
