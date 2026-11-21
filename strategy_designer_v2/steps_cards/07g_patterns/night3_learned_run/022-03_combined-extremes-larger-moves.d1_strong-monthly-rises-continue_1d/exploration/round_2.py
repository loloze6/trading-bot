def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows, drows = [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol20 = pd.Series(lr).rolling(20, min_periods=10).std().values
            vol60 = pd.Series(lr).rolling(60, min_periods=20).std().values
            fc = b["forecast"].values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, fwd1=c[i+1]/c[i]-1,
                                 fc=fc[i], r1=ret1[i], vol=vol20[i], vr=vol20[i]/vol60[i] if vol60[i] else np.nan,
                                 wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
            for i in range(1, n):
                drows.append(dict(coin=coin, w=w, r=ret1[i], prev=ret1[i-1], wd=ts.iloc[i].weekday(),
                                  yr=ts.iloc[i].year, vol=vol20[i-1]))
    df = pd.DataFrame(rows)
    dr = pd.DataFrame(drows).dropna()
    df["adj"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["sd"] = df.groupby("coin")["fwd"].transform("std")
    dr["adj"] = dr["r"] - dr.groupby("coin")["r"].transform("mean")
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    # 1. daily return by weekday (each day once), overall, per coin, per half
    out["daily_by_wd"] = dr.groupby("wd")["adj"].apply(tt).unstack().round(5)
    dr["half"] = np.where(dr["yr"] <= 2021, "y18_21", "y22_25")
    out["daily_wd_by_half_t"] = dr.groupby(["half", "wd"])["adj"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).unstack().round(2)
    out["daily_wd_by_coin_t"] = dr.groupby(["coin", "wd"])["adj"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).unstack().round(2)
    # 2. previous-day return -> next day (each day once), standardised by vol
    dr["z1"] = dr["prev"] / dr["vol"]
    dr["zq"] = dr.groupby("coin")["z1"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["next_day_by_prevday_decile"] = dr.groupby("zq")["adj"].apply(tt).unstack().round(5)
    res = []
    for coin, d in dr.groupby("coin"):
        d = d.dropna(subset=["z1"]); s = stats.linregress(d["z1"], d["adj"]); res.append(dict(coin=coin, slope=s.slope, t=s.slope/s.stderr, n=len(d)))
    out["next_day_on_z1_per_coin"] = pd.DataFrame(res).round(5)
    # 3. forecast slope within vol terciles and within vol-ratio terciles (5-day grid)
    for k in ["vol", "vr"]:
        df[k+"_t"] = df.groupby("coin")[k].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
        res = []
        for q, d in df.dropna(subset=[k+"_t", "adj", "fc"]).groupby(k+"_t"):
            s = stats.linregress(d["fc"], d["adj"])
            on = d[d.fc > 0]["adj"]
            res.append(dict(q=q, n=len(d), slope=s.slope, t=s.slope/s.stderr, on_mean=on.mean(), on_n=len(on)))
        out["fc_slope_by_"+k+"_tercile"] = pd.DataFrame(res).round(5)
    # fc slope by year
    res = []
    for y, d in df.dropna(subset=["adj", "fc"]).groupby("yr"):
        s = stats.linregress(d["fc"], d["adj"]); res.append(dict(yr=y, slope=s.slope, t=s.slope/s.stderr, n=len(d)))
    out["fc_slope_by_year"] = pd.DataFrame(res).round(5)
    # 4. book returns: share of book gain by top days, by weekday
    bl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.dropna(subset=["book_return"])
            bl.append(d.assign(coin=coin, wd=pd.to_datetime(d["day"]).dt.weekday))
    bl = pd.concat(bl)
    out["book_by_wd"] = bl.groupby("wd")["book_return"].apply(tt).unstack().round(5)
    srt = bl["book_return"].sort_values(ascending=False).values
    out["book_total_and_top1pct_share"] = pd.Series({"sum": srt.sum(), "top1pct_sum": srt[:len(srt)//100].sum(), "bottom1pct_sum": srt[-len(srt)//100:].sum()}).round(4)
    return out
