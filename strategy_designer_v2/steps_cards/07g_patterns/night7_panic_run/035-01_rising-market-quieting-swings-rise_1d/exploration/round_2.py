def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            b["fwd1"]=c.shift(-1)/c-1
            b["fwd3"]=c.shift(-3)/c-1
            b["ret3p"]=c/c.shift(3)-1
            b["vol30"]=r1.rolling(30).std()
            b["ret3z"]=b["ret3p"]/(b["vol30"]*np.sqrt(3))
            b["ret60"]=c/c.shift(60)-1
            b["rising"]=(b["regime"]=="unknown").astype(int)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["coin"]=coin;b["w"]=w;b["pos"]=np.arange(len(b))
            b["grid"]=(b["pos"]%3==0)
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    def cl(df,col):
        df=df.dropna(subset=[col]); n=len(df); m=df[col].mean()
        dev=(df[col]-m).groupby(df["day"]).sum(); se=np.sqrt((dev**2).sum())/n
        return pd.Series({"n":n,"days":df.day.nunique(),"mean":m,"t_cl":m/se if se>0 else np.nan})
    out={}
    B["fwd1ex"]=B["fwd1"]-B.groupby("coin")["fwd1"].transform("mean")
    out["wd_fwd1_clustered"]=B.groupby("wd").apply(lambda d:cl(d,"fwd1ex"))
    out["wd_fwd1_by_coin_mean"]=B.groupby(["coin","wd"])["fwd1ex"].mean().unstack().round(4)
    out["wd_fwd1_thu_by_year"]=B[B.wd==3].groupby("year").apply(lambda d:cl(d,"fwd1ex"))
    G=B[B.grid & B.fwd3.notna()].copy()
    G["ex"]=G["fwd3"]-G.groupby("coin")["fwd3"].transform("mean")
    R=G[(G.rising==1)&G.ret3z.notna()].copy()
    R["q"]=pd.qcut(R["ret3z"],5,labels=False)
    out["rising_ret3z_q"]=R.groupby("q").apply(lambda d:cl(d,"ex"))
    R["sx"]=R["ex"]*np.sign(R["ret3z"])*0+R["ex"]
    # slope via clustered regression approx: correlation and t by coin
    out["rising_ret3z_corr_by_coin"]=R.groupby("coin").apply(lambda d:d["ret3z"].corr(d["ex"]))
    out["rising_ret3z_top_by_window"]=R[R.q==4].groupby("w")["ex"].mean()
    N=G[(G.rising==0)&G.ret3z.notna()].copy()
    N["q"]=pd.qcut(N["ret3z"],5,labels=False)
    out["notrising_ret3z_q"]=N.groupby("q").apply(lambda d:cl(d,"ex"))
    return out
