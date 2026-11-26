def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            s=r.rolling(30,min_periods=20).std()
            z=r/s
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"zl":z.shift(1),
                "calm":(b["regime"]!="chop"),"calml":(b["regime"]!="chop").shift(1),
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"wd":ts.dt.weekday,"year":ts.dt.year,
                "day":ts.dt.floor("D")})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["f1x"]=A["f1"]-A["coin"].map(A.groupby("coin")["f1"].mean())
    g2=A[A.pos%2==0]
    A["f2x"]=A["f2"]-A["coin"].map(g2.groupby("coin")["f2"].mean())
    out={}
    def slope(g,x,y):
        g=g.dropna(subset=[x,y])
        sl=stats.linregress(g[x],g[y]); return [sl.slope,sl.slope/sl.stderr,len(g)]
    def daysure(g,y):
        d=g.dropna(subset=[y]).groupby("day")[y].sum()
        n=g.dropna(subset=[y]).shape[0]
        return [g[y].mean(), d.mean()/d.std()*np.sqrt(len(d)), n, len(d)]
    res={}
    # delayed: day after a rise (yesterday's z>0, yesterday calm), next 1-day return
    D=A[(A.calml==True)&(A.zl>0)]
    res["calm_lag_up_all"]=slope(D,"zl","f1x")
    for y,g in D.groupby("year"): res[f"calm_lag_up_{y}"]=slope(g,"zl","f1x")
    for c_,g in D.groupby("coin"): res[f"calm_lag_up_{c_}"]=slope(g,"zl","f1x")
    D2=A[(A.calml==False)&(A.zl>0)]
    res["agit_lag_up_all"]=slope(D2,"zl","f1x")
    out["delayed_slope"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # weighted mean of the delayed case
    D=D.assign(w_=D.zl)
    out["calm_lag_up_wmean"]=float((D.f1x*D.zl).sum()/D.zl.sum())
    out["calm_lag_up_sure_zl_gt1"]=pd.Series(daysure(D[D.zl>1],"f1x"),index=["mean","t_day","n","days"])
    # agitated down-day rebound next day
    res={}
    E=A[(A.calm==False)&(A.z<0)]
    res["agit_down_f1_all"]=slope(E,"z","f1x")
    for y,g in E.groupby("year"): res[f"agit_down_f1_{y}"]=slope(g,"z","f1x")
    for c_,g in E.groupby("coin"): res[f"agit_down_f1_{c_}"]=slope(g,"z","f1x")
    out["agit_down_slope"]=pd.DataFrame(res,index=["slope","t","n"]).T
    out["agit_down_sure_z_lt_m1"]=pd.Series(daysure(E[E.z<-1],"f1x"),index=["mean","t_day","n","days"])
    # weekday by year
    out["wd_by_year"]=A.dropna(subset=["f1x"]).pivot_table(index="wd",columns="year",values="f1x",aggfunc="mean")
    out["wd_sure"]=pd.DataFrame({wd:daysure(g,"f1x") for wd,g in A.groupby("wd")},index=["mean","t_day","n","days"]).T
    return out
