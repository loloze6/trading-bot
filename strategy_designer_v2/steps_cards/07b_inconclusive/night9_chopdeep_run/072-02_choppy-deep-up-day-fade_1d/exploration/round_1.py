def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r1.rolling(20,min_periods=20).std()
            depth=(c-hi)/hi/sd
            tr60=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":b["timestamp"].astype(str).str[:10],
                "r1":r1,"depth":depth,"tr60":tr60,"fc":b["forecast"].astype(float),
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    for h in [1,2,3,5]:
        D["x%d"%h]=np.nan
    # drift per coin over all windows, non-overlapping
    for h in [1,2,3,5]:
        m=D[D.pos%h==0].groupby("coin")["f%d"%h].mean()
        D["x%d"%h]=-(D["f%d"%h]-D.coin.map(m))
    ch=D[(D.tr60.abs()<=0.10)&D.depth.notna()&D.x1.notna()].copy()
    ch["up"]=ch.r1>0
    def tt(s,days):
        g=s.groupby(days).sum(); 
        return pd.Series({"mean%":s.mean()*100,"n":len(s),"days":g.size,"t":g.mean()/(g.std()/np.sqrt(len(g)))})
    res=[]
    for up in [True,False]:
        for h in [1,2,3,5]:
            s=ch[(ch.up==up)&(ch.pos%h==0)].dropna(subset=["x%d"%h])
            s=s[s.depth<0]
            q=pd.qcut(s.depth,3,labels=["deep","mid","shallow"])
            row={"up":up,"h":h}
            for k in ["deep","mid","shallow"]:
                ss=s[q==k]; row[k]=ss["x%d"%h].mean()*100
            a=tt(s["x%d"%h]*(-s.depth),s.day); row.update({"wt_t":a["t"],"n":a["n"]})
            row["deep_t"]=tt(s[q=="deep"]["x%d"%h],s[q=="deep"].day)["t"]
            res.append(row)
    out["by_side_horizon"]=pd.DataFrame(res)
    cs=ch[ch.depth<0]
    cs["q"]=pd.qcut(cs.depth,5,labels=False)
    out["quint_all_h1"]=cs.groupby("q").agg(depth=("depth","mean"),x1=("x1",lambda s:s.mean()*100),n=("x1","size"))
    cs["year"]=cs.day.str[:4]
    def g(s):
        return pd.Series({"x1_weighted":(s.x1*-s.depth).mean()*100,"deep_x1":s[s.q<=1].x1.mean()*100,"shallow_x1":s[s.q>=3].x1.mean()*100,"n":len(s)})
    out["by_coin"]=cs.groupby("coin").apply(g)
    out["by_window"]=cs.groupby("w").apply(g)
    out["by_upside"]=cs.groupby("up").apply(g)
    act=D[D.fc<0]
    out["active_check"]=pd.Series({"n":len(act),"x1":act.x1.mean()*100,"t":tt(act.x1*(-act.fc/10),act.day)["t"]})
    return out
