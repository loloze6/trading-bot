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
            # 60d trend within window
            tr=pd.Series(c)/pd.Series(c).shift(60)-1
            n=len(c)
            for h in [1,2,3,5,10]:
                for t in range(0,n-h,h):
                    rows.append((coin,w,h,t,b["timestamp"].iloc[t],b["regime"].iloc[t],z.iloc[t],tr.iloc[t],c[t+h]/c[t]-1))
    d=pd.DataFrame(rows,columns=["coin","w","h","t","ts","regime","z","tr","ret"])
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["ex"]=d["ret"]-d["drift"]
    d["calm"]=d["regime"]!="chop"
    d["year"]=pd.to_datetime(d["ts"]).dt.year
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    out={}
    def stat(g):
        s=-g["ex"]  # short direction
        n=len(s)
        return pd.Series({"n":n,"mean_short_ex":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    dn=d[d.z<0].copy()
    dn["zb"]=pd.cut(dn.z,[-99,-2,-1.5,-1,-0.5,0])
    out["by_h_calm_zbin"]=dn[dn.calm].groupby(["h","zb"],observed=True).apply(stat).reset_index()
    out["by_h_agit_zbin"]=dn[~dn.calm].groupby(["h","zb"],observed=True).apply(stat).reset_index()
    # up days in calm (other side): continuation long
    up=d[(d.z>0)&d.calm].copy(); up["zb"]=pd.cut(up.z,[0,0.5,1,1.5,2,99])
    def statl(g):
        s=g["ex"];n=len(s);return pd.Series({"n":n,"mean_long_ex":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n))})
    out["calm_up_h5_zbin"]=up[up.h==5].groupby("zb",observed=True).apply(statl).reset_index()
    c5=dn[(dn.h==5)&dn.calm]
    out["calm_down_h5_by_coin"]=c5.groupby("coin").apply(stat).reset_index()
    out["calm_down_h5_by_year"]=c5.groupby("year").apply(stat).reset_index()
    c5=c5.copy(); c5["trend"]=np.where(c5.tr>0.1,"rising",np.where(c5.tr<-0.1,"falling","choppy"))
    out["calm_down_h5_by_trend"]=c5.groupby("trend").apply(stat).reset_index()
    out["calm_down_h5_trend_zbin"]=c5.groupby(["trend","zb"],observed=True).apply(stat).reset_index()
    return out
