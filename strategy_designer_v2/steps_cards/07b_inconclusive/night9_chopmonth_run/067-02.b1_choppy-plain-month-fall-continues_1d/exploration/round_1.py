def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=7
    bars=data["bars"]
    rows=[]; drift={}
    for coin,ws in bars.items():
        allr=[]
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            n=len(c)
            ts=pd.to_datetime(df["timestamp"])
            r30=pd.Series(c).pct_change(30).values
            r60=pd.Series(c).pct_change(60).values
            f=df["forecast"].values
            raw=df.get("debug_info.components.fall30.last_history_value")
            raw=raw.values if raw is not None else np.full(n,np.nan)
            for i in range(0,n-H,H):
                fr=c[i+H]/c[i]-1
                allr.append(fr)
                rows.append(dict(coin=coin,w=w,yr=ts[i].year,day=ts[i].normalize(),f=f[i],raw=raw[i],r30=r30[i],r60=r60[i],fr=fr,
                                 fr3=c[min(i+3,n-1)]/c[i]-1,fr14=(c[i+14]/c[i]-1) if i+14<n else np.nan,fr30=(c[i+30]/c[i]-1) if i+30<n else np.nan))
        drift[coin]=np.mean(allr)
    d=pd.DataFrame(rows)
    d["ex"]=d["fr"]-d["coin"].map(drift)
    s=d[d.f<0].copy()
    s["sx"]=-s["ex"]   # short-direction excess
    s["w_meas"]=-(s.f/10)*s.ex
    def ct(x,day):
        g=pd.DataFrame({"x":x-x.mean(),"d":day}).groupby("d").x.sum()
        D=len(g); se=np.sqrt((g**2).sum()*D/(D-1))/len(x)
        return x.mean()/se if se>0 else np.nan, D
    out={}
    t,D=ct(s.sx,s.day); tw,_=ct(s.w_meas,s.day)
    out["overall"]=pd.Series(dict(n=len(s),mean_sx=s.sx.mean(),t=t,days=D,weighted=s.w_meas.mean(),t_w=tw,
        share_raw30_pos=(s.r30>=0).mean(),mean_f=s.f.mean(),min_f=s.f.min()))
    s["q"]=pd.qcut(s.f.rank(method="first"),4,labels=["deepest","q2","q3","shallow"])
    out["by_f_quartile"]=s.groupby("q").agg(n=("sx","size"),f=("f","mean"),r30=("r30","mean"),sx=("sx","mean"),wm=("w_meas","mean"))
    s["r30pos"]=s.r30>=0
    out["by_r30sign"]=s.groupby("r30pos").agg(n=("sx","size"),sx=("sx","mean"),wm=("w_meas","mean"))
    s["r30b"]=pd.cut(s.r30,[-1,-0.2,-0.1,-0.05,0,0.05,1])
    out["by_r30bin"]=s.groupby("r30b").agg(n=("sx","size"),sx=("sx","mean"),sxmed=("sx","median"))
    out["by_coin"]=s.groupby("coin").agg(n=("sx","size"),sx=("sx","mean"),wm=("w_meas","mean"))
    out["by_window"]=s.groupby("w").agg(n=("sx","size"),sx=("sx","mean"),wm=("w_meas","mean"))
    out["by_year"]=s.groupby("yr").agg(n=("sx","size"),sx=("sx","mean"),wm=("w_meas","mean"))
    for h in ["fr3","fr14","fr30"]:
        x=-s[h].dropna()
        out["raw_short_"+h]=pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    # among all choppy grid cells (all r30), relation r30 vs fr
    ch=d[(d.r60.abs()<=0.10)].dropna(subset=["r30"])
    out["choppy_corr_r30_ex"]=pd.Series(dict(n=len(ch),spearman=stats.spearmanr(ch.r30,ch.ex)[0],
        neg_n=(ch.r30<0).sum(),neg_ex=ch[ch.r30<0].ex.mean(),pos_ex=ch[ch.r30>=0].ex.mean()))
    return out
