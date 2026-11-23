def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            d["day"] = pd.to_datetime(d["day"])
            d = d.sort_values("day").reset_index(drop=True)
            r = d["coin_return"]
            scale = r.abs().rolling(30, min_periods=20).mean().shift(1)
            df = pd.DataFrame({"coin": coin, "w": w, "wd": d["day"].dt.weekday, "yr": d["day"].dt.year,
                               "r": r, "z": r / scale, "next1": r.shift(-1),
                               "next2": (1 + r.shift(-1)) * (1 + r.shift(-2)) - 1})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["z", "next1"])
    mu = D["next1"].mean()
    D["ex1"] = D["next1"] - mu
    # graded: deciles of z, excess next day
    D["zd"] = pd.qcut(D["z"], 10, labels=False)
    g = D.groupby("zd")
    out["ex1_by_z_decile"] = pd.DataFrame({"zmean": g["z"].mean(), "ex1": g["ex1"].mean(),
                                           "t": g["ex1"].mean() / (g["ex1"].std() / np.sqrt(g.size())), "n": g.size()})
    # falls only: slope of next1 on -z
    F = D[D.z < 0]
    sl = stats.linregress(-F["z"], F["ex1"])
    out["falls_slope"] = pd.DataFrame({"slope": [sl.slope], "t": [sl.slope / sl.stderr], "n": [len(F)]})
    U = D[D.z > 0]
    sl = stats.linregress(U["z"], U["ex1"])
    out["rises_slope"] = pd.DataFrame({"slope": [sl.slope], "t": [sl.slope / sl.stderr], "n": [len(U)]})
    # consistency of bottom-decile rebound by coin and by year
    B = D[D.zd == 0]
    g = B.groupby("coin")["ex1"]
    out["bottom_decile_by_coin"] = pd.DataFrame({"ex1": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    g = B.groupby("yr")["ex1"]
    out["bottom_decile_by_year"] = pd.DataFrame({"ex1": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    # weekend vs weekday for falls
    B["wkend"] = B["wd"].isin([5, 6]).astype(int)
    g = B.groupby("wkend")["ex1"]
    out["bottom_decile_weekend_vs_week"] = pd.DataFrame({"ex1": g.mean(), "n": g.count(),
                                                         "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    # hourly: hours 20-21 UTC by year and coin, and weekday
    H = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            r1 = pd.Series(c).pct_change().values  # return of bar ending at this bar's close
            H.append(pd.DataFrame({"coin": coin, "h": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                                   "yr": ts.dt.year.values, "r": r1}))
    H = pd.concat(H).dropna()
    H["mu"] = H.groupby("coin")["r"].transform("mean")
    H["ex"] = H["r"] - H["mu"]
    E = H[H.h.isin([20, 21])]
    g = E.groupby("yr")["ex"]
    out["h20_21_by_year_bp"] = pd.DataFrame({"ex_bp": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    g = E.groupby("coin")["ex"]
    out["h20_21_by_coin_bp"] = pd.DataFrame({"ex_bp": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    g = E.groupby("wd")["ex"]
    out["h20_21_by_weekday_bp"] = pd.DataFrame({"ex_bp": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    # Saturday by year
    S = D[D.wd == 4]  # day before Saturday -> next1 is Saturday
    g = S.groupby("yr")["ex1"]
    out["saturday_ex_by_year"] = pd.DataFrame({"ex1": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    return out
