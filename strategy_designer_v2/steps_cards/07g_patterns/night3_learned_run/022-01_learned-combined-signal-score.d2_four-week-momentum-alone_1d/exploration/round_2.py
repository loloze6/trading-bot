def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            rng = (b["high"] - b["low"]) / c
            rng_rel = rng / rng.rolling(20).mean()
            rng_rel5 = rng.rolling(3).mean() / rng.rolling(30).mean()
            cl_pos = (c - b["low"]) / (b["high"] - b["low"])
            vol_rel = r1.rolling(20).std() / r1.rolling(60, min_periods=40).std()
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b) - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, f=b["forecast"][i], r1=r1[i], rng_rel=rng_rel[i],
                                 rng_rel5=rng_rel5[i], clpos=cl_pos[i], vol_rel=vol_rel[i],
                                 wd=ts[i].weekday(), yr=ts[i].year,
                                 ex=(fwd - drift[coin]) / usual[coin], exr=fwd - drift[coin]))
    d = pd.DataFrame(rows)
    out = {}
    def sp(x, col):
        x = x.dropna(subset=[col, "ex"])
        if len(x) < 20: return pd.Series({"n": len(x), "rho": np.nan, "t": np.nan})
        r = stats.spearmanr(x[col], x["ex"]).correlation
        return pd.Series({"n": len(x), "rho": r, "t": r * np.sqrt(len(x))})
    out["rng_rel_by_coin"] = d.groupby("coin").apply(lambda z: sp(z, "rng_rel"))
    out["rng_rel_by_year"] = d.groupby("yr").apply(lambda z: sp(z, "rng_rel"))
    out["rng_rel_by_r1sign"] = d.dropna(subset=["r1"]).groupby(np.sign(d["r1"])).apply(lambda z: sp(z, "rng_rel"))
    out["rng_rel5_all"] = sp(d, "rng_rel5")
    out["clpos_all"] = sp(d, "clpos")
    # signed: range x sign of day
    d["rng_signed"] = d["rng_rel"] * np.sign(d["r1"])
    out["rng_signed_all"] = sp(d, "rng_signed")
    # weekday by coin: mon+tue vs rest
    d["mt"] = d["wd"].isin([0, 1])
    def wt(z):
        a = z[z.mt]["ex"]; b = z[~z.mt]["ex"]
        t = stats.ttest_ind(a, b, equal_var=False)
        return pd.Series({"n_mt": len(a), "diff": a.mean() - b.mean(), "t": t.statistic})
    out["montue_minus_rest_by_coin"] = d.groupby("coin").apply(wt)
    out["montue_minus_rest_by_year"] = d.groupby("yr").apply(wt)
    # momentum by vol_rel tercile per coin (sign of difference)
    x = d.dropna(subset=["vol_rel"]).copy()
    x["vg"] = x.groupby("coin")["vol_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["fx"] = x["f"] / 10 * x["exr"]
    out["mom_lowvol_minus_highvol_by_coin"] = x.groupby("coin").apply(
        lambda z: pd.Series({"low": z[z.vg == 0]["fx"].mean(), "high": z[z.vg == 2]["fx"].mean(),
                             "t": stats.ttest_ind(z[z.vg == 0]["fx"], z[z.vg == 2]["fx"], equal_var=False).statistic}))
    # momentum: positive vs negative forecast side, strength in direction
    x["dirstr"] = np.sign(x["f"]) * x["ex"]
    out["dir_strength_by_side"] = x.groupby(np.sign(x["f"]))["dirstr"].agg(
        ["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # book worst days: per coin-day, side and preceding 28d context
    rr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            nx = b["close"].shift(-1) / b["close"] - 1
            g = b["postRebalance_current_allocation"] * nx
            rr.append(pd.DataFrame({"g": g, "a": b["postRebalance_current_allocation"], "nx": nx,
                                    "f": b["forecast"]}))
    R = pd.concat(rr).dropna()
    q1, q99 = R["g"].quantile([0.01, 0.99])
    out["coinday_worst1pct"] = pd.Series({"n": (R.g <= q1).sum(), "share_long": (R[R.g <= q1].a > 0).mean(),
                                          "mean_abs_alloc": R[R.g <= q1].a.abs().mean(),
                                          "mean_abs_alloc_all": R.a.abs().mean(),
                                          "share_of_total_loss": R[R.g <= q1].g.sum() / R[R.g < 0].g.sum()})
    out["coinday_best1pct"] = pd.Series({"n": (R.g >= q99).sum(), "share_long": (R[R.g >= q99].a > 0).mean(),
                                         "share_of_total_gain": R[R.g >= q99].g.sum() / R[R.g > 0].g.sum(),
                                         "sum_g_all": R.g.sum(), "sum_g_best1pct": R[R.g >= q99].g.sum()})
    return out
