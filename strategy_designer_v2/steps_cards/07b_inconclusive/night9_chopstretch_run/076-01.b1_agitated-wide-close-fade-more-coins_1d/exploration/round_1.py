def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"]; allr.append((c.shift(-1)/c-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])
            mult=rng/rng.rolling(20,min_periods=20).mean()
            loc=(c-b["low"])/rng.replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "r1":c.shift(-1)/c-1-mu,"r3":c.shift(-3)/c-1-3*mu,
                "tr60":c/c.shift(60)-1,"mult":mult,"loc":loc,"prod":mult*loc,
                "calm":(b["regime"]=="chop"),"case":b["forecast"]<0,"ret0":c/c.shift(1)-1,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1","mult","loc"])
    d["s1"]=-d["r1"]; d["s3"]=-d["r3"]
    def ct(x,col="s1"):
        x=x.dropna(subset=[col])
        g=x.groupby("day")[col].agg(["sum","count"])
        m=x[col].mean(); dev=(x[col]-m).groupby(x["day"]).sum()
        nd=len(g); se=np.sqrt((dev**2).sum()*nd/(nd-1))/len(x) if nd>1 else np.nan
        return pd.Series({"n":len(x),"days":nd,"mean":m,"t":m/se if se else np.nan})
    cases=d[d.case]
    out={}
    out["cases_all"]=ct(cases)
    out["cases_3d"]=ct(cases,"s3")
    out["by_coin"]=cases.groupby("coin").apply(ct)
    out["by_year"]=cases.groupby("year").apply(ct)
    cases=cases.copy()
    cases["trend"]=pd.cut(cases["tr60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["by_trend"]=cases.groupby("trend").apply(ct)
    cases["pq"]=pd.qcut(cases["prod"],4,labels=False)
    out["by_prod_q"]=cases.groupby("pq").apply(ct)
    cases["lq"]=pd.qcut(cases["loc"],4,labels=False)
    out["by_loc_q"]=cases.groupby("lq").apply(ct)
    cases["up"]=cases["ret0"]>0
    out["by_dayup"]=cases.groupby("up").apply(ct)
    # wider grid: all wide high-close days by agitation
    d["wide"]=d["mult"]>=1.5; d["high"]=d["loc"]>=0.75
    out["grid_calm_wide_high"]=d.groupby(["calm","wide","high"]).apply(ct)
    return out
