def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    out={}
    # coin mean daily return over all windows
    dy=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["w"]=w; dy.append(x)
    dy=pd.concat(dy)
    mu=dy.groupby("coin")["coin_return"].mean()
    out["coin_mean_daily"]=mu
    # decomposition per coin from bars: alloc at last bar of day x coin mean daily return
    dec=[]
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(cl)
            a=b["postRebalance_current_allocation"].fillna(0).values
            g=np.r_[a[:-1]*(cl[1:]/cl[:-1]-1),np.nan]
            dec.append(dict(coin=c,w=w,gain=np.nanmean(g),drift_part=np.nanmean(a[:-1])*mu[c],mean_alloc=a.mean()))
            raw=b["debug_info.components.resistance.last_history_value"].values
            prevmax=pd.Series(raw).shift(1).rolling(5,min_periods=1).max().values
            r30=pd.Series(cl).pct_change(30).values
            hi90=pd.Series(cl).rolling(90,min_periods=30).max().shift(1).values
            fr=np.full(n,np.nan); fr[:n-H]=cl[H:]/cl[:n-H]-1
            for i in range(0,n-H,H):
                rows.append(dict(coin=c,w=w,raw=raw[i],prevmax=prevmax[i],
                    above=(cl[i]/hi90[i]-1) if hi90[i]==hi90[i] else np.nan,r30=r30[i],fr=fr[i]))
    dec=pd.DataFrame(dec)
    out["book_bar_gain_decomp"]=dec[["gain","drift_part","mean_alloc"]].mean()
    out["share_windows_book_gain_neg"]=float((dec.groupby("w")["gain"].mean()<0).mean())
    d=pd.DataFrame(rows).dropna(subset=["fr"])
    d["drift"]=d.groupby("coin")["fr"].transform("mean"); d["un"]=d["fr"]-d["drift"]
    # breakouts: no level above now, had a level within last 5 bars; graded by previous count
    bk=d[(d.raw==0)&(d.prevmax>0)].copy()
    bk["pb"]=pd.cut(bk["prevmax"],[0,0.5,1,2,100])
    out["breakout_by_prevcount"]=bk.groupby("pb")["un"].agg(["count","mean"])
    out["breakout_all"]=pd.Series(dict(n=len(bk),mean=bk.un.mean(),t=bk.un.mean()/bk.un.std()*np.sqrt(len(bk)),total=bk.fr.mean()))
    # close above prior 90-day high, graded by how far above
    ab=d[d.above>0].copy()
    ab["ab"]=pd.qcut(ab["above"],3,duplicates="drop")
    out["above_prior90high"]=ab.groupby("ab")["un"].agg(["count","mean"]).assign(tot=ab.groupby("ab")["fr"].mean())
    out["above_all_t"]=float(ab.un.mean()/ab.un.std()*np.sqrt(len(ab)))
    out["usual_move_5d"]=float(d.groupby("coin")["fr"].std().mean())
    # r30 graded
    d["rq"]=pd.qcut(d["r30"],5)
    out["r30_quintiles"]=d.groupby("rq")["un"].agg(["count","mean"]).assign(t=d.groupby("rq")["un"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["spearman_above_un"]=float(stats.spearmanr(d["above"],d["un"],nan_policy="omit")[0])
    return out
