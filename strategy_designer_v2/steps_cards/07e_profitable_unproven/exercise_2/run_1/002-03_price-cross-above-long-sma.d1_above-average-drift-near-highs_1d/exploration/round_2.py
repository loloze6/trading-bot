def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            a=b["postRebalance_current_allocation"].astype(float)
            r20=c/c.shift(20)-1
            hi=c.rolling(20).max(); lo=c.rolling(20).min()
            pos=(c-lo)/(hi-lo)
            ma200=c.rolling(200,min_periods=200).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"alloc":a,"fc":b["forecast"].astype(float),
               "regime":b["regime"].astype(str),"r20":r20,"pos":pos})
            for h in [1,5,10,20]:
                df[f"f{h}"]=c.shift(-h)/c-1
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    drift=D.groupby("coin").f1.mean()
    D["ex"]=D.alloc*(D.f1-D.coin.map(drift))
    d=D.dropna(subset=["f1"])
    g=d.groupby("coin").ex
    out["timing_excess_daily"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/g.std()*np.sqrt(g.size()),"n":g.size()})
    out["timing_excess_all"]=pd.Series({"mean":d.ex.mean(),"t":d.ex.mean()/d.ex.std()*np.sqrt(len(d)),
        "drift_part_mean":(d.alloc*d.coin.map(drift)).mean(),"gain_mean":(d.alloc*d.f1).mean()})
    # horizons, non-overlapping grid, trending, forecast tercile vs coin mean
    res=[]
    for h in [1,5,10,20]:
        s=D[(D.i%h==0)].dropna(subset=[f"f{h}"]).copy()
        m=s.groupby("coin")[f"f{h}"].mean()
        s["x"]=s[f"f{h}"]-s.coin.map(m)
        t=s[s.regime=="trending"]
        pos_=t[t.fc>0]; 
        hi_=pos_[pos_.fc>pos_.fc.median()]; lo_=pos_[pos_.fc<=pos_.fc.median()]
        z=t[t.fc<=0]
        r=stats.ttest_ind(hi_.x,z.x,equal_var=False)
        res.append({"h":h,"hi_fc_ex":hi_.x.mean(),"n_hi":len(hi_),"lo_fc_ex":lo_.x.mean(),"n_lo":len(lo_),
                    "trend_fc0_ex":z.x.mean(),"n_z":len(z),"t_hi_minus_fc0":r.statistic,
                    "t_hi_vs0":hi_.x.mean()/hi_.x.std()*np.sqrt(len(hi_))})
    out["horizon_trending"]=pd.DataFrame(res).set_index("h")
    # outside regime: same raw signal predicts?
    res=[]
    for h in [1,5,20]:
        s=D[(D.i%h==0)].dropna(subset=[f"f{h}","r20","pos"]).copy()
        m=s.groupby("coin")[f"f{h}"].mean(); s["x"]=s[f"f{h}"]-s.coin.map(m)
        s["sig"]=s.groupby("coin").r20.rank(pct=True)+s.groupby("coin").pos.rank(pct=True)
        for reg in ["trending","unknown"]:
            u=s[s.regime==reg]
            q=pd.qcut(u.sig,3,labels=["low","mid","high"])
            mm=u.groupby(q).x.mean()
            r=stats.ttest_ind(u.x[q=="high"],u.x[q=="low"],equal_var=False)
            res.append({"h":h,"reg":reg,"low":mm["low"],"mid":mm["mid"],"high":mm["high"],"t_high_minus_low":r.statistic,"n":len(u)})
    out["signal_by_regime"]=pd.DataFrame(res)
    # book concentration on daily returns
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["w"]=w; dd.append(x)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    day=DD.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).reset_index()
    b=day.b.sort_values(ascending=False)
    n=len(b)
    out["book_conc"]=pd.Series({"n_days":n,"mean":b.mean(),"mean_wo_top1pct":b.iloc[n//100:].mean(),
       "mean_wo_top5pct":b.iloc[n//20:].mean(),"share_pos_days":(b>0).mean()})
    day["hq"]=pd.qcut(day.h,5)
    out["book_by_market_day"]=day.groupby("hq").agg(book=("b","mean"),hold=("h","mean"),n=("b","size"))
    beta=np.polyfit(day.h,day.b,1)
    resid=day.b-beta[0]*day.h
    out["beta_alpha"]=pd.Series({"beta":beta[0],"alpha_daily":beta[1],"t_alpha":resid.mean()/resid.std()*np.sqrt(len(resid))})
    return out
