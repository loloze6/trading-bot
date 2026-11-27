def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean()
            sd=r.rolling(20).std()
            dist=(c/sma-1)/sd
            tr30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in (5,10,20):
                fwd=c.shift(-h)/c-1
                for i in range(0,len(b)-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=yr[i],day=str(b["timestamp"][i])[:10],
                        fc=b["forecast"][i],ag=b["regime"][i]!="chop",dist=dist[i],tr30=tr30[i],fwd=fwd[i]))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["un"]=d["fwd"]-d["drift"]
    out={}
    def summ(g):
        n=len(g); m=g["un"].mean(); t=m/(g["un"].std()/np.sqrt(n)) if n>2 else np.nan
        sl=np.nan;ts=np.nan
        if n>5 and g["dist"].std()>0:
            res=stats.linregress(-g["dist"],g["un"]); sl=res.slope; ts=res.slope/res.stderr
        return pd.Series(dict(n=n,mean_un=m,t=t,mean_fwd=g["fwd"].mean(),slope_depth=sl,t_slope=ts))
    below=d[d["dist"]<0]
    out["by_h_ag"]=below.groupby(["h","ag"]).apply(summ)
    b10=below[below.h==10].copy()
    b10["q"]=pd.qcut(-b10["dist"],4,labels=["q1shallow","q2","q3","q4deep"])
    out["depth_q_ag"]=b10.groupby(["ag","q"]).apply(summ)
    a10=b10[b10.ag]
    out["ag_coin"]=a10.groupby("coin").apply(summ)
    out["ag_window"]=a10.groupby("w").apply(summ)
    out["ag_year"]=a10.groupby("year").apply(summ)
    a10=a10.copy(); a10["tr"]=np.where(a10.tr30>0.05,"up",np.where(a10.tr30<-0.05,"down","flat"))
    out["ag_tr30"]=a10.groupby("tr").apply(summ)
    out["ag_fc_pos"]=b10[(b10.ag)&(b10.fc>0)].pipe(summ)
    return out
