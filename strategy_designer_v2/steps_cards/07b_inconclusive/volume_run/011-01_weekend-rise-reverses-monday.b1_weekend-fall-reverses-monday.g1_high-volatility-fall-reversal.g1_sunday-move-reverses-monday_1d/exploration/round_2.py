def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    allrows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            rs.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            ts = pd.to_datetime(df["timestamp"])
            r2 = c/c.shift(2)-1
            d = pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"z":r/sd,"z2":r2/(sd*np.sqrt(2)),
                              "sd":sd,"n1":c.shift(-1)/c-1-mu,"n2":c.shift(-2)/c-1-2*mu,
                              "fc":df["forecast"],"reg":df["regime"],"yr":ts.dt.year,
                              "sd60":r.rolling(60).std()})
            allrows.append(d)
    A = pd.concat(allrows)
    def slope(x,y):
        m = x.notna()&y.notna(); x=x[m]; y=y[m]
        if len(x)<10: return (np.nan,np.nan,len(x))
        res = stats.linregress(x,y); return (res.slope*1e4, res.slope/res.stderr, len(x))
    out={}
    S = A[A.wd==6].copy()
    out["sun_2day_weekend_z_vs_monday"]=pd.DataFrame([slope(-S.z2,S.n1),slope(-S.z,S.n1),slope(-S.z,S.n2)],
        index=["-z2day->n1","-z->n1","-z->n2(overlap n/a: weekly grid)"],columns=["slope_bp","t","n"])
    # vol regime: sd relative to coin's own sd terciles
    S["vq"]=S.groupby("coin")["sd"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    t=[]
    for k,g in S.groupby("vq"): t.append((k,)+slope(-g.z,g.n1)+(slope(g.fc,g.n1)[0],slope(g.fc,g.n1)[1]))
    out["sun_by_vol_tercile_level"]=pd.DataFrame(t,columns=["vq","slope_z_bp","t_z","n","slope_fc_bp","t_fc"])
    # sign-only effect: mean next by sign, Sunday vs other days
    t=[]
    for wd,g in A.dropna(subset=["z","n1"]).groupby("wd"):
        up=g[g.z>0].n1; dn=g[g.z<0].n1
        tt=stats.ttest_ind(dn,up,equal_var=False)
        t.append((wd,dn.mean()*1e4,up.mean()*1e4,(dn.mean()-up.mean())*1e4,tt.statistic,len(g)))
    out["next_after_down_minus_up_by_wd"]=pd.DataFrame(t,columns=["wd","dn_bp","up_bp","diff_bp","t","n"])
    # sunday |z| buckets: down-minus-up by magnitude
    S2=S.dropna(subset=["z","n1"]).copy()
    S2["m"]=pd.qcut(S2.z.abs(),3,labels=False)
    t=[]
    for k,g in S2.groupby("m"):
        up=g[g.z>0].n1; dn=g[g.z<0].n1; tt=stats.ttest_ind(dn,up,equal_var=False)
        t.append((k,g.z.abs().mean(),(dn.mean()-up.mean())*1e4,tt.statistic,len(g)))
    out["sun_down_minus_up_by_absz_tercile"]=pd.DataFrame(t,columns=["m","absz","diff_bp","t","n"])
    # year group 2018-21 vs 22-25 for Saturday too
    t=[]
    for wd in [5,6]:
        for lab,g in A[A.wd==wd].groupby(A.yr<=2021): t.append((wd,lab)+slope(-g.z,g.n1))
    out["sat_sun_early_late"]=pd.DataFrame(t,columns=["wd","yr<=2021","slope_bp","t","n"])
    return out
