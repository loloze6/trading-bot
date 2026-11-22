def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std().shift(1)
            z=r/sd
            r20=c/c.shift(20)-1
            vol=r.rolling(20).std()
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"r20":r20,"vol":vol,"f5":f5,"f1":f1,
                             "reg":b["regime"],"wd":ts.dt.weekday,"yr":ts.dt.year,
                             "fc":b["forecast"],"pos":b["postRebalance_current_allocation"]})
            df["grid"]=(np.arange(len(df))%5==0)
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    g=A[A.grid].copy()
    drift=g.groupby("coin")["f5"].mean()
    g["u5"]=g["f5"]-g["coin"].map(drift)
    sd5=g.groupby("coin")["f5"].std()
    g["s5"]=g["u5"]/g["coin"].map(sd5)
    def summ(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean_u5":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    g["zb"]=pd.cut(g["z"],[-99,-3,-2,-1,0,1,2,3,99])
    out={}
    out["z_bucket_by_regime"]=g.groupby(["reg","zb"],observed=True)["u5"].apply(summ).unstack()
    # vol level per coin rank
    g["volq"]=g.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"),3,labels=["lo","mid","hi"]))
    out["vol_tercile_by_regime"]=g.groupby(["reg","volq"],observed=True)["u5"].apply(summ).unstack()
    # 20-day return quintile by regime
    g["r20q"]=g.groupby("coin")["r20"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    out["r20_quintile_by_regime"]=g.groupby(["reg","r20q"])["u5"].apply(summ).unstack()
    # weekday on daily f1
    dm=A.groupby("coin")["f1"].transform("mean")
    A["u1"]=A["f1"]-dm
    out["weekday_u1"]=A.groupby("wd")["u1"].apply(summ).unstack()
    # trades
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T,ignore_index=True)
    out["trades_side_regime"]=T.groupby(["side","entry_regime"])["net_profit_loss_percent"].agg(["count","mean","median",lambda x:(x>0).mean()])
    # book daily
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D,ignore_index=True)
    bd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    bd["yr"]=pd.to_datetime(bd.index.get_level_values("day")).year
    out["book_by_year"]=bd.groupby("yr").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean"),
        sharpe=("book_return",lambda x:x.mean()/x.std()*np.sqrt(365)))
    s=bd["book_return"].sort_values()
    tot=s.sum()
    out["book_tail_share"]=pd.Series({"sum_all":tot,"top20_sum":s.tail(20).sum(),"bottom20_sum":s.head(20).sum(),
        "corr_book_hold":bd["book_return"].corr(bd["coin_return"])})
    return out
