def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        # coin mean per horizon over all visible windows
        for h in [1,3,5,10]:
            pass
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            r1=pd.Series(c).pct_change().values
            sd30=pd.Series(r1).rolling(30).std().values
            raw=r1/sd30
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for h in [1,3,5,10]:
                for i in range(0,len(b)-h,h):
                    rows.append(dict(coin=coin,win=w,h=h,i=i,year=yr[i],
                        day=str(b["timestamp"].iloc[i])[:10],
                        fwd=c[i+h]/c[i]-1,fc=b["forecast"].iloc[i],
                        reg=b["regime"].iloc[i],raw=raw[i]))
    df=pd.DataFrame(rows)
    df["mu"]=df.groupby(["coin","h"])["fwd"].transform("mean")
    df["ex"]=df["fwd"]-df["mu"]
    out={}
    def tstat(s):
        s=s.dropna()
        return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))
    def slope(g):
        g=g.dropna(subset=["ex","fc"])
        if len(g)<5: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g["fc"],g["ex"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    pos=df[df.fc>0]
    out["slope_by_h_pos"]=pos.groupby("h").apply(slope)
    out["mean_ex_by_h_pos"]=pos.groupby("h")["ex"].apply(tstat).unstack()
    p5=pos[pos.h==5]
    out["h5_by_coin"]=p5.groupby("coin")["ex"].apply(tstat).unstack()
    out["h5_slope_by_coin"]=p5.groupby("coin").apply(slope)
    out["h5_by_year"]=p5.groupby("year")["ex"].apply(tstat).unstack()
    p5=p5.copy(); p5["q"]=pd.qcut(p5["fc"],4,labels=False,duplicates="drop")
    out["h5_by_fc_quartile"]=p5.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"))
    # in-profile, all grid days, by raw scaled day move (both sides)
    inp=df[(df.reg=="unknown")&(df.h==5)].copy()
    inp["rb"]=pd.cut(inp["raw"],[-99,-1.5,-0.5,0.5,1.5,99])
    out["inprof_h5_by_raw"]=inp.groupby("rb")["ex"].apply(tstat).unstack()
    outp=df[(df.reg!="unknown")&(df.h==5)].copy()
    outp["rb"]=pd.cut(outp["raw"],[-99,-1.5,-0.5,0.5,1.5,99])
    out["outprof_h5_by_raw"]=outp.groupby("rb")["ex"].apply(tstat).unstack()
    for h in [3,10]:
        x=df[(df.reg=="unknown")&(df.h==h)].copy()
        x["rb"]=pd.cut(x["raw"],[-99,-1.5,-0.5,0.5,1.5,99])
        out[f"inprof_h{h}_by_raw"]=x.groupby("rb")["ex"].apply(tstat).unstack()
    out["share_inprof_grid"]=float((df[df.h==5].reg=="unknown").mean())
    return out
