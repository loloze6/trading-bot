def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []; hrows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp","close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"].values; ts = d["timestamp"]
            n = len(d)
            # hourly returns
            hr = pd.Series(c).pct_change().shift(-1)
            hh = pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r1":hr})
            hrows.append(hh)
            closet = ts + pd.Timedelta(hours=1)
            idx = np.where(closet.dt.hour.values == 0)[0]
            for i in idx:
                if i-48 < 0 or i+48 >= n: continue
                if (ts[i]-ts[i-48]) != pd.Timedelta(hours=48) or (ts[i+48]-ts[i]) != pd.Timedelta(hours=48): continue
                rows.append(dict(coin=coin, w=w, wd=closet[i].weekday(),
                    p24=c[i]/c[i-24]-1, p48=c[i]/c[i-48]-1,
                    f24=c[i+24]/c[i]-1, f48=c[i+48]/c[i]-1,
                    vol=np.std(np.diff(np.log(c[max(0,i-168):i+1])))))
    R = pd.DataFrame(rows)
    sd = R.groupby("coin")["f24"].transform("std")
    R["drift24"] = R.groupby("coin")["f24"].transform("mean")
    R["drift48"] = R.groupby("coin")["f48"].transform("mean")
    R["u24"] = (R.f24-R.drift24)/sd; R["u48"]=(R.f48-R.drift48)/sd
    R["z24"] = R.p24/sd; R["z48"]=R.p48/sd
    out = {}
    def reg(g, x, y):
        g = g[[x,y]].dropna()
        s = stats.linregress(g[x], g[y])
        return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr,
                          "fade_mean":(-np.sign(g[x])*g[y]).mean()})
    out["by_startday_p24_f24 (0=Mon)"] = R.groupby("wd").apply(lambda g: reg(g,"z24","u24"))
    out["by_startday_p24_f48"] = R.groupby("wd").apply(lambda g: reg(g,"z24","u48"))
    out["by_startday_p48_f48"] = R.groupby("wd").apply(lambda g: reg(g,"z48","u48"))
    M = R[R.wd==0].copy()
    out["monday_by_coin"] = M.groupby("coin").apply(lambda g: reg(g,"z24","u24"))
    M["vt"] = M.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    out["monday_by_vol_tercile"] = M.groupby("vt").apply(lambda g: reg(g,"z24","u24"))
    M["zq"] = pd.qcut(M.z24,5,labels=False)
    out["monday_quintile_mean_u24"] = M.groupby("zq")[["z24","u24"]].agg(["mean","count"])
    M["yr"]=0
    out["monday_by_window_slope_sign"] = pd.Series({"windows_pos":(M.groupby("w").apply(lambda g: reg(g,"z24","u24")["slope"])>0).sum(),"windows":M.w.nunique()})
    H = pd.concat(hrows).dropna()
    H["z"] = H.r1/H.groupby("coin")["r1"].transform("std")
    hs = H.groupby("hour")["z"].agg(["mean","count","std"]); hs["t"]=hs["mean"]/(hs["std"]/np.sqrt(hs["count"]))
    out["hour_mean_std_return"] = hs
    ws = H.groupby("wd")["z"].agg(["mean","count","std"]); ws["t"]=ws["mean"]/(ws["std"]/np.sqrt(ws["count"]))
    out["weekday_mean_std_hourly"] = ws
    # book daily by weekday
    D=[]
    for coin in days:
        for w,df in days[coin].items():
            x=df.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; D.append(x)
    D=pd.concat(D)
    bk = D.groupby("day").agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    bk["wd"]=pd.to_datetime(bk.index).weekday
    out["book_by_weekday"]=bk.groupby("wd")[["br","cr"]].mean()
    return out
