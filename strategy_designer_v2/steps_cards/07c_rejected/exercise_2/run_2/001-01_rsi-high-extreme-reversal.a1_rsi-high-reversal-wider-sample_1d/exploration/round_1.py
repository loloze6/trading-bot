def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            d=c.diff()
            up=d.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
            dn=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
            rsi=100-100/(1+up/dn)
            z=(rsi-rsi.rolling(60,min_periods=20).mean())/rsi.rolling(60,min_periods=20).std()
            r20=c/c.shift(20)-1
            yr=pd.to_datetime(df["timestamp"]).dt.year
            for h in [1,5,10,20]:
                idx=np.arange(0,len(df),h)
                fr=(c.shift(-h)/c-1).values
                for i in idx:
                    if np.isnan(fr[i]): continue
                    rows.append(dict(coin=coin,w=w,h=h,rsi=rsi.iloc[i],z=z.iloc[i],fc=df["forecast"].iloc[i],r20=r20.iloc[i],yr=yr.iloc[i],fr=fr[i]))
    R=pd.DataFrame(rows)
    R["ex"]=R["fr"]-R.groupby(["coin","h"])["fr"].transform("mean")
    R=R.dropna(subset=["rsi"])
    R["rb"]=pd.cut(R["rsi"],[0,30,40,50,60,70,80,100])
    def agg(g):
        return pd.Series(dict(n=len(g),mean=g["ex"].mean(),t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out={}
    out["rsi_bucket_by_h"]=R.groupby(["h","rb"]).apply(agg).unstack(0)
    R5=R[R.h==5]
    out["h5_coin_rsi>70"]=R5[R5.rsi>70].groupby("coin").apply(agg)
    out["h5_coin_rsi<30"]=R5[R5.rsi<30].groupby("coin").apply(agg)
    out["h5_year_rsi>70"]=R5[R5.rsi>70].groupby("yr").apply(agg)
    out["h5_fc<=-5_by_h"]=R[R.fc<=-5].groupby("h").apply(agg)
    # regime: 20-day return sign
    R5b=R5.dropna(subset=["r20"]).copy()
    R5b["reg"]=np.where(R5b.r20>0,"up20","down20")
    out["h5_reg_rb"]=R5b.groupby(["reg","rb"]).apply(agg).unstack(0)
    # correlation rsi vs ex per h
    out["spearman_rsi_ex"]=R.groupby("h").apply(lambda g: pd.Series(stats.spearmanr(g.rsi,g.ex)[:2],index=["rho","p"]))
    # book: daily returns, gain from market vs timing
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            D.append(df.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book_mean_daily_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    return out
