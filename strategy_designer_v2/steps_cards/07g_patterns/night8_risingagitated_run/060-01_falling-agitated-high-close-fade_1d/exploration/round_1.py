def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            d=pd.DataFrame({"coin":c,"win":w})
            d["loc"]=((cl-l)/(h-l)).where(h>l)
            d["ret"]=cl/cl.shift(1)-1
            d["rng"]=(h-l)/cl
            d["n1"]=cl.shift(-1)/cl-1
            d["n3"]=cl.shift(-3)/cl-1
            d["n5"]=cl.shift(-5)/cl-1
            d["pos"]=np.arange(len(b))
            d["fa"]=(b["regime"]=="unknown").astype(int)
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            d["alloc"]=b["postRebalance_current_allocation"]
            d["r20"]=cl/cl.shift(20)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["rngz"]=d["rng"]/d["rng"].rolling(20).mean()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu1=D.groupby("coin")["n1"].transform("mean")
    D["x1"]=D["n1"]-mu1
    for k in (3,5):
        D["x%d"%k]=D["n%d"%k]-D.groupby("coin")["n%d"%k].transform("mean")
    def summ(g,col):
        g=g[col].dropna()
        return pd.Series({"n":len(g),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out={}
    D["locq"]=pd.cut(D["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["q1lo","q2","q3","q4","q5hi"])
    out["next1_by_loc_fa"]=D.groupby(["fa","locq"]).apply(summ,"x1")
    for k in (3,5):
        G=D[D["pos"]%k==0]
        out["next%d_by_loc_fa"%k]=G.groupby(["fa","locq"]).apply(summ,"x%d"%k)
    D["retq"]=D.groupby("coin")["ret"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["next1_by_dayret_q_fa"]=D.groupby(["fa","retq"]).apply(summ,"x1")
    D["rngq"]=D.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["next1_by_relrange_q_fa"]=D.groupby(["fa","rngq"]).apply(summ,"x1")
    D["hi"]=(D["loc"]>=2/3).astype(int); D["up"]=(D["ret"]>0).astype(int)
    out["next1_hiclose_x_updown_fa"]=D[D["fa"]==1].groupby(["hi","up"]).apply(summ,"x1")
    out["next1_by_weekday_all"]=D.groupby("wd").apply(summ,"x1")
    out["next1_by_weekday_fa"]=D[D["fa"]==1].groupby("wd").apply(summ,"x1")
    D["r20q"]=D.groupby("coin")["r20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    G=D[D["pos"]%5==0]
    out["next5_by_r20q_all"]=G.groupby("r20q").apply(summ,"x5")
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["next1_by_volq"]=D.groupby("volq").apply(summ,"x1")
    out["fa_share_by_coin"]=D.groupby("coin")["fa"].mean()
    # book
    dd=[]
    for c,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=c; t["win"]=w; dd.append(t)
    Y=pd.concat(dd)
    Y["wd"]=pd.to_datetime(Y["day"]).dt.dayofweek
    out["book_by_win"]=Y.groupby("win").agg(book=("book_return","mean"),coin=("coin_return","mean"))*100
    out["book_by_coin"]=Y.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))*100
    return out
