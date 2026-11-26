def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=20
    rows=[]; drows=[]
    for c,ws in data["bars"].items():
        grids=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            hi=cl.shift(1).rolling(60,min_periods=60).max()
            lo=cl.shift(1).rolling(60,min_periods=60).min()
            r1=cl.pct_change()
            f=pd.DataFrame({
              "dist":cl/hi-1,
              "low_dist":cl/lo-1,
              "width":hi/lo-1,
              "ret20":cl/cl.shift(20)-1,
              "ret60":cl/cl.shift(60)-1,
              "vol20":r1.rolling(20).std(),
              "fwd":cl.shift(-H)/cl-1,
              "pos":b["postRebalance_current_allocation"].astype(float),
              "fc":b["forecast"].astype(float)})
            f["volratio"]=f["vol20"]/r1.rolling(60).std()
            f["coin"]=c; f["win"]=w
            g=f.iloc[::H].copy()
            grids.append(g)
            d=pd.DataFrame({"r":r1,"nxt":r1.shift(-1),"nxt5":cl.shift(-5)/cl-1,
                            "z":r1/r1.shift(1).rolling(60).std(),
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"coin":c})
            drows.append(d)
        G=pd.concat(grids)
        drift=G["fwd"].mean()
        G["ex"]=G["fwd"]-drift
        rows.append(G)
    G=pd.concat(rows).dropna(subset=["ex"])
    out={}
    def tab(col,q=5):
        x=G.dropna(subset=[col]).copy()
        x["b"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        r=x.groupby("b")["ex"].agg(["mean","std","count"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["xmean"]=x.groupby("b")[col].mean()
        return r.round(4)
    for col in ["dist","low_dist","width","ret20","ret60","vol20","volratio"]:
        out["ex20 by "+col+" quintile (per coin)"]=tab(col)
    # breakouts only: by width (choppiness)
    br=G[G["dist"]>0]
    if len(br)>10:
        br=br.copy(); br["wb"]=pd.qcut(br["width"].rank(method="first"),3,labels=False)
        r=br.groupby("wb")["ex"].agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        out["breakouts: ex20 by prior range width tercile"]=r.round(4)
    D=pd.concat(drows).dropna()
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    r=D.groupby("zb")[["nxt","nxt5"]].agg(["mean","count"])
    out["next day/5d return by today's z-move"]=r.round(5)
    r=D.groupby("wd")["r"].agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["daily return by weekday"]=r.round(5)
    # book
    T=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=c; T.append(t)
    T=pd.concat(T)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    T["fb"]=pd.qcut(T["entry_forecast"].rank(method="first"),3,labels=False)
    out["trades by entry forecast tercile"]=T.groupby("fb")[["entry_forecast","net_profit_loss_percent"]].agg(["mean","count"]).round(3)
    return out
