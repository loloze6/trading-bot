def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        vals = []; vals1 = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2); vals.extend(c[idx + 2] / c[idx] - 1)
            idx = np.arange(0, len(c) - 1, 1); vals1.extend(c[idx + 1] / c[idx] - 1)
        m2 = np.nanmean(vals); m1 = np.nanmean(vals1)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(20).std().values
            r1 = r1.values
            for i in range(20, len(c) - 2):
                if not np.isfinite(sd[i]) or sd[i] == 0: continue
                rows.append({"coin": coin, "dow": ts.iloc[i].dayofweek, "phase": i % 7,
                             "z": r1[i] / sd[i], "x2": c[i + 2] / c[i] - 1 - m2,
                             "x1": c[i + 1] / c[i] - 1 - m1})
    d = pd.DataFrame(rows)
    d["s"] = -np.sign(d["z"])
    d["sx2"] = d["s"] * d["x2"]; d["sx1"] = d["s"] * d["x1"]
    out = {}
    # non-overlapping: one dow per week, so per-dow samples are 7 days apart
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))})
    out["signed_x2_by_dow"] = d.groupby("dow")["sx2"].apply(tt).unstack()
    out["signed_x1_by_dow"] = d.groupby("dow")["sx1"].apply(tt).unstack()
    d["sun"] = d["dow"] == 6
    d["az"] = pd.qcut(d["z"].abs(), 4, labels=False)
    out["sx2_by_absz_q_sun_vs_rest"] = d.groupby(["az", "sun"])["sx2"].mean().unstack()
    d["side"] = np.where(d["z"] > 0, "rise", "fall")
    out["sx2_by_side_sun_vs_rest"] = d.groupby(["side", "sun"])["sx2"].mean().unstack()
    su = d[d["sun"]]
    out["sun_side_by_absz_q"] = su.groupby(["az", "side"])["sx2"].apply(tt).unstack()
    out["sun_rise_by_coin"] = su[su.side == "rise"].groupby("coin")["sx2"].apply(tt).unstack()
    # weekday-adjusted: Sunday minus other days mean signed x2 within |z| quartile, t Welch
    from scipy import stats
    res = {}
    for q, g in d.groupby("az"):
        a = g[g.sun]["sx2"].dropna(); b = g[~g.sun]["sx2"].dropna()
        res[q] = pd.Series({"diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    out["sun_minus_rest_by_absz"] = pd.DataFrame(res).T
    return out
