def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]
    for coin,ws in bars.items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r1.rolling(20,min_periods=20).std()
            depth=(c/hi-1)/sd  # <=0
            vol30=r1.rolling(30,min_periods=30).std()
            n=len(b)
            for h in (1,5,10,20):
                b[f"f{h}"]=c.shift(-h)/c-1
            b["depth"]=depth; b["vol30"]=vol30; b["up"]=r1>0
            b["ret20"]=c/c.shift(20)-1
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(n)
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","pos","year","forecast","regime","depth","vol30","up","ret20","f1","f5","f10","f20","postRebalance_current_allocation","timestamp"]])
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.pos%10==0].groupby("coin")["f10"].mean()
    A["d10"]=A["f10"]-A["coin"].map(drift)
    vm=A.groupby("coin")["vol30"].median()
    A["agit"]=A["vol30"]>A["coin"].map(vm)
    A["choppy"]=A["regime"].isin(["mean_reversion","unknown"])
    G=A[(A.pos%10==0)&A.f10.notna()&A.choppy&A.depth.notna()].copy()
    G["dq"]=pd.qcut(G["depth"],5,labels=["deep1","q2","q3","q4","shallow5"])
    def summ(g):
        return pd.Series({"n":len(g),"f10":g.f10.mean(),"d10":g.d10.mean(),"t_f10":stats.ttest_1samp(g.f10,0).statistic if len(g)>2 else np.nan})
    out={}
    out["choppy grid by depth quintile x up"]=G.groupby(["dq","up"]).apply(summ)
    out["choppy grid by depth quintile x agit (up days)"]=G[G.up].groupby(["dq","agit"]).apply(summ)
    S=G[G.up&(G.forecast<0)]
    out["signal cases by year"]=S.groupby("year").apply(summ)
    out["signal cases by ret20 sign"]=S.groupby(S.ret20>0).apply(summ)
    # all horizons on signal cases vs choppy up without signal
    hz={}
    for h in (1,5,10,20):
        s=A[(A.pos%h==0)&A.choppy&A.up&(A.forecast<0)][f"f{h}"].dropna()
        o=A[(A.pos%h==0)&A.choppy&A.up&~(A.forecast<0)][f"f{h}"].dropna()
        hz[h]={"sig_mean":s.mean(),"sig_n":len(s),"t":stats.ttest_1samp(s,0).statistic,"nosig_mean":o.mean(),"nosig_n":len(o)}
    out["horizons signal vs not (choppy up)"]=pd.DataFrame(hz).T
    # book
    D=[]
    for coin,ws in days.items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; d["year"]=pd.to_datetime(d["day"]).dt.year; D.append(d)
    D=pd.concat(D)
    out["book ret by year"]=D.groupby("year")["book_return"].agg(["mean","count"])
    out["book ret by coin"]=D.groupby("coin")["book_return"].agg(["mean","count"])
    pos=A[A.postRebalance_current_allocation.abs()>1e-6]
    out["days in pos by regime/agit"]=pos.groupby(["agit"]).apply(lambda g: pd.Series({"n":len(g),"mean_next1":(g.f1).mean()}))
    return out
