def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            sd20=r1.rolling(20).std()
            z=r1/sd20
            fwd=c.shift(-H)/c-1
            ret20=c/c.shift(20)-1
            ret5=c/c.shift(5)-1
            rng=(df["high"]-df["low"])/c
            volz=df["volume"]/df["volume"].rolling(20).mean()
            idx=np.arange(0,len(df),H)
            sub=pd.DataFrame({"coin":coin,"w":w,"z":z.iloc[idx].values,"sd20":sd20.iloc[idx].values,
                "fwd":fwd.iloc[idx].values,"ret20":ret20.iloc[idx].values,"ret5":ret5.iloc[idx].values,
                "rng":rng.iloc[idx].values,"volz":volz.iloc[idx].values,
                "reg":df["regime"].iloc[idx].values,
                "wd":pd.to_datetime(df["timestamp"]).iloc[idx].dt.dayofweek.values,
                "yr":pd.to_datetime(df["timestamp"]).iloc[idx].dt.year.values})
            rows.append(sub)
    A=pd.concat(rows)
    A=A.dropna(subset=["fwd"])
    drift=A.groupby("coin")["fwd"].mean()
    A["u"]=A["fwd"]-A["coin"].map(drift)
    A["down"]=(A["reg"]=="mean_reversion")
    def tab(col,q=5):
        B=A.dropna(subset=[col]).copy()
        B["b"]=B.groupby("down")[col].transform(lambda s: pd.qcut(s,q,labels=False,duplicates="drop"))
        out=B.groupby(["down","b"])["u"].agg(["mean","count","std"])
        out["t"]=out["mean"]/(out["std"]/np.sqrt(out["count"]))
        out["xmean"]=B.groupby(["down","b"])[col].mean()
        return out.drop(columns="std").round(4)
    res={}
    res["z_quintile_by_regime"]=tab("z")
    res["ret20_quintile_by_regime"]=tab("ret20")
    res["ret5_quintile_by_regime"]=tab("ret5")
    res["sd20_quintile_by_regime"]=tab("sd20")
    res["range_quintile_by_regime"]=tab("rng")
    res["volume_ratio_quintile_by_regime"]=tab("volz")
    # weekday daily returns
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            d=df.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D).dropna(subset=["coin_return"])
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    wd=D.groupby("wd")["coin_return"].agg(["mean","count","std"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    res["weekday_coin_daily"]=wd.drop(columns="std").round(5)
    # book by year
    bk=D.dropna(subset=["book_return"]).groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=pd.to_datetime(bk["day"]).dt.year
    by=bk.groupby("yr").agg(book=("book_return","mean"),hold=("coin_return","mean"),n=("book_return","count"))
    by["book_sharpe"]=bk.groupby("yr")["book_return"].apply(lambda s: s.mean()/s.std()*np.sqrt(365))
    res["book_by_year"]=by.round(5)
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,df in ws.items():
            if len(df): d=df.copy(); d["coin"]=coin; T.append(d)
    T=pd.concat(T)
    T["fq"]=pd.qcut(T["entry_forecast"].abs(),4,labels=False,duplicates="drop")
    tt=T.groupby(["side","fq"]).agg(n=("net_profit_loss_percent","count"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),
        dur_d=("duration_minutes",lambda s:s.mean()/1440),fc=("entry_forecast","mean"))
    res["trades_by_forecast"]=tt.round(3)
    return res
