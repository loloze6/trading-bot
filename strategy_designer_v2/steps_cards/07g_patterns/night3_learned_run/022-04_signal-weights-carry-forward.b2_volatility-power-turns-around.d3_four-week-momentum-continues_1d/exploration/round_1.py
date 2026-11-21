import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].values.astype(float)
            n = len(c)
            if n < 40: continue
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            s = pd.Series(c)
            ret28 = (s/s.shift(28)-1).values
            ret5p = (s/s.shift(5)-1).values
            vol20 = pd.Series(r1).rolling(20).std().values
            hi60 = s.rolling(60, min_periods=20).max().values
            near = c/hi60-1
            fc = b["forecast"].values.astype(float)
            for h in (5,10,20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=fc[i], r28=ret28[i], r5p=ret5p[i], r1=r1[i],
                                     vol=vol20[i], near=near[i], wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                     fwd=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["fwd_dm"] = df["fwd"] - df.groupby(["coin","h"])["fwd"].transform("mean")
    out = {}
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n":len(x),"mean_%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # 1 forecast quintiles, h=5
    d5 = df[df.h==5].copy()
    d5["fq"] = d5.groupby("coin")["f"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["fwd5_dm by forecast quintile"] = d5.groupby("fq")["fwd_dm"].apply(tt).unstack()
    # 2 horizon decay: regress demeaned fwd on r28/vol scaled
    hz = []
    for h in (5,10,20):
        d = df[df.h==h].dropna(subset=["r28","fwd_dm","vol"])
        x = d["r28"]/(d["vol"]*np.sqrt(28))
        sl = stats.linregress(x, d["fwd_dm"])
        hz.append(dict(h=h, n=len(d), slope=sl.slope, t=sl.slope/sl.stderr))
    out["horizon r28z slope"] = pd.DataFrame(hz)
    # 3 after large 1-day moves (z by vol)
    d5["z1"] = d5["r1"]/d5["vol"]
    d5["z1q"] = pd.cut(d5["z1"],[-99,-2,-1,0,1,2,99])
    out["fwd5_dm by 1d z"] = d5.groupby("z1q")["fwd_dm"].apply(tt).unstack()
    # past 5d return z
    d5["z5"] = d5["r5p"]/(d5["vol"]*np.sqrt(5))
    d5["z5q"] = pd.cut(d5["z5"],[-99,-1.5,-0.5,0.5,1.5,99])
    out["fwd5_dm by past5d z"] = d5.groupby("z5q")["fwd_dm"].apply(tt).unstack()
    # 4 vol tercile: momentum slope within
    d5["vq"] = d5.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    vs = []
    for q,g in d5.dropna(subset=["vq","r28","fwd_dm"]).groupby("vq"):
        x = g["r28"]/(g["vol"]*np.sqrt(28)); sl = stats.linregress(x,g["fwd_dm"])
        vs.append(dict(vq=q,n=len(g),slope=sl.slope,t=sl.slope/sl.stderr,mean_fwd_dm=100*g["fwd_dm"].mean(), absfwd=100*g["fwd"].abs().mean()))
    out["by vol tercile"] = pd.DataFrame(vs)
    # 5 nearness to 60d high
    d5["nq"] = d5.groupby("coin")["near"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["fwd5_dm by near60 quintile"] = d5.groupby("nq")["fwd_dm"].apply(tt).unstack()
    # 6 weekday daily coin returns and book returns
    dl = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d.copy(); dd["coin"]=coin; dd["w"]=w; dl.append(dd)
    D = pd.concat(dl); D["day"]=pd.to_datetime(D["day"]); D["wd"]=D["day"].dt.dayofweek; D["yr"]=D["day"].dt.year
    out["coin_return by weekday"] = D.groupby("wd")["coin_return"].apply(tt).unstack()
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=bk["day"].dt.year
    g = bk.groupby("yr").agg(n=("book_return","size"), book_mean_bps=("book_return",lambda x:1e4*x.mean()),
                              book_sh=("book_return",lambda x:x.mean()/x.std()*np.sqrt(365)),
                              hold_sh=("coin_return",lambda x:x.mean()/x.std()*np.sqrt(365)))
    out["book by year"] = g
    # 7 book returns by direction of 28d (long vs short side contribution)
    d5["side"]=np.sign(d5["f"])
    out["signed fwd5_dm by side"] = d5.groupby("side").apply(lambda g: tt(g["fwd_dm"]*g["side"])).reset_index()
    return out
