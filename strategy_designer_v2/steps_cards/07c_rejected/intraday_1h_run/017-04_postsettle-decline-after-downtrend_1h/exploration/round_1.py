def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean h-bar returns on non-overlapping grid
        means = {}
        for h in (1, 2, 4, 8):
            r = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                r.append(c[idx + h] / c[idx] - 1)
            means[h] = np.nanmean(np.concatenate(r))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w,
                               "hour": (ts + pd.Timedelta(hours=1)).dt.hour,
                               "year": ts.dt.year})
            r72 = c.pct_change(72)
            z = (r72 - r72.rolling(73, min_periods=20).mean()) / r72.rolling(73, min_periods=20).std()
            df["r72"] = r72
            df["z"] = z
            for h in (1, 2, 4, 8):
                df[f"x{h}"] = c.shift(-h) / c - 1 - means[h]
            df["pre2"] = c / c.shift(2) - 1 - means[2]
            df["volrel"] = b["volume"] / b["volume"].rolling(24).mean()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["z", "x2"])
    d["settle"] = d["hour"].isin([0, 8, 16])
    out = {}
    # by close hour: down-trend events (z<0), mean excess 2-bar and graded slope
    g = []
    for hr, s in d.groupby("hour"):
        dn = s[s.z < 0]
        f = -(np.clip(dn.z, None, 0) ** 2)
        gain = -(f / 10) * dn.x2
        up = s[s.z > 0]
        g.append({"hour": hr, "n_dn": len(dn), "x2_dn_bp": dn.x2.mean() * 1e4,
                  "t_x2_dn": stats.ttest_1samp(dn.x2, 0).statistic,
                  "t_gain": stats.ttest_1samp(gain, 0).statistic,
                  "corr_z_x2_dn": dn[["z", "x2"]].corr().iloc[0, 1],
                  "x2_up_bp": up.x2.mean() * 1e4,
                  "corr_z_x2_all": s[["z", "x2"]].corr().iloc[0, 1]})
    out["by_close_hour"] = pd.DataFrame(g).round(4)
    # settlement vs non-settlement, z bins, horizons
    d["zbin"] = pd.cut(d.z, [-10, -2, -1, -0.5, 0, 0.5, 1, 2, 10])
    t = d.groupby(["settle", "zbin"], observed=True)[["x1", "x2", "x4", "x8", "pre2"]].mean() * 1e4
    t["n"] = d.groupby(["settle", "zbin"], observed=True).size()
    out["zbin_bp"] = t.round(2)
    st = d[d.settle & (d.z < 0)]
    out["settle_dn_by_coin"] = st.groupby("coin").agg(n=("x2", "size"), x2bp=("x2", lambda v: v.mean() * 1e4),
        t=("x2", lambda v: stats.ttest_1samp(v, 0).statistic), corr=("z", lambda v: np.corrcoef(v, st.loc[v.index, "x2"])[0, 1])).round(3)
    out["settle_dn_by_year"] = st.groupby("year").agg(n=("x2", "size"), x2bp=("x2", lambda v: v.mean() * 1e4),
        t=("x2", lambda v: stats.ttest_1samp(v, 0).statistic), corr=("z", lambda v: np.corrcoef(v, st.loc[v.index, "x2"])[0, 1])).round(3)
    nst = d[~d.settle & (d.z < 0)]
    out["settle_minus_other_x2_dn_t"] = stats.ttest_ind(st.x2, nst.x2, equal_var=False).statistic
    out["volrel_by_settle"] = d.groupby("settle")["volrel"].mean()
    return out
