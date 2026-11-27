import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            width=((b["high"]-b["low"])/c)/sd
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(c-b["low"])/rng
            nxt=c.shift(-1)/c-1
            tr=100*(c/c.shift(60)-1)
            volr=sd/sd.expanding(min_periods=60).median()
            df=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "regime":b["regime"],"cl":cl,"width":width,"nxt":nxt,"tr":tr,"volr":volr,
                "pos":b["postRebalance_current_allocation"],"r1":r})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["nxt"])
    drift=D.groupby("coin")["nxt"].mean()
    D["dev"]=D["nxt"]-D["coin"].map(drift)
    D["day"]=D["ts"].dt.floor("D")
    def ct(g,sign=1):
        g=g.dropna(subset=["dev"]); x=g["dev"]*sign; n=len(x)
        if n<5: return pd.Series({"n":n,"mean%":np.nan,"t":np.nan,"days":0})
        m=x.mean(); S=(x-m).groupby(g["day"]).sum(); G=len(S)
        se=np.sqrt(G/(G-1)*(S**2).sum())/n
        return pd.Series({"n":n,"mean%":100*m,"t":m/se,"days":G})
    D["wq"]=pd.qcut(D["width"],3,labels=["narrow","mid","wide"])
    D["trend"]=pd.cut(D["tr"],[-1e9,-10,10,1e9],labels=["falling","choppy","rising"])
    D["agit"]=np.where(D["volr"]>1,"agit_proxy","calm_proxy"); D.loc[D["volr"].isna(),"agit"]=np.nan
    out_={}
    O=D[D["regime"]=="chop"]
    lo=O[O["cl"]<=0.25]; hi=O[O["cl"]>=0.75]
    out_["out-profile low close x trend x width (long)"]=lo.groupby(["trend","wq"]).apply(ct)
    out_["out-profile high close x trend x width (long sign)"]=hi.groupby(["trend","wq"]).apply(ct)
    w=lo[lo["wq"]=="wide"]
    out_["out-profile wide low close x trend x agit proxy"]=w.groupby(["trend","agit"]).apply(ct)
    wh=hi[hi["wq"]=="wide"]
    out_["out-profile wide high close x trend x agit proxy (long sign)"]=wh.groupby(["trend","agit"]).apply(ct)
    # graded: all wide low closes, width quintile
    L=D[D["cl"]<=0.25].copy()
    L["w5"]=pd.qcut(L["width"],5,labels=False)
    out_["all low closes by width quintile"]=L.groupby("w5").apply(ct)
    H=D[D["cl"]>=0.75].copy()
    H["w5"]=pd.qcut(H["width"],5,labels=False)
    out_["all high closes by width quintile (long sign)"]=H.groupby("w5").apply(ct)
    # book: biggest gain/loss days
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd.append(d.assign(coin=coin))
    DD=pd.concat(dd)
    act=DD[DD["book_return"].abs()>0]
    out_["book active days count"]=len(act)
    out_["book return quantiles on active days"]=act["book_return"].quantile([.01,.05,.25,.5,.75,.95,.99])
    return out_
