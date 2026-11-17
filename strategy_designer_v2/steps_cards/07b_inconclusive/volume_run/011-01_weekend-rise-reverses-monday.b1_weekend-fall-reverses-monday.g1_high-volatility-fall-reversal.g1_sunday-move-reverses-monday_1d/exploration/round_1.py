def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allrows = []
    for coin, wins in bars.items():
        # coin mean daily return over all windows
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
            z = r/sd
            nxt = c.shift(-1)/c - 1 - mu
            ts = pd.to_datetime(df["timestamp"])
            vr = df["volume"]/df["volume"].rolling(20).mean()
            yr = ts.dt.year
            d = pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"z":z,"nxt":nxt,"vr":vr,"yr":yr,
                              "fc":df["forecast"],"reg":df["regime"],
                              "vol":df.get("debug_info.components.sunday_volume.last_history_value")})
            allrows.append(d)
    A = pd.concat(allrows).dropna(subset=["z","nxt"])
    S = A[A.reg=="mean_reversion"].copy()
    def slope(x,y):
        m = x.notna()&y.notna()
        x=x[m];y=y[m]
        if len(x)<10: return (np.nan,np.nan,len(x))
        res = stats.linregress(x,y)
        return (res.slope, res.slope/res.stderr, len(x))
    out={}
    # reversal of -z on next day by weekday of the bar
    t=[]
    for wd,g in A.groupby("wd"):
        b,tt,n = slope(-g.z,g.nxt); t.append((wd,b*1e4,tt,n))
    out["by_weekday_bar_slope_of_next_on_minus_z_bp"]=pd.DataFrame(t,columns=["wd","slope_bp","t","n"])
    # Sunday forecast slope by coin
    t=[]
    for k,g in S.groupby("coin"):
        b,tt,n=slope(g.fc,g.nxt); t.append((k,b*1e4,tt,n))
    out["sun_by_coin"]=pd.DataFrame(t,columns=["coin","slope_bp","t","n"])
    t=[]
    for k,g in S.groupby("yr"):
        b,tt,n=slope(g.fc,g.nxt); t.append((k,b*1e4,tt,n))
    out["sun_by_year"]=pd.DataFrame(t,columns=["yr","slope_bp","t","n"])
    # side
    t=[]
    for k,g in S.groupby(np.sign(S.z)):
        b,tt,n=slope(g.fc,g.nxt); t.append((k,b*1e4,tt,n,g.nxt.mean()*1e4))
    out["sun_by_side(sign z)"]=pd.DataFrame(t,columns=["side","slope_bp","t","n","mean_next_bp"])
    # size quintiles of forecast
    S["q"]=pd.qcut(S.fc,5,labels=False,duplicates="drop")
    g=S.groupby("q").agg(n=("nxt","size"),fc=("fc","mean"),next_bp=("nxt",lambda x:x.mean()*1e4),
                         t=("nxt",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    out["sun_fc_quintiles"]=g
    # volume tercile per coin
    S["vt"]=S.groupby("coin")["vr"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    t=[]
    for k,gg in S.groupby("vt"):
        b,tt,n=slope(gg.fc,gg.nxt); t.append((k,b*1e4,tt,n))
    out["sun_by_vol_tercile"]=pd.DataFrame(t,columns=["vt","slope_bp","t","n"])
    # z-slope on sunday, saturday (weekend) for comparison of raw
    return out
