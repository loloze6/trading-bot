def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        tmp=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])
            ratio=rng/rng.rolling(30).mean()
            ret30=c/c.shift(30)-1
            r1=c/c.shift(1)-1
            clv=(c-b["low"])/rng.replace(0,np.nan)
            fwd=c.shift(-3)/c-1
            fwd1=c.shift(-1)/c-1
            idx=np.arange(0,len(b),3)
            d=pd.DataFrame({"ratio":ratio,"ret30":ret30,"r1":r1,"clv":clv,"fwd":fwd,"fwd1":fwd1,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year,"win":w,
                            "alloc":b["postRebalance_current_allocation"]}).iloc[idx]
            d=d[d["fwd"].notna()]
            tmp.append(d)
        d=pd.concat(tmp); d["coin"]=coin
        d["ex"]=d["fwd"]-d["fwd"].mean()
        d["usd"]=d["fwd"].std()
        rows.append(d)
    D=pd.concat(rows).dropna(subset=["ratio","ret30","clv"])
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean_ex_%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    dn=D[D["ret30"]<=0].copy()
    # graded: push-up score = (ratio-1)+ * (2clv-1)
    dn["push"]=np.clip(dn["ratio"]-1,0,None)*(2*dn["clv"]-1)
    W=dn[dn["ratio"]>1].copy()
    W["pq"]=pd.qcut(W["push"],5,labels=["q1","q2","q3","q4","q5"])
    out["down30_wide_by_pushscore_quintile"]=W.groupby("pq").apply(summ)
    r,p=stats.spearmanr(W["push"],W["ex"]); out["down30_wide_spearman_push"]=pd.Series({"rho":r,"p":p,"n":len(W)})
    HC=W[W["clv"]>=W["clv"].quantile(2/3)]
    out["down30_wide_highclose_by_coin"]=HC.groupby("coin").apply(summ)
    out["down30_wide_highclose_by_year"]=HC.groupby("yr").apply(summ)
    HC2=HC.copy(); HC2["rq"]=pd.qcut(HC2["ratio"],3,labels=["lowwide","midwide","verywide"])
    out["down30_wide_highclose_by_width"]=HC2.groupby("rq").apply(summ)
    out["down30_wide_highclose_strength"]=pd.Series({"mean_strength":(HC["ex"]/HC["usd"]).mean(),
        "share_windows_neg":(HC.groupby(["coin","win"])["ex"].mean()<0).mean(),
        "n_coin_windows":HC.groupby(["coin","win"]).ngroups,
        "mean_fwd1_ex_%":100*(HC["fwd1"]-D["fwd1"].mean()).mean()})
    # same pattern in up30 for contrast, graded by clv
    up=D[(D["ret30"]>0)&(D["ratio"]>1)].copy()
    up["cq"]=pd.qcut(up["clv"],5,labels=["q1","q2","q3","q4","q5"])
    out["up30_wide_by_clv_quintile"]=up.groupby("cq").apply(summ)
    dn2=dn.copy(); dn2["cq"]=pd.qcut(dn2["clv"],5,labels=["q1","q2","q3","q4","q5"])
    out["down30_all_by_clv_quintile"]=dn2.groupby("cq").apply(summ)
    # book's daily: largest gains/losses days, coin returns before
    rr=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dd=dd.copy(); dd["prev_coin"]=dd["coin_return"].shift(1); dd["coin"]=coin; rr.append(dd)
    Y=pd.concat(rr).dropna(subset=["book_return","prev_coin"])
    Y=Y[Y["book_return"]!=0]
    Y["bq"]=pd.qcut(Y["book_return"],10,labels=False,duplicates="drop")
    out["book_decile_prev_coin_ret_%"]=Y.groupby("bq").agg(n=("book_return","size"),book_mean=("book_return","mean"),prev_coin=("prev_coin","mean"))
    return out
