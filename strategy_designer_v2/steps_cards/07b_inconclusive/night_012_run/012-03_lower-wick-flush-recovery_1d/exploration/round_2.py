def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3]
    cmean = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(20).std()
            z = (r1 / sd).values
            vr = (df["volume"] / df["volume"].shift(1).rolling(20).mean()).values
            rng = (df["high"] - df["low"]).values
            wick = np.where(rng > 0, (cl - df["low"].values) / rng, np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            sharp = z <= -2
            last = -99
            for i in np.where(sharp)[0]:
                if i - last < 3:
                    continue
                last = i
                d = dict(coin=c, win=w, year=yr[i], z=z[i], vr=vr[i], wick=wick[i],
                         flush=bool(vr[i] >= 2))
                for h in H:
                    d[f"x{h}"] = (cl[i + h] / cl[i] - 1 - cmean[(c, h)]) if i + h < len(cl) else np.nan
                rows.append(d)
    f = pd.DataFrame(rows)
    out = {}
    def slope_t(sub, y, x="wick"):
        s = sub[[x, y]].dropna()
        if len(s) < 5: return (np.nan, np.nan, len(s))
        r = stats.linregress(s[x], s[y])
        return (r.slope, r.slope / r.stderr, len(s))
    rr = []
    for k, sub in f.groupby("flush"):
        for h in H:
            s, t, n = slope_t(sub, f"x{h}")
            m = sub[f"x{h}"].dropna()
            rr.append(dict(flush=k, h=h, slope=s, t=t, n=n, mean=m.mean(),
                           t_mean=m.mean() / (m.std() / np.sqrt(len(m)))))
    out["sharp_falls_by_volume_burst"] = pd.DataFrame(rr)
    for h in H:
        a = f.loc[f.flush, f"x{h}"].dropna(); b = f.loc[~f.flush, f"x{h}"].dropna()
        out[f"flush_minus_nonflush_x{h}"] = f"{a.mean()-b.mean():.5f} t={stats.ttest_ind(a,b,equal_var=False).statistic:.2f}"
    fl = f[f.flush].copy()
    # graded: close nearer the low (1 - wick) on flush bars -> x1
    fl["dist"] = 1 - fl["wick"]
    rr = []
    for g in ["coin", "year"]:
        for k, sub in fl.groupby(g):
            s, t, n = slope_t(sub, "x1", "dist")
            rr.append(dict(group=g, key=str(k), slope_x1_on_closelow=s, t=t, n=n))
    out["x1_on_closenearlow_by_group"] = pd.DataFrame(rr)
    s = fl[["x1", "dist", "z", "vr"]].dropna()
    X = np.column_stack([np.ones(len(s)), s["dist"], s["z"], np.log(s["vr"])])
    beta, res, *_ = np.linalg.lstsq(X, s["x1"].values, rcond=None)
    e = s["x1"].values - X @ beta
    cov = (e @ e / (len(s) - 4)) * np.linalg.inv(X.T @ X)
    out["x1_multi_t"] = pd.DataFrame(dict(beta=beta, t=beta / np.sqrt(np.diag(cov))),
                                      index=["const", "closenearlow", "z", "logvr"])
    fl["q"] = pd.qcut(fl["dist"], 4, labels=False)
    out["x1_x3_by_closenearlow_quartile"] = fl.groupby("q")[["x1", "x3", "dist"]].mean().assign(n=fl.groupby("q").size())
    return out
