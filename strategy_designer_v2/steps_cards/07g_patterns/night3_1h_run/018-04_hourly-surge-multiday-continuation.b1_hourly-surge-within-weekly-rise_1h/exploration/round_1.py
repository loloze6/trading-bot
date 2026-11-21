def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hr=[]; bookd=[]
    H=120
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1=c.pct_change()
            r24=c/c.shift(24)-1
            z=r24/r24.abs().rolling(720,min_periods=120).mean().shift(1)
            r168=c/c.shift(168)-1
            r720=c/c.shift(720)-1
            vol=r1.rolling(720,min_periods=120).std()
            volrel=vol/vol.rolling(2160,min_periods=500).mean()
            f24=c.shift(-24)/c-1; f120=c.shift(-H)/c-1
            hi=c.rolling(720,min_periods=200).max(); lo=c.rolling(720,min_periods=200).min()
            pos=(c-lo)/(hi-lo)
            idx=np.arange(0,len(c),H)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z.iloc[idx].values,"r168":r168.iloc[idx].values,
                "r720":r720.iloc[idx].values,"volrel":volrel.iloc[idx].values,"pos":pos.iloc[idx].values,
                "f24":f24.iloc[idx].values,"f120":f120.iloc[idx].values,
                "fc":b["forecast"].iloc[idx].values,"wd":ts.iloc[idx].dt.weekday.values})
            rows.append(d)
            hr.append(pd.DataFrame({"coin":coin,"h":ts.dt.hour,"r":r1.values,"wd":ts.dt.weekday}))
    D=pd.concat(rows); D=D.dropna(subset=["f120"])
    D["drift"]=D.groupby("coin")["f120"].transform("mean")
    D["u"]=D["f120"]-D["drift"]
    def tab(col,q=5):
        x=D.dropna(subset=[col]).copy()
        x["b"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        g=x.groupby("b")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["mean_x"]=x.groupby("b")[col].mean()
        return g.round(4)
    out={}
    for col in ["z","r168","r720","volrel","pos"]:
        out["u120 by "+col]=tab(col)
    # spearman per coin
    sp={}
    for col in ["z","r168","r720","volrel","pos"]:
        for coin,g in D.dropna(subset=[col]).groupby("coin"):
            sp[(col,coin)]=stats.spearmanr(g[col],g["u"])[0]
    out["spearman col x coin"]=pd.Series(sp).unstack().round(3)
    # z by sign of r168
    x=D.dropna(subset=["z","r168"]).copy()
    x["zb"]=pd.cut(x["z"],[-99,-2,-1,0,1,2,99]); x["up"]=x["r168"]>0
    g=x.groupby(["up","zb"])["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["u120 by week sign x z"]=g.round(4)
    Hh=pd.concat(hr).dropna()
    Hh["u"]=Hh["r"]-Hh.groupby("coin")["r"].transform("mean")
    g=Hh.groupby("h")["u"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["1h ret by hour bps"]=(g.assign(mean=g["mean"]*1e4)).round(2)
    # book days
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd.append(d.assign(coin=coin,w=w))
    Dd=pd.concat(dd).dropna(subset=["book_return"])
    Dd["wd"]=pd.to_datetime(Dd["day"]).dt.weekday
    g=Dd.groupby("wd")[["book_return","coin_return"]].mean()*1e4
    out["book/coin daily by weekday bps"]=g.round(2)
    bw=Dd.groupby("w")[["book_return","coin_return"]].agg(["mean","std"])
    out["by window"]=(bw*1e4).round(1)
    return out
