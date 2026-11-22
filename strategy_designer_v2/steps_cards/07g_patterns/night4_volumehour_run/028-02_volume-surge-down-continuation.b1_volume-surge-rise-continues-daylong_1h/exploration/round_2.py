def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows1 = []; rows24 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            r = pd.Series(c).pct_change()
            sd = r.rolling(720, min_periods=240).std().values
            n = len(b)
            idx = np.arange(0, n - 1)
            rows1.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year.values[idx],
                                       "hour": ts.dt.hour.values[idx], "f": c[idx + 1] / c[idx] - 1}))
            for H in (24, 72):
                idx = np.arange(24, n - H, H)
                past = c[idx] / c[idx - 24] - 1
                past72 = np.where(idx >= 72, c[idx] / c[np.maximum(idx - 72, 0)] - 1, np.nan)
                rows24.append(pd.DataFrame({"coin": coin, "w": w, "H": H, "year": ts.dt.year.values[idx],
                                            "pz": past / (sd[idx] * np.sqrt(24)), "p72z": past72 / (sd[idx] * np.sqrt(72)),
                                            "f": c[idx + H] / c[idx] - 1}))
    A = pd.concat(rows1).dropna()
    A["u"] = A["f"] - A.groupby("coin")["f"].transform("mean")
    out = {}
    A["slot"] = np.where(A.hour.isin([20, 21]), "h20-21", np.where(A.hour.isin([0, 1, 2, 3]), "h0-3", "other"))
    def agg(x):
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["hour slot by year (unusual 1h, bp)"] = A.groupby(["year", "slot"])["u"].apply(agg).unstack().unstack()
    out["hour slot by coin"] = A.groupby(["coin", "slot"])["u"].apply(agg).unstack()
    A["wgrp"] = A["w"].str[1:].astype(int).sub(1) // 6
    out["h20-21 by window group"] = A[A.slot == "h20-21"].groupby(["wgrp", "coin"])["u"].apply(agg).unstack()
    # sum of hours 20+21 vs gap  -> day-level: share of daily drift
    B = pd.concat(rows24).dropna(subset=["pz", "f"])
    B["u"] = B["f"] - B.groupby(["coin", "H"])["f"].transform("mean")
    res = []
    for (coin, H), g in B.groupby(["coin", "H"]):
        rho, p = stats.spearmanr(g.pz, g.u)
        sl = stats.linregress(g.pz, g.u)
        res.append({"coin": coin, "H": H, "n": len(g), "spearman": rho, "p": p, "slope_bp_per_z": sl.slope * 1e4, "t_slope": sl.slope / sl.stderr})
    out["future vs past-24h z (reversal)"] = pd.DataFrame(res)
    res = []
    for (coin, H), g in B.dropna(subset=["p72z"]).groupby(["coin", "H"]):
        sl = stats.linregress(g.p72z, g.u)
        res.append({"coin": coin, "H": H, "n": len(g), "slope_bp_per_z": sl.slope * 1e4, "t_slope": sl.slope / sl.stderr})
    out["future vs past-72h z"] = pd.DataFrame(res)
    res = []
    for (y, coin), g in B[B.H == 24].groupby(["year", "coin"]):
        sl = stats.linregress(g.pz, g.u)
        res.append({"year": y, "coin": coin, "n": len(g), "slope_bp_per_z": sl.slope * 1e4, "t": sl.slope / sl.stderr})
    out["24h reversal by year"] = pd.DataFrame(res)
    # book: days around largest book gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return", "coin_return"])
    D["q"] = D.groupby("coin")["book_return"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    out["book decile: mean book vs coin return bp"] = D.groupby("q")[["book_return", "coin_return"]].mean() * 1e4
    out["book vs coin daily corr"] = D.groupby("coin").apply(lambda g: g.book_return.corr(g.coin_return))
    return out
