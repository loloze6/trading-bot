def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w})
            d["pos"]=np.arange(len(b))
            rng=(h-l).replace(0,np.nan)
            d["loc"]=(c-l)/rng
            d["r1"]=c.pct_change()
            d["r5"]=c.pct_change(5); d["r20"]=c.pct_change(20); d["r60"]=c.pct_change(60)
            d["vol30"]=d["r1"].rolling(30).std()
            d["rangepct"]=rng/c
            for H in (1,2,5,10):
                d[f"f{H}"]=c.shift(-H)/c-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["fc"]=b["forecast"].astype(float)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["volrel"]=D["vol30"]/D.groupby("coin")["vol30"].transform("median")
    D["agit"]=D["volrel"]>1
    D["trend"]=np.where(D["r60"]>0.10,"rising",np.where(D["r60"]<-0.10,"falling",np.where(D["r60"].notna(),"choppy",None)))
    D["prof"]=D["trend"].astype(str)+"_"+np.where(D["agit"],"agit","calm")
    out={}
    def tstat(x):
        x=x.dropna(); 
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    for H in (2,10):
        G=D[(D["pos"]%H==0)].copy()
        G["fx"]=G[f"f{H}"]-G.groupby("coin")[f"f{H}"].transform("mean")
        G["locq"]=pd.cut(G["loc"],[-0.01,0.2,0.4,0.6,0.8,1.01])
        out[f"loc_q_fwd{H}_by_profile"]=G.groupby(["prof","locq"])["fx"].apply(tstat).unstack().query("n>20")
        G["r1q"]=G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out[f"r1quint_fwd{H}"]=G.groupby("r1q")["fx"].apply(tstat).unstack()
        G["r20q"]=G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out[f"r20quint_fwd{H}_by_agit"]=G.groupby(["agit","r20q"])["fx"].apply(tstat).unstack()
    G=D[D["pos"]%1==0].copy(); G["fx"]=G["f1"]-G.groupby("coin")["f1"].transform("mean")
    out["weekday_fwd1"]=G.groupby("wd")["fx"].apply(tstat).unstack()
    G["rq"]=G.groupby("coin")["rangepct"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["rangequint_x_loc_fwd1"]=G.assign(lochi=G["loc"]>0.5).groupby(["rq","lochi"])["fx"].apply(tstat).unstack()
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    Dy=pd.concat(dd)
    out["book_by_window"]=Dy.groupby("w").agg(br=("book_return",lambda s:100*s.sum()),cr=("coin_return",lambda s:100*s.mean()))
    out["active_share_by_prof"]=D.assign(act=D["alloc"].abs()>0).groupby("prof")["act"].agg(["mean","sum"])
    return out
