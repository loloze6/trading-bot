def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift={}
    H=[5,10]
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=np.mean(rs)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            hi=c.shift(1).rolling(20).max()
            sd=r.rolling(20).std()
            depth=(c/hi-1)/sd
            vol30=r.rolling(30).std()
            volmed=vol30.rolling(365,min_periods=60).median()
            agit=(vol30>volmed)
            f=b["forecast"].values; n=len(b)
            for g in range(0,n,5):
                for i in range(g,min(g+5,n)):
                    if f[i]<=-2:
                        d=dict(coin=coin,w=w,fc=f[i],depth=depth.iloc[i],
                               agit=("agitated" if agit.iloc[i] else "calm") if not np.isnan(volmed.iloc[i]) else "na",
                               day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()))
                        for h in H:
                            if i+h<n:
                                d[f"x{h}"]=-(c.iloc[i+h]/c.iloc[i]-1-drift[(coin,h)])
                        rows.append(d); break
    df=pd.DataFrame(rows)
    def dayt(g,col="x5"):
        x=g.dropna(subset=[col])
        s=x.groupby("day")[col].sum(); cnt=x.groupby("day")[col].size()
        D=len(s); m=x[col].mean()
        dev=x.assign(dv=x[col]-m).groupby("day")["dv"].sum()
        se=np.sqrt((dev**2).sum()*D/(D-1))/len(x) if D>1 else np.nan
        return pd.Series({"mean":m,"t_day":m/se if se else np.nan,"n":len(x),"days":D})
    res={}
    res["all"]=dayt(df)
    med=df["fc"].abs().median()
    res["fc_hi_minus_lo"]=pd.DataFrame({"hi":dayt(df[df.fc.abs()>med]),"lo":dayt(df[df.fc.abs()<=med])})
    dmed=df["depth"].median()
    res["depth_deep_vs_shallow"]=pd.DataFrame({"deep":dayt(df[df.depth<dmed]),"shallow":dayt(df[df.depth>=dmed])})
    res["depth_deep_vs_shallow_x10"]=pd.DataFrame({"deep":dayt(df[df.depth<dmed],"x10"),"shallow":dayt(df[df.depth>=dmed],"x10")})
    x=df.dropna(subset=["x5","depth"])
    res["spearman_depth_x5"]=pd.Series(stats.spearmanr(-x.depth,x.x5),index=["rho","p"])
    res["spearman_absfc_x5"]=pd.Series(stats.spearmanr(x.fc.abs(),x.x5),index=["rho","p"])
    res["agit"]=df.groupby("agit").apply(dayt)
    df["dq"]=pd.qcut(df["depth"],4,labels=False)
    res["agit_x_deep"]=df.groupby(["agit","dq"]).apply(dayt)
    res["x10_all"]=dayt(df,"x10")
    df["db"]=pd.cut(df["depth"],[-99,-6,-4.5,-3.5,-2.5,0])
    res["depth_bins"]=df.groupby("db").apply(dayt)
    return res
