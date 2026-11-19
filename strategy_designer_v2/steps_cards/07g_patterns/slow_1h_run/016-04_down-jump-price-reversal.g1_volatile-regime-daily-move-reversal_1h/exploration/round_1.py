def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # 1. book gross vs net: per-bar gross gain, fee drag
    rows=[]
    for c in bars:
        g=[];f=[];turn=[]
        for w,df in bars[c].items():
            pos=df["postRebalance_current_allocation"].values
            cl=df["close"].values
            r=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            g.append(pos*r)
            fee=(df["total_portfolio_value"]-df["postRebalance_total_value"])/df["total_portfolio_value"]
            f.append(fee.values)
            turn.append(np.abs(df["postRebalance_current_allocation"]-df["previous_allocation"]).values)
        g=np.concatenate(g);f=np.concatenate(f);turn=np.concatenate(turn)
        rows.append({"coin":c,"gross_per_day":np.nanmean(g)*24,"fee_per_day":np.nanmean(f)*24,
                     "turnover_per_day":np.nanmean(turn)*24,"mean_abs_pos":np.nanmean(np.abs(np.concatenate([bars[c][w]["postRebalance_current_allocation"].values for w in bars[c]])))})
    out["gross_fee"]=pd.DataFrame(rows)
    # 2. forecast quintile vs forward returns at several horizons (grid), signed
    res=[]
    for h in [1,6,24,72,168]:
        xs=[];ys=[]
        for c in bars:
            allr=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                idx=np.arange(0,len(cl)-h,h)
                allr.append(cl[idx+h]/cl[idx]-1)
            m=np.nanmean(np.concatenate(allr))
            for w,df in bars[c].items():
                cl=df["close"].values; fc=df["forecast"].values
                idx=np.arange(0,len(cl)-h,h)
                xs.append(fc[idx]); ys.append(cl[idx+h]/cl[idx]-1-m)
        x=np.concatenate(xs);y=np.concatenate(ys)
        ok=~np.isnan(x)&~np.isnan(y)
        p=x[ok]/10*y[ok]
        res.append({"h":h,"n":ok.sum(),"mean":p.mean(),"t":p.mean()/p.std()*np.sqrt(len(p))})
    out["fc_by_horizon"]=pd.DataFrame(res)
    # 3. quintiles of raw scaled move (component last_history_value) and 24h forward excess, split by sign
    q=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-24,24)
            d=pd.DataFrame({"fc":df["forecast"].values[idx],"r":cl[idx+24]/cl[idx]-1,
                            "past":cl[idx]/np.r_[np.full(24,np.nan),cl[:-24]][idx]-1,"coin":c})
            q.append(d)
    q=pd.concat(q)
    q["r"]=q["r"]-q.groupby("coin")["r"].transform("mean")
    q["qf"]=q.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["fc_quint"]=q.groupby("qf")["r"].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # 4. book daily by weekday and coin
    dd=pd.concat([d.assign(coin=c) for c in days for w,d in days[c].items()])
    dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
    out["book_by_coin"]=dd.groupby("coin")[["book_return","coin_return"]].mean()
    # 5. hourly: position gross gain by hour
    hh=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df["close"].values
            r=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            hh.append(pd.DataFrame({"h":pd.to_datetime(df["timestamp"]).dt.hour.values,"g":df["postRebalance_current_allocation"].values*r,"r":r}))
    hh=pd.concat(hh)
    out["hour"]=hh.groupby("h").agg(g=("g","mean"),r=("r","mean"),n=("r","count"))
    return out
