def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            r=pd.Series(c).pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            tr=pd.Series(c)/pd.Series(c).shift(60)-1
            n=len(c);h=5
            for t in range(0,n-h,h):
                rows.append((coin,w,t,b["timestamp"].iloc[t],b["regime"].iloc[t],z.iloc[t],tr.iloc[t],c[t+h]/c[t]-1))
    d=pd.DataFrame(rows,columns=["coin","w","t","ts","regime","z","tr","ret"])
    d["ex"]=d["ret"]-d.groupby("coin")["ret"].transform("mean")
    d["calm"]=d["regime"]!="chop"
    d["year"]=pd.to_datetime(d["ts"]).dt.year
    d["trend"]=np.where(d.tr>0.1,"rising",np.where(d.tr<-0.1,"falling","choppy"))
    d["kind"]=np.where(d.z<0,"down","up_or_flat")
    out={}
    def st(g):
        s=-g["ex"];n=len(s)
        return pd.Series({"n":n,"short_ex":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    cm=d[d.calm]
    out["calm_year_kind"]=cm.groupby(["year","kind"]).apply(st).reset_index()
    out["calm_trend_kind"]=cm.groupby(["trend","kind"]).apply(st).reset_index()
    # down minus all calm bars of same coin-window (removes window drift)
    cm=cm.copy()
    cm["wex"]=cm["ret"]-cm.groupby(["coin","w"])["ret"].transform("mean")
    dn=cm[cm.kind=="down"]
    s=-dn["wex"]
    out["down_vs_window_mean"]=pd.DataFrame({"n":[len(s)],"short_wex":[s.mean()],"t":[s.mean()/(s.std()/np.sqrt(len(s)))]})
    # graded: correlation of z with short ex within down days, by trend
    res=[]
    for tname,g in dn.groupby("trend"):
        rr,p=stats.spearmanr(-g["z"],-g["ex"])
        rr2,p2=stats.spearmanr(-g["z"],-g["wex"])
        res.append((tname,len(g),rr,p,rr2,p2))
    rr,p=stats.spearmanr(-dn["z"],-dn["ex"]);rr2,p2=stats.spearmanr(-dn["z"],-dn["wex"])
    res.append(("all",len(dn),rr,p,rr2,p2))
    out["grading_spearman"]=pd.DataFrame(res,columns=["trend","n","rho_ex","p","rho_wex","p_w"])
    return out
