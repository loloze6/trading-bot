def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    H = 20
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            logr = np.log(c)
            for i in range(0, n - H, H):
                r = c[i+H]/c[i]-1
                r5 = c[min(i+5, n-1)]/c[i]-1 if i+5 < n else np.nan
                past1 = c[i]/c[i-1]-1 if i>=1 else np.nan
                past5 = c[i]/c[i-5]-1 if i>=5 else np.nan
                past20 = c[i]/c[i-20]-1 if i>=20 else np.nan
                vol20 = np.std(np.diff(logr[max(0,i-20):i+1])) if i>=10 else np.nan
                hi = np.max(c[max(0,i-60):i]) if i>=20 else np.nan
                lo = np.min(c[max(0,i-60):i]) if i>=20 else np.nan
                rng = (c[i]-lo)/(hi-lo) if i>=20 and hi>lo else np.nan
                rows.append(dict(coin=coin, w=w, fc=df["forecast"].iloc[i], r=r,
                                 past1=past1, past5=past5, past20=past20, vol=vol20,
                                 rng=rng, wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                                 alloc=df["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["mean_r"] = g.groupby("coin")["r"].transform("mean")
    g["ex"] = g["r"] - g["mean_r"]
    g["sd"] = g.groupby("coin")["r"].transform("std")
    g["z"] = g["ex"]/g["sd"]
    out["n_grid"] = len(g)
    def qtab(col, q=5):
        d = g.dropna(subset=[col, "z"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q").agg(n=("z","size"), mean_ex=("ex","mean"), mean_z=("z","mean"))
        sl = stats.linregress(d.groupby("coin")[col].transform(lambda s:(s-s.mean())/s.std()), d["z"])
        t["slope_t_pooled"] = sl.slope/sl.stderr
        return t
    for col in ["fc","past1","past5","past20","vol","rng"]:
        out["q_"+col] = qtab(col)
    out["by_year"] = g.groupby("yr").agg(n=("z","size"), mean_ex=("ex","mean"))
    out["by_coin_fc_corr"] = g.dropna(subset=["fc"]).groupby("coin").apply(lambda d: pd.Series({"n":len(d),"corr_fc":d["fc"].corr(d["z"]),"corr_past20":d["past20"].corr(d["z"]),"corr_rng":d["rng"].corr(d["z"])}))
    # daily book: mean across coins per day
    dl = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; dl.append(d)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["weekday_coin_ret"] = D.groupby("wd").agg(n=("coin_return","count"), mean=("coin_return","mean"), t=("coin_return", lambda s: s.mean()/(s.std()/np.sqrt(s.count()))))
    # next-day return after large daily moves (vol-scaled), daily, by sign/size
    D = D.sort_values(["coin","w","day"])
    D["sd60"] = D.groupby(["coin","w"])["coin_return"].transform(lambda s: s.rolling(30, min_periods=15).std().shift(1))
    D["zr"] = D["coin_return"]/D["sd60"]
    D["next5"] = D.groupby(["coin","w"])["close"].transform(lambda s: s.shift(-5)/s - 1)
    D["zb"] = pd.cut(D["zr"], [-99,-2,-1,0,1,2,99])
    out["after_daily_move_next5"] = D.groupby("zb").agg(n=("next5","count"), mean=("next5","mean"), sd=("next5","std"))
    # book: top/bottom days
    B = D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_mean_by_w_share_pos"] = float((D.groupby("w")["book_return"].mean()>0).mean())
    return out
