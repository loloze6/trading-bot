def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            df=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),
                "inprof":(b["regime"]=="unknown").values,
                "r1":r,"z":r/sd.shift(1),
                "r3":c/c.shift(3)-1,"r5":c/c.shift(5)-1,
                "z5":(c/c.shift(5)-1)/(sd.shift(1)*np.sqrt(5)),
                "cl":(c-l)/(h-l).replace(0,np.nan),
                "rng":(h-l)/c/sd.shift(1),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc":b["postRebalance_current_allocation"]})
            for H in [1,2,3,5]:
                df[f"f{H}"]=c.shift(-H)/c-1
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    out["counts"]=d.groupby("coin")["inprof"].agg(["size","mean"])
    drift={H:d[f"f{H}"].mean() for H in [1,2,3,5]}
    p=d[d.inprof].copy()
    res=[]
    for var in ["z","z5","cl","rng"]:
        for H in [1,2,3,5]:
            s=p[(p.pos%H==0)].dropna(subset=[var,f"f{H}"])
            x=s[var].clip(-5,5); y=s[f"f{H}"]-drift[H]
            if len(s)<20: continue
            sl=stats.linregress(x,y)
            res.append({"var":var,"H":H,"n":len(s),"slope":sl.slope,"t":sl.slope/sl.stderr,"meanex":y.mean()})
    out["slopes_inprof"]=pd.DataFrame(res)
    s=p.dropna(subset=["z","f1"])
    s["zb"]=pd.cut(s.z,[-10,-2,-1,0,1,2,10])
    out["f1_by_z"]=s.groupby("zb")["f1"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    s=p[p.pos%3==0].dropna(subset=["z5","f3"])
    s["b"]=pd.qcut(s.z5,5)
    out["f3_by_z5"]=s.groupby("b")["f3"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    s=p[p.pos%3==0].dropna(subset=["cl","f3"])
    s["b"]=pd.qcut(s.cl,4)
    out["f3_by_closeloc"]=s.groupby("b")["f3"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    s=p.dropna(subset=["f1"])
    out["f1_by_wd"]=s.groupby("wd")["f1"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    out["drift"]=pd.Series(drift)
    out["f1_all_vs_prof"]=pd.Series({"all":d.f1.mean(),"prof":p.f1.mean(),"out":d[~d.inprof].f1.mean(),"nprof":p.f1.notna().sum()})
    return out
