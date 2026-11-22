def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            cs = b["close"].astype(float)
            c = cs.values; n = len(c)
            r = cs.pct_change()
            sd = r.rolling(20, min_periods=20).std().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(n), "z": (r / sd).values,
                               "ret90": cs.pct_change(90).values, "reg": b["regime"].values,
                               "yr": ts.dt.year.values, "wd_own": ts.dt.weekday.values, "r": r.values,
                               "dkey": (ts.astype("int64") // 86400000000000).values})
            for h in (5, 10, 20):
                f = np.full(n, np.nan); f[:n-h] = c[h:] / c[:n-h] - 1; df[f"f{h}"] = f
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["down"] = A["reg"] == "mean_reversion"
    drift = {h: A[A["i"] % h == 0].groupby("coin")[f"f{h}"].mean() for h in (5, 10, 20)}
    def cases(mask, h):
        S = A[mask & A[f"f{h}"].notna()].copy()
        S["cell"] = S["i"] // h
        S = S.groupby(["coin", "w", "cell"]).head(1)
        S["u"] = S[f"f{h}"] - S["coin"].map(drift[h])
        return S
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # graded big up days in risers, finer bins
    res = []
    for h in (5, 10, 20):
        for lo, hi in [(1, 1.5), (1.5, 2), (2, 2.5), (2.5, 3), (3, 99)]:
            for d in (False, True):
                s = summ(cases((A["z"] >= lo) & (A["z"] < hi) & (A["down"] == d), h)["u"])
                s["h"] = h; s["z"] = f"{lo}-{hi}"; s["down"] = d; res.append(s)
    out["fine_z"] = pd.DataFrame(res)
    # z>=2 in risers: per coin, per year (5d and 20d)
    res = []
    for h in (5, 20):
        S = cases((A["z"] >= 2) & (~A["down"]), h)
        for k, g in S.groupby("coin"):
            s = summ(g["u"]); s["h"] = h; s["by"] = k; res.append(s)
        for k, g in S.groupby("yr"):
            s = summ(g["u"]); s["h"] = h; s["by"] = str(k); res.append(s)
    out["bigup_riser_by_coin_year"] = pd.DataFrame(res)
    # slope of 5d/20d unusual on z among up days in risers, and on ret90 among z>=1.5
    res = []
    for h in (5, 20):
        S = cases((A["z"] > 0) & (~A["down"]), h)
        sl = stats.linregress(S["z"], S["u"]); res.append(pd.Series({"h": h, "x": "z|z>0,riser", "slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(S)}))
        S = cases((A["z"] > 0) & (A["down"]), h)
        sl = stats.linregress(S["z"], S["u"]); res.append(pd.Series({"h": h, "x": "z|z>0,faller", "slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(S)}))
        S = cases((A["z"] >= 1.5) & A["ret90"].notna(), h)
        sl = stats.linregress(S["ret90"], S["u"]); res.append(pd.Series({"h": h, "x": "ret90|z>=1.5", "slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(S)}))
    out["slopes"] = pd.DataFrame(res)
    # weekday of the day's own return, averaged over coins per day first (cluster by day)
    dd = A.dropna(subset=["r"]).groupby(["dkey", "wd_own", "yr"])["r"].mean().reset_index()
    out["weekday_own_dayavg"] = dd.groupby("wd_own")["r"].apply(summ).unstack()
    res = []
    for y, g in dd.groupby("yr"):
        for wd in (4, 5, 6, 0):
            s = summ(g[g["wd_own"] == wd]["r"]); s["yr"] = y; s["wd"] = wd; res.append(s)
    out["weekday_own_by_year"] = pd.DataFrame(res)
    out["weekday_own_by_coin_t"] = A.dropna(subset=["r"]).groupby(["coin", "wd_own"])["r"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))).unstack()
    return out
