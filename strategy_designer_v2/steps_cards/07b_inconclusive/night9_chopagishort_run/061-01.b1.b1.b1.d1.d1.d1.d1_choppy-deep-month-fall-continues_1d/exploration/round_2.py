def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].values
            for i in range(0,len(c)-H,H):
                allr.append(c[i+H]/c[i]-1)
        dr=np.mean(allr); sd=np.std(allr)
        for w,df in wins.items():
            c=df["close"].values; n=len(c)
            r1=pd.Series(c).pct_change()
            fp=df.get("debug_info.components.fall20.post_pipeline_value")
            for i in range(60,n-H,H):
                r20=c[i]/c[i-20]-1; r60=c[i]/c[i-60]-1
                if not (-0.10<=r60<=0.10 and r20<=-0.10): continue
                fwd=c[i+H]/c[i]-1
                rows.append(dict(coin=coin,w=w,r20=r20,
                    vol30=r1.iloc[i-29:i+1].std(),
                    alloc=abs(df["postRebalance_current_allocation"].iloc[i]),
                    fc=abs(df["forecast"].iloc[i]),
                    fpost=(abs(fp.iloc[i]) if fp is not None and pd.notna(fp.iloc[i]) else np.nan),
                    un=-(fwd-dr), z=-(fwd-dr)/sd,
                    un2=-(c[i+2]/c[i]-1-dr*2/5),
                    un10=(-(c[i+10]/c[i]-1-dr*2)) if i+10<n else np.nan))
    S=pd.DataFrame(rows)
    out={}
    sp=lambda a,b: pd.Series(stats.spearmanr(S[a],S[b],nan_policy="omit")[:2],index=["rho","p"])
    out["spearman"]=pd.DataFrame({"depth_vs_un":sp("r20","un"),"depth_vs_z":sp("r20","z"),
        "depth_vs_alloc":sp("r20","alloc"),"depth_vs_forecast":sp("r20","fc"),
        "depth_vs_fpost":sp("r20","fpost"),"vol_vs_alloc":sp("vol30","alloc"),
        "alloc_vs_un":sp("alloc","un"),"forecast_vs_un":sp("fc","un"),"depth_vs_vol":sp("r20","vol30")}).T
    S["deep_half"]=S.r20<=S.r20.median()
    def summ(g):
        return pd.Series(dict(n=len(g),mean_r20=g.r20.mean(),mean_alloc=g.alloc.mean(),mean_fc=g.fc.mean(),
            un=g.un.mean(),t=g.un.mean()/(g.un.std()/np.sqrt(len(g))),strength=g.z.mean(),
            un2=g.un2.mean(),un10=g.un10.mean()))
    out["by_depth_half"]=S.groupby("deep_half").apply(summ)
    out["by_forecast_half"]=S.groupby(S.fc>S.fc.median()).apply(summ)
    out["all"]=summ(S).to_frame().T
    return out
