def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    # basic: regime counts, forecast nonzero, window lengths
    rc = {}; fnz = 0; ntot = 0; lens = []
    for c in bars:
        for w, df in bars[c].items():
            lens.append(len(df))
            for r, n in df["regime"].value_counts().items():
                rc[r] = rc.get(r, 0) + n
            fnz += int((df["forecast"].fillna(0) != 0).sum()); ntot += len(df)
    out["regime_counts"] = pd.Series(rc)
    out["forecast_nonzero_bars"] = f"{fnz} of {ntot}"
    out["window_len"] = pd.Series(lens).describe()

    def clust_ols(x, y, g):
        x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
        X = np.column_stack([np.ones_like(x), x]); n = len(y)
        if n < 10: return (np.nan, np.nan, n)
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        meat = np.zeros((2, 2)); G = 0
        for k in pd.unique(g):
            m = g == k; s = X[m].T @ e[m]; meat += np.outer(s, s); G += 1
        V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return (b[1], b[1] / np.sqrt(V[1, 1]), n)

    rows = []
    for H in (14, 30):
        for L in (14, 30, 60, 90):
            xs, ys, gs, xv, yv, gv = [], [], [], [], [], []
            for c in bars:
                # coin sd and drift
                rets = []; fwd_all = []
                for w, df in bars[c].items():
                    cl = df["close"].values
                    rets.append(np.diff(np.log(cl)))
                    for t in range(0, len(cl) - H, H):
                        fwd_all.append(cl[t + H] / cl[t] - 1)
                sd = np.std(np.concatenate(rets)); drift = np.mean(fwd_all)
                for w, df in bars[c].items():
                    cl = df["close"].values; vol = df["volume"].values; ts = df["timestamp"].values
                    for t in range(0, len(cl) - H, H):
                        if t < L: continue
                        past = np.log(cl[t] / cl[t - L]) / (sd * np.sqrt(L))
                        f = cl[t + H] / cl[t] - 1 - drift
                        xs.append(past); ys.append(f); gs.append(ts[t])
                        if t >= 60 and L == 60:
                            vr = np.log(vol[t-13:t+1].mean() / vol[t-59:t+1].mean())
                            xv.append(vr * np.sign(-past) if False else vr); yv.append(f); gv.append(ts[t])
            b, tt, n = clust_ols(xs, ys, gs)
            rows.append({"H": H, "L": L, "slope_on_zpast": b, "t": tt, "n": n})
            xs = np.array(xs); ys = np.array(ys)
            for name, m in (("past_z<=-1", xs <= -1), ("past_z>=1", xs >= 1)):
                rows.append({"H": H, "L": L, "group": name, "mean_excess": ys[m].mean() if m.sum() else np.nan,
                             "t": ys[m].mean() / (ys[m].std(ddof=1) / np.sqrt(m.sum())) if m.sum() > 2 else np.nan,
                             "n": int(m.sum())})
            if L == 60 and len(xv):
                b, tt, n = clust_ols(xv, yv, gv)
                rows.append({"H": H, "L": L, "group": "volratio14/60", "slope_on_zpast": b, "t": tt, "n": n})
    out["past_vs_fwd"] = pd.DataFrame(rows)
    return out
