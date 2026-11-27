def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r1=c.pct_change()
            mabs=r1.abs().rolling(20,min_periods=10).mean()
            rng=(h-l).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),
                "cl":(c-l)/rng,"r1":r1,"g":r1/mabs,"rngs":((h-l)/c)/mabs,
                "body":(c-o)/rng,
                "tr60":c/c.shift(60)-1,"tr20":c/c.shift(20)-1,
                "inprof":(b["regime"]!="chop").astype(int),
                "sig":(b["regime"]=="mean_reversion").astype(int),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "vol":b["volume"].astype(float)/b["volume"].astype(float).rolling(20,min_periods=10).mean()})
            for H in (1,2,5):
                df[f"f{H}"]=c.shift(-H)/c-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    out={}
    for H in (1,2,5):
        drift=A.groupby("coin")[f"f{H}"].transform(lambda s: s.iloc[::H].mean())
        A[f"u{H}"]=A[f"f{H}"]-drift
    def grid(H): return A[A.pos%H==0].dropna(subset=[f"u{H}"])
    def tab(H,col,q=5):
        G=grid(H).dropna(subset=[col]).copy()
        G["b"]=pd.qcut(G[col].rank(method="first"),q,labels=False)
        t=G.groupby("b")[f"u{H}"].agg(["count","mean","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["lo"]=G.groupby("b")[col].min()
        return t.round(4)
    out["share_inprof"]=A.inprof.mean(); out["share_sig"]=A.sig.mean()
    for col in ["cl","g","rngs","body","vol","tr20"]:
        out[f"u2_by_{col}"]=tab(2,col)
    for col in ["cl","g"]:
        out[f"u5_by_{col}"]=tab(5,col)
    G=grid(2).dropna(subset=["cl"])
    r=[]
    for k,s in G.groupby("inprof"):
        rr=stats.pearsonr(s.cl,s.u2); r.append([k,len(s),rr[0],rr[1]])
    out["corr_cl_u2_by_inprof"]=pd.DataFrame(r,columns=["inprof","n","r","p"])
    G=grid(1)
    t=G.groupby("wd")["u1"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]));out["u1_wd"]=t.round(4)
    G=grid(5).dropna(subset=["tr60"]).copy()
    G["tc"]=pd.cut(G.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["clb"]=pd.cut(G.cl,[-.01,.2,.8,1.01],labels=["low","mid","high"])
    t=G.groupby(["tc","clb"])["u5"].agg(["count","mean","std"]);t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]));out["u5_trend_cl"]=t.round(4)
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,win=w))
    D=pd.concat(D); 
    out["book_ret_by_coin"]=D.groupby("coin")["book_return"].agg(["count","sum","mean"]).round(5)
    out["book_ret_by_year"]=D.assign(yr=pd.to_datetime(D.day).dt.year).groupby("yr")["book_return"].sum().round(4)
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()]) if any(len(ws) for ws in data["trades"].values()) else pd.DataFrame()
    if len(T):
        out["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    return out
