def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            for H in (5,10,20):
                pass
            idx=np.arange(0,len(c)-10,10)
            g+=list(c[idx+10]/c[idx]-1)
        drift[coin]=np.mean(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r30=b.get("debug_info.components.fall30.last_history_value")
            rc=pd.Series(c).pct_change(30).values*100
            for i in range(0,n,10):
                if b.loc[i,"regime"]!="unknown": continue
                v=r30.iloc[i] if r30 is not None and pd.notna(r30.iloc[i]) else rc[i]
                if pd.isna(v): continue
                d={"coin":coin,"win":w,"year":pd.Timestamp(b.loc[i,"timestamp"]).year,"r30":v,"fc":b.loc[i,"forecast"],"day":str(b.loc[i,"timestamp"])[:10]}
                for H in (3,5,10,20):
                    d[f"f{H}"]=c[i+H]/c[i]-1 if i+H<n else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    df["dr"]=df.coin.map(drift)
    df["ex10"]=df.f10-df.dr
    out={}
    def summ(x,col="ex10"):
        x=x.dropna(subset=[col]); 
        if len(x)<3: return pd.Series({"n":len(x)})
        m=x[col].mean(); t=stats.ttest_1samp(x[col],0).statistic
        return pd.Series({"n":len(x),"mean":m,"t":t})
    df["side"]=np.where(df.r30<0,"fall","rise")
    out["by_side"]=df.groupby("side").apply(summ)
    fa=df[df.r30<0].copy()
    fa["q"]=pd.qcut(fa.r30,4,labels=["deep","q2","q3","shallow"])
    out["fall_by_depth_q"]=fa.groupby("q").apply(summ)
    ri=df[df.r30>=0].copy()
    ri["q"]=pd.qcut(ri.r30,4,labels=["small","q2","q3","big"])
    out["rise_by_size_q"]=ri.groupby("q").apply(summ)
    out["fall_by_year"]=fa.groupby("year").apply(summ)
    out["fall_by_coin"]=fa.groupby("coin").apply(summ)
    hz={}
    for H in (3,5,10,20):
        x=fa[f"f{H}"].dropna(); hz[H]=(len(x),x.mean(),stats.ttest_1samp(x,0).statistic)
    out["fall_raw_fwd_by_H(n,mean,t)"]=pd.DataFrame(hz,index=["n","mean","t"]).T
    out["corr_r30_ex10_all"]=pd.Series({"spearman":stats.spearmanr(df.r30,df.ex10,nan_policy='omit')[0],"n":df.ex10.notna().sum()})
    out["fc_neg_share_of_falls"]=float((fa.fc<0).mean())
    return out
