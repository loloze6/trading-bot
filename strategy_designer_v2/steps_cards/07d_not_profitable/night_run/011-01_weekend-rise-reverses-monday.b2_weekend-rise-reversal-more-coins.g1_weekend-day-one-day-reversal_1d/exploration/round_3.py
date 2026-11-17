import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            cl=b["close"]
            b["ret"]=cl.pct_change()
            b["vol"]=b["ret"].rolling(20).std()
            b["z"]=b["ret"]/b["vol"]
            b["ret2"]=cl/cl.shift(2)-1
            b["z2"]=b["ret2"]/(b["vol"]*np.sqrt(2))
            b["f1"]=cl.shift(-1)/cl-1
            b["f2"]=cl.shift(-2)/cl-1
            b["volu"]=b["volume"]/b["volume"].rolling(20).median()
            b["volu2"]=(b["volume"]+b["volume"].shift(1))/(2*b["volume"].rolling(20).median())
            b["pos"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=c; b["win"]=w; b["wd"]=b["ts"].dt.weekday; b["year"]=b["ts"].dt.year
            rows.append(b[["coin","win","wd","year","z","z2","f1","f2","volu","volu2","pos","fee"]])
    B=pd.concat(rows)
    mu=B.groupby("coin")["f1"].mean(); B["mu"]=B["coin"].map(mu)
    def tt(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    out={}
    S=B[B.wd==6].dropna(subset=["z2","f2"]).copy()
    S["fadeW2"]=-S["z2"]*(S["f2"]-2*S["mu"])
    S["fadeW1"]=-S["z2"]*(S["f1"]-S["mu"])
    S["fadeSun2"]=-S["z"]*(S["f2"]-2*S["mu"])
    out["sunday_close_fades"]=pd.DataFrame({k:tt(S[k]) for k in ["fadeW1","fadeW2","fadeSun2"]}).T
    S["aq"]=pd.qcut(S["z2"].abs(),5,labels=False)
    out["weekend2d_by_absz"]=S.groupby("aq").apply(lambda s: pd.Series({"absz2":s["z2"].abs().mean(),"signfade2":(-np.sign(s["z2"])*(s["f2"]-2*s["mu"])).mean(),"n":len(s)}))
    S["vq"]=pd.qcut(S["volu2"],3,labels=False)
    out["weekend2d_by_vol"]=S.groupby("vq").apply(lambda s: tt(-s["z2"]*(s["f2"]-2*s["mu"])))
    out["weekend2d_by_year"]=S.groupby("year").apply(lambda s: tt(-s["z2"]*(s["f2"]-2*s["mu"])))
    Sat=B[B.wd==5].dropna(subset=["z","f2"]).copy()
    Sat["fadeSat_toSun"]=-Sat["z"]*(Sat["f1"]-Sat["mu"])
    Sat["fadeSat_toMon"]=-Sat["z"]*(Sat["f2"]-2*Sat["mu"])
    out["saturday_fades"]=pd.DataFrame({k:tt(Sat[k]) for k in ["fadeSat_toSun","fadeSat_toMon"]}).T
    W=B[B.wd.isin([5,6])].copy(); W["g"]=W["pos"]*W["f1"]
    out["weekend_net_by_day"]=W.groupby("wd").apply(lambda s: pd.Series({"gross":s["g"].mean(),"fee":s["fee"].mean(),"net":s["g"].mean()-s["fee"].mean()}))
    return out
