def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z, "fwd1": c.shift(-1) / c - 1,
                                      "fwd2_5": c.shift(-5) / c.shift(-1) - 1, "i": np.arange(len(b)),
                                      "yr": ts.dt.year, "wd": ts.dt.weekday}))
    A = pd.concat(rows).dropna(subset=["z", "fwd1"])
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    dn = A[A["z"] < 0]
    sl = stats.linregress(dn["z"], dn["ex1"])
    out["down days: slope next-day ex on z, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(dn)}"
    up = A[A["z"] > 0]
    sl = stats.linregress(up["z"], up["ex1"])
    out["up days: slope next-day ex on z, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(up)}"
    res = {}
    for coin, g in dn.groupby("coin"):
        s = stats.linregress(g["z"], g["ex1"]); res[coin] = s.slope / s.stderr
    out["per coin t, down-day next-day slope"] = pd.Series(res)
    res = {}
    for yr, g in dn.groupby("yr"):
        s = stats.linregress(g["z"], g["ex1"]); res[yr] = s.slope / s.stderr
    out["per year t, down-day next-day slope"] = pd.Series(res)
    A["zb"] = pd.cut(A["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["next-day ex by z bucket"] = A.groupby("zb")["ex1"].agg(["count", "mean", tt])
    # delayed continuation, grid 5, days 2-5 excess
    G = A[A["i"] % 5 == 0].dropna(subset=["fwd2_5"]).copy()
    G["ex25"] = G["fwd2_5"] - G.groupby("coin")["fwd2_5"].transform("mean")
    gu = G[G["z"] > 0]
    sl = stats.linregress(gu["z"], gu["ex25"])
    out["up days: slope days2-5 ex on z, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(gu)}"
    res = {}
    for yr, g in gu.groupby("yr"):
        s = stats.linregress(g["z"], g["ex25"]); res[yr] = s.slope / s.stderr
    out["per year t, up-day days2-5 slope"] = pd.Series(res)
    # weekday: Fri+Sat share of windows positive diff
    D = pd.concat([d.assign(coin=c, w=w) for c in days for w, d in days[c].items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["fs"] = D["wd"].isin([4, 5])
    pw = D.groupby(["coin", "w", "fs"])["coin_return"].mean().unstack()
    diff = pw[True] - pw[False]
    out["Fri+Sat minus other per coin-window: share>0, t, n"] = f"{(diff>0).mean():.3f}, t={tt(diff):.2f}, n={diff.notna().sum()}"
    return out
