def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"ts":ts,"r1":r1,"wd":ts.dt.weekday,"yr":ts.dt.year,
                             "pos":b["postRebalance_current_allocation"].astype(float).shift(1)})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1"])
    d["ex"]=d["r1"]-d.groupby("coin")["r1"].transform("mean")
    out={}
    # daily returns by weekday of the bar (return from previous close to this close), pooled
    o=d.groupby("wd")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["daily_ex_by_weekday_pooled"]=o
    # clustered by date: average across coins per day first
    m=d.groupby(["ts","wd"])["ex"].mean().reset_index()
    o=m.groupby("wd")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["daily_ex_by_weekday_dateclustered"]=o
    # stability: by year, mean ex on each weekday (date clustered)
    m["yr"]=m["ts"].dt.year
    out["weekday_by_year_mean"]=m.pivot_table(index="yr",columns="wd",values="ex",aggfunc="mean")
    # per coin t of Sunday and Monday
    def ct(s):
        return s.mean()/(s.std()/np.sqrt(len(s)))
    pc=d.groupby(["coin","wd"])["ex"].apply(ct).unstack()
    out["t_by_coin_weekday"]=pc
    # weekend effect graded? returns on Mon by size of weekend (Sat+Sun) move
    d=d.sort_values(["coin","w","ts"])
    d["prev2"]=d.groupby(["coin","w"])["r1"].transform(lambda s:(1+s).rolling(2).apply(np.prod,raw=True)-1).shift(0)
    # book gain by weekday (position x next return)
    d["bg"]=d["pos"]*d["r1"]
    o=d.groupby("wd")["bg"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["book_bar_gain_by_weekday"]=o
    # volatility by weekday
    out["abs_ret_by_weekday"]=d.groupby("wd")["r1"].apply(lambda s:s.abs().mean())
    # Monday return vs weekend return (Sat+Sun), date-clustered correlation, by coin pooled
    x=d.copy()
    x["wkend"]=x.groupby(["coin","w"])["r1"].shift(1).fillna(0)+x.groupby(["coin","w"])["r1"].shift(2).fillna(0)
    mon=x[x["wd"]==0].dropna(subset=["wkend","ex"])
    mon["q"]=mon.groupby("coin")["wkend"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    o=mon.groupby("q")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["monday_ex_by_weekend_move_q"]=o
    return out
