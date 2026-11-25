def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wd in data["bars"].items():
        for w,df in wd.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            n=len(c)
            fwd=c.shift(-H)/c-1
            pmax=c.shift(1).rolling(60).max()
            pmin=c.shift(1).rolling(60).min()
            r1=c.pct_change()
            absmv=r1.abs().rolling(60).mean()
            feat=pd.DataFrame({
                "coin":coin,"win":w,"pos":np.arange(n),
                "fwd":fwd,
                "dist_hi":(c/pmax-1),
                "dist_lo":(c/pmin-1),
                "brk_in_moves":(c/pmax-1)/absmv,
                "ret1":r1,
                "ret5":c/c.shift(5)-1,
                "ret20":c/c.shift(20)-1,
                "ret60":c/c.shift(60)-1,
                "vol20":r1.rolling(20).std(),
                "rng_moves":(pmax/pmin-1)/absmv,
                "wd":pd.to_datetime(df["timestamp"]).dt.weekday,
                "fc":df["forecast"].astype(float),
                "alloc":df["postRebalance_current_allocation"].astype(float),
                "year":pd.to_datetime(df["timestamp"]).dt.year,
            })
            rows.append(feat)
    A=pd.concat(rows,ignore_index=True)
    # drift per coin: non-overlapping all bars grid
    G=A[A["pos"]%H==0].dropna(subset=["fwd"]).copy()
    drift=G.groupby("coin")["fwd"].mean()
    G["ux"]=G["fwd"]-G["coin"].map(drift)
    out={}
    out["drift_and_n"]=pd.DataFrame({"drift":drift,"n":G.groupby("coin").size()})
    def qtab(df,col,q=5):
        d=df.dropna(subset=[col,"ux"]).copy()
        d["q"]=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        g=d.groupby("q")["ux"]
        t=g.mean()/(g.std()/np.sqrt(g.count()))
        return pd.DataFrame({"mean_col":d.groupby("q")[col].mean(),"mean_ux":g.mean(),"t":t,"n":g.count()})
    for col in ["ret1","ret5","ret20","ret60","vol20","rng_moves","dist_hi","dist_lo"]:
        out["all_q_"+col]=qtab(G,col)
    B=G[G["dist_hi"]>0]
    out["brk_n"]=len(B)
    out["brk_q_dist"]=qtab(B,"dist_hi",3)
    out["brk_q_inmoves"]=qtab(B,"brk_in_moves",3)
    out["brk_q_ret60"]=qtab(B,"ret60",3)
    out["brk_q_vol20"]=qtab(B,"vol20",3)
    L=G[G["dist_lo"]<0]
    out["breakdown_n_mean_t"]=pd.Series({"n":len(L),"mean":L["ux"].mean(),"t":L["ux"].mean()/(L["ux"].std()/np.sqrt(len(L)))})
    out["breakdown_q_dist"]=qtab(L,"dist_lo",3)
    g=G.groupby("wd")["ux"]
    out["weekday"]=pd.DataFrame({"m":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    g=B.groupby("coin")["ux"]
    out["brk_by_coin"]=pd.DataFrame({"m":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    g=B.groupby("win")["ux"]
    out["brk_by_win"]=pd.DataFrame({"m":g.mean(),"n":g.count()})
    return out
