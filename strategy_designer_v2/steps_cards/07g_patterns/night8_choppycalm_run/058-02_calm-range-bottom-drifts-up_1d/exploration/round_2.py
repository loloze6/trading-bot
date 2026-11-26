def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); sd = np.std(allr, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = (b["close"] - lo) / (hi - lo) * 2 - 1
            r5 = b["close"].shift(-H) / b["close"] - 1
            r1 = b["close"] / b["close"].shift(1) - 1
            tr60 = b["close"] / b["close"].shift(60) - 1
            v30 = r1.rolling(30).std()
            vpct = v30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i], pos=pos.iloc[i],
                                 ex=r5.iloc[i] - drift, exs=(r5.iloc[i] - drift) / sd,
                                 prof=b["regime"].iloc[i] == "unknown", tr60=tr60.iloc[i], vpct=vpct.iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=["pos", "ex", "tr60"])
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")
    df["trend"] = pd.cut(df["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    df["agit"] = np.where(df["vpct"] > 0.5, "agit", np.where(df["vpct"].notna(), "calm", "na"))
    def reg(g):
        if len(g) < 20: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["pos"], g["ex"])
        lo = g[g.pos < -0.2]["ex"]; hi = g[g.pos > 0.2]["ex"]
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              low_mean=lo.mean(), n_low=len(lo), high_mean=hi.mean(), n_high=len(hi)))
    out = {}
    out["slope_by_trend_agit"] = df.groupby(["trend", "agit"]).apply(reg)
    out["slope_by_window_all"] = df.groupby("w").apply(reg)
    out["slope_by_coin_all"] = df.groupby("coin").apply(reg)
    out["prof_slope_by_coin"] = df[df.prof].groupby("coin").apply(reg)
    out["prof_slope_by_window"] = df[df.prof].groupby("w").apply(reg)
    fa = df[(df.trend == "fall") & (df.agit == "agit") & (df.pos < 0)]
    d = fa.groupby("day")["ex"].sum()
    out["fall_agit_lower_half"] = f"n {len(fa)} mean {fa.ex.mean():.4f} t_day {d.mean()/(d.std()/np.sqrt(len(d))):.2f} days {len(d)}"
    D = pd.concat([d_.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d_ in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    D["fs"] = D["wd"].isin([4, 5])
    g = D.dropna(subset=["coin_return"]).groupby(["yr", "fs"])["coin_return"].mean().unstack()
    out["fri_sat_vs_rest_by_year"] = g
    return out
