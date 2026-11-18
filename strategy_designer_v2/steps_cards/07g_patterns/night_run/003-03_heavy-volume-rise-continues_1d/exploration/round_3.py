import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(n))

def explore(data):
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            z = r / sd
            rv = v / v.rolling(30, min_periods=20).mean()
            fwd = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), 5)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "z": z.iloc[idx].values, "rv": rv.iloc[idx].values,
                "fwd": fwd.iloc[idx].values, "yr": ts.iloc[idx].dt.year.values}))
            daily.append(pd.DataFrame({"coin": coin, "win": w, "r": r.values, "wd": ts.dt.dayofweek.values,
                "yr": ts.dt.year.values, "z": z.values, "rv": rv.values, "f1": fwd1.values}))
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "z", "rv"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    Dd = pd.concat(daily, ignore_index=True).dropna(subset=["r"])
    out = {}
    # Saturday by coin and year
    Dd["sat"] = Dd["wd"] == 5
    def satdiff(d):
        a = d.loc[d.sat, "r"]; o = d.loc[~d.sat, "r"]
        return pd.Series({"sat_mean": a.mean(), "diff": a.mean() - o.mean(),
                          "t": stats.ttest_ind(a, o, equal_var=False).statistic, "n_sat": len(a)})
    out["saturday minus other days by coin"] = Dd.groupby("coin").apply(satdiff).round(4)
    out["saturday minus other days by year"] = Dd.groupby("yr").apply(satdiff).round(4)
    # cross-sectional average day (one obs per date) to remove coin correlation
    Dd["day_key"] = Dd.groupby(["coin", "win"]).cumcount()
    # up days: joint regression of ex on z and log rv
    up = G[G.z > 0.3].copy(); up["lrv"] = np.log(up.rv)
    X = np.column_stack([np.ones(len(up)), up.z, up.lrv])
    beta, res, *_ = np.linalg.lstsq(X, up.ex.values, rcond=None)
    e = up.ex.values - X @ beta
    s2 = (e @ e) / (len(up) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["up days: ex ~ z + log rv"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z", "lrv"]).round(4)
    dn = G[G.z < -0.3].copy(); dn["lrv"] = np.log(dn.rv)
    X = np.column_stack([np.ones(len(dn)), dn.z, dn.lrv])
    beta, *_ = np.linalg.lstsq(X, dn.ex.values, rcond=None)
    e = dn.ex.values - X @ beta
    s2 = (e @ e) / (len(dn) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["down days: ex ~ z + log rv"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z", "lrv"]).round(4)
    out["down days spearman rv vs ex by coin"] = dn.groupby("coin").apply(
        lambda d: pd.Series(stats.spearmanr(d.rv, d.ex), index=["rho", "p"])).round(4)
    out["up days spearman z vs ex by coin"] = G[G.z > 0.3].groupby("coin").apply(
        lambda d: pd.Series(stats.spearmanr(d.z, d.ex), index=["rho", "p"])).round(4)
    dn["rvq"] = dn.groupby("coin")["rv"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["down days by rv tercile"] = dn.groupby("rvq")["ex"].agg(mean="mean", n="count", t=_t).round(4)
    out["down days by rv tercile by year"] = dn.groupby(["yr", "rvq"])["ex"].mean().unstack().round(4)
    return out
