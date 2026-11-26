def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c/sma-1)/sd
            r60=c/c.shift(60)-1
            vol30=r.rolling(30).std()
            volrank=vol30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            r1z=r/r.rolling(30).std().shift(1)
            r5=c.pct_change(5)/(sd*np.sqrt(5))
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            hi=b["high"].astype(float); lo=b["low"].astype(float)
            clv=(c-lo)/(hi-lo)
            rngz=((hi-lo)/c)/((hi-lo)/c).rolling(20).mean()
            vz=b["volume"]/b["volume"].rolling(20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r60":r60,"vr":volrank,"r1z":r1z,"r5z":r5,
                            "fwd":fwd,"fwd1":fwd1,"clv":clv,"rngz":rngz,"vz":vz,
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year,
                            "fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            d["grid"]=(np.arange(len(d))%H==0)
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.grid].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    A["trend"]=np.where(A.r60>0.10,"rising",np.where(A.r60<-0.10,"falling","choppy"))
    A.loc[A.r60.isna(),"trend"]=np.nan
    A["agit"]=np.where(A.vr>0.5,"agit","calm"); A.loc[A.vr.isna(),"agit"]=np.nan
    G=A[A.grid].dropna(subset=["ex","z","trend"])
    out={}
    def tab(df,col,q=5):
        df=df.dropna(subset=[col,"ex"]).copy()
        df["b"]=pd.qcut(df[col],q,labels=False,duplicates="drop")
        g=df.groupby("b").agg(n=("ex","size"),lo=(col,"min"),hi=(col,"max"),mean_ex=("ex","mean"),sd=("ex","std"))
        g["t"]=g.mean_ex/(g.sd/np.sqrt(g.n)); return g.drop(columns="sd").round(4)
    out["z_quint_choppy"]=tab(G[G.trend=="choppy"],"z")
    out["z_quint_all"]=tab(G,"z")
    # slope of ex on z per trend x agit
    res=[]
    for (t,a),g in G.dropna(subset=["agit"]).groupby(["trend","agit"]):
        if len(g)>30:
            s=stats.linregress(g.z,g.ex); res.append([t,a,len(g),s.slope,s.slope/s.stderr])
    out["slope_z_by_profile"]=pd.DataFrame(res,columns=["trend","agit","n","slope","t"]).round(4)
    res=[]
    for col in ["r1z","r5z","clv","rngz","vz"]:
        for (t,a),g in G.dropna(subset=["agit",col]).groupby(["trend","agit"]):
            if len(g)>30:
                s=stats.linregress(g[col],g.ex); res.append([col,t,a,len(g),s.slope,s.slope/s.stderr])
    out["slope_other_by_profile"]=pd.DataFrame(res,columns=["feat","trend","agit","n","slope","t"]).round(4)
    out["ex_by_weekday"]=G.groupby("wd")["ex"].agg(["size","mean"]).round(4)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D); D["wd"]=pd.to_datetime(D["day"]).dt.weekday; D["yr"]=pd.to_datetime(D["day"]).dt.year
    bk=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean"),wd=("wd","first"),yr=("yr","first")).dropna()
    out["book_by_window"]=bk.groupby("w").agg(n=("br","size"),book=("br","mean"),coin=("cr","mean")).round(5)
    out["book_by_year"]=bk.groupby("yr").agg(n=("br","size"),book=("br","mean"),coin=("cr","mean")).round(5)
    out["book_by_coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean")).round(5)
    A["pos_side"]=np.sign(A.pos.fillna(0))
    A["pnl"]=A.pos.fillna(0)*A.fwd1
    out["pnl_by_side"]=A.groupby("pos_side")["pnl"].agg(["size","mean","sum"]).round(5)
    q=A.dropna(subset=["pnl"]); q=q[q.pos_side!=0]
    big=q.nlargest(40,"pnl"); sm=q.nsmallest(40,"pnl")
    out["extremes_context"]=pd.DataFrame({"best":big[["z","r1z","r60","vr","pos"]].mean(),"worst":sm[["z","r1z","r60","vr","pos"]].mean()}).round(3)
    return out
