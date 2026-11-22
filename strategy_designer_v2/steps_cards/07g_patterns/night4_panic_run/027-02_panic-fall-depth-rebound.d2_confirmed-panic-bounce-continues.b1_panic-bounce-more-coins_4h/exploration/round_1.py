import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=84
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    rows=[]; hourly=[]
    for coin,wins in bars.items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            rng6=hi.rolling(6).max()-lo.rolling(6).min()
            rngrel=rng6/c
            mult=rngrel/rngrel.rolling(180,min_periods=30).mean()
            r6=c/c.shift(6)-1
            r1=np.log(c/c.shift(1))
            vol=r1.rolling(180,min_periods=60).std()
            z6=r6/(vol*np.sqrt(6))
            r42=c/c.shift(42)-1
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(df["timestamp"])
            hourly.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"f1":fwd1,"z6":z6}))
            n=len(df)
            # grid samples
            for s in range(0,n,H):
                cell=slice(s,min(s+H,n))
                rows.append(dict(coin=coin,w=w,pos=s,year=ts.iloc[s].year,fwd=fwd.iloc[s],z6=z6.iloc[s],
                                 mult=mult.iloc[s],vol=vol.iloc[s],r42=r42.iloc[s],r6=r6.iloc[s]))
            # panic events: first bar per grid cell where mult>=3 and r6<0 (at end of stretch)
            pan=(mult>=3)&(r6<0)
            for s in range(0,n,H):
                idx=np.where(pan.iloc[s:s+H].values)[0]
                if len(idx):
                    i=s+idx[0]
                    rows.append(dict(coin=coin,w=w,pos=-1,panic=1,fwd=fwd.iloc[i],z6=z6.iloc[i],mult=mult.iloc[i],
                                     r6=r6.iloc[i],r42=r42.iloc[i],vol=vol.iloc[i],year=ts.iloc[i].year,
                                     fwd6=(c.shift(-6)/c-1).iloc[i], fwd84_after6=(c.shift(-90)/c.shift(-6)-1).iloc[i]))
    R=pd.DataFrame(rows)
    G=R[R.pos>=0].dropna(subset=["fwd"]).copy()
    cm=G.groupby("coin")["fwd"].mean()
    G["ex"]=G["fwd"]-G["coin"].map(cm)
    P=R[R.pos==-1].copy(); P["ex"]=P["fwd"]-P["coin"].map(cm)
    out={}
    def tab(df,key,q=5):
        d=df.dropna(subset=[key,"ex"]).copy()
        d["b"]=pd.qcut(d[key],q,labels=False,duplicates="drop")
        g=d.groupby("b")["ex"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["keymean"]=d.groupby("b")[key].mean(); return g.round(4)
    out["grid ex by z6 (24h move z)"]=tab(G,"z6")
    out["grid ex by vol level"]=tab(G,"vol")
    out["grid ex by 7d return"]=tab(G,"r42")
    out["grid ex by range mult"]=tab(G,"mult")
    out["grid ex by year"]=G.groupby("year")["ex"].agg(["count","mean"]).round(4)
    Pd=P.dropna(subset=["ex"])
    out["panic n, mean ex, t"]=pd.Series({"n":len(Pd),"mean":Pd.ex.mean(),"t":stats.ttest_1samp(Pd.ex,0).statistic,"mean_fwd":Pd.fwd.mean()}).round(4)
    out["panic ex by r6 depth"]=tab(Pd,"r6",4)
    out["panic ex by mult"]=tab(Pd,"mult",4)
    out["panic ex by prior 7d"]=tab(Pd,"r42",4)
    out["panic ex by year"]=Pd.groupby("year")["ex"].agg(["count","mean"]).round(4)
    Hh=pd.concat(hourly).dropna(subset=["f1"])
    g=Hh.groupby("hour")["f1"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"])); out["next-bar ret by hour"]=g.round(5)
    g=Hh.groupby("wd")["f1"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"])); out["next-bar ret by weekday"]=g.round(5)
    # book
    D=[]
    for coin,wins in days.items():
        for w,df in wins.items():
            d=df[["day","book_return","coin_return"]].copy(); d["w"]=w; d["coin"]=coin; D.append(d)
    D=pd.concat(D).dropna()
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean()
    out["book daily mean/std, coin"]=bk.agg(["mean","std","count"]).round(5)
    # trades
    T=[]
    for coin,wins in trades.items():
        for w,df in wins.items():
            if len(df): d=df.copy(); d["coin"]=coin; T.append(d)
    T=pd.concat(T)
    T["fb"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades by entry forecast q"]=T.groupby("fb")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    out["trades by entry year"]=T.groupby(pd.to_datetime(T.entry_time).dt.year)["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    return out
