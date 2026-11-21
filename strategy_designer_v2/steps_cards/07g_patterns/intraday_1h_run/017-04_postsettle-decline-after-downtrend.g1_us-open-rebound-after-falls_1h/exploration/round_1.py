def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; pos=[]; daysl=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            b["hour"]=ts.dt.hour.values
            b["wd"]=ts.dt.weekday.values
            cl=b["close"].values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            r2=np.r_[cl[2:]/cl[:-2]-1,np.nan,np.nan]
            f72=pd.Series(cl).pct_change(72).values
            b["r1"]=r1; b["r2"]=r2; b["f72"]=f72
            b["pos"]=b["postRebalance_current_allocation"].fillna(0)
            b["gain"]=b["pos"]*r1
            b["fee"]=b["total_portfolio_value"]-b["postRebalance_total_value"]
            b["feerate"]=b["fee"]/b["total_portfolio_value"]
            b["coin"]=c; b["w"]=w
            rows.append(b[["coin","w","hour","wd","r1","r2","f72","pos","gain","feerate","volume"]])
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["w"]=w; daysl.append(d)
    B=pd.concat(rows,ignore_index=True)
    D=pd.concat(daysl,ignore_index=True)
    out={}
    # by bar hour: mean 1-bar return, t
    g=B.dropna(subset=["r1"]).groupby("hour")["r1"]
    out["r1_by_hour"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # position & gain & fee by hour
    gp=B.groupby("hour")
    out["book_by_hour"]=pd.DataFrame({"mean_pos":gp["pos"].mean(),"gain_bp_sum_per_coinday":gp["gain"].sum()/B.groupby(["coin","w"]).size().sum()*24*1e4,"feerate_mean_bp":gp["feerate"].mean()*1e4})
    # slope of next 1-bar return on 3-day fall depth per decision hour (decision bar hour h -> return of bar h+1)
    res=[]
    for h in range(24):
        s=B[(B.hour==h)].dropna(subset=["r2","f72"])
        x=np.clip(-s["f72"],0,None); y=s["r2"]
        sl=stats.linregress(x,y)
        dn=s[s.f72<0]["r2"]; up=s[s.f72>=0]["r2"]
        res.append([h,sl.slope,sl.slope/sl.stderr,dn.mean()*1e4,up.mean()*1e4,stats.ttest_ind(dn,up,equal_var=False).statistic,len(s)])
    out["r2_on_fall_by_hour"]=pd.DataFrame(res,columns=["hour","slope","t_slope","r2_after_fall_bp","r2_after_rise_bp","t_diff","n"]).set_index("hour")
    D2=D.dropna(subset=["book_return"])
    out["book_daily"]=pd.Series({"mean":D2.book_return.mean(),"sd":D2.book_return.std(),"n":len(D2),
        "coin_mean":D2.coin_return.mean()})
    out["book_by_coin"]=D2.groupby("coin")["book_return"].agg(["mean","std","count"])
    out["fee_total_per_day"]=B["feerate"].sum()/len(D2)
    out["gross_gain_per_day"]=B["gain"].sum()/len(D2)
    return out
