def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            s = pd.Series(c)
            r1 = s.pct_change().values
            vol20 = s.pct_change().rolling(20, min_periods=20).std().values
            hi60 = s.rolling(60, min_periods=60).max().values
            dist = (hi60 - c) / hi60 * 100
            r28 = s.pct_change(28).values
            for i in range(n - 3):
                rows.append(dict(coin=coin, w=w, r1=r1[i], vol=vol20[i], dist=dist[i], r28=r28[i],
                                 f1=c[i+1]/c[i]-1, f2=c[i+2]/c[i]-1 if i % 2 == 0 else np.nan,
                                 f3=c[i+3]/c[i]-1 if i % 3 == 0 else np.nan,
                                 wd=ts[i+1].weekday(), year=ts[i].year, wnum=int(str(w)[1:])))
    d = pd.DataFrame(rows)
    for h in ["f1", "f2", "f3"]:
        d[h + "_ex"] = d[h] - d.groupby("coin")[h].transform("mean")
    d["rz"] = d["r1"] / d["vol"]
    out = {}
    def tstat(x):
        x = x.dropna()
        return pd.Series({"mean_bps": x.mean() * 1e4, "n": len(x), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    x = d.dropna(subset=["rz"]).copy()
    x["dec"] = x.groupby("coin")["rz"].transform(lambda v: pd.qcut(v.rank(method="first"), 10, labels=False))
    out["rz_decile_next1_ex"] = x.groupby("dec")["f1_ex"].apply(tstat).unstack().round(2)
    out["rz_decile_next2_ex"] = x.groupby("dec")["f2_ex"].apply(tstat).unstack().round(2)
    out["rz_decile_next3_ex"] = x.groupby("dec")["f3_ex"].apply(tstat).unstack().round(2)
    out["rz_decile_next1_total"] = x.groupby("dec")["f1"].apply(tstat).unstack().round(2)
    low = x[x.dec == 0]
    out["low_dec_by_coin"] = low.groupby("coin")["f1_ex"].apply(tstat).unstack().round(2)
    out["low_dec_by_year"] = low.groupby("year")["f1_ex"].apply(tstat).unstack().round(2)
    # graded regression of next-day ex on rz (down days only, signed)
    dn = x[x.rz < 0]
    for nm, sub in [("dn", dn), ("up", x[x.rz > 0])]:
        X = np.column_stack([np.ones(len(sub)), sub.rz.values])
        yv = sub.f1_ex.values
        bta, *_ = np.linalg.lstsq(X, yv, rcond=None)
        res = yv - X @ bta
        se = np.sqrt(np.diag(res @ res / (len(sub) - 2) * np.linalg.inv(X.T @ X)))
        out["reg_next1_on_rz_" + nm] = pd.Series({"slope_bps_per_sd": bta[1] * 1e4, "t": bta[1] / se[1], "n": len(sub)}).round(3)
    # reversal by vol regime and by dist regime
    low = low.copy()
    low["vq"] = pd.qcut(low.vol.rank(method="first"), 3, labels=False)
    out["low_dec_by_volterc"] = low.groupby("vq")["f1_ex"].apply(tstat).unstack().round(2)
    low2 = low.dropna(subset=["dist"]).copy()
    low2["dq"] = pd.qcut(low2.dist.rank(method="first"), 3, labels=False)
    out["low_dec_by_distterc"] = low2.groupby("dq")["f1_ex"].apply(tstat).unstack().round(2)
    # weekday robustness: saturday (wd 5) by coin and year
    sat = d[d.wd == 5]
    out["sat_by_coin"] = sat.groupby("coin")["f1_ex"].apply(tstat).unstack().round(2)
    out["sat_by_year"] = sat.groupby("year")["f1_ex"].apply(tstat).unstack().round(2)
    # half windows split for reversal
    x["half"] = np.where(x.wnum <= 12, "w1-12", "w13-24")
    out["low_dec_by_half"] = x[x.dec == 0].groupby("half")["f1_ex"].apply(tstat).unstack().round(2)
    out["high_dec_by_half"] = x[x.dec == 9].groupby("half")["f1_ex"].apply(tstat).unstack().round(2)
    return out
