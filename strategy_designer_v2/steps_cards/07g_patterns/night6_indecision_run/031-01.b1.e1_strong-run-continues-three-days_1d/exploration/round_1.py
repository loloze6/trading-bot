def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ret5 = c / c.shift(5) - 1
            z5 = ret5 / (vol20 * np.sqrt(5))
            z1 = r1 / vol20
            rng = (hi - lo) / c.shift(1)
            rngz = rng / rng.rolling(20, min_periods=15).mean()
            body = (c - o).abs() / (hi - lo).replace(0, np.nan)
            clv = ((c - lo) / (hi - lo).replace(0, np.nan))  # close location
            fwd = c.shift(-H) / c - 1
            vol60 = r1.rolling(60, min_periods=30).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "fc": b["forecast"].astype(float), "fwd": fwd, "z5": z5, "z1": z1,
                              "rngz": rngz, "body": body, "clv": clv, "vol20": vol20,
                              "volrat": vol20 / vol60, "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by_z5_bucket"] = G.groupby(pd.cut(G["z5"], [-9, -2, -1, -0.5, 0, 0.5, 1, 2, 9])).apply(summ)
    out["by_z1_bucket"] = G.groupby(pd.cut(G["z1"], [-20, -2, -1, 0, 1, 2, 20])).apply(summ)
    # brief: wide flat day after run, signed in run direction
    G["rundir"] = np.sign(G["z5"])
    G["ex_run"] = G["ex"] * G["rundir"]
    R = G[G["z5"].abs() > 1].copy()
    R["wide"] = pd.qcut(R["rngz"], 3, labels=["narrow", "mid", "wide"])
    R["flat"] = np.where(R["body"] < 0.3, "flat", "body")
    def summ2(g):
        x = g["ex_run"].dropna()
        return pd.Series({"n": len(x), "mean_ex_rundir_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["run_days_by_range_body"] = R.groupby(["wide", "flat"]).apply(summ2)
    out["run_up_vs_down"] = R.groupby("rundir").apply(summ2)
    out["by_rangez_all"] = G.groupby(pd.qcut(G["rngz"], 5)).apply(summ)
    out["by_vol_regime"] = G.groupby(pd.qcut(G["volrat"], 4)).apply(summ)
    out["by_closeloc"] = G.groupby(pd.cut(G["clv"], [0, .2, .4, .6, .8, 1.0001])).apply(summ)
    # z5 slope by coin and year
    def slope(g):
        g = g.dropna(subset=["z5", "ex"])
        s = stats.linregress(g["z5"], g["ex"])
        return pd.Series({"n": len(g), "slope_%": 100 * s.slope, "t": s.slope / s.stderr})
    out["z5_slope_by_coin"] = G.groupby("coin").apply(slope)
    out["z5_slope_by_year"] = G.groupby("yr").apply(slope)
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["book_coin_by_weekday_%"] = D.groupby("wd")[["book_return", "coin_return"]].mean() * 100
    out["coin_ret_weekday_t"] = D.groupby("wd")["coin_return"].apply(lambda x: x.mean() / (x.std() / np.sqrt(x.count())))
    return out
