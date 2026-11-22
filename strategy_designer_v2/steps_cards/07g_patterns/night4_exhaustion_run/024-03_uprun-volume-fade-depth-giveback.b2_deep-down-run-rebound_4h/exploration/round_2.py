import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=18
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            sd18=r.rolling(180,min_periods=45).std()*np.sqrt(H)
            past18=(c/c.shift(H)-1)/sd18
            volr=v.rolling(6).mean()/v.shift(6).rolling(36).mean()
            vlev=r.rolling(30).std()/r.rolling(180,min_periods=45).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for off in [0,6,12]:
                idx=np.arange(off,n,H)
                d=pd.DataFrame({"coin":coin,"w":w,"off":off,"fwd":fwd.values[idx],"past18":past18.values[idx],
                    "volr":volr.values[idx],"vlev":vlev.values[idx],"sd18":sd18.values[idx],
                    "wd":ts.dt.weekday.values[idx],"year":ts.dt.year.values[idx],"tkey":ts.values[idx]})
                rows.append(d)
    g=pd.concat(rows).dropna(subset=["fwd","past18","volr","vlev"])
    g["drift"]=g.groupby("coin")["fwd"].transform("mean")
    g["u"]=g["fwd"]-g["drift"]
    g["us"]=g["u"]/g["sd18"]
    g0=g[g.off==0].copy()
    out={}
    def tt(x): 
        x=x.dropna(); return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    # graded slopes, grid 0, and time-clustered (mean across coins per timestamp)
    res=[]
    for k in ["past18","volr","vlev"]:
        for gg,lab in [(g0,"grid0"),(g[g.off==6],"grid6"),(g[g.off==12],"grid12")]:
            x=gg[k].rank(pct=True); y=gg["us"]
            s=stats.linregress(x,y); res.append([k,lab,s.slope,s.slope/s.stderr,len(gg)])
    out["slopes_us_on_rank"]=pd.DataFrame(res,columns=["key","grid","slope","t","n"]).round(4)
    # multivariate on grid0
    X=np.column_stack([np.ones(len(g0)),g0["past18"].rank(pct=True),np.log(g0["volr"]).clip(-3,3),g0["vlev"]])
    y=g0["us"].values
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-4))
    out["multivar_grid0"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","past18rank","logvolr","vlev"]).round(4)
    # past18 top quintile, by year and by volume
    g0["pq"]=pd.qcut(g0["past18"].rank(method="first"),5,labels=False)
    top=g0[g0.pq==4]
    out["top_past18_by_year"]=top.groupby("year")["u"].apply(tt).unstack().round(4)
    g0["vq"]=pd.qcut(g0["volr"].rank(method="first"),3,labels=False)
    out["pq_x_volr_terc_mean_u"]=g0.pivot_table(index="pq",columns="vq",values="u",aggfunc="mean").round(4)
    # time-clustered: average over coins per timestamp for top quintile past18 and volr
    tc=top.groupby("tkey")["u"].mean(); out["top_past18_timeclustered"]=tt(tc).round(4)
    vt=g0[g0.volr>g0.volr.quantile(0.8)].groupby("tkey")["u"].mean(); out["top_volr_timeclustered"]=tt(vt).round(4)
    # Sunday from daily data: next 3 days coin return after each weekday's close, non-overlapping per weekday
    dl=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.reset_index(drop=True).copy()
            d["f3"]=d["close"].shift(-3)/d["close"]-1; d["f1"]=d["close"].shift(-1)/d["close"]-1
            d["wd"]=pd.to_datetime(d["day"]).dt.weekday; d["coin"]=coin
            d["year"]=pd.to_datetime(d["day"]).dt.year
            dl.append(d)
    D=pd.concat(dl).dropna(subset=["f1"])
    D["u1"]=D["f1"]-D.groupby("coin")["f1"].transform("mean")
    out["next_day_u_by_weekday_of_close"]=D.groupby("wd")["u1"].apply(tt).unstack().round(5)
    out["grid_wd_by_year_sun"]=g0[g0.wd==6].groupby("year")["u"].mean().round(4)
    out["book_day_by_year"]=D.groupby("year")[["book_return","coin_return"]].mean().round(5)
    return out
