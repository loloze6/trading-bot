def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy(); cl=b["close"].values; n=len(cl)
            b["r1f"]=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            r5=np.full(n,np.nan)
            if n>5: r5[:-5]=cl[5:]/cl[:-5]-1
            b["r5f"]=r5
            r5d=np.full(n,np.nan)
            if n>6: r5d[1:-5]=cl[6:]/cl[1:-5]-1
            b["r5d"]=r5d  # 5-day return starting one day later
            b["alloc"]=b["postRebalance_current_allocation"]
            b["gain"]=b["alloc"]*b["r1f"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["turn"]=(b["alloc"]-b["previous_allocation"]).abs()
            s=pd.Series(cl)
            b["ret20"]=(s/s.shift(20)-1).values
            b["ret60"]=(s/s.shift(60)-1).values
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(n)
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    cm1=B.groupby("coin")["r1f"].mean(); B["cm1"]=B["coin"].map(cm1)
    G=B[B.pos%5==0]
    cm5=G.groupby("coin")["r5f"].mean(); B["x5"]=B["r5f"]-B["coin"].map(cm5)
    cm5d=G.groupby("coin")["r5d"].mean(); B["x5d"]=B["r5d"]-B["coin"].map(cm5d)
    G=B[(B.pos%5==0)&(B.forecast>0)]
    out={}
    def slope(df,y):
        d=df[["forecast",y]].dropna()
        if len(d)<30: return [np.nan,np.nan,len(d)]
        r=stats.linregress(d["forecast"],d[y]); return [r.slope,r.slope/r.stderr,len(d)]
    res={}
    for nm,m in [("all",G.index==G.index),("ret20>0",G.ret20>0),("ret20<=0",G.ret20<=0),("ret60>0",G.ret60>0),("ret60<=0",G.ret60<=0)]:
        sub=G[m]
        res[nm]=slope(sub,"x5")+slope(sub,"x5d")[:2]+[sub["x5"].mean()]
    out["grid_slope_by_trend"]=pd.DataFrame(res,index=["slope5","t5","n","slope5_skip1","t5_skip1","meanx5"]).T
    # book gain/fee split by trend context (all bars, by allocation)
    B["ctx"]=np.where(B.ret20>0,"up20","down20")
    out["book_by_ctx"]=B.groupby("ctx").agg(n=("gain","size"),gain=("gain","mean"),fee=("fee","mean"),alloc=("alloc","mean"),turn=("turn","mean"))
    # turnover sources: share of turnover from days where forecast went to 0 vs >0
    B["fprev"]=B.groupby(["coin","w"])["forecast"].shift(1)
    B["kind"]=np.select([(B.forecast>0)&(B.fprev==0),(B.forecast==0)&(B.fprev>0),(B.forecast>0)&(B.fprev>0)],["enter","exit","resize"],"flat")
    out["turn_by_kind"]=B.groupby("kind").agg(n=("turn","size"),turn=("turn","sum"),fee=("fee","sum"))
    # mean length of consecutive positive-forecast runs
    runs=[]
    for (c,w),b in B.groupby(["coin","w"]):
        p=(b.forecast>0).astype(int).values
        cnt=0
        for v in p:
            if v: cnt+=1
            elif cnt: runs.append(cnt); cnt=0
        if cnt: runs.append(cnt)
    out["pos_run_len"]=pd.Series(runs).describe()
    # day-1 excess by quintile of forecast
    P=B[B.forecast>0].copy(); P["x1"]=P["r1f"]-P["cm1"]
    P["q"]=pd.qcut(P["forecast"].rank(method="first"),5,labels=False)
    out["x1_x5skip_by_q"]=P.groupby("q").agg(x1=("x1","mean"),x5d=("x5d","mean"))
    return out
