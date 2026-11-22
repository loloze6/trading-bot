def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = []; W = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp", "close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            c = pd.Series(d["close"].values); ts = d["ts"]
            ok1 = (ts - ts.shift(1)) == pd.Timedelta(hours=1)
            r_own = pd.Series(np.where(ok1, c / c.shift(1) - 1, np.nan))  # move of the bar starting at ts
            vol = r_own.rolling(720, min_periods=200).std().shift(1)
            H.append(pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year, "hr": ts.dt.hour, "wd": ts.dt.weekday,
                                   "r": r_own, "z": r_own / vol}))
            def back(k):
                ok = (ts - ts.shift(k)) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, c / c.shift(k) - 1, np.nan))
            def fwd(k):
                ok = (ts.shift(-k) - ts) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, c.shift(-k) / c - 1, np.nan))
            r24 = back(24); f24 = fwd(24); f48 = fwd(48)
            f2 = (1 + f48) / (1 + f24) - 1
            sel = ts.dt.hour == 23
            W.append(pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year, "wd": ts.dt.weekday, "wk": ts.dt.isocalendar().week.values,
                                   "z24": r24 / (vol * np.sqrt(24)), "y24": f24 / (vol * np.sqrt(24)),
                                   "y2": f2 / (vol * np.sqrt(24)), "f24": f24, "f2": f2})[sel])
    H = pd.concat(H).dropna(subset=["z"])
    out = {}
    g = H.groupby("hr")["z"].agg(["mean", "std", "count"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    g["raw_bp"] = H.groupby("hr")["r"].mean() * 1e4
    out["own_bar_move_by_start_hour"] = g[["mean", "t", "raw_bp", "count"]]
    top = g["t"].abs().sort_values(ascending=False).index[:3].tolist()
    for h in top:
        s = H[H.hr == h]
        a = s.groupby("wd")["z"].agg(["mean", "count"]); a["t"] = s.groupby("wd")["z"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        out[f"hour{h}_by_weekday"] = a
        b = s.groupby("yr")["z"].agg(["mean", "count"]); b["t"] = s.groupby("yr")["z"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        b["raw_bp"] = s.groupby("yr")["r"].mean() * 1e4
        out[f"hour{h}_by_year"] = b
        cc = s.groupby("coin")["z"].agg(["mean", "count"]); cc["raw_bp"] = s.groupby("coin")["r"].mean() * 1e4
        out[f"hour{h}_by_coin"] = cc
    A = pd.concat(W).dropna(subset=["z24", "y24", "y2"])
    S = A[A.wd == 5]
    res = []
    for y, s in S.groupby("yr"):
        if len(s) < 30: continue
        r1 = stats.linregress(s.z24, s.y24); r2 = stats.linregress(s.z24, s.y2)
        res.append({"yr": y, "t_sat_to_sun": r1.slope / r1.stderr, "t_sat_to_mon": r2.slope / r2.stderr, "slope_mon": r2.slope, "n": len(s)})
    out["saturday_move_by_year"] = pd.DataFrame(res)
    # one case per week: average across coins to remove cross-coin dependence
    Sw = S.groupby(["w", "yr", "wk"])[["z24", "y24", "y2"]].mean().dropna()
    r1 = stats.linregress(Sw.z24, Sw.y24); r2 = stats.linregress(Sw.z24, Sw.y2)
    out["saturday_weekly_avg_t"] = pd.DataFrame([{"t_sun": r1.slope / r1.stderr, "t_mon": r2.slope / r2.stderr, "slope_mon": r2.slope, "n_weeks": len(Sw)}])
    S = S.copy(); S["q"] = pd.qcut(S.z24, 5, labels=False)
    out["saturday_quintile"] = S.groupby("q").agg(z24=("z24", "mean"), sun_pct=("f24", "mean"), mon_pct=("f2", "mean"), n=("f2", "size"))
    res = []
    for wd in range(7):
        s = A[A.wd == wd]; sw = s.groupby(["w", "yr", "wk"])[["z24", "y2"]].mean().dropna()
        r = stats.linregress(sw.z24, sw.y2); res.append({"wd": wd, "t_dayafter_weekavg": r.slope / r.stderr, "n": len(sw)})
    out["dayafter_by_weekday_weekavg"] = pd.DataFrame(res)
    return out
