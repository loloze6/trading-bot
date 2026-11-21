import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); hi = df["high"].values.astype(float); lo = df["low"].values.astype(float)
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            for h in (7, 26):
                for t in range(0, n-h, h):
                    fwd = c[t+h]/c[t]-1
                    past26 = c[t]/c[t-26]-1 if t>=26 else np.nan
                    past7 = c[t]/c[t-7]-1 if t>=7 else np.nan
                    vol20 = np.nanstd(r1[max(1,t-19):t+1]) if t>=20 else np.nan
                    if t>=25:
                        H=hi[t-25:t+1].max(); L=lo[t-25:t+1].min()
                        rngpos=(c[t]-L)/(H-L) if H>L else np.nan
                    else: rngpos=np.nan
                    rows.append(dict(coin=coin,w=w,h=h,fwd=fwd,past26=past26,past7=past7,vol20=vol20,
                                     rngpos=rngpos,fc=df["forecast"].iloc[t],
                                     trend=float(df["regime"].iloc[t]=="trending"),
                                     wd=pd.Timestamp(df["timestamp"].iloc[t]).weekday()))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby(["coin","h"])["fwd"].transform("mean")
    g["z"] = g["ex"]/g.groupby(["coin","h"])["fwd"].transform("std")
    res=[]
    for h in (7,26):
        s=g[g.h==h]
        for f in ["past26","past7","vol20","rngpos","fc","trend"]:
            x=s[[f,"z","coin"]].dropna()
            # standardise feature within coin
            x=x.assign(fz=x.groupby("coin")[f].transform(lambda v:(v-v.mean())/v.std()))
            r,p=stats.pearsonr(x["fz"],x["z"])
            percoin=x.groupby("coin").apply(lambda d: np.corrcoef(d["fz"],d["z"])[0,1])
            res.append(dict(h=h,feat=f,n=len(x),corr=r,t=r*np.sqrt((len(x)-2)/(1-r*r)),
                            coins_pos=(percoin>0).sum(),minc=percoin.min(),maxc=percoin.max()))
    out["feature_vs_fwd_z"]=pd.DataFrame(res)
    # quintiles of rngpos and past26 at h=26
    s=g[(g.h==26)].dropna(subset=["rngpos","past26"])
    s=s.assign(q=s.groupby("coin")["rngpos"].transform(lambda v: pd.qcut(v,3,labels=False,duplicates="drop")))
    out["h26_by_rngpos_tercile"]=s.groupby("q")[["fwd","ex","z"]].agg(["mean","count"])
    s=s.assign(q2=s.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v,3,labels=False,duplicates="drop")))
    out["h26_by_vol_tercile"]=s.groupby("q2")[["fwd","z"]].agg(["mean","count"])
    # daily: weekday and after big moves
    d=[]
    for coin,wins in bars.items():
        for w,df in wins.items():
            c=df["close"].values.astype(float)
            r=pd.Series(c).pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            zz=r/sd
            nxt=r.shift(-1); n5=pd.Series(c).shift(-5)/pd.Series(c)-1
            wd=pd.to_datetime(df["timestamp"]).dt.weekday.values
            d.append(pd.DataFrame(dict(coin=coin,r=r,zz=zz,nxt=nxt,n5=n5,wd=wd)))
    d=pd.concat(d)
    out["weekday"]=d.groupby("wd")["r"].agg(["mean","std","count"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    d["zb"]=pd.cut(d["zz"],[-99,-2,-1,1,2,99])
    out["after_move_z"]=d.groupby("zb")[["nxt","n5"]].agg(["mean","count"])
    # book
    bk=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            bk.append(df.assign(coin=coin,w=w))
    bk=pd.concat(bk)
    out["book_by_coin"]=bk.groupby("coin")[["book_return","coin_return"]].mean()*1e4
    return out
