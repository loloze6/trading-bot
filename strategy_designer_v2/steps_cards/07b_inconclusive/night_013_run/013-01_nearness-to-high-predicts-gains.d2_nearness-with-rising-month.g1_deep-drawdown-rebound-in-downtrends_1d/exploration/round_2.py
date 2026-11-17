import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            ret30 = c / c.shift(30) - 1
            depth = c / c.rolling(60, min_periods=20).max() - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            reg = (b["regime"] == "mean_reversion")
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, year=int(yr[i]), fwd=c[i + 7] / c[i] - 1,
                                 reg=bool(reg[i]), r30=ret30[i], deep=-depth[i]))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    d = df[df.reg].dropna(subset=["deep", "ex", "r30"]).copy()
    out = {}
    def st(g, x="deep"):
        if len(g) < 10: return (np.nan, np.nan, np.nan, len(g))
        r = stats.linregress(g[x], g["ex"])
        rho = stats.spearmanr(g[x], g["ex"])[0]
        return (r.slope, r.slope / r.stderr, rho, len(g))
    lo, hi = d.ex.quantile([0.01, 0.99])
    dt = d[(d.ex > lo) & (d.ex < hi)]
    out["robust"] = pd.DataFrame([dict(sample="all", **dict(zip(["slope","t","rho","n"], st(d)))),
                                  dict(sample="trim1pct", **dict(zip(["slope","t","rho","n"], st(dt)))),
                                  dict(sample="r30_bottom_half", **dict(zip(["slope","t","rho","n"], st(d[d.r30 < d.r30.median()])))),
                                  dict(sample="r30_top_half", **dict(zip(["slope","t","rho","n"], st(d[d.r30 >= d.r30.median()]))))])
    # regress on both deep and r30
    X = np.column_stack([np.ones(len(d)), d.deep, d.r30])
    beta, *_ = np.linalg.lstsq(X, d.ex, rcond=None)
    res = d.ex - X @ beta
    s2 = (res ** 2).sum() / (len(d) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi"] = pd.DataFrame(dict(beta=beta, t=beta / se), index=["const", "deep", "r30"])
    # 30-day return as signal itself (negated)
    d["fall30"] = -d["r30"]
    out["fall30_slope"] = pd.Series(dict(zip(["slope","t","rho","n"], st(d, "fall30"))))
    d["dq"] = pd.qcut(d.deep, 3, labels=False)
    d["rq"] = pd.qcut(d.r30, 3, labels=False)
    out["grid_deep_x_r30"] = d.pivot_table(index="dq", columns="rq", values="ex", aggfunc="mean")
    out["grid_n"] = d.pivot_table(index="dq", columns="rq", values="ex", aggfunc="size")
    top = d[d.dq == 2]
    out["top_third_depth_by_year"] = top.groupby("year").ex.agg(["mean", "size"])
    out["top_third_t"] = float(top.ex.mean() / (top.ex.std() / np.sqrt(len(top))))
    return out
