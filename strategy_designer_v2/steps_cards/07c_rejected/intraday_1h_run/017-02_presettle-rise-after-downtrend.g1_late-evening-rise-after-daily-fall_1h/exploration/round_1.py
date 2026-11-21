def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r24=c/c.shift(24)-1
            z=(r24-r24.rolling(60,min_periods=20).mean())/r24.rolling(60,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"year":ts.dt.year,"r24":r24,"z":z})
            for h in [1,2,4,6,12,24]:
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin mean 2-bar return (approx via all-hour mean f2 / used per hour cases)
    cm={h:D.groupby("coin")[f"f{h}"].mean() for h in [1,2,4,6,12,24]}
    for h in cm: D[f"x{h}"]=D[f"f{h}"]-D["coin"].map(cm[h])
    def slope(df,y,x="z"):
        df=df[[y,x]].dropna()
        if len(df)<30: return (np.nan,np.nan,len(df))
        r=stats.linregress(df[x],df[y]); return (r.slope,r.slope/r.stderr,len(df))
    # by hour: slope of x2 on z, and mean x2
    out=[]
    for hr,g in D.groupby("hour"):
        s,t,n=slope(g,"x2")
        m=g["x2"].dropna(); out.append([hr,s*1e4,t,m.mean()*1e4,m.mean()/m.std()*np.sqrt(len(m)),n])
    byhour=pd.DataFrame(out,columns=["hour","slope_bp","slope_t","mean_bp","mean_t","n"]).set_index("hour")
    g21=D[D.hour==21]
    out=[]
    for h in [1,2,4,6,12,24]:
        s,t,n=slope(g21,f"x{h}"); out.append([h,s*1e4,t,n])
    hz=pd.DataFrame(out,columns=["h","slope_bp","t","n"])
    # 21:00 by coin, by year
    bc=pd.DataFrame([[k,*slope(g,"x2")] for k,g in g21.groupby("coin")],columns=["coin","slope","t","n"])
    by=pd.DataFrame([[k,*slope(g,"x2")] for k,g in g21.groupby("year")],columns=["year","slope","t","n"])
    # z quintiles at 21:00 (full z, both sides)
    g=g21.dropna(subset=["z","x2"]).copy(); g["q"]=pd.qcut(g.z,5,labels=False)
    q=g.groupby("q").agg(z=("z","mean"),x2_bp=("x2",lambda s:s.mean()*1e4),t=("x2",lambda s:s.mean()/s.std()*np.sqrt(len(s))),n=("x2","size"))
    # all hours, z quintile vs x2 pooled (non-overlap: use hours 0,2,..)
    a=D[D.hour%2==0].dropna(subset=["z","x2"]).copy(); a["q"]=pd.qcut(a.z,5,labels=False)
    qa=a.groupby("q").agg(z=("z","mean"),x2_bp=("x2",lambda s:s.mean()*1e4),t=("x2",lambda s:s.mean()/s.std()*np.sqrt(len(s))),n=("x2","size"))
    return {"byhour":byhour,"h21_horizons":hz,"h21_coin":bc,"h21_year":by,"h21_zquint":q,"allhours_even_zquint":qa}
