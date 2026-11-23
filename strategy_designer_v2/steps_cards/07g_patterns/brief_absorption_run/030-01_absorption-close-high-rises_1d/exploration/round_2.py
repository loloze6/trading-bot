def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # daily coin returns by weekday, by year halves
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    dd = pd.concat(dd).dropna(subset=["coin_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    dd["yr"] = pd.to_datetime(dd["day"]).dt.year
    dd["z"] = dd["coin_return"] - dd.groupby("coin")["coin_return"].transform("mean")
    g = dd.groupby("wd")["z"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["daily_unusual_by_weekday"] = g
    p = dd.pivot_table(index="yr", columns="wd", values="z", aggfunc="mean")
    out["daily_unusual_weekday_by_year"] = p
    p2 = dd.pivot_table(index="coin", columns="wd", values="z", aggfunc="mean")
    out["daily_unusual_weekday_by_coin"] = p2

    # close location on heavy volume days, several horizons, nonoverlapping grid
    res = {}; yrs = {}
    for H in [1, 2, 3, 5, 10]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
                o = b["open"].astype(float); v = b["volume"].astype(float)
                rng = (hi - lo).replace(0, np.nan)
                df = pd.DataFrame({"coin": coin, "cl": 2 * (c - lo) / rng - 1,
                                   "body": (c - o).abs() / rng,
                                   "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                                   "fwd": c.shift(-H) / c - 1,
                                   "yr": pd.to_datetime(b["timestamp"]).dt.year,
                                   "pos": np.arange(len(b))})
                rows.append(df[df["pos"] % H == 0])
        d = pd.concat(rows).dropna(subset=["fwd", "cl"])
        d["un"] = (d["fwd"] - d.groupby("coin")["fwd"].transform("mean")) / d.groupby("coin")["fwd"].transform("std")
        for name, s in [("all", d), ("vr<1", d[d["vr"] < 1]), ("vr1-2", d[(d["vr"] >= 1) & (d["vr"] < 2)]),
                        ("vr>=2", d[d["vr"] >= 2]), ("vr>=2_flat", d[(d["vr"] >= 2) & (d["body"] <= 0.3)]),
                        ("vr>=2_notflat", d[(d["vr"] >= 2) & (d["body"] > 0.3)])]:
            s = s.dropna(subset=["cl", "un"])
            if len(s) < 20: continue
            r = stats.linregress(s["cl"], s["un"])
            res[f"H{H}_{name}"] = {"n": len(s), "slope": r.slope, "t": r.slope / r.stderr}
        if H == 5:
            for y, s in d[d["vr"] >= 1.5].groupby("yr"):
                if len(s) > 15:
                    r = stats.linregress(s["cl"], s["un"]); yrs[y] = {"n": len(s), "slope": r.slope, "t": r.slope / r.stderr}
            # interaction cl x vr on all days
            s = d.dropna(subset=["vr"]).copy()
            s["clvr"] = s["cl"] * np.log(s["vr"])
            X = np.column_stack([np.ones(len(s)), s["cl"], np.log(s["vr"]), s["clvr"]])
            beta, *_ = np.linalg.lstsq(X, s["un"].values, rcond=None)
            resid = s["un"].values - X @ beta
            cov = np.linalg.inv(X.T @ X) * resid.var(ddof=4)
            out["H5_interaction_cl_logvr"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                                         index=["const", "cl", "logvr", "cl_x_logvr"])
    out["cl_slopes_by_volume"] = pd.DataFrame(res).T
    out["H5_cl_slope_vr1.5_by_year"] = pd.DataFrame(yrs).T
    return out
