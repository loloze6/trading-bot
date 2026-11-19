def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            d=b[["timestamp","close","volume"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["hour"]=d["ts"].dt.hour; d["year"]=d["ts"].dt.year
            d["r1"]=d["close"].shift(-1)/d["close"]-1
            d["past1"]=d["close"]/d["close"].shift(1)-1
            d["past24"]=d["close"]/d["close"].shift(24)-1
            d["past72"]=d["close"]/d["close"].shift(72)-1
            d["f24"]=d["close"].shift(-24)/d["close"]-1
            d["f6"]=d["close"].shift(-6)/d["close"]-1
            d["vol24"]=d["past1"].rolling(24).std()
            d["vol168"]=d["past1"].rolling(168).std()
            d["coin"]=c; d["win"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["r1x"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    out={}
    tt=lambda s:s.mean()/s.std()*np.sqrt(s.count())
    # hour effects by coin and by year (r1 at ts h = return of bar h+1)
    for h in [12,13,19,20,21,1,2]:
        x=A[A["hour"]==h]
        out[f"h{h}_by_coin_bp"]=None
    hc=A[A["hour"].isin([13,20,21,2])].groupby(["hour","coin"])["r1x"].agg(lambda s:s.mean()*1e4).unstack()
    out["hour_by_coin_bp"]=hc
    hy=A[A["hour"].isin([13,20,21,2])].groupby(["hour","year"])["r1x"].agg(lambda s:s.mean()*1e4).unstack()
    out["hour_by_year_bp"]=hy
    # cross-coin: per (hour) daily average across coins then t over days
    A["day"]=A["ts"].dt.floor("D")
    m=A.groupby(["hour","day"])["r1x"].mean().groupby("hour").agg(["mean",tt,"count"])
    m.columns=["mean_bp","t_daycluster","ndays"]; m["mean_bp"]*=1e4
    out["hour_daycluster"]=m
    out={k:v for k,v in out.items() if v is not None}
    # 24h reversal, non-overlapping, by coin and year, graded by quintile
    S=A[A["pos"]%24==0].dropna(subset=["f24","past24","vol168"]).copy()
    S["f24x"]=S["f24"]-S.groupby("coin")["f24"].transform("mean")
    S["z24"]=S["past24"]/(S["vol168"]*np.sqrt(24))
    out["rev24_by_coin"]=S.groupby("coin").apply(lambda x:pd.Series({"corr":x[["past24","f24x"]].corr().iloc[0,1],"n":len(x)}))
    out["rev24_by_year"]=S.groupby("year").apply(lambda x:pd.Series({"corr":x[["past24","f24x"]].corr().iloc[0,1],"n":len(x)}))
    S["q"]=S.groupby("coin")["z24"].transform(lambda s:pd.qcut(s,5,labels=False))
    out["rev24_quintile"]=S.groupby("q")["f24x"].agg(mean_bp=lambda s:s.mean()*1e4,t=tt,n="count")
    # volatility tercile interaction
    S["vq"]=S.groupby("coin")["vol168"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["rev24_corr_by_volterc"]=S.groupby("vq").apply(lambda x:pd.Series({"corr":x[["z24","f24x"]].corr().iloc[0,1],"n":len(x)}))
    # 1h reversal by coin, deciles of past1/vol24 within coin, extreme spread
    A["z1"]=A["past1"]/A["vol24"]
    A["q1"]=A.groupby("coin")["z1"].transform(lambda s:pd.qcut(s,10,labels=False))
    sp=A[A["q1"].isin([0,9])].groupby(["coin","q1"])["r1x"].mean().unstack()*1e4
    out["rev1_extreme_by_coin_bp"]=sp
    # 6h non-overlap after 1h move
    S6=A[A["pos"]%6==0].dropna(subset=["f6","z1"]).copy()
    S6["f6x"]=S6["f6"]-S6.groupby("coin")["f6"].transform("mean")
    S6["q"]=S6.groupby("coin")["z1"].transform(lambda s:pd.qcut(s,5,labels=False))
    out["f6_by_past1_quint"]=S6.groupby("q")["f6x"].agg(mean_bp=lambda s:s.mean()*1e4,t=tt,n="count")
    return out
