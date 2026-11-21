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
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            lr = np.r_[np.nan, np.diff(np.log(c))]
            n = len(c)
            for h in (24, 72, 168):
                for t in range(0, n - h, h):
                    past = c[t] / c[t - 72] - 1 if t >= 72 else np.nan
                    resid = np.nan
                    if t >= 72:
                        seg = lr[t - 71:t + 1]
                        net = np.nansum(seg)
                        if net > 0:
                            top = np.sort(seg[~np.isnan(seg)])[-3:].sum()
                            resid = 1 - top / net
                    rows.append((coin, w, h, yr[t], f[t], c[t + h] / c[t] - 1, past, resid))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "yr", "f", "fwd", "past", "resid"])
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in (24, 72, 168):
        s = d[(d.h == h) & (d.f > 0)].dropna(subset=["ex"])
        sl, t = ols_t(s.ex, [s.f])
        s2 = s.dropna(subset=["past"])
        sl2, t2 = ols_t(s2.ex, [s2.f, s2.past])
        slp, tp = ols_t(s2.ex, [s2.past])
        z = d[(d.h == h) & (d.f == 0)].ex.dropna()
        res.append(dict(h=h, n=len(s), t_f=t, t_f_ctrl_past=t2, t_past_only=tp,
                        mean_ex_on=s.ex.mean(), mean_ex_off=z.mean(), n_off=len(z),
                        welch_on_off=stats.ttest_ind(s.ex, z, equal_var=False).statistic))
    out["by_horizon"] = pd.DataFrame(res)
    s = d[(d.h == 72) & (d.f > 0)].dropna(subset=["ex"]).copy()
    g = []
    for k, x in s.groupby("coin"):
        g.append(dict(coin=k, n=len(x), t=ols_t(x.ex, [x.f])[1], mean_ex=x.ex.mean()))
    out["by_coin_72"] = pd.DataFrame(g)
    g = []
    for k, x in s.groupby("yr"):
        g.append(dict(yr=k, n=len(x), t=ols_t(x.ex, [x.f])[1], mean_ex=x.ex.mean()))
    out["by_year_72"] = pd.DataFrame(g)
    s["fq"] = pd.qcut(s.f, 5, labels=False, duplicates="drop")
    out["by_fq_72"] = s.groupby("fq").agg(n=("ex", "size"), f=("f", "mean"), ex=("ex", "mean"),
                                           sd=("ex", "std"), resid=("resid", "mean"), past=("past", "mean"))
    s3 = s.dropna(subset=["past"]).copy()
    s3["pq"] = pd.qcut(s3.past, 3, labels=False)
    g = []
    for k, x in s3.groupby("pq"):
        g.append(dict(past_terc=k, n=len(x), past=x.past.mean(), t_f=ols_t(x.ex, [x.f])[1],
                      t_resid=ols_t(x.dropna(subset=["resid"]).ex, [x.dropna(subset=["resid"]).resid])[1],
                      mean_ex=x.ex.mean()))
    out["by_past_terc_72"] = pd.DataFrame(g)
    # raw residual share (unstandardised) on all rises
    r = d[(d.h == 72)].dropna(subset=["resid", "ex"])
    out["raw_resid_72"] = pd.Series(dict(n=len(r), t_resid=ols_t(r.ex, [r.resid])[1],
                                         t_resid_ctrl_past=ols_t(r.ex, [r.resid, r.past])[1],
                                         corr_f_resid=s.dropna(subset=["resid"])[["f", "resid"]].corr().iloc[0, 1]))
    return out
