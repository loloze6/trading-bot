def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            m30=np.full(n,np.nan); m30[30:]=c[30:]/c[:-30]-1
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,
                        ret=c[i+h]/c[i]-1,fc=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i],m30=m30[i],
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        day=str(pd.Timestamp(df["timestamp"].iloc[i]).date())))
    R=pd.DataFrame(rows)
    R["drift"]=R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"]=R["ret"]-R["drift"]
    def tday(s,d):
        g=pd.DataFrame({"v":s-s.mean(),"d":d}).groupby("d")["v"].sum()
        se=np.sqrt((g**2).sum())/len(s)
        return s.mean()/se if se>0 else np.nan
    out={}
    ins=R[R.reg=="unknown"].dropna(subset=["m30"])
    # continuation test: excess return in direction of month sign, by horizon
    t=[]
    for h in (3,7,14):
        s=ins[ins.h==h]
        corr=stats.spearmanr(s.m30,s.ex)
        for nm,ss in [("all",s),("m30<0",s[s.m30<0]),("m30>0",s[s.m30>0]),("fc<0",s[s.fc<0])]:
            short=-ss.ex  # short direction excess
            t.append(dict(h=h,grp=nm,n=len(ss),days=ss.day.nunique(),short_ex=short.mean(),t=tday(short,ss.day),raw_short=(-ss.ret).mean(),spearman_all=corr[0]))
    out["by_horizon_group"]=pd.DataFrame(t)
    s=ins[ins.h==7].copy()
    s["q"]=pd.qcut(s.m30,5,labels=False)
    out["quintile_m30_h7"]=s.groupby("q").agg(n=("ex","size"),m30=("m30","mean"),ex=("ex","mean"),ret=("ret","mean"))
    out["by_coin_h7_short"]=s.groupby("coin").agg(n=("ex","size"),short_ex=("ex",lambda x:-x.mean()))
    out["by_year_h7_short"]=s.groupby("year").agg(n=("ex","size"),short_ex=("ex",lambda x:-x.mean()),m30=("m30","mean"))
    out["by_window_h7_short"]=s.groupby("w").agg(n=("ex","size"),short_ex=("ex",lambda x:-x.mean()))
    # outside profile (regime chop), all grid: relation m30 vs next week
    o=R[(R.reg!="unknown")&(R.h==7)].dropna(subset=["m30"]).copy()
    o["q"]=pd.qcut(o.m30,5,labels=False)
    out["outside_profile_quintiles_h7"]=o.groupby("q").agg(n=("ex","size"),m30=("m30","mean"),ex=("ex","mean"))
    return out
