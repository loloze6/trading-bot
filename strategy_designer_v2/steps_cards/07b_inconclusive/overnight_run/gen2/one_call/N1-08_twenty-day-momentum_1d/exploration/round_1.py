def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            fwd=c.shift(-20)/c-1
            r=c.pct_change()
            vol=r.rolling(20).std()
            sma50=c.rolling(50,min_periods=30).mean()
            mom=df.get("debug_info.components.mom20.last_history_value")
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(df["timestamp"]).dt.year,
                "fc":df["forecast"].astype(float),"fwd":fwd,"vol":vol,
                "above50":(c>sma50).where(sma50.notna()),
                "mom":mom.astype(float) if mom is not None else np.nan})
            d=d.iloc[::20]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd","fc"])
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D["sret"]=np.sign(D["fc"])*D["fwd"]
    def reg(g):
        if len(g)<10 or g["fc"].std()==0: return pd.Series({"n":len(g),"slope_t":np.nan,"mean_signed_ret":np.nan})
        s=stats.linregress(g["fc"],g["ex"])
        return pd.Series({"n":len(g),"slope_t":s.slope/s.stderr,"mean_signed_ret":g["sret"].mean(),
                          "t_signed":g["sret"].mean()/g["sret"].std()*np.sqrt(len(g))})
    out={}
    out["all"]=reg(D)
    out["by_coin"]=D.groupby("coin").apply(reg)
    out["by_year"]=D.groupby("year").apply(reg)
    D["q"]=pd.qcut(D["fc"],5,labels=False)
    out["by_fc_quintile"]=D.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex_mean=("ex","mean"),fwd_mean=("fwd","mean"),fwd_sd=("fwd","std"))
    D["side"]=np.where(D["fc"]>0,"long","short")
    out["by_side"]=D.groupby("side").apply(reg)
    D["volhi"]=D["vol"]>D.groupby("coin")["vol"].transform("median")
    out["by_volhi"]=D.groupby("volhi").apply(reg)
    out["by_above50"]=D.dropna(subset=["above50"]).groupby("above50").apply(reg)
    D["strong"]=D["fc"].abs()>=15
    out["by_strong"]=D.groupby("strong").apply(reg)
    out["side_x_above50"]=D.dropna(subset=["above50"]).groupby(["side","above50"]).apply(reg)
    D["rawmq"]=pd.qcut(D["mom"].rank(method="first"),5,labels=False)
    out["by_rawmom_quint"]=D.groupby("rawmq").agg(n=("ex","size"),mom=("mom","mean"),ex_mean=("ex","mean"),fwd_sd=("fwd","std"))
    return out
