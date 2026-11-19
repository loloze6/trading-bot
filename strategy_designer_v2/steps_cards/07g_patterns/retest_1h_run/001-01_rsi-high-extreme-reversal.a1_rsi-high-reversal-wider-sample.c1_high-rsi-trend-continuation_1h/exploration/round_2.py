def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    tt = lambda x: x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    # 24h grid, past 24h return, vol-scaled
    h = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            lr = np.log(b["close"]).diff()
            vol = (lr.rolling(720, min_periods=240).std() * np.sqrt(24)).values
            idx = np.arange(24, len(b) - 24, 24)
            h.append(pd.DataFrame({"coin": c, "win": w, "year": ts.dt.year.values[idx],
                                   "f24": cl[idx + 24] / cl[idx] - 1, "p24": cl[idx] / cl[idx - 24] - 1,
                                   "f72": np.where(idx + 72 < len(b), cl[np.minimum(idx + 72, len(b) - 1)] / cl[idx] - 1, np.nan),
                                   "vol": vol[idx]}))
    H = pd.concat(h, ignore_index=True)
    H["ex"] = H.f24 - H.groupby("coin").f24.transform("mean")
    H["z"] = H.p24 / H.vol
    H["q"] = H.groupby("coin").p24.transform(lambda x: pd.qcut(x, 10, labels=False))
    lo = H[H.q == 0]
    out["low_decile_by_coin"] = lo.groupby("coin").ex.agg(["mean", "median", "count", tt])
    out["low_decile_by_year"] = lo.groupby("year").ex.agg(["mean", "median", "count", tt])
    hi = H[H.q == 9]
    out["high_decile_by_coin"] = hi.groupby("coin").ex.agg(["mean", "median", "count", tt])
    # graded: on down days, regress ex on z
    dn = H[(H.p24 < 0)].dropna(subset=["z", "ex"])
    r = stats.linregress(dn.z, dn.ex)
    out["down_days_slope_ex_on_z"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(dn)})
    up = H[(H.p24 > 0)].dropna(subset=["z", "ex"])
    r = stats.linregress(up.z, up.ex)
    out["up_days_slope_ex_on_z"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(up)})
    H["zq"] = pd.qcut(H.z, 10, labels=False)
    out["fwd1d_by_volscaled_past1d_decile"] = H.groupby("zq").ex.agg(["mean", "median", "count", tt])
    # trimmed low decile mean (winsor 1%)
    e = lo.ex.clip(lo.ex.quantile(0.01), lo.ex.quantile(0.99))
    out["low_decile_winsor"] = pd.Series({"mean": e.mean(), "t": tt(e)})
    # 3-day follow on low decile
    H["ex72"] = H.f72 - H.groupby("coin").f72.transform("mean")
    out["low_decile_fwd3d"] = pd.Series({"mean": H[H.q == 0].ex72.mean(), "n": H[H.q == 0].ex72.notna().sum()})
    # hour effect: 20-21 UTC by coin and year
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"])
            r1 = b["close"].shift(-1) / b["close"] - 1
            rows.append(pd.DataFrame({"coin": c, "year": ts.dt.year, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                      "r1": r1}))
    B = pd.concat(rows, ignore_index=True).dropna()
    B["ex"] = B.r1 - B.groupby("coin").r1.transform("mean")
    B["h2021"] = B.hour.isin([20, 21])
    s = B[B.h2021]
    out["h20_21_by_coin"] = s.groupby("coin").ex.agg(["mean", "count", tt])
    out["h20_21_by_year"] = s.groupby("year").ex.agg(["mean", "count", tt])
    out["fri_by_coin"] = B[B.wd == 4].groupby("coin").ex.agg(["mean", tt])
    # book largest days: coin return on days before/after
    drows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            d = d.copy()
            d["prev_coin"] = d.coin_return.shift(1)
            d["next_coin"] = d.coin_return.shift(-1)
            d["coin_sym"] = c
            drows.append(d)
    D = pd.concat(drows).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D.book_return, 20, labels=False)
    out["book_extremes"] = D[D.bq.isin([0, 19])].groupby("bq")[["book_return", "coin_return", "prev_coin", "next_coin"]].mean()
    return out
