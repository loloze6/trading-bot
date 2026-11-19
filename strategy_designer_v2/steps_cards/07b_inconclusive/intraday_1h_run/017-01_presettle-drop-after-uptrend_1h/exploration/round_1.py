def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 2-bar return on non-overlapping grid
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g.append(c[idx + 2] / c[idx] - 1)
        mu2 = np.concatenate(g).mean()
        for w, df in wins.items():
            d = df[["timestamp", "close", "volume", "forecast"]].copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"]
            d["r72"] = c / c.shift(72) - 1
            d["f2"] = c.shift(-2) / c - 1 - mu2
            d["f1"] = c.shift(-1) / c - 1 - mu2 / 2
            d["post2"] = c.shift(-4) / c.shift(-2) - 1 - mu2   # 2h after settlement
            d["f8"] = c.shift(-8) / c - 1 - 4 * mu2
            vmed = d["volume"].rolling(168, min_periods=48).median()
            d["vrel2"] = (d["volume"].shift(-1) + d["volume"].shift(-2)) / (2 * vmed)
            d["hour"] = d["ts"].dt.hour
            d["year"] = d["ts"].dt.year
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["r72", "f2"])
    out = {}
    # by starting hour: up-trend episodes, mean excess 2h return and slope on r72
    def summ(x):
        up = x[x.r72 > 0]
        s = stats.linregress(up.r72, up.f2) if len(up) > 30 else None
        allslope = stats.linregress(x.r72, x.f2)
        return pd.Series({"n_up": len(up), "mean_up_bp": up.f2.mean() * 1e4,
                          "t_up": up.f2.mean() / up.f2.std() * np.sqrt(len(up)),
                          "slope_up_t": s.slope / s.stderr if s else np.nan,
                          "slope_all_t": allslope.slope / allslope.stderr,
                          "vrel2": x.vrel2.median()})
    out["by_start_hour"] = A.groupby("hour").apply(summ)
    S = A[A.hour.isin([21, 5, 13])].copy()
    S["q"] = pd.qcut(S.r72, 10, labels=False)
    out["settle_by_r72_decile"] = S.groupby("q").agg(r72=("r72", "mean"), n=("f2", "size"),
        pre2_bp=("f2", lambda v: v.mean() * 1e4), post2_bp=("post2", lambda v: v.mean() * 1e4),
        f1_bp=("f1", lambda v: v.mean() * 1e4), f8_bp=("f8", lambda v: v.mean() * 1e4))
    U = S[S.r72 > 0]
    out["settle_up_by_coin"] = U.groupby("coin").apply(lambda x: pd.Series({
        "n": len(x), "pre2_bp": x.f2.mean() * 1e4, "t": x.f2.mean() / x.f2.std() * np.sqrt(len(x)),
        "post2_bp": x.post2.mean() * 1e4, "slope_t": (lambda s: s.slope / s.stderr)(stats.linregress(x.r72, x.f2))}))
    out["settle_up_by_year"] = U.groupby("year").apply(lambda x: pd.Series({
        "n": len(x), "pre2_bp": x.f2.mean() * 1e4, "t": x.f2.mean() / x.f2.std() * np.sqrt(len(x)),
        "post2_bp": x.post2.mean() * 1e4}))
    out["settle_up_by_hour"] = U.groupby("hour").apply(lambda x: pd.Series({
        "n": len(x), "pre2_bp": x.f2.mean() * 1e4, "t": x.f2.mean() / x.f2.std() * np.sqrt(len(x)),
        "post2_bp": x.post2.mean() * 1e4}))
    D = S[S.r72 < 0]
    out["settle_down"] = pd.Series({"n": len(D), "pre2_bp": D.f2.mean() * 1e4,
        "t": D.f2.mean() / D.f2.std() * np.sqrt(len(D)), "post2_bp": D.post2.mean() * 1e4})
    return out
