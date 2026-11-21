def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; rows72 = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; n = len(c)
            if n < 150: continue
            ts = pd.to_datetime(df["timestamp"])
            hour = ts.dt.hour.values; wd = ts.dt.weekday.values; yr = ts.dt.year.values
            fc = df["forecast"].astype(float).values
            r1 = pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1])
            vol20 = r1.rolling(20, min_periods=20).std().values
            vs42 = pd.Series(c).pct_change(42).values/(vol20*np.sqrt(42))
            r = r1.values
            for t in range(1, n):
                rows.append((coin, w, yr[t-1], wd[t-1], hour[t-1], r[t]))
            for H in (72, 108):
                for t in range(0, n-H, H):
                    rows72.append((coin, w, H, yr[t], c[t+H]/c[t]-1, fc[t], vs42[t]))
    A = pd.DataFrame(rows, columns=["coin","w","yr","wd","hour","r"])
    A["z"] = A["r"]/A.groupby("coin")["r"].transform("std")
    out = {}
    def tt(g, col="z"):
        return g.agg(m=(col,"mean"), sd=(col,"std"), n=(col,"size")).assign(t=lambda x: x.m/(x.sd/np.sqrt(x.n)))
    # A: return of bar starting at given hour (realised during that bar); exz relative to coin mean
    A["ex"] = A["r"] - A.groupby("coin")["r"].transform("mean")
    A["exz"] = A["ex"]/A.groupby("coin")["r"].transform("std")
    h16 = A[A.hour==16]; h20 = A[A.hour==20]
    out["bar16_by_coin"] = tt(h16.groupby("coin"), "exz")
    out["bar16_by_year"] = tt(h16.groupby("yr"), "exz")
    out["bar20_by_year"] = tt(h20.groupby("yr"), "exz")
    fri = A[A.wd==4]
    out["friday_by_hour"] = tt(fri.groupby("hour"), "ex")
    # daily Friday from days table
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["wd"] = pd.to_datetime(x["day"]).dt.weekday; x["yr"] = pd.to_datetime(x["day"]).dt.year
            dd.append(x[["coin","wd","yr","coin_return","book_return"]])
    Dd = pd.concat(dd).dropna(subset=["coin_return"])
    Dd["ex"] = Dd["coin_return"] - Dd.groupby("coin")["coin_return"].transform("mean")
    out["day_by_weekday"] = tt(Dd.groupby("wd"), "ex")
    f = Dd[Dd.wd==4]
    out["friday_by_coin"] = tt(f.groupby("coin"), "ex")
    out["friday_by_year"] = tt(f.groupby("yr"), "ex")
    # long horizon momentum
    M = pd.DataFrame(rows72, columns=["coin","w","H","yr","fwd","fc","vs42"]).dropna()
    M["ex"] = M["fwd"] - M.groupby(["coin","H"])["fwd"].transform("mean")
    M["usual"] = M.groupby(["coin","H"])["fwd"].transform("std")
    M["sz"] = np.sign(M["fc"])*M["ex"]
    M["szz"] = M["sz"]/M["usual"]
    res = []
    for H, g in M.groupby("H"):
        s = stats.linregress(g["vs42"], g["ex"]); s2 = stats.linregress(g["fc"], g["ex"])
        res.append((H, len(g), s.slope/s.stderr, s2.slope/s2.stderr, g["sz"].mean(), g["szz"].mean()))
    out["mom_long"] = pd.DataFrame(res, columns=["H","n","t_raw","t_fc","unusual","strength"])
    g = M[M.H==72]
    out["mom72_by_coin"] = tt(g.groupby("coin"), "szz")
    out["mom72_by_year"] = tt(g.groupby("yr"), "szz")
    g = g.copy(); g["q"] = pd.qcut(g["vs42"].rank(method="first"), 5, labels=False)
    out["mom72_rawvs_quintile"] = g.groupby("q").agg(vs=("vs42","mean"), ex=("ex","mean"), sd=("ex","std"), n=("ex","size")).assign(t=lambda x: x.ex/(x.sd/np.sqrt(x.n)))
    return out
