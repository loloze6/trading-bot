def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        g=[]
        for w,df in wins.items():
            c=df["close"].values
            if len(c)>3: g.extend(list(c[3::3]/c[:-3:3]-1))
        m3=np.mean(g)
        for w,df in wins.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["wd"]=d["ts"].dt.weekday; d["year"]=d["ts"].dt.year
            d["date"]=d["ts"].dt.floor("D")
            d["r1"]=d["close"].pct_change()
            mu=d["r1"].rolling(60,min_periods=20).mean(); sd=d["r1"].rolling(60,min_periods=20).std()
            d["z"]=(d["r1"]-mu)/sd
            d["ex3"]=d["close"].shift(-3)/d["close"]-1-m3
            d["ex1"]=d["close"].shift(-1)/d["close"]-1
            d["ex2"]=d["close"].shift(-2)/d["close"]-1
            d["coin"]=coin; d["win"]=w
            rows.append(d[["coin","win","wd","year","date","z","ex3","ex1","ex2"]])
    A=pd.concat(rows).dropna(subset=["z","ex3"])
    out={}
    def tt(x):
        x=np.asarray(x,dtype=float); x=x[~np.isnan(x)]
        if len(x)<3: return pd.Series({"n":len(x),"mean%":np.nan,"t":np.nan})
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))})
    # date-clustered: per date, mean over coins of (-z clipped)*ex3 ; t over dates
    res=[]
    for wd in range(7):
        s=A[A.wd==wd].copy()
        s["fall"]=(-s.z).clip(lower=0); s["rise"]=s.z.clip(lower=0)
        s["pf"]=s.fall*s.ex3; s["pr"]=-s.rise*s.ex3
        pdf=s.groupby("date")[["pf","pr"]].mean()
        a=tt(pdf.pf); b=tt(pdf.pr)
        res.append({"wd":wd,"n_dates":a["n"],"fall_x_ex3_%":a["mean%"],"t_fall_clust":a["t"],
                    "rise_x_minusex3_%":b["mean%"],"t_rise_clust":b["t"]})
    out["clustered_by_weekday"]=pd.DataFrame(res).round(3)
    # graded bins of z for Thu, Fri, Sun, Mon
    bins=[-99,-2,-1,-0.5,0,0.5,1,2,99]
    for wd,name in [(3,"thu"),(4,"fri"),(6,"sun"),(0,"mon")]:
        s=A[A.wd==wd].copy(); s["zb"]=pd.cut(s.z,bins)
        out[f"{name}_zbins_ex3"]=s.groupby("zb",observed=True)["ex3"].apply(tt).unstack().round(3)
    # by year, date-clustered fall product for thu, fri
    for wd,name in [(3,"thu"),(4,"fri")]:
        s=A[A.wd==wd].copy(); s["pf"]=(-s.z).clip(lower=0)*s.ex3
        pdf=s.groupby(["year","date"])["pf"].mean().reset_index()
        out[f"{name}_fall_by_year_clust"]=pdf.groupby("year")["pf"].apply(tt).unstack().round(3)
    # path: Thu fall -> which day carries rebound (ex1,ex2,ex3 raw)
    s=A[(A.wd==3)&(A.z<=-1)]
    out["thu_fall_path%"]=(s[["ex1","ex2"]].mean()*100).round(3)
    s=A[(A.wd==4)&(A.z<=-1)]
    out["fri_fall_path%"]=(s[["ex1","ex2"]].mean()*100).round(3)
    return out
