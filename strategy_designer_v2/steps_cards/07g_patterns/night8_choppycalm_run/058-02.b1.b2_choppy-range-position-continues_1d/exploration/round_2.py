def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=15).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r1":r1,"vol30":vol30,
                "tr20":c/c.shift(20)-1,"r5":c/c.shift(5)-1,"fwd":fwd,
                "choppy":(b["regime"]!="chop").values,"yr":ts.dt.year,
                "rng":(hi-lo)/c,"clv":(c-lo)/(hi-lo)})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    cm=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(cm)
    A["vrank"]=A.groupby("coin")["vol30"].rank(pct=True)
    A["agit"]=A.vrank>0.5
    A["r1z"]=A.r1/A.vol30
    A["r5z"]=A.r5/(A.vol30*np.sqrt(5))
    A["rngz"]=A.rng/A.groupby("coin")["rng"].transform(lambda s: s.rolling(20,min_periods=10).mean())
    G=A[A.pos%H==0].dropna(subset=["ex"]).copy()
    out={}
    def tab(df,key):
        g=df.groupby(key)["ex"]
        t=g.agg(["count","mean","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); return t.round(4)
    def slope(df,x):
        d=df.dropna(subset=[x,"ex"])
        if len(d)<20: return pd.Series({"n":len(d),"b":np.nan,"t":np.nan})
        X=d[x].values; y=d.ex.values; X=X-X.mean()
        bb=(X*(y-y.mean())).sum()/(X**2).sum()
        res=y-y.mean()-bb*X; se=np.sqrt((res**2).sum()/(len(d)-2)/(X**2).sum())
        return pd.Series({"n":len(d),"b":bb,"t":bb/se})
    G["prof"]=np.where(G.choppy,"chop","trend")+"_"+np.where(G.agit,"agit","calm")
    out["r1z_slope_by_prof"]=G.groupby("prof").apply(lambda x: slope(x,"r1z")).round(4)
    out["r1z_slope_by_window"]=G[~G.agit].groupby("w").apply(lambda x: slope(x,"r1z")).round(3)
    out["r1z_slope_by_year_calm"]=G[~G.agit].groupby("yr").apply(lambda x: slope(x,"r1z")).round(3)
    out["r1z_slope_by_coin_calm"]=G[~G.agit].groupby("coin").apply(lambda x: slope(x,"r1z")).round(3)
    G["zq"]=pd.qcut(G.r1z,5,labels=False)
    out["r1z_q_calm"]=tab(G[~G.agit],"zq")
    out["r5z_slope_by_prof"]=G.groupby("prof").apply(lambda x: slope(x,"r5z")).round(4)
    out["tr20_slope_by_prof"]=G.groupby("prof").apply(lambda x: slope(x,"tr20")).round(4)
    out["tr20_choppy_by_window"]=G[G.choppy].groupby("w").apply(lambda x: slope(x,"tr20")).round(3)
    out["rngz_slope_by_prof"]=G.groupby("prof").apply(lambda x: slope(x,"rngz")).round(4)
    G["clvs"]=2*G.clv-1
    out["clv_slope_by_prof"]=G.groupby("prof").apply(lambda x: slope(x,"clvs")).round(4)
    out["prof_mean"]=tab(G,"prof")
    # big up day by direction of 20d trend
    G["trs"]=np.where(G.tr20>0,"up20","dn20")
    out["r1z_slope_by_tr20sign_calm"]=G[~G.agit].groupby("trs").apply(lambda x: slope(x,"r1z")).round(4)
    return out
