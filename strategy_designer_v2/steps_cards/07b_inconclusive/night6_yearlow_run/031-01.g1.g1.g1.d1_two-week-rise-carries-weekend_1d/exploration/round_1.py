def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        g2=[]
        for w,b in wins.items():
            c=b["close"].values
            g2+= [c[i+2]/c[i]-1 for i in range(0,len(c)-2,2)]
        drift=np.mean(g2)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]
            lr=np.log(c).diff()
            r14=np.log(c/c.shift(14))/(lr.rolling(20).std()*np.sqrt(14))
            f2=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            d=pd.DataFrame({"coin":coin,"win":w,"day":ts.dt.floor("D"),"year":ts.dt.year,
                            "wd":ts.dt.weekday,"r14":r14,"fc":b["forecast"],"ex":f2-drift,"ex1":f1-drift/2})
            rows.append(d[d.wd==4])
    d=pd.concat(rows).dropna(subset=["ex","r14"])
    def summ(x):
        dd=x.groupby("day")["ex"].sum(); nd=x.groupby("day").size()
        t=x["ex"].sum()/np.sqrt(((dd-nd*x["ex"].mean())**2).sum()) if len(x)>2 else np.nan
        return pd.Series({"n":len(x),"mean_ex":x["ex"].mean(),"t_day":t,"mean_sat":x["ex1"].mean()})
    out={}
    d["q"]=pd.qcut(d["r14"],5,labels=["q1low","q2","q3","q4","q5high"])
    out["by_r14_quintile_all_fridays"]=d.groupby("q").apply(summ)
    d["side"]=np.where(d["fc"]>0,"fc>0","fc=0")
    out["by_forecast_side"]=d.groupby("side").apply(summ)
    pos=d[d.fc>0].copy()
    pos["fq"]=pd.qcut(pos["fc"],4,labels=["f1","f2","f3","f4"])
    out["fc>0_by_forecast_quartile"]=pos.groupby("fq").apply(summ)
    out["fc>0_by_coin"]=pos.groupby("coin").apply(summ)
    out["fc>0_by_year"]=pos.groupby("year").apply(summ)
    out["all_fridays_by_year"]=d.groupby("year").apply(summ)
    # slope of ex on r14 per coin, all Fridays
    sl={}
    for coin,x in d.groupby("coin"):
        r=stats.linregress(x["r14"],x["ex"]); sl[coin]=(r.slope,r.slope/r.stderr,len(x))
    out["slope_r14_all_fridays_by_coin"]=pd.DataFrame(sl,index=["slope","t","n"]).T
    r=stats.linregress(d["r14"],d["ex"]); out["slope_r14_all_fridays_pooled"]=f"slope {r.slope:.5f} t {r.slope/r.stderr:.2f} n {len(d)}"
    r=stats.linregress(pos["r14"],pos["ex"]); out["slope_r14_fc>0"]=f"slope {r.slope:.5f} t {r.slope/r.stderr:.2f} n {len(pos)}"
    return out
