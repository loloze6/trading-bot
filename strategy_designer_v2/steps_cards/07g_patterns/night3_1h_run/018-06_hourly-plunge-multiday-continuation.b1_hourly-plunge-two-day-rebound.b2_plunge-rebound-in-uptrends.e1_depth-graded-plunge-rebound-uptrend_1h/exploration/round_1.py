def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=96
    rows=[]
    hrs=[]
    for coin,ws in data["bars"].items():
        recs=[]
        for w,df in ws.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            r24=c/c.shift(24)-1
            mad=r24.abs().rolling(720,min_periods=360).mean()
            z=r24/mad
            r30=c/c.shift(720)-1
            r7=c/c.shift(168)-1
            f96=c.shift(-H)/c-1
            f24=c.shift(-24)/c-1
            f240=c.shift(-240)/c-1
            fc=df["forecast"].astype(float)
            ts=pd.to_datetime(df["timestamp"])
            g=np.arange(len(df))%H==0
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r30":r30,"r7":r7,"mad":mad,"f96":f96,"f24":f24,"f240":f240,"fc":fc,"grid":g,"hour":ts.dt.hour,"wd":ts.dt.weekday})
            recs.append(d)
            h1=c.shift(-1)/c-1
            hrs.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"r":h1,"z":z,"absr1":(c/c.shift(1)-1)}))
        dd=pd.concat(recs)
        drift=dd.loc[dd.grid,"f96"].mean()
        dd["u96"]=dd["f96"]-drift
        sd=dd.loc[dd.grid,"f96"].std()
        dd["s96"]=dd["u96"]/sd
        dd["madq"]=pd.qcut(dd["mad"],3,labels=["lowvol","midvol","highvol"])
        rows.append(dd)
    A=pd.concat(rows)
    G=A[A.grid].dropna(subset=["z","r30","u96"])
    def summ(x,col="u96"):
        v=x[col].dropna()
        n=len(v)
        return pd.Series({"n":n,"mean":v.mean(),"t":v.mean()/(v.std()/np.sqrt(n)) if n>2 else np.nan})
    G["zb"]=pd.cut(G["z"],[-99,-3,-2,-1,0,1,2,3,99])
    G["trend"]=np.where(G["r30"]>0,"up30","down30")
    out={}
    out["u96 by zbin x trend"]=G.groupby(["trend","zb"]).apply(summ).unstack(0)
    out["strength by zbin x trend"]=G.groupby(["trend","zb"]).apply(lambda x:summ(x,"s96")).unstack(0)
    # horizons after deep falls
    hz={}
    for col in ["f24","f96","f240"]:
        Gc=A[A.grid].dropna(subset=["z",col])
        m=Gc.groupby("coin")[col].transform("mean")
        Gc=Gc.assign(u=Gc[col]-m)
        for nm,sel in [("z<-2",Gc.z<-2),("z>2",Gc.z>2),("all",Gc.z==Gc.z)]:
            v=Gc.loc[sel,"u"]
            hz[(col,nm)]=[len(v),v.mean(),v.mean()/(v.std()/np.sqrt(len(v)))]
    out["horizons"]=pd.DataFrame(hz,index=["n","mean","t"]).T
    out["u96 by vol tercile x zsign"]=G.assign(zs=np.sign(G.z)).groupby(["madq","zs"]).apply(summ).unstack(1)
    G["r7b"]=pd.qcut(G["r7"],5,labels=False)
    out["u96 by 7d return quintile"]=G.groupby("r7b").apply(summ)
    out["u96 by weekday"]=G.groupby("wd").apply(summ)
    Hh=pd.concat(hrs).dropna(subset=["r"])
    out["1h return by hour"]=Hh.groupby("hour")["r"].agg(["count","mean",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))])
    # book
    br=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            df=df.copy();df["coin"]=coin;df["w"]=w
            df["n1"]=df.book_return.shift(-1);df["n3"]=df.book_return.shift(-1)+df.book_return.shift(-2)+df.book_return.shift(-3)
            df["c1"]=df.coin_return.shift(-1)
            br.append(df)
    B=pd.concat(br).dropna(subset=["book_return"])
    B=B[B.book_return!=0]
    q=B.book_return.quantile([0.02,0.98])
    out["after book extremes"]=pd.DataFrame({
        "bigloss":B.loc[B.book_return<=q.iloc[0],["n1","n3","c1"]].mean(),
        "biggain":B.loc[B.book_return>=q.iloc[1],["n1","n3","c1"]].mean(),
        "active_all":B[["n1","n3","c1"]].mean()})
    T=[]
    for coin,ws in data["trades"].items():
        for w,df in ws.items():
            if len(df): T.append(df.assign(coin=coin))
    T=pd.concat(T)
    T["eh"]=pd.to_datetime(T.entry_time).dt.hour//6
    T["fq"]=pd.qcut(T.entry_forecast.rank(method="first"),3,labels=False)
    out["trades by entry 6h block"]=T.groupby("eh")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by entry forecast tercile"]=T.groupby("fq")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trade duration h"]=(T.duration_minutes/60).describe()
    return out
