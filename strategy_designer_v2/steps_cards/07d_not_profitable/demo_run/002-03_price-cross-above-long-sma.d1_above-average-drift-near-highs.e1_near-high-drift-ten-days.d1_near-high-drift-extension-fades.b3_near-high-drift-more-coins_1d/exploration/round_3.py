def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out={}
    bars=data["bars"]
    rows=[];grid=[]
    for c in bars:
        for w,b in bars[c].items():
            r1=b["close"].shift(-1)/b["close"]-1
            pos=b["postRebalance_current_allocation"]
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            ext=b.get("debug_info.components.ext30.post_pipeline_value")
            rng=b.get("debug_info.components.range20.post_pipeline_value")
            r30=b.get("debug_info.components.ext30.last_history_value")
            df=pd.DataFrame({"coin":c,"w":w,"pos":pos,"r1":r1,"fee":fee,"regime":b["regime"],"ext":ext,"rng":rng,"ret30":r30})
            se=(df["regime"]=="trending")&(df["pos"]<0)&(df["ext"]<=-1)
            df["g_book"]=df["pos"]*df["r1"]-df["fee"]
            df["g_noext_short"]=np.where(se,0,df["pos"]*df["r1"]-df["fee"])
            df["g_flip"]=np.where(se,-df["pos"]*df["r1"],df["pos"]*df["r1"]-df["fee"])
            df["g_longonly"]=df["pos"].clip(lower=0)*df["r1"]-np.where(df["pos"]>0,df["fee"],0)
            rows.append(df)
            idx=np.arange(0,len(b),10)
            gg=df.iloc[idx].copy();gg["f10"]=(b["close"].shift(-10)/b["close"]-1).iloc[idx].values
            grid.append(gg)
    A=pd.concat(rows);G=pd.concat(grid)
    G["ex10"]=G["f10"]-G.groupby("coin")["f10"].transform("mean")
    def sh(x):
        x=x.dropna();return x.mean()/x.std()*np.sqrt(365)
    res={}
    for k in ["g_book","g_noext_short","g_flip","g_longonly"]:
        m=A.groupby("w")[k].mean()
        loo=[sh(A[A["w"]!=w][k]) for w in A["w"].unique()]
        res[k]={"mean":A[k].mean(),"sharpe":sh(A[k]),"min_loo_sharpe":min(loo),"windows_neg":(m<0).sum()}
    out["counterfactuals"]=pd.DataFrame(res).T
    GT=G[G["regime"]=="trending"].dropna(subset=["ex10","ret30"])
    lr=stats.linregress(GT["ret30"].clip(upper=GT["ret30"].quantile(0.99)),GT["ex10"])
    out["trend grid slope ex10 on ret30"]=pd.Series({"slope":lr.slope,"t":lr.slope/lr.stderr,"n":len(GT)})
    GT=GT.copy();GT["comb"]=GT["rng"].rank(pct=True)+GT["ret30"].rank(pct=True)
    GT["cq"]=pd.qcut(GT["comb"].rank(method="first"),5,labels=False)
    out["ex10 by range+ret30 rank quintile"]=GT.groupby("cq").agg(ex10=("ex10","mean"),n=("ex10","size"))
    return out
