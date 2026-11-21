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
            for h in [2,4]:
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [2,4]:
        D[f"x{h}"]=D[f"f{h}"]-D["coin"].map(D.groupby("coin")[f"f{h}"].mean())
    def slope(df,y,x="z"):
        df=df[[y,x]].dropna()
        if len(df)<30: return (np.nan,np.nan,len(df))
        r=stats.linregress(df[x],df[y]); return (r.slope*1e4,r.slope/r.stderr,len(df))
    def mt(s):
        s=s.dropna(); return (s.mean()*1e4, s.mean()/s.std()*np.sqrt(len(s)), len(s))
    g21=D[D.hour==21]
    y4=pd.DataFrame([[k,*slope(g,"x4")] for k,g in g21.groupby("year")],columns=["year","slope_bp","t","n"])
    c4=pd.DataFrame([[k,*slope(g,"x4")] for k,g in g21.groupby("coin")],columns=["coin","slope_bp","t","n"])
    # raw r24 slope on 21:00 x4 (unstandardised), pooled
    g=g21.dropna(subset=["r24","x4"]); r=stats.linregress(g.r24,g.x4)
    raw=pd.Series({"slope_x4_on_r24":r.slope,"t":r.slope/r.stderr,"n":len(g)})
    # 21:00 up-side vs down-side, 4h
    g=g21.dropna(subset=["z","x4"]).copy(); g["q"]=pd.qcut(g.z,5,labels=False)
    q4=g.groupby("q").apply(lambda s:pd.Series(dict(zip(["x4_bp","t","n"],mt(s.x4)))))
    up=g[g.z>0]; dn=g[g.z<0]
    sides=pd.DataFrame([["z>0",*slope(up,"x4")],["z<0",*slope(dn,"x4")]],columns=["side","slope_bp","t","n"])
    # hour-20 mean 2h (19->... ) stability: hour 19 and 20 by year and coin
    g20=D[D.hour==20]; g19=D[D.hour==19]
    h20y=pd.DataFrame([[k,*mt(s.x2)] for k,s in g20.groupby("year")],columns=["year","mean_bp","t","n"])
    h20c=pd.DataFrame([[k,*mt(s.x2)] for k,s in g20.groupby("coin")],columns=["coin","mean_bp","t","n"])
    h19y=pd.DataFrame([[k,*mt(s.x2)] for k,s in g19.groupby("year")],columns=["year","mean_bp","t","n"])
    # hour 0-2 negative: hour 0 x2 by year
    h0y=pd.DataFrame([[k,*mt(s.x2)] for k,s in D[D.hour==0].groupby("year")],columns=["year","mean_bp","t","n"])
    return {"h21_x4_year":y4,"h21_x4_coin":c4,"h21_x4_raw_r24":raw,"h21_x4_zquint":q4,"h21_x4_sides":sides,
            "h20_x2_year":h20y,"h20_x2_coin":h20c,"h19_x2_year":h19y,"h0_x2_year":h0y}
