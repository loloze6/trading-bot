def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            m30=np.full(n,np.nan); m30[30:]=c[30:]/c[:-30]-1
            m60=np.full(n,np.nan); m60[60:]=c[60:]/c[:-60]-1
            sd30=pd.Series(r).rolling(30).std().values
            for h in (7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,ret=c[i+h]/c[i]-1,fc=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i],m30=m30[i],m60=m60[i],sd30=sd30[i],
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
    R=R.dropna(subset=["m30","m60"])
    R["choppy"]=R.m60.abs()<=0.10
    t=[]
    for h in (7,14):
        for nm,ss in [("choppy_all",R[(R.h==h)&R.choppy]),("choppy_outside_profile(calm)",R[(R.h==h)&R.choppy&(R.reg!="unknown")]),("in_profile",R[(R.h==h)&(R.reg=="unknown")])]:
            sl=stats.linregress(ss.m30,ss.ex) if len(ss)>3 else None
            short=-ss.ex
            dirx=np.sign(ss.m30)*ss.ex
            t.append(dict(h=h,grp=nm,n=len(ss),days=ss.day.nunique(),short_ex=short.mean(),t_short=tday(short,ss.day),
                          contin_ex=dirx.mean(),t_contin=tday(dirx,ss.day),slope=sl.slope if sl else np.nan,
                          spearman=stats.spearmanr(ss.m30,ss.ex)[0]))
    out["groups"]=pd.DataFrame(t)
    s=R[(R.h==7)&(R.reg=="unknown")].copy()
    s["fc_half"]=np.where(s.fc<=s.fc.median(),"deeper","shallower")
    out["in_profile_by_fc_half"]=s.groupby("fc_half").agg(n=("ex","size"),days=("day","nunique"),short_ex=("ex",lambda x:-x.mean()))
    s["m60sign"]=np.sign(s.m60)
    out["in_profile_by_m60sign"]=s.groupby("m60sign").agg(n=("ex","size"),short_ex=("ex",lambda x:-x.mean()))
    c=R[(R.h==7)&R.choppy&(R.reg!="unknown")].copy()
    c["q"]=pd.qcut(c.m30,5,labels=False)
    out["choppy_calm_quintiles_h7"]=c.groupby("q").agg(n=("ex","size"),m30=("m30","mean"),ex=("ex","mean"))
    return out
