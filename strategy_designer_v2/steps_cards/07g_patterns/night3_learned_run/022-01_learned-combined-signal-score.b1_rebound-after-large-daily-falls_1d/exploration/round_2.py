def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            z = r1 / vol
            volrank = vol.rolling(180, min_periods=60).apply(lambda x: (x[-1] > x[:-1]).mean(), raw=True)
            volratio = vol / r1.rolling(180, min_periods=60).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z,
                               "volrank": volrank, "volratio": volratio, "year": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in [1, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 5, 10]:
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean(); s = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(m)
        D[f"s{h}"] = D[f"x{h}"] / D["coin"].map(s)
    out = {}
    agg = lambda s: pd.Series({"n": s.count(), "mean_bps": s.mean() * 1e4,
                               "t": s.mean() / s.std() * np.sqrt(s.count())})
    # A. fall x volatility: graded interaction, next 1 day
    g = D[(D["z"] < 0)].dropna(subset=["z", "x1", "volratio"]).copy()
    g["fall"] = -g["z"]; g["inter"] = g["fall"] * g["volratio"]
    X = np.column_stack([np.ones(len(g)), g["fall"], g["volratio"], g["inter"]])
    beta, res, *_ = np.linalg.lstsq(X, g["x1"].values, rcond=None)
    e = g["x1"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(g) - 4)
    out["fall_vol_interaction"] = pd.DataFrame({"beta_bps": beta * 1e4, "t": beta / np.sqrt(np.diag(cov))},
                                               index=["const", "fall", "volratio", "fall*volratio"]).round(3)
    f = D[D["z"] < -1].dropna(subset=["x1", "volratio"]).copy()
    f["vq"] = pd.qcut(f["volratio"], 4, labels=False)
    out["falls_by_volratio_q"] = f.groupby("vq")["x1"].apply(agg).unstack().round(2)
    out["falls_by_volratio_q_strength"] = f.groupby("vq")["s1"].mean().round(3)
    f2 = D[D["z"] < -1].dropna(subset=["x1", "volrank"])
    f2 = f2.assign(hv=np.where(f2["volrank"] > 0.66, "high", "notHigh"))
    out["falls_hv_by_year"] = f2.groupby(["year", "hv"])["x1"].apply(agg).unstack().round(2)
    out["falls_hv_by_coin"] = f2.groupby(["coin", "hv"])["x1"].apply(agg).unstack().round(2)
    # B. continuation after large rises, next 5 and 10 days, on grid
    for h in [5, 10]:
        g = D[(D["pos"] % h == 0)].dropna(subset=["z", f"x{h}"])
        u = g[g["z"] > 0]
        sl = stats.linregress(u["z"], u[f"x{h}"])
        out[f"rise_slope_h{h}"] = pd.Series({"n": len(u), "slope_bps": sl.slope * 1e4,
                                             "t": sl.slope / sl.stderr,
                                             "full_slope_bps": stats.linregress(g["z"], g[f"x{h}"]).slope * 1e4,
                                             "full_t": (lambda s: s.slope / s.stderr)(stats.linregress(g["z"], g[f"x{h}"]))}).round(3)
        big = u[u["z"] > 1.5]
        out[f"bigrise_h{h}_by_year"] = big.groupby("year")[f"x{h}"].apply(agg).unstack().round(2)
        out[f"bigrise_h{h}_by_coin"] = big.groupby("coin")[f"x{h}"].apply(agg).unstack().round(2)
        out[f"bigrise_h{h}_strength_total"] = pd.Series({"strength": big[f"s{h}"].mean(),
                                                        "total_bps": big[f"f{h}"].mean() * 1e4,
                                                        "x_bps": big[f"x{h}"].mean() * 1e4, "n": len(big)}).round(3)
        gq = u.assign(q=pd.qcut(u["z"], 4, labels=False))
        out[f"rise_quart_h{h}"] = gq.groupby("q").agg(z=("z", "mean"), x_bps=(f"x{h}", lambda s: s.mean() * 1e4),
                                                      strength=(f"s{h}", "mean"), n=(f"x{h}", "count")).round(3)
        # rise in high vol
        uu = u.dropna(subset=["volrank"]).assign(hv=lambda d: np.where(d["volrank"] > 0.66, "high", "notHigh"))
        out[f"rise_z>1_h{h}_by_vol"] = uu[uu["z"] > 1].groupby("hv")[f"x{h}"].apply(agg).unstack().round(2)
    # C. book's worst and best days: coin z on the day before
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd.append(d.assign(coin=coin, w=w))
    Dd = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    q1, q9 = Dd["book_return"].quantile([0.02, 0.98])
    Dd["prevcoin"] = Dd.groupby(["coin", "w"])["coin_return"].shift(1)
    out["book_extremes"] = pd.DataFrame({
        "worst2pct": [Dd.loc[Dd["book_return"] < q1, "coin_return"].mean() * 1e4,
                      Dd.loc[Dd["book_return"] < q1, "prevcoin"].mean() * 1e4,
                      (Dd["book_return"] < q1).sum()],
        "best2pct": [Dd.loc[Dd["book_return"] > q9, "coin_return"].mean() * 1e4,
                     Dd.loc[Dd["book_return"] > q9, "prevcoin"].mean() * 1e4,
                     (Dd["book_return"] > q9).sum()]},
        index=["coin_ret_same_day_bps", "coin_ret_prev_day_bps", "n"]).round(2)
    return out
