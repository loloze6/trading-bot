def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    H=[5,10,20,40]
    rows=[]
    drift={}
    for c,ws in bars.items():
        for h in H:
            rs=[]
            for w,df in ws.items():
                cl=df["close"].values
                for i in range(0,len(cl)-h,h):
                    rs.append(cl[i+h]/cl[i]-1)
            drift[(c,h)]=np.mean(rs) if rs else np.nan
    for c,ws in bars.items():
        for w,df in ws.items():
            cl=df["close"].values; n=len(cl)
            reg=df["regime"].values
            fc=df["forecast"].values
            raw=pd.to_numeric(df.get("debug_info.components.fall30.last_history_value"),errors="coerce").values if "debug_info.components.fall30.last_history_value" in df else np.full(n,np.nan)
            for i in range(0,n,10):
                if reg[i]!="unknown": continue
                r30=raw[i]
                if np.isnan(r30) and i>=30: r30=(cl[i]/cl[i-30]-1)*100
                if np.isnan(r30): continue
                d={"coin":c,"win":w,"r30":r30,"fc":fc[i],"grid20":(i%20==0)}
                for h in H:
                    d[f"f{h}"]=(cl[i+h]/cl[i]-1-drift[(c,h)]) if i+h<n else np.nan
                rows.append(d)
    X=pd.DataFrame(rows)
    out={}
    X["side"]=np.where(X.r30<0,"fall","rise")
    X["q"]=pd.qcut(X.r30,6,labels=False)
    def summ(g,col):
        v=g[col].dropna(); return pd.Series({"n":len(v),"mean":v.mean(),"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
    # continuation sign: for fall, -f ; for rise, f
    for h in H:
        X[f"c{h}"]=np.where(X.r30<0,-X[f"f{h}"],X[f"f{h}"])
    out["by side, continuation per horizon"]=pd.concat({f"h{h}":X.groupby("side").apply(lambda g:summ(g,f"c{h}")) for h in H},axis=1)
    out["by r30 sextile, unusual fwd (not signed)"]=pd.concat({f"h{h}":X.groupby("q").apply(lambda g:summ(g,f"f{h}")) for h in H},axis=1)
    out["r30 sextile bounds"]=X.groupby("q").r30.agg(["min","max","count"])
    co={}
    for h in H:
        v=X[["r30",f"f{h}"]].dropna()
        f=v[v.r30<0]; r=v[v.r30>=0]
        co[f"h{h}"]={"rank_all":stats.spearmanr(v.r30,v[f"f{h}"])[0],"rank_fall":stats.spearmanr(f.r30,f[f"f{h}"])[0],"rank_rise":stats.spearmanr(r.r30,r[f"f{h}"])[0],"n":len(v)}
    out["spearman r30 vs fwd"]=pd.DataFrame(co).T
    F=X[X.r30<0]
    out["fall, c20 by coin"]=F.groupby("coin").apply(lambda g:summ(g,"c20"))
    F=F.assign(wn=F.win.str[1:].astype(int))
    out["fall, c20 by window"]=F.groupby("wn").apply(lambda g:summ(g,"c20"))
    R=X[X.r30>=0].assign(wn=lambda d:d.win.str[1:].astype(int))
    out["rise, c20 by window"]=R.groupby("wn").apply(lambda g:summ(g,"c20"))
    return out
