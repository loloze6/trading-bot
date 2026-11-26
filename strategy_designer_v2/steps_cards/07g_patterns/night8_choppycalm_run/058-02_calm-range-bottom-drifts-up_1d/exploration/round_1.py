def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 5-bar return over all windows (grid)
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr)
        sd = np.std(allr, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = (b["close"] - lo) / (hi - lo) * 2 - 1
            r5 = b["close"].shift(-H) / b["close"] - 1
            r1 = b["close"] / b["close"].shift(1) - 1
            r5p = b["close"] / b["close"].shift(5) - 1
            tr60 = b["close"] / b["close"].shift(60) - 1
            vol20 = r1.rolling(20).std()
            n = len(b)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i], pos=pos.iloc[i],
                                 ex=r5.iloc[i] - drift, exs=(r5.iloc[i] - drift) / sd,
                                 prof=b["regime"].iloc[i] == "unknown", r1=r1.iloc[i], r5p=r5p.iloc[i],
                                 tr60=tr60.iloc[i], vol20=vol20.iloc[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows).dropna(subset=["pos", "ex"])
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")
    def summ(g):
        d = g.groupby("day")["ex"].sum()
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) * 1 if len(d) > 2 else np.nan
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t_day=t, strength=g["exs"].mean()))
    df["posq"] = pd.cut(df["pos"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out = {}
    out["profile_by_pos"] = df[df.prof].groupby("posq").apply(summ)
    out["nonprofile_by_pos"] = df[~df.prof].groupby("posq").apply(summ)
    np_ = df[~df.prof].dropna(subset=["tr60"]).copy()
    np_["trend"] = pd.cut(np_["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["nonprof_trend_pos"] = np_.groupby(["trend", "posq"]).apply(summ)
    df["r5q"] = pd.qcut(df["r5p"], 5)
    out["past5_quint_all"] = df.dropna(subset=["r5p"]).groupby("r5q").apply(summ)
    out["past5_quint_prof"] = df[df.prof].dropna(subset=["r5p"]).groupby("r5q").apply(summ)
    out["prof_low_by_window"] = df[df.prof & (df.pos < -0.2)].groupby("w").apply(summ)
    out["prof_low_by_coin"] = df[df.prof & (df.pos < -0.2)].groupby("coin").apply(summ)
    for k in ["profile_by_pos", "nonprofile_by_pos"]:
        sub = df[df.prof] if k.startswith("profile") else df[~df.prof]
        s = stats.linregress(sub["pos"], sub["ex"])
        out[k + "_slope_on_pos"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(sub)}"
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            days.append(d.assign(coin=coin, w=w))
    D = pd.concat(days)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    return out
