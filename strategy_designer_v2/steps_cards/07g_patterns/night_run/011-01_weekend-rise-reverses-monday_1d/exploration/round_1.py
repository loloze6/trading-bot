def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float).values; v=b["volume"].astype(float).values
            r=pd.Series(c).pct_change()
            scale=r.abs().rolling(60,min_periods=20).mean().shift(0)
            z=r/scale
            vr=pd.Series(v)/pd.Series(v).rolling(60,min_periods=20).mean()
            f1=pd.Series(c).shift(-1)/pd.Series(c)-1
            f2=pd.Series(c).shift(-2)/pd.Series(c)-1
            f3=pd.Series(c).shift(-3)/pd.Series(c)-1
            r2=pd.Series(c)/pd.Series(c).shift(2)-1
            df=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday.values,"r":r,"z":z,"vr":vr,
                             "z2":r2/scale,"f1":f1,"f2":f2,"f3":f3,"scale":scale,"year":ts.dt.year.values})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    m1=d.groupby("coin")["f1"].transform("mean")
    d["e1"]=d["f1"]-m1
    d["e2"]=d["f2"]-2*m1; d["e3"]=d["f3"]-3*m1
    out={}
    def slope(x,y):
        ok=x.notna()&y.notna(); x=x[ok]; y=y[ok]
        res=stats.linregress(x,y); return res.slope,res.slope/res.stderr,len(x)
    t=[]
    for wd in range(7):
        s=d[d.wd==wd]
        a=slope(s.z.clip(-5,5),s.e1); b2=slope(s.z.clip(-5,5),s.e2)
        mm=s.e1.dropna()
        t.append([wd,a[0]*1e3,a[1],b2[0]*1e3,b2[1],a[2],mm.mean()*1e3,stats.ttest_1samp(mm,0).statistic])
    out["by weekday of signal day: slope next1 /next2 on z (x1e3), mean next-day excess"]=pd.DataFrame(t,columns=["wd","sl1","t1","sl2","t2","n","next_ex_mean","t_mean"])
    # Sunday by sign and quartile
    s=d[(d.wd==6)&d.z.notna()&d.e2.notna()].copy()
    s["q"]=pd.qcut(s.z,6,labels=False)
    out["sunday z sextile -> e1,e2"]=s.groupby("q").agg(zmean=("z","mean"),e1=("e1","mean"),e2=("e2","mean"),n=("e2","size"))
    # sat+sun 2-day move at sunday close
    a=slope(s.z2.clip(-6,6),s.e2); out["sunday weekend2d z2 slope e2"]=f"{a[0]*1e3:.3f} t={a[1]:.2f} n={a[2]}"
    # all days: large moves
    d["zq"]=pd.cut(d.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["all days z bucket -> next1, next3 excess"]=d.groupby("zq").agg(e1=("e1","mean"),e3=("e3","mean"),n=("e1","count"))
    # volume interaction on weekend
    s["lowvol"]=s.vr<s.vr.median()
    out["sunday slope e2 on z by low/high volume"]=pd.DataFrame([[k,*slope(g.z.clip(-5,5),g.e2)] for k,g in s.groupby("lowvol")],columns=["lowvol","slope","t","n"])
    # per coin weekday mean next-day
    out["next-day excess mean by coin x weekday (x1e3)"]=(d.groupby(["coin","wd"]).e1.mean()*1e3).unstack()
    # vol level
    d["volq"]=d.groupby("coin").scale.transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["vol quartile: slope next1 on z"]=pd.DataFrame([[k,*slope(g.z.clip(-5,5),g.e1)] for k,g in d.groupby("volq")],columns=["volq","slope","t","n"])
    return out
