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
            tr60=(c/c.shift(60)-1)*100
            f=b["forecast"].values; n=len(b)
            for h in H:
                for g in range(0,n,h):
                    for i in range(g,min(g+h,n)):
                        if f[i]<=-2:
                            if i+h<n:
                                rows.append(dict(h=h,coin=coin,w=w,fc=f[i],depth=depth.iloc[i],tr60=tr60.iloc[i],
                                    day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                                    x=-(c.iloc[i+h]/c.iloc[i]-1-drift[(coin,h)])))
                            break
    df=pd.DataFrame(rows)
    def dayt(x):
        x=x.dropna(subset=["x"])
        D=x["day"].nunique(); m=x["x"].mean()
        dev=x.assign(dv=x["x"]-m).groupby("day")["dv"].sum()
        se=np.sqrt((dev**2).sum()*D/(D-1))/len(x) if D>1 else np.nan
        return pd.Series({"mean":m,"t_day":m/se,"n":len(x),"days":D})
    res={}
    for h in H:
        d=df[df.h==h].copy()
        res[f"all_h{h}"]=dayt(d)
        med=d.fc.abs().median()
        res[f"fc_split_h{h}"]=pd.DataFrame({"hi":dayt(d[d.fc.abs()>med]),"lo":dayt(d[d.fc.abs()<=med])})
        d["dq"]=pd.qcut(d.depth,4,labels=False)
        res[f"depthq_h{h}"]=d.groupby("dq").apply(dayt)
        d["tq"]=pd.cut(d.tr60,[-100,-5,0,5,100])
        res[f"trend_h{h}"]=d.groupby("tq").apply(dayt)
        x=d.dropna(subset=["depth","x"])
        res[f"spearman_depth_h{h}"]=pd.Series(stats.spearmanr(-x.depth,x.x),index=["rho","p"])
        res[f"window_pos_share_h{h}"]=float((d.groupby("w")["x"].mean()>0).mean())
    return res
