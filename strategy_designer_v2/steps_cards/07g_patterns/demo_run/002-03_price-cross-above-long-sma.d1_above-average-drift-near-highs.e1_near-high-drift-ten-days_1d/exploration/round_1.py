def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            r1=cl.pct_change()
            hi=cl.rolling(20,min_periods=20).max(); lo=cl.rolling(20,min_periods=20).min()
            rp=(cl-lo)/(hi-lo)
            past10=cl/cl.shift(10)-1
            past3=cl/cl.shift(3)-1
            vol20=r1.rolling(20,min_periods=15).std()
            fwd=cl.shift(-10)/cl-1
            fwd3=cl.shift(-3)/cl-1
            idx=np.arange(0,len(b),10)
            d=pd.DataFrame({"coin":c,"w":w,"rp":rp.iloc[idx].values,"past10":past10.iloc[idx].values,
                            "vol20":vol20.iloc[idx].values,"fwd":fwd.iloc[idx].values,
                            "trend":(b["regime"].iloc[idx]=="trending").values,
                            "fc":b["forecast"].iloc[idx].values,
                            "wd":pd.to_datetime(b["timestamp"].iloc[idx]).dt.weekday.values})
            rows.append(d)
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def slope(df,x):
        df=df.dropna(subset=[x,"ex"])
        if len(df)<20: return (np.nan,np.nan,len(df))
        r=stats.linregress(df[x],df["ex"]); return (r.slope,r.slope/r.stderr,len(df))
    res=[]
    for reg,sub in [("trend",g[g.trend]),("below",g[~g.trend]),("all",g)]:
        for x in ["rp","past10","vol20"]:
            s,t,n=slope(sub,x); res.append([reg,x,s,t,n])
    out["slopes"]=pd.DataFrame(res,columns=["reg","x","slope","t","n"])
    # rp tercile by regime
    g["rpq"]=pd.qcut(g["rp"],3,labels=False)
    out["rp_tercile"]=g.groupby(["trend","rpq"])["ex"].agg(["mean","count"])
    g["volq"]=pd.qcut(g["vol20"],3,labels=False)
    out["vol_tercile"]=g.groupby(["trend","volq"])["ex"].agg(["mean","count"])
    g["p10q"]=pd.qcut(g["past10"],5,labels=False)
    out["past10_quint"]=g.groupby(["trend","p10q"])["ex"].agg(["mean","count"])
    # per coin slope rp in trend
    pc=[]
    for c,sub in g[g.trend].groupby("coin"):
        s,t,n=slope(sub,"rp"); s2,t2,n2=slope(g[(~g.trend)&(g.coin==c)],"rp"); pc.append([c,t,n,t2,n2])
    out["percoin_rp_t"]=pd.DataFrame(pc,columns=["coin","t_trend","n","t_below","n_b"])
    # daily: book and coin returns by weekday, regime
    dd=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=c; d["w"]=w; dd.append(d)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["by_weekday"]=D.groupby("wd")[["book_return","coin_return"]].agg(["mean","count"])
    out["by_year"]=D.groupby("yr")[["book_return","coin_return"]].mean()
    # daily coin return after large prior-day moves
    D=D.sort_values(["coin","w","day"])
    D["prev"]=D.groupby(["coin","w"])["coin_return"].shift(1)
    D["prevq"]=pd.qcut(D["prev"],5,labels=False)
    out["next_after_prev_quint"]=D.groupby("prevq")["coin_return"].agg(["mean","count","std"])
    # book exposure
    allb=pd.concat([b.assign(coin=c) for c,ws in data["bars"].items() for b in ws.values()])
    out["alloc_by_regime"]=allb.groupby("regime")["postRebalance_current_allocation"].agg(["mean","count"])
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=T.groupby("side")["net_profit_loss_percent"].agg(["mean","count","median"])
    return out
