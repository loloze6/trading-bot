def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r.rolling(20,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "r":r,"depth":(hi-c)/hi/sd,"tr60":(c/c.shift(60)-1)*100,"fc":b["forecast"].astype(float)})
            for h in [1,3,5]:
                d[f"f{h}"]=c.shift(-h)/c-1
            d["i"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,3,5]:
        D[f"x{h}"]=D[f"f{h}"]-D.groupby("coin")["f1"].transform("mean")*h
    out={}
    def tt(s,col):
        s=s.dropna(subset=[col,"depth"])
        if len(s)<30: return [np.nan]*5
        q=pd.qcut(s["depth"].rank(method="first"),3,labels=["sh","mid","deep"])
        a=s.loc[q=="deep",col]; bb=s.loc[q=="sh",col]
        return [bb.mean(),s.loc[q=="mid",col].mean(),a.mean(),stats.ttest_ind(a,bb,equal_var=False).statistic,len(s)]
    cols=["shallow","mid","deep","t","n"]
    ch=D[D.tr60.abs()<=10]
    res={}
    for h in [1,3,5]:
        g=ch[ch.i%h==0]
        res[f"all_h{h}"]=tt(g,f"x{h}")
        res[f"up_h{h}"]=tt(g[g.r>0],f"x{h}")
        res[f"down_h{h}"]=tt(g[g.r<=0],f"x{h}")
        res[f"active_h{h}"]=tt(g[g.fc<0],f"x{h}")
    out["choppy_grid"]=pd.DataFrame(res,index=cols).T
    res={}
    for y,g in ch.groupby("year"):
        res[f"all_{y}"]=tt(g,"x1"); res[f"up_{y}"]=tt(g[g.r>0],"x1")
    out["choppy_by_year_h1"]=pd.DataFrame(res,index=cols).T
    # by coin, all choppy days h1
    res={}
    for cn,g in ch.groupby("coin"):
        res[cn]=tt(g,"x1")
    out["choppy_all_by_coin_h1"]=pd.DataFrame(res,index=cols).T
    # depth deciles on choppy all days h1
    s=ch.dropna(subset=["x1","depth"])
    q=pd.qcut(s.depth.rank(method="first"),5,labels=False)
    out["choppy_all_quintiles_h1"]=s.groupby(q)["x1"].agg(["mean","count"])
    sp=stats.spearmanr(s.depth,s.x1)
    out["choppy_all_spearman"]=f"rho {sp.correlation:.4f} p {sp.pvalue:.4f} n {len(s)}"
    return out
