def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=20
    out={}
    allG=[]; D=[]
    for c,ws in data["bars"].items():
        gs=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            hi=cl.shift(1).rolling(60,min_periods=60).max()
            r1=cl.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            f=pd.DataFrame({"dist":cl/hi-1,"fwd":cl.shift(-H)/cl-1,
                            "vol60":r1.rolling(60).std(),"yr":ts.dt.year,"win":w,"coin":c})
            gs.append(f.iloc[::H])
            z=r1/r1.shift(1).rolling(60).std()
            for h in [1,5,10]:
                pass
            d=pd.DataFrame({"z":z,"n1":cl.shift(-1)/cl-1,"n5":cl.shift(-5)/cl-1,"n10":cl.shift(-10)/cl-1,
                            "vol":r1.shift(1).rolling(60).std(),"yr":ts.dt.year,"coin":c,"win":w})
            D.append(d)
        G=pd.concat(gs); G["ex"]=G["fwd"]-G["fwd"].mean(); allG.append(G)
    G=pd.concat(allG).dropna(subset=["ex","dist"])
    G["dz"]=G["dist"]/(G["vol60"]*np.sqrt(60))
    bins=[-9,-0.4,-0.25,-0.15,-0.08,-0.03,0,9]
    G["db"]=pd.cut(G["dist"],bins)
    r=G.groupby("db",observed=True)["ex"].agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["ex20 by distance to 60d high (fixed bins)"]=r.round(4)
    rho,p=stats.spearmanr(G["dist"],G["ex"]); out["spearman dist vs ex20 all"]=f"rho {rho:.3f} p {p:.4f} n {len(G)}"
    sub=G[G["dist"]>-0.15]; rho,p=stats.spearmanr(sub["dist"],sub["ex"])
    out["spearman dist vs ex20, dist>-15%"]=f"rho {rho:.3f} p {p:.4f} n {len(sub)}"
    rho,p=stats.spearmanr(G["dz"].dropna(),G.loc[G["dz"].notna(),"ex"]); out["spearman vol-scaled dist vs ex20"]=f"rho {rho:.3f} p {p:.4f}"
    G["top"]=G.groupby("coin")["dist"].transform(lambda s:s.rank(pct=True))>0.8
    r=G.groupby(["yr","top"])["ex"].agg(["mean","count"]).unstack(); out["ex20 top-quintile-dist vs rest by year"]=r.round(4)
    r=G.groupby(["coin","top"])["ex"].mean().unstack(); out["ex20 top vs rest by coin"]=r.round(4)
    D=pd.concat(D).dropna()
    # non-overlap for n5: sample every 5th? use all days but report t; also grid 5
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,1,2,99])
    res={}
    for h in ["n1","n5","n10"]:
        g=D.groupby("zb",observed=True)[h].agg(["mean","std","count"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        res[h]=g
    out["fwd returns by z-move (all days, overlapping for 5/10)"]=pd.concat(res,axis=1).round(4)
    big=D[D["z"]>2]; out["after z>2: n5 by year"]=big.groupby("yr")["n5"].agg(["mean","count"]).round(4)
    out["after z>2: n5 by coin"]=big.groupby("coin")["n5"].agg(["mean","count"]).round(4)
    gz=D[D["z"]>0].copy(); rho,p=stats.spearmanr(gz["z"],gz["n5"]); out["spearman up-z vs n5"]=f"rho {rho:.3f} p {p:.4f} n {len(gz)}"
    dn=D[D["z"]<-2]; out["after z<-2: n1 by year"]=dn.groupby("yr")["n1"].agg(["mean","count"]).round(4)
    # book: day returns around biggest losses
    B=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=c; B.append(d)
    B=pd.concat(B).dropna(subset=["book_return"])
    out["book day ret quantiles"]=B["book_return"].quantile([0.01,0.05,0.5,0.95,0.99]).round(5)
    return out
