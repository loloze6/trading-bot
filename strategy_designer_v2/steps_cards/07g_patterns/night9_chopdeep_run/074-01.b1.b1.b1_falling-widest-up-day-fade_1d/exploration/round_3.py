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
            nxt=c.shift(-1)/c-1
            nx2=c.shift(-2)/c.shift(-1)-1
            df=pd.DataFrame({"coin":coin,"w":w,"day":b["timestamp"].dt.floor("D"),
                "r1":r1,"r1s":r1/vol20,"rm":rm,"clpos":clpos,"r60":r60,
                "nxt":nxt,"nx2":nx2,"falling":(b["regime"]!="chop")})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["un"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d["unz"]=d["un"]/d.groupby("coin")["nxt"].transform("std")
    d["un2"]=d["nx2"]-d.groupby("coin")["nxt"].transform("mean")
    d=d.dropna(subset=["un","rm","r1","r60"])
    def summ(g,col="un"):
        g=g.dropna(subset=[col])
        s=g.groupby("day")[col].sum()
        t=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"mean":g[col].mean(),"t_day":t})
    out={}
    up=d[d.r1>0]
    out["up_by_r60_all"]=up.groupby(pd.cut(up.r60,[-1,-0.25,-0.15,-0.1,-0.05,0,0.05,0.1,0.2,0.5,10])).apply(summ)
    fu=d[d.falling&(d.r1>0)]
    out["fu_by_r1s"]=fu.groupby(pd.qcut(fu.r1s,5)).apply(summ)
    hi=fu[fu.clpos>0.7]
    hi=hi.assign(rq=pd.cut(hi.rm,[0,0.8,1.2,1.7,10]))
    out["fu_hiclose_width_day2"]=hi.groupby("rq").apply(lambda g: summ(g,"un2"))
    hi["half"]=np.where(hi.w.str[1:].astype(int)<=12,"w7-12","w13-18")
    out["fu_hiclose_width_byhalf"]=hi.groupby(["half","rq"]).apply(summ)
    out["fu_hiclose_corr_rm_unz"]=pd.Series({"spearman":hi[["rm","unz"]].corr("spearman").iloc[0,1],"n":len(hi)})
    fu2=fu.assign(half=np.where(fu.w.str[1:].astype(int)<=12,"w7-12","w13-18"))
    out["fu_shallow_byhalf"]=fu2.groupby(["half",pd.cut(fu2.r60,[-1,-0.25,-0.1])]).apply(summ)
    return out
