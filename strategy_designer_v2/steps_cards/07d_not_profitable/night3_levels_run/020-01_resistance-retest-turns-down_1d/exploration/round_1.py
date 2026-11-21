def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(cl)
            f=b["forecast"].fillna(0).values
            raw=b["debug_info.components.resistance.last_history_value"].values
            r30=pd.Series(cl).pct_change(30).values
            hi90=pd.Series(cl).rolling(90,min_periods=30).max().values
            fr=np.full(n,np.nan); fr[:n-H]=cl[H:]/cl[:n-H]-1
            # breakout: raw went from >0 to 0 (no level above) on this bar
            prevraw=np.r_[np.nan,raw[:-1]]
            for i in range(0,n-H,H):
                rows.append(dict(coin=c,w=w,f=f[i],raw=raw[i],r30=r30[i],near=cl[i]/hi90[i]-1 if hi90[i]==hi90[i] else np.nan,
                                 brk=(prevraw[i]>0)&(raw[i]==0) if raw[i]==raw[i] else False,fr=fr[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows).dropna(subset=["fr"])
    d["drift"]=d.groupby("coin")["fr"].transform("mean"); d["un"]=d["fr"]-d["drift"]
    out={}
    d["fb"]=pd.cut(d["f"],[-21,-10,-5,-0.01,0.01,21])
    out["by_forecast"]=d.groupby("fb")["un"].agg(["count","mean"]).assign(t=d.groupby("fb")["un"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    d["rb"]=pd.qcut(d["r30"],4)
    s=d[d.f<=-5]
    out["short_cases_by_r30"]=s.groupby("rb")["un"].agg(["count","mean"])
    out["all_by_r30"]=d.groupby("rb")["un"].agg(["count","mean"])
    d["rawb"]=pd.cut(d["raw"],[-0.01,0.001,1,2,3,5,100])
    out["by_raw"]=d.groupby("rawb")["un"].agg(["count","mean"]).assign(t=d.groupby("rawb")["un"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan))
    d["nb"]=pd.qcut(d["near"],5,duplicates="drop")
    out["by_near90high"]=d.groupby("nb")["un"].agg(["count","mean"]).assign(t=d.groupby("nb")["un"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["breakout_bars"]=d.groupby("brk")["un"].agg(["count","mean"])
    out["corr_raw_un_ifraw>0"]=float(stats.spearmanr(d.loc[d.raw>0,"raw"],d.loc[d.raw>0,"un"],nan_policy="omit")[0])
    dy=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["w"]=w; dy.append(x)
    dy=pd.concat(dy)
    g=dy.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_mean_by_window"]=g.groupby(level=0)["book_return"].mean().describe()
    out["share_windows_coin_up"]=float((g.groupby(level=0)["coin_return"].mean()>0).mean())
    out["mean_alloc"]=float(d["alloc"].mean())
    return out
