def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,
                "r":r,"n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c.shift(-1)-1,
                "n3":c.shift(-3)/c-1,
                "r3":c/c.shift(3)-1,
                "rng":(b["high"]-b["low"])/c,
                "cl":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "agit":(b["regime"]!="chop").astype(int),
                "pos":b["postRebalance_current_allocation"].astype(float),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            df["vol60"]=r.abs().rolling(60,min_periods=20).mean().shift(0)
            df["z"]=df["r"]/df["vol60"]
            df["pnl"]=df["pos"]*df["n1"]
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["n1"].transform("mean")
    d["x1"]=d["n1"]-drift
    d=d.dropna(subset=["z","x1"])
    out={}
    d["zb"]=pd.cut(d["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    g=d.groupby(["agit","zb"])["x1"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    g.columns=["n","mean_next","t"]; out["next by z bucket x agit"]=g
    res=[]
    for a in [0,1]:
        for side in ["up","down"]:
            s=d[(d.agit==a)&((d.r>0) if side=="up" else (d.r<0))]
            sl=stats.linregress(s["z"],s["x1"])
            res.append([a,side,len(s),sl.slope,sl.slope/sl.stderr])
            sl2=stats.linregress(s["z"],s["n2"].fillna(0))
    out["slope next on z"]=pd.DataFrame(res,columns=["agit","side","n","slope","t"])
    # two-day reversal by 3-day return
    d["z3"]=d["r3"]/(d["vol60"]*np.sqrt(3))
    res=[]
    for a in [0,1]:
        s=d[d.agit==a].dropna(subset=["z3","n2"])
        for col in ["x1","n2"]:
            sl=stats.linregress(s["z"],s[col]); res.append([a,"z->"+col,sl.slope,sl.slope/sl.stderr,len(s)])
        sl=stats.linregress(s["z3"],s["x1"]); res.append([a,"z3->x1",sl.slope,sl.slope/sl.stderr,len(s)])
        sl=stats.linregress(s["cl"].fillna(0.5),s["x1"]); res.append([a,"closeloc->x1",sl.slope,sl.slope/sl.stderr,len(s)])
        sl=stats.linregress(s["rng"]/s["vol60"],s["x1"]); res.append([a,"rangez->x1",sl.slope,sl.slope/sl.stderr,len(s)])
    out["regressions"]=pd.DataFrame(res,columns=["agit","what","slope","t","n"])
    g=d.groupby("wd")["x1"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))]);g.columns=["n","mean","t"]
    out["next-day excess by weekday of signal day"]=g
    g=d.groupby(["coin","agit"]).apply(lambda s:pd.Series({"n":len(s),"corr_z_x1":s["z"].corr(s["x1"])}))
    out["corr by coin"]=g
    g=d.groupby("w").apply(lambda s:pd.Series({"n":len(s),"corr_up":s[s.r>0]["z"].corr(s[s.r>0]["x1"]),"corr_dn":s[s.r<0]["z"].corr(s[s.r<0]["x1"]),"pnl":s["pnl"].mean()}))
    out["by window"]=g
    return out
