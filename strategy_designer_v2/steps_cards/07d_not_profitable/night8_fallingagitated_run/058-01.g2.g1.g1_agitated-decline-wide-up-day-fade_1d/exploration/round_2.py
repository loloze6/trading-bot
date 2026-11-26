def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days=data["days"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            prev=np.r_[np.nan,cl[1:]/cl[:-1]-1]
            prev2=np.r_[np.nan,np.nan,cl[1:-1]/cl[:-2]-1]
            sd30=pd.Series(prev).rolling(30,min_periods=20).std().values
            rng=(b["high"]-b["low"]).values/cl
            r5p=np.r_[[np.nan]*5,cl[5:]/cl[:-5]-1]
            r60=np.r_[[np.nan]*60,cl[60:]/cl[:-60]-1]
            up=(prev>0).astype(int); st=np.zeros(len(b)); s=0
            for i in range(len(b)):
                s=s+1 if up[i] else 0; st[i]=s
            pos=b["postRebalance_current_allocation"].values
            gain=pos*r1
            rows.append(pd.DataFrame({"coin":c,"w":w,"day":b["timestamp"].astype(str).str[:10],
              "regime":b["regime"].values,"fc":b["forecast"].values,"r1":r1,"prev":prev,"prev2_sd":prev2/sd30,
              "rng_sd":rng/sd30,"r5p_sd":r5p/sd30,"st":st,"sd30":sd30,"r60":r60,"gain":gain,"alloc":pos}))
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean(); D["mu"]=D.coin.map(mu)
    D["u1"]=-(D.r1-D.mu)
    def summ(g,col="u1"):
        x=g[col].dropna()
        if len(x)<3: return pd.Series({"n":len(x),"mean%":100*x.mean() if len(x) else np.nan,"t":np.nan})
        dd=g.assign(dev=g[col]-x.mean()).groupby("day")["dev"].sum()
        se=np.sqrt(len(dd)/(len(dd)-1)*(dd**2).sum())/len(x)
        return pd.Series({"n":len(x),"days":g.day.nunique(),"mean%":100*x.mean(),"t_day":x.mean()/se,"hit":(x>0).mean()})
    out={}
    cases=D[(D.fc<0)&D.r1.notna()].copy()
    cases["first"]=np.where(cases.st==1,"first_up","later_up")
    out["first_vs_later"]=cases.groupby("first").apply(summ)
    out["book_gain_by_first_bp"]=cases.groupby("first")["gain"].agg(lambda x:1e4*x.sum())
    f=cases[cases.st==1].copy()
    f["rq"]=pd.qcut(f.rng_sd,3,labels=False)
    out["first_up_by_range_tercile"]=f.groupby("rq").apply(summ)
    f["pq"]=pd.qcut(f.prev2_sd,3,labels=False)
    out["first_up_by_prior_down_size_tercile"]=f.groupby("pq").apply(summ)
    l=cases[cases.st>=2].copy(); l["rq"]=pd.qcut(l.rng_sd,3,labels=False)
    out["later_up_by_range_tercile"]=l.groupby("rq").apply(summ)
    # control: first up day outside profile (condition without the profile signal)
    valid=D[D.r1.notna()&D.sd30.notna()]
    out["first_up_outside_profile"]=summ(valid[(valid.regime=="chop")&(valid.st==1)])
    out["later_up_outside_profile"]=summ(valid[(valid.regime=="chop")&(valid.st>=2)])
    out["all_up_outside_profile"]=summ(valid[(valid.regime=="chop")&(valid.st>=1)])
    # big losses: what precedes
    big=cases[cases.u1<-0.05]
    out["bigloss_profile"]=pd.DataFrame({"bigloss":big[["st","rng_sd","r5p_sd","prev2_sd"]].median(),"all":cases[["st","rng_sd","r5p_sd","prev2_sd"]].median()})
    out["bigloss_share_by_first"]=cases.assign(b=cases.u1<-0.05).groupby("first")["b"].mean()
    # 5-day past return terciles
    cases["r5q"]=pd.qcut(cases.r5p_sd,3,labels=False)
    out["by_5dpast_tercile"]=cases.groupby(["first","r5q"]).apply(summ)
    # deeper decline: r60
    cases["r60q"]=pd.qcut(cases.r60,3,labels=False)
    out["by_r60_tercile"]=cases.groupby("r60q").apply(summ)
    # simulated first-up-only book vs all, total gain sum and worst single gains
    out["gain_tail"]=pd.Series({"first_min_gain%":100*f.gain.min(),"later_min_gain%":100*l.gain.min(),
        "first_sum%":100*f.gain.sum(),"later_sum%":100*l.gain.sum()})
    return out
