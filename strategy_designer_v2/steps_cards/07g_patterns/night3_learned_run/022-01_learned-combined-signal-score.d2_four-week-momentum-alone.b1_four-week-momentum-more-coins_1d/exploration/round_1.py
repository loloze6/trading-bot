def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            s = pd.Series(c)
            lr = pd.Series(r1)
            vol20 = lr.rolling(20, min_periods=15).std().values
            mom28 = (s/s.shift(28)-1).values
            mom7 = (s/s.shift(7)-1).values
            mom84 = (s/s.shift(84)-1).values
            near = (s/s.rolling(56, min_periods=40).max()-1).values
            r3 = (s/s.shift(3)-1).values
            fc = b["debug_info.components.mom28.post_pipeline_value"].values if "debug_info.components.mom28.post_pipeline_value" in b else np.full(n, np.nan)
            alloc = b["postRebalance_current_allocation"].astype(float).values
            for h in (5, 10, 20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i+h]/c[i]-1, r1=r1[i], r3=r3[i],
                                     vol=vol20[i]/ (np.nanmedian(vol20) if np.isfinite(np.nanmedian(vol20)) else np.nan),
                                     volabs=vol20[i], mom28=mom28[i], mom7=mom7[i], mom84=mom84[i], near=near[i],
                                     fc=fc[i], alloc=alloc[i], wd=ts[i].dayofweek, yr=ts[i].year))
    df = pd.DataFrame(rows)
    # coin-level drift and usual move per h
    g = df.groupby(["coin","h"])["fwd"]
    df["ex"] = df["fwd"] - g.transform("mean")
    df["z"] = df["ex"] / g.transform("std")
    out = {}
    def slope(sub, x):
        s = sub[[x,"z"]].dropna()
        if len(s) < 50: return (np.nan, np.nan, len(s))
        xs = (s[x]-s[x].mean())/s[x].std()
        r = stats.linregress(xs, s["z"])
        return (r.slope, r.slope/r.stderr, len(s))
    res = []
    for h in (5,10,20):
        sub = df[df.h==h]
        for x in ["fc","mom7","mom28","mom84","near","r1","r3","vol","volabs"]:
            sl,t,nn = slope(sub,x); res.append(dict(h=h,x=x,slope_z_per_sd=sl,t=t,n=nn))
    out["slopes_strength_per_sd"] = pd.DataFrame(res)
    s5 = df[df.h==5].copy()
    def quint(x, lab):
        s = s5[[x,"ex","z"]].dropna().copy()
        s["q"] = pd.qcut(s[x].rank(method="first"), 5, labels=False)
        a = s.groupby("q").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_z=("z","mean"), xmean=(x,"mean"))
        a["t"] = s.groupby("q")["ex"].apply(lambda v: v.mean()/(v.std()/np.sqrt(len(v))))
        out[lab] = a
    quint("fc","q_forecast_5d"); quint("r1","q_r1_5d"); quint("vol","q_relvol_5d"); quint("near","q_near56_5d"); quint("mom84","q_mom84_5d")
    # mom28 slope by vol tercile
    s = s5.dropna(subset=["vol","mom28"]).copy()
    s["vt"] = pd.qcut(s["vol"].rank(method="first"),3,labels=["lowvol","mid","highvol"])
    out["mom28_by_vol"] = pd.DataFrame({k: slope(v,"mom28") for k,v in s.groupby("vt")}, index=["slope","t","n"]).T
    # mom28 slope by sign of mom84 (regime)
    s = s5.dropna(subset=["mom84","mom28"]).copy()
    s["reg"] = np.where(s.mom84>0,"up84","down84")
    out["mom28_by_mom84sign"] = pd.DataFrame({k: slope(v,"mom28") for k,v in s.groupby("reg")}, index=["slope","t","n"]).T
    out["weekday_5d"] = s5.groupby("wd")["z"].agg(["size","mean"])
    out["fc_slope_by_year"] = pd.DataFrame({k: slope(v,"fc") for k,v in s5.groupby("yr")}, index=["slope","t","n"]).T
    # book long vs short gain on daily
    lg=[];sg=[]
    tot=[]
    for coin,wins in bars.items():
        for w,b in wins.items():
            c=b["close"].astype(float).values; a=b["postRebalance_current_allocation"].astype(float).values
            g_=a[:-1]*(c[1:]/c[:-1]-1)
            tot.append(pd.DataFrame(dict(g=g_, a=a[:-1])))
    T=pd.concat(tot)
    out["pos_gain_by_side"]=T.assign(side=np.sign(T.a)).groupby("side")["g"].agg(["size","mean","sum"])
    # book days: after largest gains/losses
    D=[]
    for coin,wins in days.items():
        for w,d in wins.items():
            d=d.reset_index(drop=True)
            D.append(pd.DataFrame(dict(br=d.book_return, nbr=d.book_return.shift(-1), nbr5=d.book_return[::-1].rolling(5).sum()[::-1].shift(-1), cr=d.coin_return)))
    D=pd.concat(D).dropna()
    D["q"]=pd.qcut(D.br.rank(method="first"),10,labels=False)
    out["book_after_decile"]=D.groupby("q")[["br","nbr","nbr5"]].mean()
    return out
