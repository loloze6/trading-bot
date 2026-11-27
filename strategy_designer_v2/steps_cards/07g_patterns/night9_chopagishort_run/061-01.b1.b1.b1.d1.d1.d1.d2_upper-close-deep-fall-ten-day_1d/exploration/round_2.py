def explore(data):
    import pandas as pd, numpy as np
    out={}
    def tstat(x):
        x=x.dropna()
        n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean() if n else np.nan,
                          "t":x.mean()/(x.std()/np.sqrt(n)) if n>2 and x.std()>0 else np.nan})
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["w"]=w
            d["pos"]=np.arange(len(b))
            rng=(h-l).replace(0,np.nan)
            d["loc"]=(c-l)/rng
            d["r1"]=c.pct_change()
            d["r5"]=c.pct_change(5); d["r20"]=c.pct_change(20); d["r60"]=c.pct_change(60)
            d["vol30"]=d["r1"].rolling(30,min_periods=20).std()
            d["rangepct"]=rng/c
            for H in (1,2,5,10):
                d[f"f{H}"]=c.shift(-H)/c-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["regime"]=b["regime"].astype(str)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["volrel"]=D["vol30"]/D.groupby("coin")["vol30"].transform("median")
    D["agit"]=np.where(D["volrel"].isna(),"na",np.where(D["volrel"]>1,"agit","calm"))
    D["trend"]=np.where(D["r60"].isna(),"na",np.where(D["r60"]>0.10,"rising",np.where(D["r60"]<-0.10,"falling","choppy")))
    D["prof"]=D["trend"]+"_"+D["agit"]
    for H in (2,10):
        try:
            G=D[(D["pos"]%H==0)].copy()
            G["fx"]=G[f"f{H}"]-G.groupby("coin")[f"f{H}"].transform("mean")
            G["locq"]=pd.cut(G["loc"],[-0.01,0.33,0.67,1.01],labels=["low","mid","high"]).astype(str)
            r=G[G["trend"]!="na"].groupby(["prof","locq"])["fx"].apply(tstat).unstack()
            out[f"loc_fwd{H}_by_profile"]=r[r["n"]>15]
        except Exception as e: out[f"err_loc{H}"]=str(e)[:100]
        try:
            G["r1q"]=G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
            out[f"r1quint_fwd{H}_by_agit"]=G[G["agit"]!="na"].groupby(["agit","r1q"])["fx"].apply(tstat).unstack()
            G["r20q"]=G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
            out[f"r20quint_fwd{H}_by_trend"]=G[G["trend"]!="na"].groupby(["trend","r20q"])["fx"].apply(tstat).unstack()
        except Exception as e: out[f"err_q{H}"]=str(e)[:100]
    try:
        G=D.copy(); G["fx"]=G["f1"]-G.groupby("coin")["f1"].transform("mean")
        out["weekday_fwd1"]=G.groupby("wd")["fx"].apply(tstat).unstack()
        G["rq"]=G.groupby("coin")["rangepct"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        G["locq"]=pd.cut(G["loc"],[-0.01,0.33,0.67,1.01],labels=["low","mid","high"]).astype(str)
        G2=D[D["pos"]%2==0].copy(); G2["fx"]=G2["f2"]-G2.groupby("coin")["f2"].transform("mean")
        G2["rq"]=G2.groupby("coin")["rangepct"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        G2["locq"]=pd.cut(G2["loc"],[-0.01,0.33,0.67,1.01],labels=["low","mid","high"]).astype(str)
        out["rangequint_x_loc_fwd2"]=G2.groupby(["rq","locq"])["fx"].apply(tstat).unstack()
    except Exception as e: out["err_wd"]=str(e)[:100]
    try:
        A=D[D["alloc"].abs()>0]
        out["active_by_prof"]=A.groupby("prof").size()
        A2=A.copy(); A2["g"]=A2["alloc"]*A2["f1"]
        out["active_gain_by_r1q_of_entrybar"]=A2.assign(lq=pd.cut(A2["loc"],[-0.01,0.33,0.67,1.01],labels=["low","mid","high"]).astype(str)).groupby("lq")["g"].apply(tstat).unstack()
    except Exception as e: out["err_act"]=str(e)[:100]
    try:
        dd=[]
        for coin,ws in data["days"].items():
            for w,x in ws.items():
                dd.append(x.assign(coin=coin,w=w))
        Dy=pd.concat(dd,ignore_index=True)
        bk=Dy.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
        out["book_by_window"]=bk.groupby("w").agg(br_sum_pct=("br",lambda s:100*s.sum()),cr_mean_pct=("cr",lambda s:100*s.mean()),n=("br","size"))
        bk=bk.dropna()
        q=bk["br"].quantile([0.01,0.99])
        out["book_extremes_coin_ret"]=pd.DataFrame({"worst1pct_cr%":[100*bk.loc[bk["br"]<=q.iloc[0],"cr"].mean()],"best1pct_cr%":[100*bk.loc[bk["br"]>=q.iloc[1],"cr"].mean()],"corr_book_coin":[bk["br"].corr(bk["cr"])]})
    except Exception as e: out["err_book"]=str(e)[:100]
    return out
