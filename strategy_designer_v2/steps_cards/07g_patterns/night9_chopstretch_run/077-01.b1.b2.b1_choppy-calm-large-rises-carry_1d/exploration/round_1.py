def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            vsr = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            r1d = r1
            r3 = c / c.shift(3) - 1
            vs3 = r3 / (sd30 * np.sqrt(3))
            tr60 = c / c.shift(60) - 1
            pct = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (d["high"] - d["low"]) / c / sd30
            clo = (c - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            vol = d["volume"].astype(float)
            vrel = vol / vol.rolling(30, min_periods=20).mean()
            wd = pd.to_datetime(d["timestamp"]).dt.weekday
            yr = pd.to_datetime(d["timestamp"]).dt.year
            alloc = d["postRebalance_current_allocation"].astype(float)
            pos = np.arange(len(d))
            t = pd.DataFrame(dict(coin=coin, w=w, vsr=vsr, vs3=vs3, r1z=r1d / sd30, tr60=tr60, pct=pct,
                                  fwd=fwd, fwd1=fwd1, grid=(pos % H == 0), rng=rng, clo=clo, vrel=vrel,
                                  wd=wd, yr=yr, alloc=alloc, sd30=sd30))
            rows.append(t)
    A = pd.concat(rows, ignore_index=True)
    # coin usual move & drift on grid
    g = A[A.grid & A.fwd.notna()].copy()
    drift = g.groupby("coin").fwd.agg(["mean", "std"])
    g["ex"] = g.fwd - g.coin.map(drift["mean"])
    g["z"] = g.ex / g.coin.map(drift["std"])
    def prof(r):
        if pd.isna(r.tr60) or pd.isna(r.pct): return "na"
        t = "rising" if r.tr60 > .10 else ("falling" if r.tr60 < -.10 else "choppy")
        a = "agitated" if r.pct > .5 else "calm"
        return t + " " + a
    g["prof"] = g.apply(prof, axis=1)
    g["vbin"] = pd.cut(g.vsr, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    def summ(x):
        n = len(x); m = x.ex.mean(); s = x.ex.std()
        return pd.Series(dict(n=n, mean_ex=m, t=m / (s / np.sqrt(n)) if n > 2 else np.nan, z=x.z.mean()))
    out = {}
    out["by_prof_vbin"] = g.groupby(["prof", "vbin"]).apply(summ).query("n>=15")
    out["by_prof"] = g.groupby("prof").apply(summ)
    # correlation vsr vs z by profile
    out["corr_vsr_by_prof"] = g.dropna(subset=["vsr"]).groupby("prof").apply(
        lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x.vsr, x.z)[0])))
    g["v3bin"] = pd.cut(g.vs3, [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["by_vs3"] = g.groupby("v3bin").apply(summ)
    g["rngbin"] = pd.qcut(g.rng, 5, duplicates="drop")
    out["by_range"] = g.groupby("rngbin").apply(summ)
    g["volbin"] = pd.qcut(g.vrel, 5, duplicates="drop")
    out["by_volume"] = g.groupby("volbin").apply(summ)
    out["by_weekday_entry"] = g.groupby("wd").apply(summ)
    # 1-day: weekday returns all bars
    a1 = A[A.fwd1.notna()].copy()
    a1["ex1"] = a1.fwd1 - a1.groupby("coin").fwd1.transform("mean")
    out["next_day_by_weekday"] = a1.groupby((a1.wd + 1) % 7).ex1.agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    a1["zbin"] = pd.cut(a1.r1z, [-np.inf, -2, -1, 1, 2, np.inf])
    out["next_day_after_day_z"] = a1.groupby("zbin").ex1.agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, w=w))
    if tr:
        T = pd.concat(tr)
        out["trades_by_coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count", "mean", "sum"])
    return out
