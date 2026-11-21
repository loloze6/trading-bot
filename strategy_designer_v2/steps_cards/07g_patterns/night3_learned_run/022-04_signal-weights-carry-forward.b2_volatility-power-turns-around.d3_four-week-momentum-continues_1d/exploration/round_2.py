import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n":len(x),"mean_%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # weekday robustness: per coin, per year, and cross-coin day-average (removes coin overlap)
    dl = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d.copy(); dd["coin"]=coin; dd["w"]=w; dl.append(dd)
    D = pd.concat(dl); D["day"]=pd.to_datetime(D["day"]); D["wd"]=D["day"].dt.dayofweek; D["yr"]=D["day"].dt.year
    D["cr_dm"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    D["sat"] = D["wd"].isin([4,5])
    out["fri+sat minus other, per coin (Welch)"] = pd.DataFrame([
        dict(coin=c, n_fs=g["sat"].sum(), diff_bps=1e4*(g.loc[g.sat,"coin_return"].mean()-g.loc[~g.sat,"coin_return"].mean()),
             t=stats.ttest_ind(g.loc[g.sat,"coin_return"].dropna(), g.loc[~g.sat,"coin_return"].dropna(), equal_var=False).statistic)
        for c,g in D.groupby("coin")])
    out["fri+sat minus other, per year"] = pd.DataFrame([
        dict(yr=y, diff_bps=1e4*(g.loc[g.sat,"coin_return"].mean()-g.loc[~g.sat,"coin_return"].mean()),
             t=stats.ttest_ind(g.loc[g.sat,"coin_return"].dropna(), g.loc[~g.sat,"coin_return"].dropna(), equal_var=False).statistic)
        for y,g in D.groupby("yr")])
    avg = D.groupby(["w","day","wd"])["cr_dm"].mean().reset_index()
    out["coin-avg demeaned return by weekday"] = avg.groupby("wd")["cr_dm"].apply(tt).unstack()
    # large up-day continuation: per coin, and next-1d vs next-5d
    rows=[]
    for coin in bars:
        for w,b in bars[coin].items():
            c=b["close"].values.astype(float); n=len(c)
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            vol=pd.Series(r1).rolling(20).std().values
            s=pd.Series(c); r28=(s/s.shift(28)-1).values
            for i in range(0,n-5,5):
                rows.append(dict(coin=coin,w=w,z1=r1[i]/vol[i],r28z=r28[i]/(vol[i]*np.sqrt(28)),
                                 fwd5=c[i+5]/c[i]-1, fwd1=c[i+1]/c[i]-1))
    df=pd.DataFrame(rows).dropna()
    df["f5dm"]=df["fwd5"]-df.groupby("coin")["fwd5"].transform("mean")
    df["f1dm"]=df["fwd1"]-df.groupby("coin")["fwd1"].transform("mean")
    res=[]
    for c,g in df.groupby("coin"):
        sl=stats.linregress(g["z1"],g["f5dm"]); sl2=stats.linregress(g["r28z"],g["f5dm"])
        res.append(dict(coin=c,n=len(g),z1_slope_bps=1e4*sl.slope,z1_t=sl.slope/sl.stderr,r28_slope_bps=1e4*sl2.slope,r28_t=sl2.slope/sl2.stderr))
    sl=stats.linregress(df["z1"],df["f5dm"]); res.append(dict(coin="ALL",n=len(df),z1_slope_bps=1e4*sl.slope,z1_t=sl.slope/sl.stderr))
    out["1d z slope & r28z slope per coin (fwd5)"]=pd.DataFrame(res)
    # asymmetry of momentum: slope on positive vs negative r28z
    asy=[]
    for nm,g in (("r28>0",df[df.r28z>0]),("r28<0",df[df.r28z<0])):
        s2=stats.linregress(g["r28z"],g["f5dm"]); asy.append(dict(side=nm,n=len(g),slope_bps=1e4*s2.slope,t=s2.slope/s2.stderr))
    out["momentum slope by side"]=pd.DataFrame(asy)
    # 1d z controlled for r28z
    X=np.c_[np.ones(len(df)),df["z1"],df["r28z"]]; y=df["f5dm"].values
    beta,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-3))
    out["multi: z1 and r28z"]=pd.DataFrame(dict(beta_bps=1e4*beta,t=beta/np.sqrt(np.diag(cov))),index=["const","z1","r28z"])
    # book: worst / best days, what preceded (coin-avg demeaned returns around)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=bk["day"].dt.year
    bk["absc"]=bk["coin_return"].abs()
    bk["vq"]=pd.qcut(bk.groupby("w")["absc"].transform(lambda x:x.rolling(20,min_periods=10).mean()).rank(method="first"),3,labels=False)
    out["book by trailing market vol tercile"]=bk.groupby("vq").agg(n=("book_return","size"),bps=("book_return",lambda x:1e4*x.mean()),
                     sh=("book_return",lambda x:x.mean()/x.std()*np.sqrt(365)),hold_bps=("coin_return",lambda x:1e4*x.mean()))
    return out
