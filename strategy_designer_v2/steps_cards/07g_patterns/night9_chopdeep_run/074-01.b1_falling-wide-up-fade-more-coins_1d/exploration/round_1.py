def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; o=b["open"]; h=b["high"]; l=b["low"]
            r=c.pct_change()
            rng=(h-l)/c.shift(1)
            width=(h-l)/(h-l).rolling(20).mean()
            d=pd.DataFrame({
                "coin":coin,"w":w,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "ret":r,"width":width,
                "clv":((c-l)/(h-l)).where(h>l),
                "falling":(b["regime"]!="chop"),
                "regime":b["regime"],
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1,
                "vol30":r.rolling(30).std(),
                "ret5":c/c.shift(5)-1,
                "alloc":b["postRebalance_current_allocation"],
                "fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift={k:D.groupby("coin")[k].mean() for k in ["f1","f2","f3","f5"]}
    for k in ["f1","f2","f3","f5"]:
        D["x"+k]=D[k]-D["coin"].map(drift[k])
    def ct(sub,col):
        s=sub.dropna(subset=[col])
        if len(s)<10: return (len(s),np.nan,np.nan,0)
        g=s.groupby("day")[col].sum()
        m=s[col].mean()
        t=g.mean()/(g.std(ddof=1)/np.sqrt(len(g))) if len(g)>2 else np.nan
        return (len(s),round(m*100,3),round(t,2),len(g))
    out={}
    D["up"]=D["ret"]>0
    D["wq"]=D.groupby(["falling","up"])["width"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    res=[]
    for (f,u,q),s in D.groupby(["falling","up","wq"]):
        n,m,t,nd=ct(s,"xf1"); res.append([f,u,q,n,m,t,nd])
    out["next1_excess_by_profile_updown_widthQ"]=pd.DataFrame(res,columns=["falling","up","wq","n","mean%","t","days"])
    # horizons, non-overlapping grid, falling wide up days (width>1)
    res=[]
    for hz in [1,2,3,5]:
        for f in [True,False]:
            for u in [True,False]:
                s=D[(D.pos%hz==0)&(D.falling==f)&(D.up==u)&(D.width>1.3)]
                n,m,t,nd=ct(s,"xf%d"%hz); res.append([hz,f,u,n,m,t,nd])
    out["horizon_width_gt1.3"]=pd.DataFrame(res,columns=["h","falling","up","n","mean%","t","days"])
    # close location for falling up wide days
    s=D[D.falling&D.up&(D.width>1)].copy()
    s["cq"]=pd.qcut(s["clv"],3,labels=False)
    out["falling_upwide_by_closeloc"]=pd.DataFrame([[q]+list(ct(g,"xf1")) for q,g in s.groupby("cq")],columns=["clvT","n","mean%","t","days"])
    # by window
    out["falling_upwide_by_window"]=pd.DataFrame([[w]+list(ct(g,"xf1")) for w,g in s.groupby("w")],columns=["w","n","mean%","t","days"])
    # all bars: weekday
    out["all_weekday"]=pd.DataFrame([[k]+list(ct(g,"xf1")) for k,g in D.groupby("wd")],columns=["wd","n","mean%","t","days"])
    # large moves: return quintile scaled by vol, next day, by profile
    D["z"]=D["ret"]/D["vol30"]
    D["zq"]=pd.qcut(D["z"],7,labels=False)
    out["z_next_by_profile"]=pd.DataFrame([[f,q]+list(ct(g,"xf1")) for (f,q),g in D.groupby(["falling","zq"])],columns=["falling","zq","n","mean%","t","days"])
    # 5-day return quintile next 2 day nonoverlap
    s2=D[D.pos%2==0].copy(); s2["r5q"]=pd.qcut(s2["ret5"],5,labels=False)
    out["ret5_next2_by_profile"]=pd.DataFrame([[f,q]+list(ct(g,"xf2")) for (f,q),g in s2.groupby(["falling","r5q"])],columns=["falling","r5q","n","mean%","t","days"])
    return out
