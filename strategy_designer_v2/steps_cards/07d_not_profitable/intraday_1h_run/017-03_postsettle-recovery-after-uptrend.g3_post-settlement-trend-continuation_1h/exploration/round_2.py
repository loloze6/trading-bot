def explore(data):
    import pandas as pd, numpy as np
    H=[2,4,8,12,24]
    cases=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            ts=pd.to_datetime(b["timestamp"])
            hr=ts.dt.hour.values; yr=ts.dt.year.values
            ret72=pd.Series(cl).pct_change(72).values
            n=len(b)
            for i in range(72,n,1):
                if hr[i] not in (3,9,15,21): continue
                d=dict(coin=c,hr=hr[i],yr=yr[i],s=np.sign(ret72[i]),r72=ret72[i])
                for h in H:
                    d[f"r{h}"]=cl[i+h]/cl[i]-1 if i+h<n else np.nan
                cases.append(d)
    C=pd.DataFrame(cases).dropna(subset=["r72"])
    mu={}
    for h in H:
        C[f"x{h}"]=C[f"r{h}"]-C.groupby("coin")[f"r{h}"].transform("mean")
        C[f"sx{h}"]=C.s*C[f"x{h}"]
    out={}
    g=C.groupby("hr")
    tab=pd.DataFrame({f"m{h}":g[f"sx{h}"].mean() for h in H})
    tab["n"]=g.size()
    tab["t2"]=g["sx2"].mean()/(g["sx2"].std()/np.sqrt(g.size()))
    tab["t24"]=g["sx24"].mean()/(g["sx24"].std()/np.sqrt(g.size()))
    out["byhour_signedexcess"]=tab
    c15=C[C.hr==15].copy()
    c15["q"]=pd.qcut(c15.r72.abs().rank(method="first"),5,labels=False)
    out["h15_byq"]=c15.groupby("q")[[f"sx{h}" for h in H]].mean()
    out["h15_byyear"]=c15.groupby("yr")[["sx2","sx8","sx24"]].agg(["mean"])
    out["h15_bycoin"]=c15.groupby("coin")[["sx2","sx8","sx24"]].mean()
    return out
