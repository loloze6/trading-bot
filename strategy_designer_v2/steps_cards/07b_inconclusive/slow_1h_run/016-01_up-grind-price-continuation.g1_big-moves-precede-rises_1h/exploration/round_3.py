def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hr=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].to_numpy(dtype=float); f=b["forecast"].to_numpy(dtype=float)
            al=b["postRebalance_current_allocation"].to_numpy(dtype=float)
            vol=b["sizing_realised_vol"].to_numpy(dtype=float)
            n=len(c)
            nxt=np.full(n,np.nan); nxt[:-1]=c[1:]/c[:-1]-1
            hr.append(pd.DataFrame({"coin":coin,"f":f,"al":al,"r1":nxt}))
            for i in range(0,n,H):
                d={"coin":coin,"f":f[i],"al":al[i],"vol":vol[i],
                   "past":(c[i]/c[i-H]-1) if i>=H else np.nan}
                for h in [24,48,72]:
                    d["r%d"%h]=(c[i+h]/c[i]-1) if i+h<n else np.nan
                rows.append(d)
    d=pd.DataFrame(rows)
    for h in [24,48,72]:
        d["x%d"%h]=d["r%d"%h]-d.groupby("coin")["r%d"%h].transform("mean")
    d["side"]=np.where(d["past"]>0,"up","down")
    d["q"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    out={}
    out["q_alloc"]=d.groupby("q").agg(n=("f","size"),f=("f","mean"),al=("al","mean"),vol=("vol","mean"),x24=("x24","mean"),x72=("x72","mean"))
    def sl(g,y):
        g=g.dropna(subset=["f",y]); r=stats.linregress(g["f"],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out["side_h"]=pd.DataFrame({s+"_"+h:sl(d[d.side==s],"x"+h) for s in ["up","down"] for h in ["24","48","72"]}).T
    d["dec"]=pd.qcut(d["f"].rank(method="first"),10,labels=False)
    top=d.loc[d.dec==9,"x72"].dropna(); rest=d.loc[d.dec<9,"x72"].dropna()
    out["top_dec_vs_rest"]=pd.Series({"n_top":len(top),"top":top.mean(),"rest":rest.mean(),"t":stats.ttest_ind(top,rest,equal_var=False).statistic})
    A=pd.concat(hr).dropna(subset=["r1","al","f"])
    A["mu"]=A.groupby("coin")["r1"].transform("mean")
    A["tim"]=A["al"]*(A["r1"]-A["mu"])
    A["mkt"]=A["al"]*A["mu"]
    A["q"]=pd.qcut(A["f"].rank(method="first"),5,labels=False)
    out["hourly_q"]=A.groupby("q").agg(f=("f","mean"),al=("al","mean"),timing_sum=("tim","sum"),mkt_sum=("mkt","sum"))
    return out
