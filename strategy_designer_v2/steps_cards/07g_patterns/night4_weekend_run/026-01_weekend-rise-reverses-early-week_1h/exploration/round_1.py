def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wk = []; hr = []; d24 = []; mid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"])
            b = b.reset_index(drop=True)
            c = b["close"].values; ts = b["timestamp"]
            n = len(b)
            # hourly returns
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            hh = pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r":r1})
            # vol: abs mean of last 168 hourly returns
            lr = pd.Series(r1).shift(1)
            hh["vol"] = lr.abs().rolling(168, min_periods=100).mean().values
            hr.append(hh)
            # weekend & midweek
            idx = {t:i for i,t in enumerate(ts)}
            for i in range(n):
                t = ts.iloc[i]
                if t.hour==0 and t.weekday() in (0,2):  # Mon00 or Wed00 open bar -> use close of previous bar
                    j0 = idx.get(t - pd.Timedelta(hours=49)); jm = i-1
                    if j0 is None or jm<0 or ts.iloc[jm]!=t-pd.Timedelta(hours=1): continue
                    je = jm+48
                    if je>=n or ts.iloc[je]!=ts.iloc[jm]+pd.Timedelta(hours=48): continue
                    past = c[jm]/c[j0]-1; fut = c[je]/c[jm]-1
                    (wk if t.weekday()==0 else mid).append((coin,past,fut))
            # 24h grid
            g = np.arange(0, n-24, 24)
            if len(g)>2:
                f = c[g+24]/c[g]-1
                p = np.r_[np.nan, c[g[1:]]/c[g[1:]-24]-1] if len(g)>1 else np.nan
                d24.append(pd.DataFrame({"coin":coin,"past":p,"fut":f,"vol":hh["vol"].values[g]}))
    def reg(lst,name):
        df = pd.DataFrame(lst, columns=["coin","past","fut"])
        df["z"] = df.groupby("coin")["past"].transform(lambda x: x/x.abs().mean())
        df["fz"] = df.groupby("coin")["fut"].transform(lambda x: (x-x.mean())/x.std())
        s = stats.linregress(df["z"], df["fz"])
        df["q"] = pd.qcut(df["z"],5,labels=False)
        g = df.groupby("q")["fz"].agg(["mean","count"])
        g["t"] = g["mean"]/(df.groupby("q")["fz"].std()/np.sqrt(g["count"]))
        out[name+" slope fz on z (slope,t,n)"] = f"{s.slope:.4f}, t={s.slope/s.stderr:.2f}, n={len(df)}"
        out[name+" by quintile of past"] = g
        pc = df.groupby("coin").apply(lambda d: pd.Series({"slope":stats.linregress(d.z,d.fz).slope,"t":stats.linregress(d.z,d.fz).slope/stats.linregress(d.z,d.fz).stderr,"n":len(d)}))
        out[name+" per coin"] = pc
    reg(wk,"weekend->MonTue"); reg(mid,"MonTue->WedThu")
    H = pd.concat(hr).dropna(subset=["r"])
    H["rz"] = H.groupby("coin")["r"].transform(lambda x:(x-x.mean())/x.std())
    gh = H.groupby("hour")["rz"].agg(["mean","std","count"]); gh["t"]=gh["mean"]/(gh["std"]/np.sqrt(gh["count"]))
    out["hourly z-return by hour"] = gh[["mean","t","count"]]
    gw = H.groupby("wd")["rz"].agg(["mean","std","count"]); gw["t"]=gw["mean"]/(gw["std"]/np.sqrt(gw["count"]))
    out["hourly z-return by weekday"] = gw[["mean","t","count"]]
    D = pd.concat(d24).dropna()
    D["z"] = D["past"]/D["vol"]/24
    D["fz"] = D.groupby("coin")["fut"].transform(lambda x:(x-x.mean())/x.std())
    D["vq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    rows = {}
    for v,g in D.groupby("vq"):
        s = stats.linregress(g.z,g.fz); rows[v]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(g)}
    s = stats.linregress(D.z,D.fz); rows["all"]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(D)}
    out["24h fut on 24h past z, by vol tercile"] = pd.DataFrame(rows).T
    # book days by weekday
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["wd"]=pd.to_datetime(d["day"]).dt.weekday; d["coin"]=coin; bd.append(d)
    B = pd.concat(bd).dropna(subset=["book_return"])
    gb = B.groupby("wd")[["book_return","coin_return"]].mean()
    out["book & coin mean daily return by weekday"] = gb
    return out
