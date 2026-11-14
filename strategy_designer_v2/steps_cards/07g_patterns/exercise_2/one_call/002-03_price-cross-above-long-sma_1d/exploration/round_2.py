def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].astype(float).reset_index(drop=True)
            d=pd.DataFrame(index=range(len(cl)))
            d["coin"]=c; d["win"]=w
            d["dist"]=b["debug_info.components.above_ma.last_history_value"].astype(float).values
            d["fc"]=b["forecast"].astype(float).values
            d["alloc"]=b["postRebalance_current_allocation"].astype(float).values
            pv=b["postRebalance_total_value"].astype(float).reset_index(drop=True)
            d["br1"]=pv.pct_change()
            d["r1"]=cl.pct_change()
            d["f1"]=cl.shift(-1)/cl-1
            d["f5"]=cl.shift(-5)/cl-1
            d["f20"]=cl.shift(-20)/cl-1
            d["vol20"]=d["r1"].rolling(20).std()
            d["mom20"]=cl/cl.shift(20)-1
            d["rz"]=d["r1"]/d["vol20"].shift(1)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            d["wd"]=ts.dt.weekday.values; d["yr"]=ts.dt.year.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean()
    D["mu"]=D["coin"].map(mu)
    D["x20"]=D["f20"]-20*D["mu"]; D["x5"]=D["f5"]-5*D["mu"]; D["x1"]=D["f1"]-D["mu"]
    K={"x20":20,"x5":5,"x1":1}
    def summ(g,col):
        s=g[col].dropna()
        if len(s)<3: return pd.Series({"n":len(s),"mean":np.nan,"t":np.nan,"hit":np.nan})
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/s.std()*np.sqrt(len(s)/K[col]),"hit":(s>0).mean()})
    def two(g,a,b_):
        return pd.concat([summ(g,a).add_prefix(a+"_"),summ(g,b_).add_prefix(b_+"_")])
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="ERR "+str(e)[:100]
    D["distq"]=pd.qcut(D["dist"],10,labels=False,duplicates="drop")
    safe("by_dist_decile",lambda: D.groupby("distq").apply(lambda g: two(g,"x20","x5")).assign(dist_med=D.groupby("distq")["dist"].median()))
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    safe("by_vol_quint",lambda: D.groupby("volq").apply(lambda g: two(g,"x20","x5")))
    safe("by_vol_quint_above",lambda: D[D["dist"]>0].groupby("volq").apply(lambda g: two(g,"x20","x5")))
    D["momq"]=D.groupby("coin")["mom20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    safe("by_mom20_quint",lambda: D.groupby("momq").apply(lambda g: two(g,"x20","x5")))
    D["bigmv"]=pd.cut(D["rz"],[-99,-2.5,-1.5,1.5,2.5,99],labels=["vbigdn","dn","mid","up","vbigup"])
    safe("after_big_moves",lambda: D.groupby("bigmv").apply(lambda g: two(g,"x1","x5")))
    safe("weekday_x1",lambda: D.groupby("wd").apply(lambda g: summ(g,"x1")))
    safe("year_x20_above_vs_below",lambda: D.assign(ab=D["dist"]>0).groupby(["yr","ab"]).apply(lambda g: summ(g,"x20")["mean"]).unstack())
    safe("coin_above_below_x20",lambda: D.assign(ab=D["dist"]>0).groupby(["coin","ab"]).apply(lambda g: summ(g,"x20")).unstack())
    # book largest gains/losses: coin return before/after
    def bk():
        B=D.dropna(subset=["br1"]).copy()
        q=B["br1"].quantile([0.01,0.99])
        B["cls"]=np.where(B["br1"]<=q.iloc[0],"worst1pct",np.where(B["br1"]>=q.iloc[1],"best1pct","other"))
        return B.groupby("cls").agg(n=("br1","size"),br=("br1","mean"),dist=("dist","median"),fc=("fc","mean"),mom20=("mom20","mean"),vol20=("vol20","mean"),x5_after=("x5","mean"))
    safe("book_extremes",bk)
    def tr():
        T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
        T["dd"]=T["duration_minutes"]/1440
        T["dq"]=pd.cut(T["dd"],[-1,1.5,5,20,60,1e6])
        g=T.groupby("dq").agg(n=("dd","size"),mean_net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()),sum_net=("net_profit_loss_percent","sum"))
        return g
    safe("trades_by_duration",tr)
    return out
