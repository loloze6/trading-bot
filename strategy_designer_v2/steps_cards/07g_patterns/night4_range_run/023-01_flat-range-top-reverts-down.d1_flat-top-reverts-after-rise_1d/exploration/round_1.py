def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            hi=c.rolling(30).max(); lo=c.rolling(30).min()
            mid=(hi+lo)/2; rng=(hi-lo)
            pos=(c-mid)/(rng/2)
            net=(c/c.shift(29)-1).abs()
            flat=1-(c-c.shift(29)).abs()/rng
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            past5=c/c.shift(5)-1
            past10=c/c.shift(10)-1
            past30=c/c.shift(29)-1
            fwd=c.shift(-5)/c-1
            wd=pd.to_datetime(df["timestamp"]).dt.weekday
            for i in range(0,len(df),5):
                rows.append(dict(coin=coin,w=w,fwd=fwd[i],pos=pos[i],flat=flat[i],vol=vol[i],
                    past5=past5[i],past10=past10[i],past30=past30[i],reg=df["regime"].iloc[i],
                    fc=df["forecast"].iloc[i],wd=wd[i],yr=pd.to_datetime(df["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    def summ(g):
        x=g["ex"]; n=len(x)
        return pd.Series({"n":n,"mean_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    dd=d.dropna(subset=["pos"])
    dd["posq"]=pd.qcut(dd["pos"],5,labels=False)
    out["pos_quint_by_regime"]=dd.groupby(["reg","posq"]).apply(summ)
    for k in ["past5","past10","past30","vol"]:
        e=d.dropna(subset=[k]).copy()
        e["q"]=pd.qcut(e[k],5,labels=False)
        out[k+"_quint"]=e.groupby("q").apply(summ)
    e=dd.copy(); e["fq"]=pd.qcut(e["flat"],3,labels=False)
    out["flat_x_pos"]=e.groupby(["fq","posq"]).apply(summ)
    out["regime"]=d.groupby("reg").apply(summ)
    out["year"]=d.groupby("yr").apply(summ)
    out["coin"]=d.groupby("coin").apply(summ)
    # corr per coin of pos with ex
    out["corr_pos_ex_coin"]=dd.groupby("coin").apply(lambda g: pd.Series({"r":g["pos"].corr(g["ex"]),"n":len(g)}))
    return out
