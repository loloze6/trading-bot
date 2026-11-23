def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values; idx=np.arange(0,len(c)-24,24); g.append(c[idx+24]/c[idx]-1)
        g=np.concatenate(g); drift=np.nanmean(g); usual=np.nanstd(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True); c=b["close"]; ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=c.pct_change()
            r2=c/c.shift(2)-1; z=r2/r2.abs().rolling(720,min_periods=200).mean()
            r24p=c/c.shift(24)-1; z24=r24p/r24p.abs().rolling(720,min_periods=200).mean()
            volr=r1.abs().rolling(168,min_periods=100).mean()/r1.abs().rolling(1440,min_periods=500).mean()
            f24=c.shift(-24)/c-1; f1=c.shift(-1)/c-1
            pos=np.arange(len(b))
            d=pd.DataFrame({"coin":coin,"w":w,"pos":pos,"cell":pos//24,"hour":ts.dt.hour,"year":ts.dt.year,
               "z":z,"z24":z24,"volr":volr,"f24u":f24-drift,"f24s":(f24-drift)/usual,"f1":f1,
               "absz":z.abs()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"n":n})
    out={}
    # non-overlapping: in each 24-bar cell, the bar with the most negative z (known only ex post -> instead use grid bar pos%24==0)
    G=D[D.pos%24==0].copy()
    G["vq"]=G.groupby("coin")["volr"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    G["z24b"]=pd.cut(G.z24,[-99,-2,-1,0,1,2,99])
    out["grid_z24b_by_volq_fwd24u"]=G.groupby(["vq","z24b"],observed=True)["f24u"].apply(tt).unstack()
    out["grid_z24b_fwd24strength"]=G.groupby("z24b",observed=True)["f24s"].apply(tt).unstack()
    # graded: corr of -z24 with f24u within high vol
    H=G[G.vq==2].dropna(subset=["z24","f24u"])
    out["highvol_z24_slope"]=float(np.polyfit(H.z24.clip(-4,4),H.f24u,1)[0])
    out["highvol_z24_neg_by_year"]=G[(G.vq==2)&(G.z24<-1)].groupby("year")["f24u"].apply(tt).unstack()
    out["highvol_z24_neg_by_window_share_pos"]=float((G[(G.vq==2)&(G.z24<-1)].groupby("w")["f24u"].mean()>0).mean())
    out["lowvol_z24_neg_by_year"]=G[(G.vq==0)&(G.z24<-1)].groupby("year")["f24u"].apply(tt).unstack()
    # hour 20-21 return seasonality: per year, per coin share
    D["h2021"]=D.hour.isin([20,21])
    A=D[D.h2021]
    out["h20_21_f1_by_year"]=A.groupby("year")["f1"].apply(tt).unstack()
    out["h20_21_share_coins_pos"]=float((A.groupby("coin")["f1"].mean()>0).mean())
    out["h20_21_by_coin_t"]=A.groupby("coin")["f1"].apply(tt).unstack()["t"]
    # sum of 20+21 hours (2h return from 20:00 open) graded by volatility
    A2=D[D.hour==20].copy()
    c2=A2["f1"]  # one hour; also 2h via next
    A2["vq"]=pd.qcut(A2.volr,3,labels=False,duplicates="drop")
    out["h20_f1_by_volq"]=A2.groupby("vq")["f1"].apply(tt).unstack()
    out["h13_f1_by_year"]=D[D.hour==13].groupby("year")["f1"].apply(tt).unstack()
    return out
