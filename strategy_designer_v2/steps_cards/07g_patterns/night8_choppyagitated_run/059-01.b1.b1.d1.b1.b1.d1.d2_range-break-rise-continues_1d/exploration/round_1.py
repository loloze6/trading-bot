def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(c)
            r1=c.pct_change()
            r7=c/c.shift(7)-1
            sc=r7/(r7.abs().rolling(30).mean())
            hi=c.rolling(30).max()
            dist=(hi/c-1)
            r60=c/c.shift(60)-1
            vol30=r1.rolling(30).std()
            vol7=r1.rolling(7).std()
            fwd=c.shift(-14)/c-1
            for i in range(0,n,14):
                if i+14>=n: break
                rows.append(dict(coin=coin,w=w,fwd=fwd[i],sc=sc[i],dist=dist[i],r60=r60[i],
                                 vratio=vol7[i]/vol30[i] if vol30[i] else np.nan,
                                 reg=b["regime"][i],fc=b["forecast"][i],
                                 wd=pd.Timestamp(b["timestamp"][i]).weekday(),
                                 r1=r1[i],year=pd.Timestamp(b["timestamp"][i]).year))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def agg(g):
        x=g["ex"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out["by_regime"]=d.groupby("reg").apply(agg)
    d["inprof"]=d["reg"]=="unknown"
    out["fc_pos_vs_zero_inprof"]=d[d.inprof].groupby(d["fc"]>0).apply(agg)
    for col in ["sc","dist","r60","vratio","r1"]:
        q=d.dropna(subset=[col]).copy()
        q["b"]=pd.qcut(q[col],5,labels=False,duplicates="drop")
        out["all_"+col]=q.groupby("b").apply(agg)
        qq=q[q.inprof].copy()
        if len(qq)>50:
            qq["b"]=pd.qcut(qq[col],3,labels=False,duplicates="drop")
            out["inprof_"+col]=qq.groupby("b").apply(agg)
    out["weekday"]=d.groupby("wd").apply(agg)
    # out of profile: sc quintile among chop
    q=d[~d.inprof].dropna(subset=["sc"]).copy()
    q["b"]=pd.qcut(q["sc"],5,labels=False)
    out["outprof_sc"]=q.groupby("b").apply(agg)
    # book daily: largest gains/losses context
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dl.append(dd.assign(coin=coin,w=w))
    D=pd.concat(dl)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","std","count"])
    return out
