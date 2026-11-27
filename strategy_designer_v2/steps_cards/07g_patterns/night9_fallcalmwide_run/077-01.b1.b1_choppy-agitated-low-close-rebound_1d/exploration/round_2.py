def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            if len(b)<30: continue
            rng=(b.high-b.low)
            m20=rng.rolling(20,min_periods=20).mean()
            r0=b.close/b.close.shift(1)-1
            d=pd.DataFrame({
                "coin":coin,"w":w,
                "day":pd.to_datetime(b.timestamp).dt.floor("D"),
                "year":pd.to_datetime(b.timestamp).dt.year,
                "loc":(b.close-b.low)/rng.replace(0,np.nan),
                "width":rng/m20,
                "r0":r0,
                "r1":b.close.shift(-1)/b.close-1,
                "r2":b.close.shift(-2)/b.close-1,
                "r3":b.close.shift(-3)/b.close-1,
                "tr60":b.close/b.close.shift(60)-1,
                "v30":r0.rolling(30).std(),
                "pos":b.postRebalance_current_allocation,
            })
            d["agit"]=d.v30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in ["r1","r2","r3"]:
        D["x"+h[1]]=D[h]-D.groupby("coin")[h].transform("mean")
    def ct(g,col="x1"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"days":g.day.nunique(),"mean":np.nan,"t":np.nan})
        dev=g[col]-g[col].mean()
        s=dev.groupby(g.day).sum()
        se=np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n":len(g),"days":g.day.nunique(),"mean":g[col].mean(),"t":g[col].mean()/se})
    out={}
    D["wq"]=pd.cut(D.width,[0,1,1.25,1.5,2,99])
    L=D[D["loc"]<0.25]
    out["lowclose_by_width"]=L.groupby("wq",observed=True).apply(ct)
    H=D[D["loc"]>0.75]
    out["highclose_by_width"]=H.groupby("wq",observed=True).apply(ct)
    V=D[(D.width>=1.5)&(D["loc"]<0.25)]
    out["vwide_low_h2"]=ct(V,"x2"); out["vwide_low_h3"]=ct(V,"x3")
    out["vwide_low_by_year"]=V.groupby("year").apply(ct)
    out["vwide_low_by_coin"]=V.groupby("coin").apply(ct)
    D["trend"]=np.where(D.tr60>.1,"rising",np.where(D.tr60<-.1,"falling",np.where(D.tr60.notna(),"choppy","na")))
    D["ag"]=np.where(D.agit>0.5,"agit",np.where(D.agit.notna(),"calm","na"))
    V2=D[(D.width>=1.5)&(D["loc"]<0.25)]
    out["vwide_low_by_profile"]=V2.groupby(["trend","ag"]).apply(ct)
    H2=D[(D.width>=1.25)&(D["loc"]>0.75)]
    out["wide_high_by_profile"]=H2.groupby(["trend","ag"]).apply(ct)
    out["wide_high_falling_by_year"]=H2[H2.trend=="falling"].groupby("year").apply(ct)
    # graded within vwide low: regress x1 on (width*(1-2loc)) score
    S=D[(D.width>=1)&(D["loc"]<0.5)].dropna(subset=["x1"]).copy()
    S["score"]=S.width*(1-2*S["loc"])
    S["sq"]=pd.qcut(S.score,5)
    out["score_quintiles"]=S.groupby("sq",observed=True).apply(ct)
    return out
