import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].values; n = len(df)
            r = pd.Series(c).pct_change()
            df["r1"] = r
            for k in [2, 3, 4, 5, 7]:
                df[f"r{k}"] = pd.Series(c).pct_change(k)
            df["sd30"] = r.rolling(30, min_periods=20).std()
            df["inprof"] = df["regime"].isin(["mean_reversion", "unknown"])
            for h in [2, 3, 5]:
                fr = np.full(n, np.nan); fr[:n-h] = c[h:] / c[:n-h] - 1
                df[f"f{h}"] = fr; df[f"g{h}"] = (np.arange(n) % h == 0)
            df["coin"] = coin; df["win"] = w
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = {h: A[A[f"g{h}"]].groupby("coin")[f"f{h}"].mean() for h in [2, 3, 5]}

    def ct(d):
        m = d["u"].mean()
        dev = (d["u"] - m).groupby(d["day"]).sum()
        D = len(dev)
        if D < 3: return m, np.nan, D
        se = np.sqrt(D/(D-1) * (dev**2).sum()) / len(d)
        return m, m/se, D

    out = {}
    res = []; grade = []
    for k in [2, 3, 5, 7]:
        for h in [2, 3, 5]:
            d = A[A.inprof & A[f"g{h}"] & (A[f"r{k}"] > 0)].dropna(subset=[f"f{h}", "sd30"]).copy()
            d["u"] = -(d[f"f{h}"] - d["coin"].map(drift[h]))
            d["z"] = d[f"r{k}"] / (d.sd30 * np.sqrt(k))
            med = d.z.median()
            hi = d[d.z > med]; lo = d[d.z <= med]
            mh, th, Dh = ct(hi); ml, tl, Dl = ct(lo)
            rho, p = stats.spearmanr(d.z, d.u)
            # weighted by z (graded short)
            wm = (d.u * d.z).sum() / d.z.sum()
            res.append({"k": k, "h": h, "n": len(d), "rho": rho, "p": p,
                        "hi_mean": mh, "hi_t": th, "hi_days": Dh, "lo_mean": ml, "lo_t": tl,
                        "hi_minus_lo": mh - ml, "welch_t": stats.ttest_ind(hi.u, lo.u, equal_var=False).statistic,
                        "z_weighted_mean": wm})
    out["rise k-day, horizon h: grading"] = pd.DataFrame(res)

    # all profile bars, signed z of 3-day return vs short unusual at h=3
    d = A[A.inprof & A["g3"]].dropna(subset=["f3", "sd30", "r3"]).copy()
    d["u"] = -(d["f3"] - d["coin"].map(drift[3]))
    d["z"] = d.r3 / (d.sd30 * np.sqrt(3))
    d["q"] = pd.qcut(d.z, 5, labels=False)
    out["all profile r3 z quintile, short unusual h3"] = d.groupby("q").agg(z=("z","mean"), u=("u","mean"), n=("u","count"))

    # robustness of hi half (r3>0, h=3) by coin, year
    d = A[A.inprof & A["g3"] & (A.r3 > 0)].dropna(subset=["f3", "sd30"]).copy()
    d["u"] = -(d["f3"] - d["coin"].map(drift[3]))
    d["z"] = d.r3 / (d.sd30 * np.sqrt(3))
    d["half"] = np.where(d.z > d.z.median(), "hi", "lo")
    out["r3pos h3 by coin/half"] = d.groupby(["coin", "half"])["u"].agg(["mean", "count"])
    out["r3pos h3 by year/half"] = d.groupby(["year", "half"])["u"].agg(["mean", "count"])
    out["r3pos h3 z by half"] = d.groupby("half")["z"].agg(["mean", "min", "max"])
    return out
