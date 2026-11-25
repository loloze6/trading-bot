def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            b["r1"]=r1
            b["fwd3"]=c.shift(-3)/c-1
            b["fwd1"]=c.shift(-1)/c-1
            b["ret3p"]=c/c.shift(3)-1
            b["ret7p"]=c/c.shift(7)-1
            b["ret14p"]=c/c.shift(14)-1
            b["vol7"]=r1.rolling(7).std()
            b["vol30"]=r1.rolling(30).std()
            b["vr7_30"]=b["vol7"]/r1.shift(7).rolling(30).std()
            b["z1"]=r1/b["vol30"].shift(1)
            b["rng"]=(b["high"]-b["low"])/c
            b["clv"]=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            b["rising"]=(b["regime"]=="unknown").astype(int)
            b["raw"]=b.get("debug_info.components.quieting.last_history_value")
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["coin"]=coin;b["w"]=w;b["pos"]=np.arange(len(b))
            b["grid"]=(b["pos"]%3==0)
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    G=B[B.grid & B.fwd3.notna()].copy()
    G["drift"]=G.groupby("coin")["fwd3"].transform("mean")
    G["ex"]=G["fwd3"]-G["drift"]
    G["usual"]=G.groupby("coin")["fwd3"].transform("std")
    def summ(df,col="ex"):
        g=df.groupby("day")[col].sum()
        n=len(df); m=df[col].mean()
        se=np.sqrt((( g - g.mean()*0)**2).sum())/n if n>1 else np.nan
        # clustered t about mean
        dev=(df[col]-m).groupby(df["day"]).sum()
        se=np.sqrt((dev**2).sum())/n
        return pd.Series({"n":n,"days":df.day.nunique(),"mean":m,"t_cl":m/se if se>0 else np.nan})
    out={}
    out["share_rising"]=G.rising.mean()
    R=G[G.rising==1].copy()
    R["raw_q"]=pd.qcut(R["raw"],5,labels=False,duplicates="drop")
    out["rising_by_raw_quintile"]=R.groupby("raw_q").apply(summ)
    for nm,col in [("vr7_30","vr7_30"),("ret14p","ret14p"),("ret3p","ret3p"),("z1","z1"),("rng","rng"),("clv","clv")]:
        for reg in [1,0]:
            S=G[(G.rising==reg)&G[col].notna()].copy()
            if len(S)<50: continue
            S["q"]=pd.qcut(S[col],5,labels=False,duplicates="drop")
            out[f"{nm}_q_reg{reg}"]=S.groupby("q").apply(summ)
    out["weekday_all"]=G.groupby("wd").apply(summ)
    # 1-day forward by weekday all bars
    B["fwd1ex"]=B["fwd1"]-B.groupby("coin")["fwd1"].transform("mean")
    out["wd_fwd1"]=B.dropna(subset=["fwd1ex"]).groupby("wd")["fwd1ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["by_window_rising_ex"]=G.groupby(["w","rising"])["ex"].mean().unstack()
    # book
    D=[]
    for coin,wd in data["days"].items():
        for w,d in wd.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_corr_coin"]=bk.corr().iloc[0,1]
    big=bk.book_return.abs().quantile(0.95)
    out["book_big_days"]=pd.Series({"top_mean_coin":bk[bk.book_return>big].coin_return.mean(),"bot_mean_coin":bk[bk.book_return<-big].coin_return.mean(),"n_top":(bk.book_return>big).sum(),"n_bot":(bk.book_return<-big).sum()})
    T=pd.concat([t.assign(coin=c) for c,wd in data["trades"].items() for t in wd.values() if len(t)])
    T["fq"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades_by_fq"]=T.groupby("fq")["net_profit_loss_percent"].agg(["mean","count","median"])
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count"])
    return out
