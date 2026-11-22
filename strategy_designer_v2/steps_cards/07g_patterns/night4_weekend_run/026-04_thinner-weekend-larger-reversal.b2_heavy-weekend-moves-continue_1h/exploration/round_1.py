def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []      # 48h move ending at 23:00 of each weekday, next 48h return
    hr_rows = []   # hourly returns
    big = []       # after large 24h moves
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r1}))
            # 48h-grid usual move
            g = np.arange(0, n-48, 48)
            # anchors at 23:00
            idx = np.where(ts.dt.hour.values == 23)[0]
            for i in idx:
                if i-168 < 0 or i+48 >= n: continue
                past = c[i]/c[i-48]-1
                fut = c[i+48]/c[i]-1
                volw = v[i-47:i+1].mean(); volb = v[i-167:i-47].mean()
                vr = volw/volb if volb > 0 else np.nan
                past24 = c[i]/c[i-24]-1
                fut24 = c[i+24]/c[i]-1
                rows.append((coin, w, ts.iloc[i].weekday(), past, fut, vr, past24, fut24))
    R = pd.DataFrame(rows, columns=["coin","w","wd","past","fut","vr","past24","fut24"])
    # drift per coin: mean 48h on all anchors (approx)
    drift = R.groupby("coin")["fut"].transform("mean")
    R["u"] = R["fut"] - drift
    R["s"] = np.sign(R["past"]) * R["u"]
    R["heavy"] = R["vr"] > 1
    sd48 = R.groupby("coin")["past"].transform("std")
    R["bigpast"] = R["past"].abs() > sd48
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["signed_next48_by_wd_heavy"] = R.groupby(["wd","heavy"])["s"].apply(tt).unstack()
    out["signed_next48_by_wd_bigmove"] = R.groupby(["wd","bigpast"])["s"].apply(tt).unstack()
    # graded: Sunday by vr tercile
    S = R[R.wd == 6].copy()
    S["vrq"] = pd.qcut(S["vr"], 4, labels=False)
    out["sun_signed_by_vr_quartile"] = S.groupby("vrq")["s"].apply(tt).unstack()
    S["mq"] = pd.qcut(S["past"].abs()/sd48[S.index], 4, labels=False)
    out["sun_signed_by_absmove_quartile"] = S.groupby("mq")["s"].apply(tt).unstack()
    out["sun_signed_by_coin"] = S.groupby("coin")["s"].apply(tt).unstack()
    # weekdays (Mon-Thu anchors) with heavy volume, graded by vr
    Wd = R[R.wd.isin([0,1,2,3])].copy()
    Wd["vrq"] = pd.qcut(Wd["vr"], 4, labels=False)
    out["weekday_signed_by_vr_quartile"] = Wd.groupby("vrq")["s"].apply(tt).unstack()
    # all days pooled, vr quartile (volume-confirmed momentum generally)
    R["vrq"] = pd.qcut(R["vr"], 5, labels=False)
    out["all_signed_by_vr_quintile"] = R.groupby("vrq")["s"].apply(tt).unstack()
    # 24h version: next 24h signed by past 24h, all days, by vr
    R["s24"] = np.sign(R["past24"]) * (R["fut24"] - R.groupby("coin")["fut24"].transform("mean"))
    out["all_s24_by_vr_quintile"] = R.groupby("vrq")["s24"].apply(tt).unstack()
    H = pd.concat(hr_rows)
    H["r"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    out["hourly_by_wd"] = H.groupby("wd")["r"].apply(tt).unstack()
    hh = H.groupby("hour")["r"].apply(tt).unstack()
    out["hourly_by_hour_top_abs_t"] = hh.reindex(hh["t"].abs().sort_values(ascending=False).index).head(8)
    # book daily by weekday
    D = pd.concat([d.assign(coin=c) for c, ws in days.items() for d in ws.values()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_daily_by_wd"] = D.groupby("wd")["book_return"].apply(tt).unstack()
    return out
