import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].values
            n = len(df)
            r = pd.Series(c).pct_change()
            df["r1"] = r
            df["r3"] = pd.Series(c).pct_change(3)
            df["r5"] = pd.Series(c).pct_change(5)
            df["sd30"] = r.rolling(30, min_periods=20).std()
            df["rng"] = (df["high"] - df["low"]) / df["close"] / df["sd30"]
            df["inprof"] = df["regime"].isin(["mean_reversion", "unknown"])
            for h in [1, 2, 3, 5]:
                fr = np.full(n, np.nan)
                fr[:n - h] = c[h:] / c[:n - h] - 1
                df[f"f{h}"] = fr
                df[f"g{h}"] = (np.arange(n) % h == 0)
            df["coin"] = coin; df["win"] = w; df["pos"] = np.arange(n)
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin per horizon
    drift = {}
    for h in [1, 2, 3, 5]:
        drift[h] = A[A[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
    out["profile share"] = A.groupby("coin")["inprof"].mean()
    res = []
    conds = {
        "up_day_r3neg": lambda d: (d.r1 > 0) & (d.r3 < 0),
        "r3_pos": lambda d: d.r3 > 0,
        "r5_pos": lambda d: d.r5 > 0,
        "up_day_any": lambda d: d.r1 > 0,
        "all_profile": lambda d: d.r1.notna(),
    }
    for name, f in conds.items():
        for h in [1, 2, 3, 5]:
            d = A[A.inprof & A[f"g{h}"] & f(A)].dropna(subset=[f"f{h}"]).copy()
            d["u"] = -(d[f"f{h}"] - d["coin"].map(drift[h]))
            day = d.groupby(pd.to_datetime(d["timestamp"]).dt.floor("D"))["u"].sum()
            m = d["u"].mean()
            se = np.sqrt(len(day) / (len(day) - 1) * (day - day.mean() * 0 - m * d.groupby(pd.to_datetime(d["timestamp"]).dt.floor("D")).size()).pow(2).sum()) / len(d) if len(day) > 1 else np.nan
            res.append({"cond": name, "h": h, "n": len(d), "days": len(day), "mean_short_unusual": m, "t": m / se if se else np.nan})
    out["short unusual by cond/h"] = pd.DataFrame(res)
    # grading for r3_pos by r3/sd30 terciles at h=2,3
    g = []
    for h in [2, 3, 5]:
        d = A[A.inprof & A[f"g{h}"] & (A.r3 > 0)].dropna(subset=[f"f{h}", "sd30"]).copy()
        d["u"] = -(d[f"f{h}"] - d["coin"].map(drift[h]))
        d["z"] = d.r3 / (d.sd30 * np.sqrt(3))
        d["q"] = pd.qcut(d.z, 3, labels=["lo", "mid", "hi"])
        s = d.groupby("q")["u"].agg(["mean", "count"])
        s["h"] = h
        g.append(s.reset_index())
    out["r3pos graded by z (short unusual)"] = pd.concat(g)
    # range grading in tested cond at h=2
    d = A[A.inprof & A["g2"] & (A.r1 > 0) & (A.r3 < 0)].dropna(subset=["f2", "rng"]).copy()
    d["u"] = -(d["f2"] - d["coin"].map(drift[2]))
    d["q"] = pd.qcut(d.rng, 3, labels=["lo", "mid", "hi"])
    out["tested cond by range tercile"] = d.groupby("q")["u"].agg(["mean", "count"])
    out["tested cond by coin"] = d.groupby("coin")["u"].agg(["mean", "count"])
    out["tested cond by year"] = d.groupby("year")["u"].agg(["mean", "count"])
    # all profile 3d pos by coin/year h=3
    d = A[A.inprof & A["g3"] & (A.r3 > 0)].dropna(subset=["f3"]).copy()
    d["u"] = -(d["f3"] - d["coin"].map(drift[3]))
    out["r3pos h3 by coin"] = d.groupby("coin")["u"].agg(["mean", "count"])
    out["r3pos h3 by year"] = d.groupby("year")["u"].agg(["mean", "count"])
    return out
