def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    H=[1,3,5,10]
    for coin,ws in data["bars"].items():
        # drift per horizon over all visible windows' grids
        drift={}
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-h,h):
                    rr.append(c[i+h]/c[i]-1)
            drift[h]=np.mean(rr) if rr else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values
            ts=pd.to_datetime(b["timestamp"])
            vr=pd.Series(v).rolling(5).mean()/pd.Series(v).rolling(60,min_periods=20).mean()
            r5=pd.Series(c).pct_change(5)
            for i in range(0,len(c)-5,5):
                f=b["forecast"].iloc[i]
                if pd.isna(f) or f==0: continue
                d={"coin":coin,"win":w,"year":ts.iloc[i].year,"day":ts.iloc[i].normalize(),
                   "f":f,"side":"long" if f>0 else "short","r5past":r5.iloc[i],"vr":vr.iloc[i]}
                for h in H:
                    if i+h<len(c):
                        d[f"x{h}"]=np.sign(f)*(c[i+h]/c[i]-1-drift[h])
                    else: d[f"x{h}"]=np.nan
                d["prod"]=f/10*(c[i+5]/c[i]-1-drift[5])
                rows.append(d)
    df=pd.DataFrame(rows)
    def tstat(g,col):
        s=g.groupby("day")[col].sum()
        n=g[col].notna().sum()
        m=g[col].mean()
        dev=g.groupby("day")[col].apply(lambda x:(x-m).sum())
        G=len(dev)
        se=np.sqrt((dev**2).sum()*G/(G-1))/n if G>1 else np.nan
        return pd.Series({"n":n,"days":G,"mean":m,"t":m/se if se else np.nan})
    out={}
    out["all"]=pd.DataFrame({c:tstat(df,c) for c in ["prod","x1","x3","x5","x10"]}).T
    out["by_side_x5"]=df.groupby("side").apply(lambda g:tstat(g,"x5"))
    out["by_side_prod"]=df.groupby("side").apply(lambda g:tstat(g,"prod"))
    out["by_coin_x5"]=df.groupby("coin").apply(lambda g:tstat(g,"x5"))
    out["by_year_x5"]=df.groupby("year").apply(lambda g:tstat(g,"x5"))
    df["fq"]=pd.qcut(df["f"].abs(),3,labels=["weak","mid","strong"])
    out["by_absf_x5"]=df.groupby("fq").apply(lambda g:tstat(g,"x5"))
    df["vq"]=pd.qcut(df["vr"],3,labels=["lowvol","midvol","highvol"])
    out["by_vol_x5"]=df.groupby("vq").apply(lambda g:tstat(g,"x5"))
    out["by_vol_side_x5"]=df.groupby(["side","vq"]).apply(lambda g:tstat(g,"x5"))
    out["by_side_x10"]=df.groupby("side").apply(lambda g:tstat(g,"x10"))
    out["by_side_x3"]=df.groupby("side").apply(lambda g:tstat(g,"x3"))
    return out
