import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    drift = {}
    sdh = {}
    for c, wins in bars.items():
        for h in H:
            r = []
            for w, df in wins.items():
                cl = df["close"].values.astype(float)
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(r) if r else np.nan
            sdh[(c, h)] = np.std(r, ddof=1) if len(r) > 1 else np.nan
    rows = []
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cl = df["close"].astype(float)
            ret = cl.pct_change()
            sd30 = ret.rolling(30, min_periods=20).std()
            inprof = (df["regime"].astype(str) == "unknown").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            sigs = {}
            for p in [3, 5, 10, 20]:
                sigs[f"p{p}"] = ((cl / cl.shift(p) - 1) / sd30).values
            r60 = (cl / cl.shift(60) - 1).values
            for i in range(0, n, 5):
                d = {"coin": c, "win": w, "year": yr[i], "inprof": bool(inprof[i]),
                     "ts": str(df["timestamp"].iloc[i])[:10], "r60": r60[i]}
                for k, v in sigs.items():
                    d[k] = v[i]
                for h in H:
                    d[f"f{h}"] = (cl.iloc[i + h] / cl.iloc[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                rows.append(d)
    S = pd.DataFrame(rows)

    def slope_t(x, y, g):
        m = x.notna() & y.notna() & np.isfinite(x)
        x, y, g = x[m], y[m], g[m]
        if len(x) < 20:
            return (np.nan, np.nan, int(len(x)))
        X = np.c_[np.ones(len(x)), x.values]
        b = np.linalg.lstsq(X, y.values, rcond=None)[0]
        e = y.values - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        gv = g.values
        for k in np.unique(gv):
            ix = gv == k
            s = (X[ix] * e[ix, None]).sum(0)
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return (b[1], b[1] / np.sqrt(V[1, 1]), int(len(x)))

    out = {}
    I = S[S.inprof]; O = S[~S.inprof]
    out["samples in/out profile by coin"] = S.groupby(["coin", "inprof"]).size().unstack()
    res = []
    for lab, G in [("in", I), ("out", O)]:
        for sig in ["p3", "p5", "p10", "p20"]:
            for h in H:
                b, t, n = slope_t(G[sig], G[f"f{h}"], G["ts"])
                res.append({"prof": lab, "sig": sig, "h": h, "slope_x100": b * 100, "t": t, "n": n})
    out["slope signal x horizon, in vs out"] = pd.DataFrame(res)
    I = I.copy()
    I["q"] = pd.qcut(I["p5"], 5, labels=False)
    out["in-profile p5 quintiles, unusual % "] = I.groupby("q").agg(
        p5=("p5", "mean"), n=("f5", "count"), f1=("f1", "mean"), f3=("f3", "mean"),
        f5=("f5", "mean"), f10=("f10", "mean"), f20=("f20", "mean")).assign(
        f1=lambda d: d.f1 * 100, f3=lambda d: d.f3 * 100, f5=lambda d: d.f5 * 100,
        f10=lambda d: d.f10 * 100, f20=lambda d: d.f20 * 100)
    rc = []
    for c, g in I.groupby("coin"):
        for h in [5, 10]:
            b, t, n = slope_t(g["p5"], g[f"f{h}"], g["ts"])
            rc.append({"coin": c, "h": h, "slope_x100": b * 100, "t": t, "n": n,
                       "pos%": g.loc[g.p5 > 0, f"f{h}"].mean() * 100,
                       "neg%": g.loc[g.p5 <= 0, f"f{h}"].mean() * 100})
    out["in-profile by coin"] = pd.DataFrame(rc)
    ry = []
    for y, g in I.groupby("year"):
        b, t, n = slope_t(g["p5"], g["f5"], g["ts"])
        b2, t2, _ = slope_t(g["p5"], g["f10"], g["ts"])
        ry.append({"year": y, "slope5_x100": b * 100, "t5": t, "slope10_x100": b2 * 100, "t10": t2, "n": n})
    out["in-profile by year"] = pd.DataFrame(ry)
    pos = I[I.p5 > 0]; neg = I[I.p5 <= 0]
    rp = []
    for h in H:
        a, b2 = pos[f"f{h}"].dropna(), neg[f"f{h}"].dropna()
        bp, tp, _ = slope_t(pos["p5"], pos[f"f{h}"], pos["ts"])
        bn, tn, _ = slope_t(neg["p5"], neg[f"f{h}"], neg["ts"])
        rp.append({"h": h, "n_pos": len(a), "n_neg": len(b2), "pos%": a.mean() * 100, "neg%": b2.mean() * 100,
                   "welch_t": stats.ttest_ind(a, b2, equal_var=False).statistic,
                   "slope_pos_x100": bp * 100, "t_pos": tp, "slope_neg_x100": bn * 100, "t_neg": tn})
    out["in-profile pos vs neg push"] = pd.DataFrame(rp)
    # depth of decline: r60 terciles in profile
    I["dq"] = pd.qcut(I["r60"], 3, labels=False)
    rd = []
    for q, g in I.groupby("dq"):
        b, t, n = slope_t(g["p5"], g["f5"], g["ts"])
        b2, t2, _ = slope_t(g["p5"], g["f10"], g["ts"])
        rd.append({"r60_tercile": q, "r60_mean": g.r60.mean(), "slope5_x100": b * 100, "t5": t,
                   "slope10_x100": b2 * 100, "t10": t2, "f5%": g.f5.mean() * 100, "n": n})
    out["in-profile by 60d decline depth"] = pd.DataFrame(rd)
    return out
