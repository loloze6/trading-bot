def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=20
    bars=data["bars"]
    # normal drift per coin over 20 bars, non-overlapping
    drift={}; usual={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H):
                rs.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rs); usual[c]=np.std(rs)
    rows=[]
    base=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; f=df["forecast"].fillna(0).values
            n=len(df)
            rbv=df.get("debug_info.components.break.last_history_value")
            mav=df.get("debug_info.components.above_ma.last_history_value")
            # baseline: all bars above sma50 (computed in-window)
            sma=pd.Series(cl).rolling(50).mean().values
            for i in range(0,n-H,H):
                if not np.isnan(sma[i]):
                    base.append((c,w,cl[i]>sma[i],cl[i+H]/cl[i]-1-drift[c]))
            low=0.0; taken=set()
            for i in range(n):
                if f[i]<=0:
                    low=0.0; continue
                low=min(low,f[i])
                if f[i]-low>=2:
                    cell=i//H
                    if cell not in taken and i+H<n:
                        taken.add(cell)
                        r={}
                        for h in (5,10,20,40,60):
                            r[h]=cl[i+h]/cl[i]-1-drift[c]*h/H if i+h<n else np.nan
                        rows.append(dict(coin=c,win=w,yr=pd.Timestamp(df["timestamp"].iloc[i]).year,
                            f=f[i],rb=rbv.iloc[i] if rbv is not None else np.nan,
                            ma=mav.iloc[i] if mav is not None else np.nan,
                            u20=r[20],u5=r[5],u10=r[10],u40=r[40],u60=r[60],
                            p5=cl[max(i-5,0)]/cl[i]-1))
                    low=f[i]
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["u20"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,hit=(x>0).mean()))
    out={}
    out["overall"]=summ(d)
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("yr").apply(summ)
    for col in ["f","rb","ma"]:
        d["q_"+col]=pd.qcut(d[col].rank(method="first"),4,labels=False)
        out["by_q_"+col]=d.groupby("q_"+col).apply(lambda g: pd.Series(dict(n=len(g),med=g[col].median(),u20=g.u20.mean(),t=g.u20.mean()/(g.u20.std()/np.sqrt(g.u20.count())),u5=g.u5.mean(),u40=g.u40.mean())))
    hz={}
    for h in ["u5","u10","u20","u40","u60"]:
        x=d[h].dropna(); hz[h]=dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))))
    out["horizons"]=pd.DataFrame(hz).T
    b=pd.DataFrame(base,columns=["coin","win","above","u"])
    out["baseline_above_sma"]=b.groupby("above")["u"].agg(["count","mean","std"])
    out["drift"]=pd.Series(drift); out["usual"]=pd.Series(usual)
    d["sgn"]=np.sign(d.u20)
    out["median_u20"]=d.u20.median()
    return out
