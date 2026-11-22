def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    H = []   # hourly
    M = []   # midnight cases
    D = []   # daily
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df[["timestamp","close","volume"]].copy()
            df["ts"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df.sort_values("ts").reset_index(drop=True)
            c = df["close"].values
            r1 = pd.Series(c).pct_change().values
            # vol of 1h returns over past 720 bars
            vol = pd.Series(r1).rolling(720, min_periods=200).std().values
            prev1 = np.r_[np.nan, r1[:-1]]
            prevvol = np.r_[np.nan, vol[:-1]]
            h = pd.DataFrame({"coin":coin,"w":w,"hour":df["ts"].dt.hour,"wd":df["ts"].dt.weekday,
                              "r":r1,"zprev":prev1/prevvol,"vol":vol})
            H.append(h)
            # bars whose close is midnight: start hour 23
            idx = np.where(df["ts"].dt.hour.values==23)[0]
            n=len(c)
            vol48 = pd.Series(c).pct_change(48).abs().rolling(720, min_periods=200).mean().values
            vmean = pd.Series(df["volume"].values).rolling(48).mean().values
            vbase = pd.Series(df["volume"].values).shift(49).rolling(120).mean().values
            for i in idx:
                if i-48<0 or i+48>=n: continue
                p = c[i]/c[i-48]-1; f = c[i+48]/c[i]-1
                f24 = c[i+24]/c[i]-1
                M.append((coin,w,(df["ts"].iloc[i]+pd.Timedelta(hours=1)).weekday(),p,f,f24,
                          vol48[i], vbase[i]/vmean[i] if vmean[i]>0 else np.nan))
        for w, dd in days[coin].items():
            dd = dd.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday; dd["coin"]=coin
            D.append(dd[["coin","wd","coin_return","book_return"]])
    H = pd.concat(H); D = pd.concat(D)
    M = pd.DataFrame(M, columns=["coin","w","nextwd","past","fut","fut24","vol48","thin"])
    drift = M.groupby("coin")["fut"].transform("mean")
    M["z"] = M["past"]/M["vol48"]; M["u"] = M["fut"]-drift
    def tt(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"n":len(x)})
    out["hour_1h_ret"] = H.groupby("hour")["r"].apply(tt).unstack()
    out["weekday_daily_ret"] = D.groupby("wd")["coin_return"].apply(tt).unstack()
    out["weekday_book_ret"] = D.groupby("wd")["book_return"].apply(tt).unstack()
    # reversal by weekday of the following day: slope of 48h future unusual on z of past 48h
    rows={}
    for wd,g in M.dropna(subset=["z","u"]).groupby("nextwd"):
        s=stats.linregress(g["z"],g["u"]); rows[wd]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(g),
            "corr":s.rvalue}
    out["rev48_by_nextday"]=pd.DataFrame(rows).T
    # weekend cases (next day Monday) by thinness tercile: corr
    g=M[(M.nextwd==0)].dropna(subset=["z","u","thin"]).copy()
    g["tq"]=pd.qcut(g["thin"],3,labels=False)
    rr={}
    for q,gg in g.groupby("tq"):
        s=stats.linregress(gg["z"],gg["u"]); rr[q]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(gg),"thin_mean":gg["thin"].mean()}
    out["monday_rev_by_thin"]=pd.DataFrame(rr).T
    # z quintile, all days, signed future
    a=M.dropna(subset=["z","u"]).copy(); a["zq"]=pd.qcut(a["z"],5,labels=False)
    out["fut48_by_pastz_q_alldays"]=a.groupby("zq")["u"].apply(tt).unstack()
    # 1h after 1h moves
    hh=H.dropna(subset=["zprev","r"]).copy(); hh["q"]=pd.qcut(hh["zprev"],10,labels=False)
    out["next1h_by_prev1h_decile"]=hh.groupby("q")["r"].apply(tt).unstack()
    # vol level tercile vs next 1h ret
    hh["vq"]=hh.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["1h_ret_by_vol_tercile"]=hh.groupby("vq")["r"].apply(tt).unstack()
    out["weekday_by_coin_t"]=D.groupby(["coin","wd"])["coin_return"].apply(lambda x:x.mean()/(x.std()/np.sqrt(x.count()))).unstack()
    return out
