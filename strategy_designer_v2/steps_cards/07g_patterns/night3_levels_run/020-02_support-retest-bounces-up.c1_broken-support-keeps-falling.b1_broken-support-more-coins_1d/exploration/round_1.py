def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        grid=[]
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({
                "coin":coin,"w":w,
                "fwd":c.shift(-H)/c-1,
                "past5":c/c.shift(5)-1,
                "past20":c/c.shift(20)-1,
                "past60":c/c.shift(60)-1,
                "vol20":r1.rolling(20).std(),
                "volratio":r1.rolling(5).std()/r1.rolling(60).std(),
                "pos90":(c-lo.rolling(90,min_periods=30).min())/(hi.rolling(90,min_periods=30).max()-lo.rolling(90,min_periods=30).min()),
                "range1":(hi-lo)/c,
                "closeinbar":(c-lo)/(hi-lo),
                "raw":b.get("debug_info.components.support_above.last_history_value"),
                "fc":b["forecast"],
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
            })
            df=df.iloc[::H]
            df=df[df["fwd"].notna()]
            grid.append(df)
        g=pd.concat(grid)
        mu=g["fwd"].mean(); sd=g["fwd"].std()
        g["ex"]=g["fwd"]-mu; g["z"]=g["ex"]/sd
        rows.append(g)
    G=pd.concat(rows)
    out={}
    def by(col,q=5):
        d=G[[col,"ex","z"]].dropna()
        d["b"]=d.groupby(G.loc[d.index,"coin"] if False else d.index.map(lambda i:0))[col].transform(lambda s: s)  # placeholder
        d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        a=d.groupby("b").agg(n=("ex","size"),mean_ex=("ex","mean"),mean_z=("z","mean"),sd=("ex","std"),lo=(col,"min"),hi=(col,"max"))
        a["t"]=a.mean_ex/(a.sd/np.sqrt(a.n))
        return a.drop(columns="sd")
    # per-coin rank versions to avoid coin mixing
    for col in ["past5","past20","past60","vol20","volratio","pos90","range1","closeinbar","fc"]:
        G[col+"_r"]=G.groupby("coin")[col].rank(pct=True)
        out[col]=by(col+"_r")
    # slopes of z on rank, per feature
    sl={}
    for col in ["past5","past20","past60","vol20","volratio","pos90","range1","closeinbar","fc"]:
        d=G[[col+"_r","z"]].dropna()
        r=stats.linregress(d[col+"_r"],d["z"]); sl[col]=(r.slope,r.slope/r.stderr,len(d))
    out["slopes_z_on_rank"]=pd.DataFrame(sl,index=["slope","t","n"]).T
    wd=G.groupby("wd")["ex"].agg(["size","mean","std"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["size"]))
    out["weekday_start"]=wd
    yr=G.groupby("yr")["ex"].agg(["size","mean"]); out["year"]=yr
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book_mean_daily"]=float(D["book_return"].mean())
    out["coin_mean_daily"]=float(D["coin_return"].mean())
    # trades
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            T.append(t.assign(coin=coin))
    T=pd.concat(T)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda s:s.mean()/1440))
    return out
