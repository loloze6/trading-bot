def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "ret":r,"nxt":c.shift(-1)/c-1,"sd20":r.rolling(20).std(),"tr60":c/c.shift(60)-1,
                "clpos":(c-b["low"])/(b["high"]-b["low"]),"reg":b["regime"].astype(str),
                "fc":b["forecast"].astype(float)})
            d["z"]=d["ret"]/d["sd20"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D["day"]=D["ts"].dt.floor("D")
    D["yr"]=D["ts"].dt.year
    D["prof"]=np.where(D["reg"]=="unknown","FA",np.where(D["tr60"]<-0.1,"Fcalm",np.where(D["tr60"]>0.1,"rise",np.where(D["tr60"].notna(),"chop","na"))))
    def slope(g,x):
        g=g[[x,"ex","day"]].dropna()
        if len(g)<20: return pd.Series({"n":len(g)})
        X=g[x]-g[x].mean(); b=(X*g["ex"]).sum()/(X**2).sum()
        e=g["ex"]-g["ex"].mean()-b*X
        s=(X*e).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/(X**2).sum()
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"slope%":b*100,"t":b/se,"mean%":g["ex"].mean()*100})
    out={}
    U=D[D["z"]>0]; Dn=D[D["z"]<0]
    out["up_slope_z_by_prof"]=U.groupby("prof").apply(lambda g:slope(g,"z"))
    out["down_slope_z_by_prof"]=Dn.groupby("prof").apply(lambda g:slope(g,"z"))
    out["clpos_slope_by_prof"]=D.groupby("prof").apply(lambda g:slope(g,"clpos"))
    D["cq"]=pd.cut(D["clpos"],[-0.01,0.2,0.4,0.6,0.8,1.01])
    def tab(g):
        dm=g.groupby("day")["ex"].mean().dropna()
        return pd.Series({"n":len(g["ex"].dropna()),"days":len(dm),"mean%":dm.mean()*100,"t_day":dm.mean()/(dm.std()/np.sqrt(len(dm)))})
    out["clpos_FA_Fcalm"]=D[D["prof"].isin(["FA","Fcalm"])].groupby(["prof","cq"]).apply(tab).reset_index()
    # close position on up days in FA (does high close matter for fade)
    D["upq"]=pd.cut(D["z"],[0,0.3,1,2,99])
    out["FA_up_by_clpos"]=D[(D["prof"]=="FA")&(D["z"]>0)].assign(hi=lambda x:x["clpos"]>0.5).groupby(["upq","hi"]).apply(tab).reset_index()
    D["wd"]=D["ts"].dt.dayofweek
    D["wdg"]=np.where(D["wd"]==2,"wed",np.where(D["wd"].isin([3,4]),"thu_fri","other"))
    out["weekday_by_year"]=D.groupby(["yr","wdg"]).apply(tab).reset_index()
    out["slope_by_year_FA_up"]=U[U["prof"]=="FA"].groupby("yr").apply(lambda g:slope(g,"z"))
    out["slope_by_year_Fall_up"]=U[U["prof"].isin(["FA","Fcalm"])].groupby("yr").apply(lambda g:slope(g,"z"))
    return out
