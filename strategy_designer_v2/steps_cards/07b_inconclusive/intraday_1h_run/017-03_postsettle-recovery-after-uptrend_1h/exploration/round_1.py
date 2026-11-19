import numpy as np, pandas as pd
from scipy import stats

def _ols(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 10:
        return np.nan, np.nan, n
    r = stats.linregress(x, y)
    return r.slope, r.slope / r.stderr if r.stderr > 0 else np.nan, n

def explore(data):
    bars = data["bars"]
    H = [1, 2, 4, 8]
    rows = []
    for coin, wins in bars.items():
        # coin mean h-bar return on non-overlapping grid, pooled over windows
        means = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            means[h] = np.nanmean(np.concatenate(rs))
        for w, df in wins.items():
            d = pd.DataFrame({"ts": pd.to_datetime(df["timestamp"], utc=True), "close": df["close"].values,
                              "fc": df["forecast"].values})
            d["hour"] = d["ts"].dt.hour
            d["year"] = d["ts"].dt.year
            d["rise"] = d["close"] / d["close"].shift(72) - 1
            d["pre2"] = d["close"] / d["close"].shift(2) - 1
            for h in H:
                d[f"ex{h}"] = d["close"].shift(-h) / d["close"] - 1 - means[h]
            d["coin"] = coin
            d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A["rise"] > 0]
    out = {}
    # by hour (placebo), h=2, graded by raw rise
    t = []
    for hr, g in A.groupby("hour"):
        s, tt, n = _ols(g["rise"].values, g["ex2"].values)
        t.append({"hour": hr, "n": n, "slope_t_rise": tt, "mean_ex2_bp": g["ex2"].mean() * 1e4,
                  "mean_pre2_bp": g["pre2"].mean() * 1e4})
    out["by_hour_h2_rise>0"] = pd.DataFrame(t)
    S = A[A["hour"].isin([23, 7, 15]) & (A["fc"] > 0)]
    # horizons on main cases, graded by forecast and by raw rise
    t = []
    for h in H:
        s1, t1, n1 = _ols(S["fc"].values, S[f"ex{h}"].values)
        s2, t2, n2 = _ols(S["rise"].values, S[f"ex{h}"].values)
        wm = np.nansum(S[f"ex{h}"] * S["fc"]) / S["fc"][S[f"ex{h}"].notna()].sum()
        t.append({"h": h, "n": n1, "t_fc": t1, "t_rise": t2, "fcw_mean_bp": wm * 1e4,
                  "mean_bp": S[f"ex{h}"].mean() * 1e4})
    out["main_cases_by_horizon"] = pd.DataFrame(t)
    # by coin / year / settlement hour, h=2
    for key in ["coin", "year", "hour"]:
        t = []
        for k, g in S.groupby(key):
            s1, t1, n1 = _ols(g["fc"].values, g["ex2"].values)
            s2, t2, n2 = _ols(g["rise"].values, g["ex2"].values)
            t.append({key: k, "n": n1, "t_fc": t1, "t_rise": t2, "mean_bp": g["ex2"].mean() * 1e4})
        out[f"main_by_{key}"] = pd.DataFrame(t)
    # by forecast quintile
    S2 = S.copy()
    S2["q"] = pd.qcut(S2["fc"], 5, labels=False, duplicates="drop")
    out["main_by_fc_quintile"] = S2.groupby("q").agg(n=("ex2", "count"), mean_ex2_bp=("ex2", lambda x: x.mean() * 1e4),
                                                    t=("ex2", lambda x: x.mean() / x.std() * np.sqrt(x.count())),
                                                    mean_fc=("fc", "mean"), mean_rise=("rise", "mean"))
    S2["rq"] = pd.qcut(S2["rise"], 5, labels=False, duplicates="drop")
    out["main_by_rise_quintile"] = S2.groupby("rq").agg(n=("ex2", "count"), mean_ex2_bp=("ex2", lambda x: x.mean() * 1e4),
                                                       t=("ex2", lambda x: x.mean() / x.std() * np.sqrt(x.count())),
                                                       mean_rise=("rise", "mean"))
    return out
