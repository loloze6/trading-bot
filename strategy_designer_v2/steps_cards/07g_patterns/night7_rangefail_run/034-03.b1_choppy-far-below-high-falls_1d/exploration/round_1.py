def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c - hi) / hi / sd
            tr60 = c / c.shift(60) - 1
            r1 = r
            r5p = c / c.shift(5) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            volrank = sd / sd.rolling(60, min_periods=30).median()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "depth": depth, "tr60": tr60, "r1": r1, "r5p": r5p,
                               "fwd": fwd, "fwd1": fwd1, "regime": b["regime"].values,
                               "fc": b["forecast"].values, "alloc": b["postRebalance_current_allocation"].values,
                               "volrank": volrank, "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year.values, "sd": sd})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["fwd_adj"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0)].dropna(subset=["fwd_adj"])
    def summ(g, col="fwd_adj"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    # depth buckets by trend bucket (computed trend)
    G2 = G.dropna(subset=["depth", "tr60"]).copy()
    G2["trend"] = pd.cut(G2.tr60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G2["dq"] = pd.cut(G2.depth, [-100, -3, -1.5, -0.5, -1e-9, 100], labels=["<-3", "-3..-1.5", "-1.5..-0.5", "-0.5..0", ">=0(at/above)"])
    out["depth_by_trend"] = G2.groupby(["trend", "dq"]).apply(summ).round(3)
    # prior 5d return buckets by trend
    G2["r5q"] = pd.qcut(G2.r5p, 5, labels=False)
    out["prior5d_quintile_by_trend"] = G2.groupby(["trend", "r5q"]).apply(summ).round(3)
    # vol level
    G3 = G.dropna(subset=["volrank"]).copy()
    G3["vq"] = pd.qcut(G3.volrank, 4, labels=False)
    out["volrank_quartile"] = G3.groupby("vq").apply(summ).round(3)
    # 1-day: large moves
    D = A.dropna(subset=["r1", "sd", "fwd1"]).copy()
    D["z"] = D.r1 / D.sd.shift(1)
    D["zq"] = pd.cut(D.z, [-100, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 100])
    out["fwd1_by_prior_day_z"] = D.groupby("zq").apply(lambda g: summ(g, "fwd1")).round(3)
    out["fwd1_by_weekday"] = D.groupby("wd").apply(lambda g: summ(g, "fwd1")).round(3)
    # book: position gain by window and by trend at entry
    A["gain"] = A["alloc"] * A["fwd1"]
    out["book_gain_by_window"] = A.groupby("w").agg(gain_sum=("gain", "sum"), days_pos=("alloc", lambda s: (s.abs() > 0).sum())).round(4)
    out["book_gain_by_year"] = A.groupby("yr").agg(gain_sum=("gain", "sum")).round(4)
    return out
