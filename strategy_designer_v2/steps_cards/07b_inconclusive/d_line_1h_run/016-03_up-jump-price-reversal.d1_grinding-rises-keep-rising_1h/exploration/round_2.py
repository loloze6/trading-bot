import numpy as np, pandas as pd
from scipy import stats

def ols_t(y, X):
    X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    y = np.asarray(y, float)
    if len(y) < X.shape[1] + 3: return (np.nan, np.nan)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    s2 = r @ r / (len(y) - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return b[1], b[1] / np.sqrt(cov[1, 1])

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values.astype(float); f = b["forecast"].values.astype(float)
            v = b["volume"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            n = len(c)
            for h in (24, 72, 168):
                for t in range(0, n - h, h):
                    if t < 72: continue
                    seg = lr[t - 71:t + 1]; seg = seg[~np.isnan(seg)]
                    net = seg.sum()
                    vs = v[t - 71:t + 1]
                    vconc = np.sort(vs)[-3:].sum() / vs.sum() if vs.sum() > 0 else np.nan
                    if net > 0:
                        resid = 1 - np.sort(seg)[-3:].sum() / net
                    elif net < 0:
                        resid = 1 - np.sort(seg)[:3].sum() / net
                    else:
                        resid = np.nan
                    rows.append((coin, w, h, f[t], c[t + h] / c[t] - 1, net, resid, vconc))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "f", "fwd", "net", "resid", "vconc"])
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in (24, 72, 168):
        for side in ("up", "down"):
            s = d[(d.h == h) & ((d.net > 0) if side == "up" else (d.net < 0))].dropna(subset=["resid", "ex"])
            # signed: for down moves, continuation means negative ex; use ex*sign
            sg = 1 if side == "up" else -1
            y = s.ex * sg
            res.append(dict(h=h, side=side, n=len(s),
                            t_resid=ols_t(y, [s.resid])[1],
                            t_resid_ctrl_size=ols_t(y, [s.resid, s.net.abs()])[1],
                            t_size=ols_t(y, [s.net.abs()])[1],
                            t_vconc=ols_t(y, [s.vconc])[1],
                            mean_cont=y.mean(), t_mean=y.mean() / (y.std() / np.sqrt(len(y)))))
    out["raw_by_h_side"] = pd.DataFrame(res)
    s = d[(d.h == 72) & (d.net > 0)].dropna(subset=["resid", "ex"]).copy()
    s["rq"] = pd.qcut(s.resid, 5, labels=False, duplicates="drop")
    out["up72_by_resid_q"] = s.groupby("rq").agg(n=("ex", "size"), resid=("resid", "mean"),
                                                 ex=("ex", "mean"), sd=("ex", "std"), net=("net", "mean"),
                                                 share_f_pos=("f", lambda x: (x > 0).mean()))
    s = d[(d.h == 72) & (d.net < 0)].dropna(subset=["resid", "ex"]).copy()
    s["rq"] = pd.qcut(s.resid, 5, labels=False, duplicates="drop")
    out["down72_by_resid_q"] = s.groupby("rq").agg(n=("ex", "size"), resid=("resid", "mean"),
                                                   ex=("ex", "mean"), net=("net", "mean"))
    u = d[(d.h == 72) & (d.net > 0)]
    out["fpos_share_of_rises_72"] = pd.Series(dict(rises=len(u), f_pos=(u.f > 0).sum(),
                                                   f_pos_nonrise=((d.h == 72) & (d.net <= 0) & (d.f > 0)).sum()))
    return out
