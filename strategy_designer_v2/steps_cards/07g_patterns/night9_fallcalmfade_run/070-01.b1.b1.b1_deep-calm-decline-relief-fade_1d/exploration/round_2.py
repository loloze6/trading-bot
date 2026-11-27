def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[r[1:], np.nan]
            n2=np.r_[c[2:]/c[:-2]-1, np.nan, np.nan]
            n2=np.r_[n2[1:],np.nan]  # close[t+2]/close[t]-1
            n2=np.array([c[t+2]/c[t]-1 if t+2<n else np.nan for t in range(n)])
            ar=pd.Series(np.abs(r)).rolling(30,min_periods=20).mean().shift(1).values
            tr60=np.array([c[t]/c[t-60]-1 if t>=60 else np.nan for t in range(n)])
            ts=pd.to_datetime(b["timestamp"])
            for t in range(2,n):
                k=0; loss=0.0; j=t-1
                while j>=1 and r[j]<0:
                    k+=1; loss+=-r[j]; j-=1
                ku=0; gain=0.0; j=t-1
                while j>=1 and r[j]>0:
                    ku+=1; gain+=r[j]; j-=1
                rows.append(dict(coin=coin,w=w,t=t,day=ts[t].normalize(),yr=ts[t].year,
                    r=r[t],nxt=nxt[t],n2=n2[t],usual=ar[t],downloss=loss,upgain=gain,upk=ku,
                    tr60=tr60[t],regime=b["regime"].iloc[t]))
    d=pd.DataFrame(rows).dropna(subset=["nxt","r","usual"])
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d["ex2"]=d["n2"]-d.groupby("coin")["n2"].transform("mean")
    d["prof"]=np.where(d["regime"]=="chop","outside","fallcalm")
    d["trend"]=pd.cut(d["tr60"],[-10,-0.10,0.10,100],labels=["falling","choppy","rising"])
    d["zr"]=d["r"]/d["usual"]
    d["depth"]=d["downloss"]/d["usual"]
    d["gain_u"]=d["upgain"]/d["usual"]
    def summ(g,col="ex"):
        g=g.dropna(subset=[col])
        dd=g.groupby("day")[col].sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        return pd.Series(dict(n=len(g),days=len(dd),mean=g[col].mean(),t_day=t))
    out={}
    # pullback after up-run, outside profile, by trend
    dn=d[(d["r"]<0)&(d["prof"]=="outside")].copy()
    dn["gbin"]=pd.cut(dn["gain_u"],[-0.01,0.001,2,100],labels=["none","0-2","2+"])
    out["pullback_after_uprun_outside_by_trend"]=dn.groupby(["trend","gbin"]).apply(summ)
    out["pullback_2d"]=dn.groupby(["trend","gbin"]).apply(lambda g: summ(g,"ex2"))
    out["pullback_2plus_by_year"]=dn[dn["gbin"]=="2+"].groupby("yr").apply(summ)
    # graded slope within pullback with gain>0
    g=dn[dn["gain_u"]>0].dropna(subset=["ex"])
    s=stats.linregress(g["gain_u"].clip(upper=10),g["ex"])
    out["pullback_slope_gain"]=pd.Series(dict(slope=s.slope,t=s.slope/s.stderr,n=len(g)))
    # large up day fade in fallcalm, no prior down run vs with
    up=d[(d["r"]>0)&(d["prof"]=="fallcalm")].copy()
    up["zbin"]=pd.cut(up["zr"],[0,1,2,100])
    up["run"]=np.where(up["depth"]>0.001,"after_downrun","no_downrun")
    out["fallcalm_upday_by_size_run"]=up.groupby(["run","zbin"]).apply(summ)
    gg=up.dropna(subset=["ex"])
    m=np.c_[np.ones(len(gg)),gg["zr"].clip(upper=8),gg["depth"].clip(upper=10)]
    beta,res,_,_=np.linalg.lstsq(m,gg["ex"].values,rcond=None)
    e=gg["ex"].values-m@beta
    cov=np.linalg.inv(m.T@m)*(e@e/(len(e)-3))
    out["fallcalm_upday_ols_z_depth"]=pd.DataFrame(dict(beta=beta,t=beta/np.sqrt(np.diag(cov))),index=["c","zr","depth"])
    # deep run fade by year and 2-day
    deep=up[up["depth"]>=3]
    out["deep_fade_by_year"]=deep.groupby("yr").apply(summ)
    out["deep_fade_2d"]=summ(deep,"ex2")
    # same situation outside profile by trend
    uo=d[(d["r"]>0)&(d["prof"]=="outside")&(d["depth"]>=3)]
    out["deep_relief_outside_by_trend"]=uo.groupby("trend").apply(summ)
    return out
