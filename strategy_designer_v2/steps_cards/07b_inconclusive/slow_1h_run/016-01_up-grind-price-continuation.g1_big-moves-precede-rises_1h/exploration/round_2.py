def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hr=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values.astype(float); f=b["forecast"].values.astype(float)
            al=b["postRebalance_current_allocation"].values.astype(float)
            n=len(c)
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            fee=(b["total_portfolio_value"].values-b["postRebalance_total_value"].values)/b["total_portfolio_value"].values
            hr.append(pd.DataFrame({"coin":coin,"f":f,"al":al,"g":al*nxt,"r1":nxt,"fee":fee}))
            for i in range(0,n,H):
                past=c[i]/c[i-H]-1 if i>=H else np.nan
                d={"coin":coin,"f":f[i],"past":past,"al":al[i]}
                for h in [12,24,48,72]:
                    d["r%d"%h]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(d)
    d=pd.DataFrame(rows)
    for h in [12,24,48,72]:
        d["x%d"%h]=d["r%d"%h]-d.groupby("coin")["r%d"%h].transform("mean")
    d["side"]=np.where(d["past"]>0,"up","down")
    d["q"]=pd.qcut(d["f"].rank(method="first"),5,labels=False)
    def sl(g,y,x="f"):
        g=g.dropna(subset=[x,y]); r=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["side_by_h"]=pd.DataFrame({(s,h):sl(d[d.side==s],"x%d"%h) for s in ["up","down"] for h in [12,24,48,72]}).T
    out["alloc_by_q"]=d.groupby("q").agg(f=("f","mean"),al=("al","mean"),x72=("x72","mean"),x24=("x24","mean"))
    H_=pd.concat(hr).dropna(subset=["r1"])
    H_["q"]=pd.qcut(H_["f"].rank(method="first"),5,labels=False)
    H_["mu"]=H_.groupby("coin")["r1"].transform("mean")
    H_["tim"]=H_["al"]*(H_["r1"]-H_["mu"])
    out["hourly_by_q"]=H_.groupby("q").agg(f=("f","mean"),al=("al","mean"),gain_sum=("g","sum"),timing_sum=("tim","sum"),xr1=("r1",lambda s: (s-H_.loc[s.index,"mu"]).mean()*72))
    out["fees_total_vs_gain"]=pd.Series({"gross_gain_sum":H_["g"].sum(),"timing_sum":H_["tim"].sum(),"fee_sum":H_["fee"].sum()})
    # convexity: excess return in top decile vs rest
    d["dec"]=pd.qcut(d["f"].rank(method="first"),10,labels=False)
    out["decile_x72"]=d.groupby("dec").agg(n=("f","size"),f=("f","mean"),x72=("x72","mean"),x24=("x24","mean"))
    top=d[d.dec==9]["x72"].dropna(); rest=d[d.dec<9]["x72"].dropna()
    out["top_vs_rest_t"]=stats.ttest_ind(top,rest,equal_var=False).statistic
    return out
