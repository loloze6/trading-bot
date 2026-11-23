def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=c.pct_change()
            vol7=r1.rolling(168,min_periods=100).std()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "yr":(ts+pd.Timedelta(hours=1)).dt.year.values,
                "hc":((ts+pd.Timedelta(hours=1)).dt.hour).values,
                "r1":r1.values,
                "r2z":(c/c.shift(2)-1).values/(vol7.values*np.sqrt(2)),
                "r3z":(c/c.shift(3)-1).values/(vol7.values*np.sqrt(3)),
                "r24z":(c/c.shift(24)-1).values/(vol7.values*np.sqrt(24)),
                "r72z":(c/c.shift(72)-1).values/(vol7.values*np.sqrt(72)),
                "f24":(c.shift(-24)/c-1).values,
                "f72":(c.shift(-72)/c-1).values,
                "f2":(c.shift(-2)/c-1).values})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    d24=A[A.pos%24==0].dropna(subset=["f24"]).groupby("coin").f24.mean()
    d72=A[A.pos%72==0].dropna(subset=["f72"]).groupby("coin").f72.mean()
    A["x24"]=A.f24-A.coin.map(d24); A["x72"]=A.f72-A.coin.map(d72)
    out={}
    def tt(x): x=x.dropna(); return pd.Series({"m":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    # 1) reversal at close hour 1 of the 3h move (22->01), by side
    s=A[A.hc==1].dropna(subset=["r3z","x24"]).copy()
    s["side"]=np.where(s.r3z<0,"fall","rise")
    s["q"]=pd.qcut(s.r3z,10,labels=False)
    out["h01_r3z_dec_x24"]=s.groupby("q").x24.apply(tt).unstack()
    res=[]
    for k,g in s.groupby("coin"):
        sl=stats.linregress(-g.r3z.clip(-5,5),g.x24); res.append((k,len(g),sl.slope,sl.slope/sl.stderr))
    for k,g in s.groupby("yr"):
        sl=stats.linregress(-g.r3z.clip(-5,5),g.x24); res.append((str(k),len(g),sl.slope,sl.slope/sl.stderr))
    out["h01_r3z_slope_coin_yr"]=pd.DataFrame(res,columns=["grp","n","slope","t"])
    # 2) 24h fall reversal: grid, by coin and year, graded in lowest quintile
    g=A[A.pos%24==0].dropna(subset=["r24z","x24"]).copy()
    g["q"]=pd.qcut(g.r24z,20,labels=False)
    out["r24z_20tiles_x24"]=g.groupby("q").agg(r=("r24z","mean")).join(g.groupby("q").x24.apply(tt).unstack())
    lo=g[g.r24z<0]
    res=[]
    for k,gg in list(lo.groupby("coin"))+[(str(y),v) for y,v in lo.groupby("yr")]:
        sl=stats.linregress(-gg.r24z.clip(-6,0),gg.x24); res.append((k,len(gg),sl.slope,sl.slope/sl.stderr,gg.x24[gg.r24z<gg.r24z.quantile(0.2)].mean()))
    out["r24fall_slope_coin_yr"]=pd.DataFrame(res,columns=["grp","n","slope","t","m_lowq"])
    # 3) 72h rise continuation by coin and year
    g=A[A.pos%72==0].dropna(subset=["r72z","x72"]).copy()
    hi=g[g.r72z>0]; res=[]
    for k,gg in [("all",hi)]+list(hi.groupby("coin"))+[(str(y),v) for y,v in hi.groupby("yr")]:
        sl=stats.linregress(gg.r72z.clip(0,6),gg.x72); res.append((k,len(gg),sl.slope,sl.slope/sl.stderr,gg.x72[gg.r72z>gg.r72z.quantile(0.8)].mean()))
    out["r72rise_slope"]=pd.DataFrame(res,columns=["grp","n","slope","t","m_topq"])
    # 4) 22-23 close-hour strength by coin and year: return 21->23 close
    s=A[A.hc==21].dropna(subset=["f2"])
    out["late_2h_coin"]=s.groupby("coin").f2.apply(tt).unstack()
    out["late_2h_yr"]=s.groupby("yr").f2.apply(tt).unstack()
    return out
