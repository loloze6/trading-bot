def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["fwd"]=(c.shift(-1)/c-1)
            d["ex"]=d["fwd"]-mu
            d["fwd3"]=c.shift(-3)/c-1
            d["vr"]=v/v.shift(1).rolling(20).mean()
            rng=(b["high"]-b["low"]).astype(float)
            d["clv"]=((c-b["low"])/rng).where(rng>0)
            d["r0"]=c/c.shift(1)-1
            d["r5"]=c/c.shift(5)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["rngp"]=rng/c
            d["fc"]=b["forecast"].astype(float)
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["yr"]=ts.dt.year.values
            d["pos3"]=np.arange(len(d))%3
            d["pnl"]=d["alloc"]*d["fwd"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,key,col="ex"):
        x=df.dropna(subset=[col])
        r=x.groupby(key,observed=True)[col].agg(["count","mean","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["mean"]*=100
        return r.drop(columns="std").round(3)
    D["vrq"]=pd.qcut(D["vr"],5,labels=False)
    D["clvt"]=pd.cut(D["clv"],[-.01,1/3,2/3,1.01],labels=False)
    D["r0q"]=D.groupby("coin")["r0"].transform(lambda s: pd.qcut(s,5,labels=False))
    D["r5q"]=D.groupby("coin")["r5"].transform(lambda s: pd.qcut(s,5,labels=False))
    D["volt"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    D["rngz"]=D["rngp"]/D["vol20"]
    D["rngq"]=pd.qcut(D["rngz"],5,labels=False)
    out={}
    specs={
     "vrq":(D,"vrq"),
     "vrq_x_clv":(D,["vrq","clvt"]),
     "r0q":(D,"r0q"),
     "r0q_in_vrtop":(D[D.vrq==4],"r0q"),
     "r0q_in_vrlow":(D[D.vrq<=1],"r0q"),
     "r5q":(D,"r5q"),
     "volt":(D,"volt"),
     "volt_x_vrq":(D,["volt","vrq"]),
     "wd":(D,"wd"),
     "yr_vrtop2":(D[D.vrq>=3],"yr"),
     "rngq":(D,"rngq"),
     "coin_vrtop":(D[D.vrq==4],"coin"),
    }
    for k,(df,key) in specs.items():
        try: out[k]=g(df,key)
        except Exception as e: out[k]=str(e)[:100]
    try:
        x=D[(D.pos3==0)].dropna(subset=["fwd3","vrq"])
        out["fwd3_by_vrq_nonoverlap"]=g(x,"vrq","fwd3")
    except Exception as e: out["fwd3"]=str(e)[:100]
    try:
        x=D.dropna(subset=["pnl","r0q"])
        x=x[x.alloc.abs()>0]
        r=x.groupby("r0q")["pnl"].agg(["count","mean","sum"]); r["mean"]*=100
        out["book_pnl_by_r0q_inpos"]=r.round(4)
        top=x.reindex(x["pnl"].abs().sort_values(ascending=False).index).head(int(len(x)*0.05))
        out["largest5pct_pnl_sign_share_pos"]=float((top.pnl>0).mean())
        out["largest5pct_r0q_dist"]=top.groupby(["r0q"]).size().to_frame("n")
        out["largest5pct_vrq_dist"]=top.groupby(["vrq"]).size().to_frame("n")
    except Exception as e: out["book"]=str(e)[:100]
    return out
