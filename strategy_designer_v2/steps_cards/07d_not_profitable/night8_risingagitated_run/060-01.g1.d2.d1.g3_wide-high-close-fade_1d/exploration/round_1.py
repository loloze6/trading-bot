def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"];o=b["open"]
            rng=(h-l)
            b["cl"]=(c-l)/rng.replace(0,np.nan)
            b["rm"]=rng/rng.rolling(20,min_periods=10).mean()
            b["r1"]=c/c.shift(1)-1
            b["r3"]=c/c.shift(3)-1
            b["r10"]=c/c.shift(10)-1
            b["body"]=(c-o)/rng.replace(0,np.nan)
            b["nxt"]=c.shift(-1)/c-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["pnl"]=b["alloc"]*b["nxt"]
            b["coin"]=coin;b["w"]=w;b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["inprof"]=b["regime"].isin(["mean_reversion","unknown"])
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    drift=B.groupby("coin")["nxt"].mean()
    B["ex"]=B["nxt"]-B["coin"].map(drift)
    B["short_ex"]=-B["ex"]
    S=B[B["alloc"]<0].dropna(subset=["nxt"])
    U=B[(B["regime"]=="unknown")].dropna(subset=["nxt"])  # in profile, low close
    out={}
    def grp(df,col,q=4):
        g=pd.qcut(df[col],q,duplicates="drop")
        r=df.groupby(g,observed=True)["short_ex"].agg(["mean","count","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.reset_index().astype({col:str})
    out["by_window"]=S.groupby("w").agg(n=("pnl","size"),pnl=("pnl","sum"),short_ex=("short_ex","mean"),alloc=("alloc","mean"))
    out["by_year"]=S.groupby("year").agg(n=("pnl","size"),pnl=("pnl","sum"),short_ex=("short_ex","mean"))
    out["by_coin"]=S.groupby("coin").agg(n=("pnl","size"),pnl=("pnl","sum"),short_ex=("short_ex","mean"))
    for col in ["cl","rm","r1","r3","r10","body"]:
        out["sig_by_"+col]=grp(S,col)
        out["noSig_inprof_lowclose_by_"+col]=grp(U,col)
    # all in-profile bars by r1 (both)
    P=B[B["inprof"]].dropna(subset=["nxt"])
    out["inprof_all_by_r1"]=grp(P,"r1",5)
    # book daily drawdown
    D=[]
    for coin,wd in data["days"].items():
        for w,d in wd.items():
            d=d[["day","book_return","coin_return"]].copy();d["w"]=w;d["coin"]=coin;D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["w","day"])
    v=(1+bk["book_return"]).cumprod();dd=v/v.cummax()-1
    bk["dd"]=dd.values
    out["dd_stats"]=pd.Series({"maxdd":dd.min(),"days":len(bk),"mean":bk.book_return.mean(),"sd":bk.book_return.std()})
    out["dd_by_window"]=bk.groupby("w").agg(ret=("book_return","sum"),worst=("book_return","min"),mindd=("dd","min"))
    # worst 20 short trades features
    W=S.sort_values("pnl").head(25)
    out["worst25_means"]=W[["cl","rm","r1","r3","r10","body","nxt","alloc"]].mean()
    out["all_sig_means"]=S[["cl","rm","r1","r3","r10","body","nxt","alloc"]].mean()
    out["worst25_by_window"]=W.groupby("w").size()
    return out
