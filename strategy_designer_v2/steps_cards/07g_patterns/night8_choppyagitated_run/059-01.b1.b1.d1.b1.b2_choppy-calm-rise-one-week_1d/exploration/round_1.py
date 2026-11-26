def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        fr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-7,7):
                fr.append(c[i+7]/c[i]-1)
        drift[coin]=np.mean(fr) if fr else np.nan
    # agitation proxy: coin's 30d vol vs its median over its windows
    for coin,ws in data["bars"].items():
        vols=[]
        tmp=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            r7=c/c.shift(7)-1
            mabs=r7.abs().rolling(30).mean()
            s=r7/mabs
            tr60=c/c.shift(60)-1
            fwd=c.shift(-7)/c-1
            fwd3=c.shift(-3)/c-1
            df=pd.DataFrame({"s":s,"tr60":tr60,"vol30":vol30,"fwd":fwd,"fwd3":fwd3,
                             "regime":b["regime"],"fc":b["forecast"],
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "ret1":r1,"rng":(b["high"]-b["low"])/c})
            df["grid"]=(np.arange(len(df))%7==0)
            df["coin"]=coin; df["w"]=w
            tmp.append(df)
        d=pd.concat(tmp)
        med=d["vol30"].median()
        d["agit"]=np.where(d["vol30"]>med,"agit","calm")
        d["trend"]=np.where(d["tr60"]>0.1,"rising",np.where(d["tr60"]<-0.1,"falling","choppy"))
        d.loc[d["tr60"].isna(),"trend"]=np.nan
        d["ex"]=d["fwd"]-drift[coin]
        rows.append(d)
    A=pd.concat(rows)
    G=A[A["grid"]&A["fwd"].notna()&A["s"].notna()].copy()
    G["sq"]=pd.qcut(G["s"],5,labels=["q1","q2","q3","q4","q5"])
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex%":g["ex"].mean()*100,
            "t":g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["all by s quintile"]=G.groupby("sq").apply(summ)
    G["prof"]=G["trend"].astype(str)+" "+G["agit"]
    out["by profile x s quintile mean_ex%"]=G.groupby(["prof","sq"])["ex"].mean().unstack()*100
    out["by profile x s quintile n"]=G.groupby(["prof","sq"])["ex"].size().unstack()
    # slope t of ex on s by profile
    res={}
    for p,g in G.groupby("prof"):
        if len(g)>20:
            sl=stats.linregress(g["s"],g["ex"]); res[p]={"n":len(g),"slope":sl.slope*100,"t":sl.slope/sl.stderr}
    out["slope ex on s by profile"]=pd.DataFrame(res).T
    G["in"]=G["regime"]=="unknown"
    res={}
    for p,g in G.groupby("in"):
        sl=stats.linregress(g["s"],g["ex"]); res[str(p)]={"n":len(g),"slope":sl.slope*100,"t":sl.slope/sl.stderr}
    out["slope by in-profile(regime)"]=pd.DataFrame(res).T
    out["weekday"]=A[A["ret1"].notna()].groupby("wd")["ret1"].agg(lambda x: pd.Series([x.mean()*100]).iloc[0]).to_frame("mean%").join(
        A[A["ret1"].notna()].groupby("wd")["ret1"].agg(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).to_frame("t"))
    # book days
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book daily by window"]=D.groupby("w")["book_return"].agg(["mean","std","count"])*[100,100,1]
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            tt=t.copy(); tt["coin"]=coin; T.append(tt)
    T=pd.concat(T)
    T["fcq"]=pd.qcut(T["entry_forecast"],4,duplicates="drop")
    out["trades by entry forecast"]=T.groupby("fcq")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
