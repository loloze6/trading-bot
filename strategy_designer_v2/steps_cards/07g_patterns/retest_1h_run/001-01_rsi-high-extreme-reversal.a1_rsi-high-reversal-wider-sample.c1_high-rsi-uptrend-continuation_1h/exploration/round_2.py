def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # Build 24h grid with past 24h return, next 24h return, year, regime, 60d return sign
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            idx = np.arange(0, n - 24, 24)
            idx = idx[idx >= 24]
            fr = cl[idx + 24] / cl[idx] - 1
            past = cl[idx] / cl[idx - 24] - 1
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(168).std().values[idx] * np.sqrt(24)
            ret60 = np.full(len(idx), np.nan)
            ok = idx >= 1440
            ret60[ok] = cl[idx[ok]] / cl[idx[ok] - 1440] - 1
            # next 72h return too (same grid start, may overlap -> separate)
            rows.append(pd.DataFrame({"coin": c, "w": w, "year": ts.dt.year.values[idx], "fr": fr, "past": past,
                                      "vol": vol, "reg": b["regime"].values[idx], "ret60": ret60}))
    D = pd.concat(rows).dropna(subset=["fr", "past", "vol"])
    D["ex"] = D["fr"] - D.groupby("coin")["fr"].transform("mean")
    D["pz"] = D["past"] / D["vol"]
    D["exz"] = D["ex"] / D["vol"]
    def slope(s):
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan})
        l = stats.linregress(s["pz"], s["exz"])
        return pd.Series({"n": len(s), "slope": l.slope, "t": l.slope / l.stderr})
    out["rev24_by_coin"] = D.groupby("coin").apply(slope)
    out["rev24_by_year"] = D.groupby("year").apply(slope)
    D["volq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["rev24_by_volq"] = D.groupby("volq").apply(slope)
    out["rev24_by_regime"] = D.groupby("reg").apply(slope)
    D["wn"] = D["w"].str[1:].astype(int)
    D["half"] = np.where(D["wn"] <= 12, "w1-12", "w13-24")
    out["rev24_by_half"] = D.groupby("half").apply(slope)
    # z-scored past quintiles
    D["q"] = pd.qcut(D["pz"].rank(method="first"), 5, labels=False)
    g = D.groupby("q").agg(n=("ex", "size"), mean_pz=("pz", "mean"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    g["t"] = g.mean_ex / (g.sd / np.sqrt(g.n))
    out["rev24_zquint"] = g.drop(columns="sd")

    # Hour 20-21 effect: by coin and by year (hourly returns, every bar)
    hr = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp")
            r = (b["close"].shift(-1) / b["close"] - 1).values
            ts = pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin": c, "r": r, "hour": ts.dt.hour.values, "year": ts.dt.year.values}))
    H = pd.concat(hr).dropna()
    H["eve"] = H["hour"].isin([20, 21])
    def tdiff(s):
        a = s[s.eve].r; bb = s[~s.eve].r
        t = stats.ttest_ind(a, bb, equal_var=False).statistic
        return pd.Series({"n_eve": len(a), "eve_bp": a.mean() * 1e4, "other_bp": bb.mean() * 1e4, "t": t})
    out["eve_by_coin"] = H.groupby("coin").apply(tdiff)
    out["eve_by_year"] = H.groupby("year").apply(tdiff)
    # weekday Fri vs others by year
    return out
