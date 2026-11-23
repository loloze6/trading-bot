def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    recs=[]
    for c in coins:
        for w,d in data["days"][c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c; recs.append(dd)
    D=pd.concat(recs)
    B=D.groupby(["w","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean")).reset_index()
    B["wn"]=B["w"].str[1:].astype(int); B=B.sort_values(["wn","day"]).dropna().reset_index(drop=True)
    B["v"]=(1+B["book"]).cumprod(); B["pk"]=B["v"].cummax(); B["ddn"]=B["v"]/B["pk"]-1
    B["hv"]=(1+B["hold"]).cumprod(); B["hdd"]=B["hv"]/B["hv"].cummax()-1
    out["book_maxdd"]=float(B["ddn"].min()); out["hold_maxdd"]=float(B["hdd"].min())
    out["corr_book_hold"]=float(B["book"].corr(B["hold"]))
    sl=stats.linregress(B["hold"],B["book"]); out["beta_book_on_hold"]=float(sl.slope); out["alpha_daily"]=float(sl.intercept)
    # deepest fall span
    i_tr=int(B["ddn"].idxmin()); i_pk=int(B.loc[:i_tr,"v"].idxmax())
    seg=B.loc[i_pk:i_tr]
    out["deepest_fall"]=pd.Series({"days":len(seg),"win_start":int(seg.wn.iloc[0]),"win_end":int(seg.wn.iloc[-1]),
        "book_ret":(1+seg.book).prod()-1,"hold_ret":(1+seg.hold).prod()-1})
    g=B.groupby("wn").agg(book_ret=("book",lambda x:(1+x).prod()-1),hold_ret=("hold",lambda x:(1+x).prod()-1),dd_min=("ddn","min"))
    out["by_window"]=g.round(3)
    rows=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.copy()
            r=b["close"].pct_change()
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["vol20"]=r.rolling(20).std()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["high"]-b["close"])/rng
            b["alloc"]=b["postRebalance_current_allocation"]
            b["pg"]=b["alloc"]*b["nxt"]
            b["coin"]=c;b["wn"]=int(w[1:])
            rows.append(b[["coin","wn","nxt","vol20","ret20","loc","forecast","alloc","pg"]])
    X=pd.concat(rows).dropna()
    mu=X.groupby("coin")["nxt"].mean(); X["ex"]=X["nxt"]-X["coin"].map(mu)
    X["infall"]=X["wn"].between(out["deepest_fall"]["win_start"],out["deepest_fall"]["win_end"])
    out["mean_alloc"]=float(X["alloc"].mean())
    X["trend"]=np.where(X["ret20"]>0,"up20","down20")
    X["low"]=X["loc"]>0.5
    X["vhi"]=X.groupby("coin")["vol20"].transform(lambda s:s>s.median())
    def summ(s):
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out["nxt_trend_vhi_low"]=X.groupby(["trend","vhi","low"])["nxt"].apply(summ).unstack().round(5)
    out["pg_trend_vhi"]=X.groupby(["trend","vhi"]).agg(n=("nxt","size"),alloc=("alloc","mean"),pg=("pg","mean"),nxt=("nxt","mean")).round(5)
    res={}
    for tr,s in X.groupby("trend"):
        l=stats.linregress(s["forecast"],s["ex"]); res[tr]=[l.slope,l.slope/l.stderr,len(s)]
    out["slope_by_trend"]=pd.DataFrame(res,index=["slope","t","n"]).T
    X["fq"]=pd.qcut(X["forecast"].rank(method="first"),5,labels=False)
    out["by_fq"]=X.groupby("fq").agg(n=("nxt","size"),f=("forecast","mean"),alloc=("alloc","mean"),nxt=("nxt","mean"),pg=("pg","mean")).round(5)
    out["by_fq_infall"]=X[X.infall].groupby("fq").agg(n=("nxt","size"),alloc=("alloc","mean"),nxt=("nxt","mean"),pg=("pg","mean")).round(5)
    out["infall_trend_share"]=X[X.infall].groupby("trend").agg(n=("nxt","size"),alloc=("alloc","mean"),pg=("pg","mean")).round(5)
    return out
