def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"fwd":c.shift(-H)/c-1,
                "raw":b.get("debug_info.components.near_high.last_history_value"),
                "z1":r1/vol20.shift(1),"r20p":(c/c.shift(20)-1)/(vol20*np.sqrt(20)),
                "ret60":c/c.shift(60)-1,"wd":ts.dt.weekday,"day":ts.dt.floor("D"),"yr":ts.dt.year,
                "r1n":r1.shift(-1),"alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    res={}
    # weekday of the return's own day, clustered by day: mean over coins per day first
    A["retwd"]=(A.wd+1)%7
    dd=A.dropna(subset=["r1n"]).groupby(["day","retwd","w","yr"])["r1n"].mean().reset_index()
    wd=dd.groupby("retwd")["r1n"].agg(["size","mean","std"]);wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["size"]))
    res["ret_by_weekday_of_return_dayclustered"]=wd
    dd["fri"]=dd.retwd.isin([2,4,5])
    byw=dd.groupby(["w","fri"])["r1n"].mean().unstack();byw["diff"]=byw[True]-byw[False]
    res["wed_fri_sat_minus_rest_by_window"]=byw
    byy=dd.groupby(["yr","fri"])["r1n"].mean().unstack();byy["diff"]=byy[True]-byy[False]
    res["wed_fri_sat_minus_rest_by_year"]=byy
    # weekday per coin
    pc=A.dropna(subset=["r1n"]).assign(f=lambda x:x.retwd.isin([2,4,5])).groupby(["coin","f"])["r1n"].mean().unstack()
    pc["diff"]=pc[True]-pc[False];res["wfs_minus_rest_by_coin"]=pc
    # grid regressions, day-clustered via daily sums
    drift=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    G=A[(A.pos%H==0)].dropna(subset=["ex","raw","z1","r20p"]).copy()
    def ols(g,cols):
        X=np.column_stack([np.ones(len(g))]+[g[c].values for c in cols]);y=g.ex.values
        bta=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@bta
        XtXi=np.linalg.inv(X.T@X);meat=np.zeros((X.shape[1],)*2)
        for _,idx in g.reset_index(drop=True).groupby("day").indices.items():
            s=(X[idx]*e[idx,None]).sum(0);meat+=np.outer(s,s)
        se=np.sqrt(np.diag(XtXi@meat@XtXi))
        return pd.DataFrame({"coef":bta,"t":bta/se},index=["c"]+cols)
    res["reg_raw"]=ols(G,["raw"])
    res["reg_raw_z1_r20p"]=ols(G,["raw","z1","r20p"])
    G["far"]=np.minimum(G.raw+1.6,0);G["near"]=np.maximum(G.raw+1.6,0)
    res["reg_piecewise_far_near"]=ols(G,["far","near"])
    g2=G.dropna(subset=["ret60"]).copy()
    g2["tr"]=np.where(g2.ret60>0.1,"rising",np.where(g2.ret60<-0.1,"falling","choppy"))
    res["reg_raw_by_trend"]=pd.concat({k:ols(v,["raw"]) for k,v in g2.groupby("tr")})
    # book: market part vs timing
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;D.append(d)
    D=pd.concat(D)
    mu=D.groupby("coin").coin_return.mean()
    al=A.groupby(["coin","w","day"])["alloc"].last().reset_index()
    D["day"]=pd.to_datetime(D["day"]).dt.floor("D")
    M=D.merge(al,on=["coin","w","day"],how="left")
    M["mkt"]=M.groupby(["coin","w"])["alloc"].shift(1)*M.coin.map(mu)
    bk=M.groupby(["w","day"])[["book_return","mkt"]].mean().dropna()
    res["book_mean_vs_market_part"]=pd.Series({"book":bk.book_return.mean(),"market_part":bk.mkt.mean(),"mean_alloc":M.alloc.mean()})
    return res
