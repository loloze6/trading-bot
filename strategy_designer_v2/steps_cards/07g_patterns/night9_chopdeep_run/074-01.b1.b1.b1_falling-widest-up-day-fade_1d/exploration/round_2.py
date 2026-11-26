def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=b["high"]-b["low"]
            r1=c.pct_change()
            rm=rng/rng.rolling(20,min_periods=20).mean()
            clpos=(c-b["low"])/rng.replace(0,np.nan)
            r60=c/c.shift(60)-1
            vol20=r1.rolling(20).std()
            vol30=r1.rolling(30).std()
            r5=c/c.shift(5)-1
            nxt=c.shift(-1)/c-1
            n=len(b); grid=(np.arange(n)%1==0)
            df=pd.DataFrame({"coin":coin,"w":w,"day":b["timestamp"].dt.floor("D"),
                "r1":r1,"rm":rm,"clpos":clpos,"r60":r60,"r5s":r5/(vol20*np.sqrt(5)),
                "vol30":vol30,"nxt":nxt,"falling":(b["regime"]!="chop")})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["un"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d["unz"]=d["un"]/d.groupby("coin")["nxt"].transform("std")
    d=d.dropna(subset=["un","rm","r1"])
    def summ(g):
        s=g.groupby("day")["un"].sum()
        t=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"mean_un":g["un"].mean(),"t_day":t,"mean_z":g["unz"].mean()})
    out={}
    f=d[d.falling]
    fu=f[f.r1>0]
    out["falling_up_all"]=summ(fu).to_frame().T
    out["falling_up_by_closepos"]=fu.groupby(pd.cut(fu.clpos,[-0.01,0.2,0.4,0.6,0.8,1.01])).apply(summ)
    out["falling_up_by_r60"]=fu.groupby(pd.cut(fu.r60,[-1,-0.5,-0.35,-0.25,-0.15,-0.1])).apply(summ)
    out["falling_all_by_r60"]=f.groupby(pd.cut(f.r60,[-1,-0.5,-0.35,-0.25,-0.15,-0.1])).apply(summ)
    out["falling_by_r5s"]=f.groupby(pd.qcut(f.r5s,6,duplicates="drop")).apply(summ)
    nf=d[~d.falling]
    out["notfalling_by_r5s"]=nf.groupby(pd.qcut(nf.r5s,6,duplicates="drop")).apply(summ)
    hi=fu[fu.clpos>0.8]
    out["falling_up_highclose_by_width"]=hi.groupby(pd.cut(hi.rm,[0,0.8,1.2,1.7,10])).apply(summ)
    out["falling_up_by_year"]=fu.assign(y=fu.day.dt.year).groupby("y").apply(summ)
    return out
