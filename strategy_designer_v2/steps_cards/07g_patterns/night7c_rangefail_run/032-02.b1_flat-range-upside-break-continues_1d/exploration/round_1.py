def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(b)
            er=(c-c.shift(60)).abs()/c.diff().abs().rolling(60).sum()
            ph=hi.shift(1).rolling(60).max(); pl=lo.shift(1).rolling(60).min()
            mr=(hi-lo).rolling(60).mean()
            up=((c-ph)/mr).clip(lower=0); dn=((pl-c)/mr).clip(lower=0)
            r1=c.pct_change()
            r5p=c/c.shift(5)-1
            vol20=r1.rolling(20).std()
            vol60=r1.rolling(60).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n,H):
                if i+H>=n: break
                rows.append(dict(coin=coin,w=w,er=er[i],up=up[i],dn=dn[i],r5p=r5p[i],
                    vr=vol20[i]/vol60[i] if vol60[i]>0 else np.nan,fwd=fwd[i],
                    fc=b["forecast"][i],reg=b["regime"][i],wd=ts[i].dayofweek))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["un"]=d["fwd"]-d["drift"]
    def summ(g):
        x=g["un"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["all"]=summ(d).to_frame().T
    dd=d.dropna(subset=["er"])
    dd["erb"]=pd.cut(dd["er"],[0,0.15,0.3,0.5,1.01])
    dd["side"]=np.where(dd["up"]>0,"up",np.where(dd["dn"]>0,"down","inside"))
    out["er_x_side"]=dd.groupby(["erb","side"]).apply(summ)
    upd=dd[dd["up"]>0].copy()
    upd["upb"]=pd.qcut(upd["up"],3,duplicates="drop")
    out["up_size"]=upd.groupby("upb").apply(summ)
    dnd=dd[dd["dn"]>0].copy()
    dnd["dnb"]=pd.qcut(dnd["dn"],3,duplicates="drop")
    out["down_size"]=dnd.groupby("dnb").apply(summ)
    # past 5d move quintiles, all bars
    e=d.dropna(subset=["r5p"]).copy()
    e["q"]=e.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["past5_quint"]=e.groupby("q").apply(summ)
    v=d.dropna(subset=["vr"]).copy()
    v["q"]=pd.qcut(v["vr"],5,labels=False)
    out["volratio_quint"]=v.groupby("q").apply(summ)
    out["weekday_grid"]=d.groupby("wd").apply(summ)
    out["by_coin_up_er"]=dd[(dd["up"]>0)].groupby(["coin",dd["er"]<=0.3]).apply(summ)
    out["by_window_up"]=dd[dd["up"]>0].groupby("w").apply(summ)
    return out
