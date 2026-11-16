def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daysrows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            cl=b["close"].values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            b["r1f"]=r1
            r5=np.full(len(cl),np.nan); 
            if len(cl)>5: r5[:-5]=cl[5:]/cl[:-5]-1
            b["r5f"]=r5
            b["rpast"]=np.r_[np.nan,cl[1:]/cl[:-1]-1]
            b["alloc"]=b["postRebalance_current_allocation"]
            b["gain"]=b["alloc"]*b["r1f"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["turn"]=(b["alloc"]-b["previous_allocation"]).abs()
            # forecast held 5 bars: max of last 5 forecasts
            b["f5"]=b["forecast"].rolling(5,min_periods=1).max()
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(len(b))
            rows.append(b)
            d=data["days"][c][w].copy(); d["coin"]=c; d["w"]=w; daysrows.append(d)
    B=pd.concat(rows); D=pd.concat(daysrows)
    out={}
    bk=D.groupby("day")[["book_return","coin_return"]].mean()
    out["book_vs_hold_daily"]=pd.DataFrame({"mean":bk.mean(),"std":bk.std(),"sharpe":bk.mean()/bk.std()*np.sqrt(365)})
    out["gross_gain_mean_per_bar"]=B["gain"].mean()
    out["fee_mean_per_bar"]=B["fee"].mean()
    out["turnover_mean_per_bar"]=B["turn"].mean()
    out["share_bars_long"]=(B["alloc"]>0.01).mean()
    out["mean_alloc_when_long"]=B.loc[B["alloc"]>0.01,"alloc"].mean()
    cm=B.groupby("coin")["r1f"].mean()
    B["cm1"]=B["coin"].map(cm)
    out["market_part"]=(B["alloc"]*B["cm1"]).mean()
    out["timing_part"]=(B["alloc"]*(B["r1f"]-B["cm1"])).mean()
    # by forecast bucket: next 1 day and next 5-day returns, excess
    cm5=B[B.pos%5==0].groupby("coin")["r5f"].mean()
    B["x1"]=B["r1f"]-B["cm1"]; B["x5"]=B["r5f"]-B["coin"].map(cm5)
    pos=B[B["forecast"]>0].copy()
    pos["q"]=pd.qcut(pos["forecast"].rank(method="first"),5,labels=False)
    g=pos.groupby("q").agg(n=("x1","size"),f=("forecast","mean"),x1=("x1","mean"),x5=("x5","mean"),alloc=("alloc","mean"),gain=("gain","mean"),fee=("fee","mean"))
    out["by_fc_quintile"]=g
    z=B[B["forecast"]==0]
    out["flat_days_next"]=pd.Series({"n":len(z),"x1":z["x1"].mean(),"x5":z["x5"].mean()})
    # day-by-day after a positive forecast: excess return on days k=1..5
    res={}
    for k in range(1,6):
        s=B.groupby(["coin","w"])["rpast"].shift(-k)
        xs=(s-B["cm1"])[B["forecast"]>0]
        res[k]=[xs.mean(),xs.mean()/xs.std()*np.sqrt(xs.count()),xs.count()]
    out["excess_on_day_k_after_signal"]=pd.DataFrame(res,index=["mean","t","n"]).T
    # gain by year
    B["year"]=pd.to_datetime(B["timestamp"]).dt.year
    out["by_year"]=B.groupby("year").agg(gain=("gain","mean"),fee=("fee","mean"),longshare=("alloc",lambda a:(a>0.01).mean()),coinret=("r1f","mean"))
    out["by_coin"]=B.groupby("coin").agg(gain=("gain","mean"),fee=("fee","mean"),coinret=("r1f","mean"))
    # past 20-day trend context for signals
    B["ret20"]=B.groupby(["coin","w"])["close"].transform(lambda x:x/x.shift(20)-1)
    p=B[B["forecast"]>0].copy()
    p["tq"]=pd.qcut(p["ret20"],4,labels=False)
    out["signal_by_past20_quartile"]=p.groupby("tq").agg(n=("x5","size"),r20=("ret20","mean"),x1=("x1","mean"),x5=("x5","mean"),gain=("gain","mean"))
    return out
