import pandas as pd, numpy as np
from scipy import stats

def agg(x):
    x=x.dropna(); n=len(x); m=x.mean(); s=x.std()
    return pd.Series({"n":n,"mean_bp":m*1e4,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            typ=r1.abs().shift(1).rolling(720,min_periods=200).mean()
            vr=b["volume"]/b["volume"].shift(1).rolling(720,min_periods=200).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"year":ts.dt.year,
                "wd":ts.dt.weekday,"f1":c.shift(-1)/c-1,"f6":c.shift(-6)/c-1,
                "z":r1/typ,"vr":vr,"r6p":c/c.shift(6)-1,"typ":typ,
                "alloc":b["postRebalance_current_allocation"]})
            df["grid"]=(np.arange(len(df))%6==0)
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["u1"]=d["f1"]-d["coin"].map(d.groupby("coin")["f1"].mean())
    d["hb"]=np.where(d.hour.isin([20,21]),"h20_21",np.where(d.hour.isin([0,1,2]),"h0_2","other"))
    hc=d.groupby(["hb","coin"])["u1"].apply(agg).unstack()
    hy=d[d.hb=="h20_21"].groupby("year")["u1"].apply(agg).unstack()
    hy2=d[d.hb=="h0_2"].groupby("year")["u1"].apply(agg).unstack()
    # window consistency: share of windows with positive mean in h20_21
    wm=d[d.hb=="h20_21"].groupby(["coin","w"])["u1"].mean()
    wshare=pd.Series({"share_pos":(wm>0).mean(),"n_windows":len(wm),
                      "t_over_windows":wm.mean()/(wm.std()/np.sqrt(len(wm)))})
    # h20_21 by weekday
    hwd=d[d.hb=="h20_21"].groupby("wd")["u1"].apply(agg).unstack()
    # h20_21 graded by prior 6h return? sign-conditioned
    s=d[d.hb=="h20_21"].dropna(subset=["r6p","typ"]).copy()
    s["q"]=s.groupby("coin")["r6p"].transform(lambda x: pd.qcut(x,5,labels=False))
    hq=s.groupby("q")["u1"].apply(agg).unstack()
    # low-volume dips: grid, z<-1.5, by vr bins, by coin
    g=d[d.grid].dropna(subset=["f6","z","vr"]).copy()
    g["u6"]=g["f6"]-g["coin"].map(g.groupby("coin")["f6"].mean())
    dip=g[g.z<-1.5].copy()
    dip["vb"]=pd.cut(dip["vr"],[0,0.5,0.67,0.9,1.2,1.5,3,999])
    dv=dip.groupby("vb",observed=True)["u6"].apply(agg).unstack()
    dlow=dip[dip.vr<0.67]
    dlc=dlow.groupby("coin")["u6"].apply(agg).unstack()
    dly=dlow.groupby("year")["u6"].apply(agg).unstack()
    # book: when allocation>0, gain by hour
    d["pg"]=d["alloc"]*d["f1"]
    bh=d.groupby("hb")["pg"].apply(agg).unstack()
    return {"u1 hourblock x coin":hc,"h20_21 by year":hy,"h0_2 by year":hy2,
            "h20_21 window consistency":wshare,"h20_21 by weekday":hwd,
            "h20_21 by prior6h quintile":hq,"dip u6 by vol ratio":dv,
            "lowvol dip by coin":dlc,"lowvol dip by year":dly,"position gain by hourblock":bh}
