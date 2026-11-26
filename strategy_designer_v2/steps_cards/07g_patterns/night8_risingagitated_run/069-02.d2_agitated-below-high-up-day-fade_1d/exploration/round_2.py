def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change(); nxt=c.shift(-1)/c-1
            vol20=r1.rolling(20,min_periods=15).std()
            hh20=h.rolling(20,min_periods=15).max(); ll20=l.rolling(20,min_periods=15).min()
            r30=c/c.shift(30)-1
            df=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"r1":r1,"z1":r1/vol20,"nxt":nxt,
                "pos":(c-ll20)/(hh20-ll20),"r30":r30,"ag":(b["regime"]!="chop").astype(int),
                "alloc":b["postRebalance_current_allocation"],"vol20":vol20})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["ts"]=pd.to_datetime(d["ts"]); d["day"]=d["ts"].dt.floor("D"); d["yr"]=d["ts"].dt.year
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d=d.dropna(subset=["ex","z1","pos"])
    def stat(x):
        n=len(x); m=x["ex"].mean()
        se=np.sqrt((x.groupby("day")["ex"].apply(lambda v:(v-m).sum())**2).sum())/n
        return pd.Series({"n":n,"mean%":m*100,"t_cl":m/se if se>0 else np.nan})
    def slope(x,col):
        X=x[col].values; y=x["ex"].values; Xc=X-X.mean()
        b=(Xc*y).sum()/(Xc**2).sum(); e=y-y.mean()-b*Xc
        s=pd.Series(Xc*e).groupby(x["day"].values).sum()
        se=np.sqrt((s**2).sum())/(Xc**2).sum()
        return pd.Series({"n":len(x),"slope%":b*100,"t_cl":b/se})
    out={}
    a=d[d.ag==1].copy()
    out["ag_all_slope_z1"]=slope(a.assign(zc=a.z1.clip(-4,4)),"zc")
    out["calm_all_slope_z1"]=slope(d[d.ag==0].assign(zc=d[d.ag==0].z1.clip(-4,4)),"zc")
    up=a[a.r1>0].copy()
    out["ag_up_slope_z1"]=slope(up.assign(zc=up.z1.clip(0,4)),"zc")
    out["ag_up_slope_pos"]=slope(up,"pos")
    dn=a[a.r1<0].copy()
    out["ag_dn_slope_z1"]=slope(dn.assign(zc=dn.z1.clip(-4,0)),"zc")
    up["z1q"]=pd.qcut(up.z1,6,labels=False)
    out["ag_up_z1q"]=up.groupby("z1q").apply(stat)
    a["tr"]=pd.cut(a.r30,[-9,-0.07,0.07,99],labels=["fall","chop","rise"])
    a["up"]=(a.r1>0).astype(int)
    out["ag_trend_up"]=a.dropna(subset=["tr"]).groupby(["tr","up"]).apply(stat)
    out["ag_up_yr"]=a[a.up==1].groupby("yr").apply(stat)
    out["ag_up_w"]=a[a.up==1].groupby("w").apply(stat)
    out["ag_up_held"]=a[a.up==1].assign(h=(a.alloc<0).astype(int)).groupby("h").apply(stat)
    return out
