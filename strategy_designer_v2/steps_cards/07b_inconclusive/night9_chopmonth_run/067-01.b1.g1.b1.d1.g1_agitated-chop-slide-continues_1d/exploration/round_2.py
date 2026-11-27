def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    for H in (3,5,10):
        drift={}
        for coin,wins in data["bars"].items():
            g=[]
            for w,b in wins.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-H,H)
                g+=list(c[idx+H]/c[idx]-1)
            drift[coin]=np.mean(g)
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                b=b.reset_index(drop=True)
                c=b["close"].values; n=len(c)
                rc=pd.Series(c).pct_change(30).values*100
                for i in range(0,n-H,H):
                    if b.loc[i,"regime"]!="unknown" or pd.isna(rc[i]): continue
                    rows.append({"coin":coin,"win":w,"year":pd.Timestamp(b.loc[i,"timestamp"]).year,
                                 "day":str(b.loc[i,"timestamp"])[:10],"r30":rc[i],"fc":b.loc[i,"forecast"],
                                 "ex":c[i+H]/c[i]-1-drift[coin]})
        df=pd.DataFrame(rows)
        fa=df[df.r30<0].copy()
        fa["sx"]=-fa.ex
        dd=fa.groupby("day").sx.sum()
        nd=len(dd); m=fa.sx.mean()
        se=np.sqrt(((dd - fa.groupby("day").size()*m)**2).sum())/len(fa)
        res={"cases":len(fa),"days":nd,"mean_sx":m,"t_clust":m/se if se>0 else np.nan}
        fa["absfc"]=fa.fc.abs()
        s=fa.sort_values("absfc",kind="stable")
        k=len(s)//2
        res["big_minus_small_fc"]=s.sx.iloc[-k:].mean()-s.sx.iloc[:k].mean() if k>0 else np.nan
        s2=fa.sort_values("r30")
        k2=len(s2)//2
        res["deep_minus_shallow_r30"]=s2.sx.iloc[:k2].mean()-s2.sx.iloc[k2:].mean() if k2>0 else np.nan
        res["spearman_r30_sx"]=stats.spearmanr(fa.r30,fa.sx)[0]
        out[f"H{H}"]=pd.Series(res)
        if H==5:
            out["H5_by_year"]=fa.groupby("year").sx.agg(["count","mean"])
            fa["q"]=pd.qcut(fa.r30,3,labels=["deep","mid","shallow"])
            out["H5_by_tercile"]=fa.groupby("q").sx.agg(["count","mean","std"])
    return out
