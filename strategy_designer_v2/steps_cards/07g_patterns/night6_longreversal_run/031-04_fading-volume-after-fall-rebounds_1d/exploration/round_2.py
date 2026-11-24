def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]

    def clust_ols(x, y, g):
        x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
        ok = np.isfinite(x) & np.isfinite(y); x, y, g = x[ok], y[ok], g[ok]
        X = np.column_stack([np.ones_like(x), x]); n = len(y)
        if n < 10: return (np.nan, np.nan, n, 0)
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        meat = np.zeros((2, 2)); G = 0
        for k in pd.unique(g):
            m = g == k; s = X[m].T @ e[m]; meat += np.outer(s, s); G += 1
        V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return (b[1], b[1] / np.sqrt(V[1, 1]), n, G)

    rows = []
    wk = {}
    for H in (1, 3, 7, 14):
        feats = {k: ([], [], []) for k in
                 ("ret1d_z", "ret7d_z", "vol14_over60_log", "volume_spike1d_log", "range1d_z", "dist_from_14d_high")}
        for c in bars:
            rets = []; fwd_all = []
            for w, df in bars[c].items():
                cl = df["close"].values
                rets.append(np.diff(np.log(cl)))
                for t in range(0, len(cl) - H, H):
                    fwd_all.append(cl[t + H] / cl[t] - 1)
            sd = np.std(np.concatenate(rets)); drift = np.mean(fwd_all)
            for w, df in bars[c].items():
                cl = df["close"].values; v = df["volume"].values.astype(float)
                hi = df["high"].values; lo = df["low"].values
                ts = pd.to_datetime(df["timestamp"]).values
                lr = np.r_[np.nan, np.diff(np.log(cl))]
                for t in range(0, len(cl) - H, H):
                    if t < 60: continue
                    f = cl[t + H] / cl[t] - 1 - drift
                    vals = {
                        "ret1d_z": lr[t] / sd,
                        "ret7d_z": np.log(cl[t] / cl[t - 7]) / (sd * np.sqrt(7)),
                        "vol14_over60_log": np.log(np.nanstd(lr[t-13:t+1]) / np.nanstd(lr[t-59:t+1])),
                        "volume_spike1d_log": np.log(v[t] / v[t-29:t+1].mean()) if v[t] > 0 else np.nan,
                        "range1d_z": np.log(hi[t] / lo[t]) / sd,
                        "dist_from_14d_high": np.log(cl[t] / hi[t-13:t+1].max()) / sd,
                    }
                    for k, x in vals.items():
                        feats[k][0].append(x); feats[k][1].append(f); feats[k][2].append(ts[t])
                    if H == 1:
                        d = pd.Timestamp(ts[t + 1]).dayofweek
                        wk.setdefault(d, []).append(cl[t + 1] / cl[t] - 1 - drift)
        for k, (x, y, g) in feats.items():
            b, tt, n, G = clust_ols(x, y, g)
            rows.append({"H_days": H, "feature": k, "slope": b, "t_clustered": tt, "n": n, "days": G})
    out["feature_slopes"] = pd.DataFrame(rows)
    wd = pd.DataFrame({d: {"mean_excess": np.mean(v), "t": np.mean(v) / (np.std(v, ddof=1) / np.sqrt(len(v))), "n": len(v)}
                       for d, v in sorted(wk.items())}).T
    out["weekday_next_day_excess"] = wd
    return out
