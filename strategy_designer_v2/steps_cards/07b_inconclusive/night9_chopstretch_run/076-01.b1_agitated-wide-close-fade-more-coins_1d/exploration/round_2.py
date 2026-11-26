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
                "r1":c.shift(-1)/c-1-mu,"r2":c.shift(-2)/c-1-2*mu,"mult":mult,"loc":loc,
                "agit":(b["regime"]!="chop"),"ret0":c/c.shift(1)-1,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r1","mult","loc"])
    d["s1"]=-d["r1"]; d["s2"]=-d["r2"]
    def ct(x,col="s1"):
        x=x.dropna(subset=[col])
        nd=x["day"].nunique()
        m=x[col].mean(); dev=(x[col]-m).groupby(x["day"]).sum()
        se=np.sqrt((dev**2).sum()*nd/(nd-1))/len(x) if nd>1 else np.nan
        return pd.Series({"n":len(x),"days":nd,"mean":m,"t":m/se if se else np.nan})
    out={}
    a=d[d.agit].copy()
    # graded: high-close score = mult * (2*loc-1) positive part
    a["hc"]=a["mult"]*(2*a["loc"]-1)
    hc=a[a.hc>0].copy()
    hc["q"]=pd.qcut(hc["hc"],5,labels=False)
    out["agit_hc_quintile"]=hc.groupby("q").apply(ct)
    top=hc[hc.q>=3]
    out["agit_hc_top2_by_year"]=top.groupby("year").apply(ct)
    out["agit_hc_top2_by_coin"]=top.groupby("coin").apply(ct)
    out["agit_hc_top2_2d"]=ct(top,"s2")
    wh=a[(a.mult>=1.5)&(a.loc>=0.75)].copy()
    wh["mq"]=pd.qcut(wh["mult"],3,labels=False)
    out["agit_widehigh_by_mult"]=wh.groupby("mq").apply(ct)
    out["agit_widehigh_by_year"]=wh.groupby("year").apply(ct)
    out["agit_widehigh_by_dayup"]=wh.groupby(wh.ret0>0).apply(ct)
    c=d[~d.agit].copy(); c["hc"]=c["mult"]*(2*c["loc"]-1)
    ch=c[c.hc>0].copy(); ch["q"]=pd.qcut(ch["hc"],5,labels=False)
    out["calm_hc_quintile"]=ch.groupby("q").apply(ct)
    # correlation of score with s1 in agitated all days
    out["agit_corr_hc_s1"]=float(a[["hc","s1"]].corr().iloc[0,1])
    out["agit_corr_hc_s1_n"]=int(len(a))
    return out
