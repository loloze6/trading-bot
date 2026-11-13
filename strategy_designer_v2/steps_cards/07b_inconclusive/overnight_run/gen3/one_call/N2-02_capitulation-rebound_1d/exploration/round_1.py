def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            n=len(df)
            depth=df.get("debug_info.components.depth.last_history_value")
            for i in range(0,n-10,10):
                r=c[i+10]/c[i]-1
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                    f=df["forecast"].iloc[i],reg=df["regime"].iloc[i],r=r,
                    depth=(depth.iloc[i] if depth is not None else np.nan),
                    p5=(c[i]/c[i-5]-1) if i>=5 else np.nan,
                    p20=(c[i]/c[i-20]-1) if i>=20 else np.nan,
                    hl=np.log(df["high"].iloc[max(0,i-9):i+1]/df["low"].iloc[max(0,i-9):i+1]).mean()))
    d=pd.DataFrame(rows)
    d["ex"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    def s(g):
        x=g["ex"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),med=x.median(),sd=x.std(),
            t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,pos=(x>0).mean()))
    top=d[d.f>=10]
    out={}
    out["all_buckets"]=d.assign(b=pd.cut(d.f,[-0.1,0.001,5,10,21],right=False)).groupby("b").apply(s)
    out["top_by_coin"]=top.groupby("coin").apply(s)
    out["top_by_year"]=top.groupby("year").apply(s)
    out["top_by_window"]=top.groupby("w").apply(s)
    out["top_by_p5_sign"]=top.groupby(top.p5>0).apply(s)
    out["top_by_p20_tercile"]=top.groupby(pd.qcut(top.p20,3,labels=False)).apply(s)
    out["top_by_hl_half"]=top.groupby(top.hl>top.hl.median()).apply(s)
    out["top_f20"]=top.groupby(top.f>=19.9).apply(s)
    # market: BTC same-grid move
    btc=d[d.coin=="BTCUSD"].set_index(["w","year"])  # not aligned by date; skip
    out["top_trimmed"]=s(top[top.ex.abs()<top.ex.abs().quantile(0.95)])
    in_reg=d[(d.reg=="mean_reversion")]
    out["inreg_p5"]=in_reg.groupby([in_reg.f>=5,in_reg.p5>0]).apply(s)
    return out
