def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "c": c, "r1": r1,
                               "r28": c / c.shift(28) - 1,
                               "r60": c / c.shift(60) - 1,
                               "vol30": r1.rolling(30, min_periods=20).std(),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "i": np.arange(len(b))})
            for h in [1, 5, 10, 20]:
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # momentum graded, per horizon, rank slope per coin on own grid
    res = []
    for sig in ["r28", "r60"]:
        for h in [5, 10, 20]:
            g = A[A.i % h == 0].dropna(subset=[sig, "f%d" % h]).copy()
            g["ex"] = g["f%d" % h] - g.groupby("coin")["f%d" % h].transform("mean")
            g["sd"] = g.groupby("coin")["f%d" % h].transform("std")
            g["rk"] = g.groupby("coin")[sig].rank(pct=True) - 0.5
            g["volz"] = g[sig] / (g["vol30"] * np.sqrt(28 if sig == "r28" else 60))
            pos_coins = 0; ts_ = []
            for coin, d in g.groupby("coin"):
                s = stats.linregress(d.rk, d.ex)
                pos_coins += s.slope > 0; ts_.append(s.slope / s.stderr)
            s = stats.linregress(g.rk, g.ex / g.sd)
            top = g[g.rk > 0.3]
            res.append({"sig": sig, "h": h, "n": len(g), "slope_strength": s.slope, "t": s.slope / s.stderr,
                        "coins_pos": pos_coins, "min_coin_t": min(ts_),
                        "top_decile_ex_raw": top.ex.mean(), "top_decile_tot": top["f%d" % h].mean(),
                        "top_strength": (top.ex / top.sd).mean()})
    out["momentum_graded"] = pd.DataFrame(res)
    # weekday, 1-day returns (all bars count once at h=1)
    g = A.dropna(subset=["f1"]).copy()
    g["ex"] = g.f1 - g.groupby("coin").f1.transform("mean")
    wd = g.groupby("wd").ex.agg(["size", "mean"])
    wd["t"] = g.groupby("wd").ex.apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["weekday_1d_next"] = wd
    out["weekday_1d_by_coin"] = g.groupby(["coin", "wd"]).ex.mean().unstack()
    # weekday 5-day start, per coin and per year: Monday minus Sunday
    g5 = A[A.i % 5 == 0].dropna(subset=["f5"]).copy()
    g5["ex"] = g5.f5 - g5.groupby("coin").f5.transform("mean")
    out["wd5_by_coin"] = g5.groupby(["coin", "wd"]).ex.mean().unstack()
    out["wd5_by_year"] = g5.groupby(["yr", "wd"]).ex.mean().unstack()
    # momentum by year (top-bottom tercile r28, h10)
    g10 = A[A.i % 10 == 0].dropna(subset=["r28", "f10"]).copy()
    g10["ex"] = g10.f10 - g10.groupby("coin").f10.transform("mean")
    g10["rk"] = g10.groupby("coin").r28.rank(pct=True)
    out["mom_by_year_h10"] = g10.groupby("yr").apply(lambda d: pd.Series({
        "n": len(d), "top_minus_bottom": d[d.rk > 2/3].ex.mean() - d[d.rk < 1/3].ex.mean()}))
    return out
