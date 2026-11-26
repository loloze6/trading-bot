def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "r": r, "sd": sd20,
                               "ret5": c / c.shift(5) - 1, "ret10": c / c.shift(10) - 1,
                               "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1,
                               "fwd3": c.shift(-3) / c - 1,
                               "tr60": c / c.shift(60) - 1,
                               "regime": b["regime"].values,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["calm"] = np.where(A["regime"] == "chop", "agit", "calm")
    A["trend"] = np.where(A["tr60"] > 0.1, "rising", np.where(A["tr60"] < -0.1, "falling", np.where(A["tr60"].notna(), "choppy", "na")))
    out = {}
    def tt(s):
        return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    # calm 5d momentum, grid 5
    g5 = A[A["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    dr = g5.groupby("coin")["fwd5"].mean()
    g5["ex"] = g5["fwd5"] - g5["coin"].map(dr)
    g5 = g5.dropna(subset=["ret5", "sd"])
    g5["m"] = g5["ret5"] / (g5["sd"] * np.sqrt(5))
    res = {}
    for (reg, tr), x in g5.groupby(["calm", "trend"]):
        if len(x) > 20:
            s = stats.linregress(x["m"], x["ex"])
            res[(reg, tr)] = {"n": len(x), "slope": s.slope, "t": s.slope / s.stderr}
    out["5d_mom_slope_by_profile"] = pd.DataFrame(res).T
    c5 = g5[g5["calm"] == "calm"]
    res = {}
    for k, x in c5.groupby("year"):
        if len(x) > 15:
            s = stats.linregress(x["m"], x["ex"])
            res[k] = {"n": len(x), "slope": s.slope, "t": s.slope / s.stderr}
    out["calm_5d_mom_slope_by_year"] = pd.DataFrame(res).T
    res = {}
    for k, x in c5.groupby("coin"):
        s = stats.linregress(x["m"], x["ex"])
        res[k] = {"n": len(x), "slope": s.slope, "t": s.slope / s.stderr}
    out["calm_5d_mom_slope_by_coin"] = pd.DataFrame(res).T
    # 10d past as well
    g5b = g5.dropna(subset=["ret10"]).copy()
    g5b["m10"] = g5b["ret10"] / (g5b["sd"] * np.sqrt(10))
    res = {}
    for reg, x in g5b.groupby("calm"):
        s = stats.linregress(x["m10"], x["ex"])
        res[reg] = {"n": len(x), "slope": s.slope, "t": s.slope / s.stderr}
    out["10d_past_slope_on_5d_fwd"] = pd.DataFrame(res).T
    # agitated 1d: next-day after day z, by trend, grid 1 (1-bar horizon non-overlapping)
    d1 = A.dropna(subset=["fwd1", "r", "sd"]).copy()
    dr1 = d1.groupby("coin")["fwd1"].mean()
    d1["ex"] = d1["fwd1"] - d1["coin"].map(dr1)
    d1["z"] = d1["r"] / d1["sd"]
    res = {}
    for (reg, tr), x in d1.groupby(["calm", "trend"]):
        if len(x) > 50:
            s = stats.linregress(x["z"], x["ex"])
            res[(reg, tr)] = {"n": len(x), "slope": s.slope, "t": s.slope / s.stderr,
                              "ex_up_days": x.loc[x["z"] > 0, "ex"].mean(), "t_up": tt(x.loc[x["z"] > 0, "ex"])}
    out["1d_reversal_slope_by_profile"] = pd.DataFrame(res).T
    ag = d1[(d1["calm"] == "agit") & (d1["z"] > 0)]
    res = {}
    for k, x in ag.groupby("year"):
        res[k] = {"n": len(x), "ex": x["ex"].mean(), "t": tt(x["ex"])}
    out["agit_upday_next_ex_by_year"] = pd.DataFrame(res).T
    return out
