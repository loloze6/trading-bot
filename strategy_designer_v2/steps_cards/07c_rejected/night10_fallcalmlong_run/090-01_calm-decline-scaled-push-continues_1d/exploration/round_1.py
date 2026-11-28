import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    # drift per coin per horizon
    drift = {}
    for c, wins in bars.items():
        for h in H:
            r = []
            for w, df in wins.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(r) if r else np.nan
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            lr = np.log(cl).diff()
            sd30 = lr.rolling(30, min_periods=20).std()
            inprof = (df["regime"] == "unknown").values
            push = df["debug_info.components.push.last_history_value"].values
            p10 = (cl / cl.shift(10) - 1) / sd30
            p20 = (cl / cl.shift(20) - 1) / sd30
            p3 = (cl / cl.shift(3) - 1) / sd30
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for i in range(0, n, 5):
                if not inprof[i]:
                    continue
                d = {"coin": c, "win": w, "year": yr[i], "i": i, "push": push[i],
                     "p3": p3.iloc[i], "p10": p10.iloc[i], "p20": p20.iloc[i],
                     "ts": str(df["timestamp"].iloc[i])[:10]}
                for h in H:
                    if i + h < n:
                        d[f"f{h}"] = cl.iloc[i + h] / cl.iloc[i] - 1 - drift[(c, h)]
                    else:
                        d[f"f{h}"] = np.nan
                rows.append(d)
    S = pd.DataFrame(rows)
    out = {}
    out["n samples by coin"] = S.groupby("coin").size()

    def slope_t(x, y, g):
        m = x.notna() & y.notna()
        x, y, g = x[m], y[m], g[m]
        if len(x) < 20:
            return (np.nan, np.nan, len(x))
        X = np.c_[np.ones(len(x)), x.values]
        b = np.linalg.lstsq(X, y.values, rcond=None)[0]
        e = y.values - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for k, ix in pd.Series(range(len(g))).groupby(g.values):
            s = (X[ix.values] * e[ix.values, None]).sum(0)
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return (b[1], b[1] / np.sqrt(V[1, 1]), len(x))

    res = []
    for sig in ["push", "p3", "p10", "p20"]:
        for h in H:
            b, t, n = slope_t(S[sig], S[f"f{h}"], S["ts"])
            res.append({"sig": sig, "h": h, "slope": b, "t": t, "n": n})
    out["slope by signal x horizon"] = pd.DataFrame(res)

    # push quintiles vs forward returns
    S["q"] = pd.qcut(S["push"], 5, labels=False)
    agg = S.groupby("q").agg(push=("push", "mean"), n=("f5", "count"),
                             f1=("f1", "mean"), f3=("f3", "mean"), f5=("f5", "mean"),
                             f10=("f10", "mean"), f20=("f20", "mean"))
    out["push quintiles (unusual moves)"] = agg
    # by coin
    rc = []
    for c, g in S.groupby("coin"):
        for h in [5, 10]:
            b, t, n = slope_t(g["push"], g[f"f{h}"], g["ts"])
            rc.append({"coin": c, "h": h, "slope": b, "t": t, "n": n,
                       "mean_pos": g.loc[g.push > 0, f"f{h}"].mean(),
                       "mean_neg": g.loc[g.push <= 0, f"f{h}"].mean()})
    out["by coin"] = pd.DataFrame(rc)
    ry = []
    for y, g in S.groupby("year"):
        b, t, n = slope_t(g["push"], g["f5"], g["ts"])
        ry.append({"year": y, "slope": b, "t": t, "n": n})
    out["by year h5"] = pd.DataFrame(ry)
    # positive vs negative push
    pos = S.loc[S.push > 0]; neg = S.loc[S.push <= 0]
    rp = []
    for h in H:
        a, b2 = pos[f"f{h}"].dropna(), neg[f"f{h}"].dropna()
        bp, tp, n_p = slope_t(pos["push"], pos[f"f{h}"], pos["ts"])
        bn, tn, n_n = slope_t(neg["push"], neg[f"f{h}"], neg["ts"])
        rp.append({"h": h, "mean_pos": a.mean(), "mean_neg": b2.mean(),
                   "welch_t": stats.ttest_ind(a, b2, equal_var=False).statistic,
                   "slope_pos": bp, "t_pos": tp, "slope_neg": bn, "t_neg": tn})
    out["pos vs neg push"] = pd.DataFrame(rp)
    return out
