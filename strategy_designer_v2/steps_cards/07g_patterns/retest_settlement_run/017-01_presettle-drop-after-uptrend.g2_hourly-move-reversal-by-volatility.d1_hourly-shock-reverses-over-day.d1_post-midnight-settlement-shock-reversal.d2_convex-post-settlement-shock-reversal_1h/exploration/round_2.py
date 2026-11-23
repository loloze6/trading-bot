def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(24, min_periods=20).std()
            z = r1 / vol
            volL = r1.rolling(720, min_periods=200).std()
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "year": ts.dt.year,
                               "z": z, "r1": r1,
                               "r24": c.shift(-24) / c - 1, "r6": c.shift(-6) / c - 1,
                               "r12": c.shift(-12) / c - 1,
                               "p24z": (c / c.shift(25) - 1) / (vol * np.sqrt(24)),  # prior 24h before this hour
                               "p24": c.shift(1) / c.shift(25) - 1,
                               "vlev": vol / volL,
                               "r24_from_m1": c.shift(-24) / c.shift(1) - 1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    d = A[A.hour == 0].groupby("coin")["r24"].mean()
    A["ex24"] = A["r24"] - A["coin"].map(d)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    h0 = A[A.hour == 0].dropna(subset=["z", "ex24"]).copy()
    h0["fade"] = -np.sign(h0["z"]) * h0["ex24"]
    # graded by vol level (24h vol / 30-day vol), quintiles
    h0["vq"] = pd.qcut(h0["vlev"], 5)
    out["h0_fade_by_vollevel_q5"] = h0.groupby("vq")["fade"].apply(tt).unstack()
    # fade in units of 24h usual move by vol level
    # graded by prior 24h trend aligned with the hour's move
    h0["align"] = np.sign(h0["z"]) * h0["p24"]
    h0["aq"] = pd.qcut(h0["align"], 5)
    out["h0_fade_by_prior24_aligned_q5"] = h0.groupby("aq")["fade"].apply(tt).unstack()
    # prior 24h trend alone at hour 0 (fade the prior day's return) graded
    h0["fadeP"] = -np.sign(h0["p24"]) * h0["ex24"]
    h0["pq"] = pd.qcut(h0["p24"].abs(), 5)
    out["h0_fade_prior24_by_size_q5"] = h0.groupby("pq")["fadeP"].apply(tt).unstack()
    # same for other hours: fade of prior 24h return
    oth = A[(A.hour == 12)].dropna(subset=["p24", "ex24"]).copy()
    oth["fadeP"] = -np.sign(oth["p24"]) * oth["ex24"]
    out["h12_fade_prior24"] = tt(oth["fadeP"])
    # reversal timing at hour 0
    for k in ["r6", "r12"]:
        h0["f_" + k] = -np.sign(h0["z"]) * h0[k]
    out["h0_fade_timing"] = pd.DataFrame({k: tt(h0["f_" + k]) for k in ["r6", "r12"]})
    # does reversal give back more than the hour's move?
    out["h0_giveback_ratio"] = pd.Series({"mean_abs_r1": h0["r1"].abs().mean(),
                                           "mean_fade24": h0["fade"].mean()})
    # hour 20-21 drift graded by vol level
    for hh in [20, 21]:
        x = A[A.hour == hh].dropna(subset=["vlev"]).copy()
        x["nxt"] = x.groupby(["coin", "w"])["r1"].shift(0)
    B = A.copy()
    B["fwd1"] = B.groupby(["coin", "w"])["r1"].shift(-1)
    x = B[B.hour.isin([20])].dropna(subset=["fwd1", "vlev"]).copy()
    x["vq"] = pd.qcut(x["vlev"], 4)
    out["h20_fwd1_by_vollevel"] = x.groupby("vq")["fwd1"].apply(tt).unstack()
    out["h20_fwd1_by_year"] = x.groupby("year")["fwd1"].apply(tt).unstack()
    # book: largest gains/losses days vs coin
    dd = []
    for coin, wins in days.items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; dd.append(t)
    D = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    q = D["book_return"].quantile([0.01, 0.99])
    out["book_extreme_days"] = pd.DataFrame({
        "worst1pct": [D[D.book_return <= q[0.01]]["coin_return"].mean(), D[D.book_return <= q[0.01]]["coin_return"].abs().mean()],
        "best1pct": [D[D.book_return >= q[0.99]]["coin_return"].mean(), D[D.book_return >= q[0.99]]["coin_return"].abs().mean()],
        "all": [D["coin_return"].mean(), D["coin_return"].abs().mean()]}, index=["coin_ret_mean", "coin_absret_mean"])
    return out
