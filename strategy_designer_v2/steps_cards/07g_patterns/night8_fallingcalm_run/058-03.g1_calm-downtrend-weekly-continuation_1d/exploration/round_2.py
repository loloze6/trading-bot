def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["ret1"] = c / c.shift(1) - 1
            b["ret5"] = c / c.shift(5) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["vol30"] = b["ret1"].rolling(30).std()
            b["vpct"] = b["vol30"].rolling(365, min_periods=120).apply(lambda s: (s <= s[-1]).mean(), raw=True)
            b["inprof"] = (b["regime"] == "unknown").astype(int)
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % H == 0)
            b["gain"] = b["postRebalance_current_allocation"] * b["fwd1"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B[B.grid].groupby("coin")["fwd"].mean()
    sd = B[B.grid].groupby("coin")["fwd"].std()
    B["ex"] = B["fwd"] - B["coin"].map(drift)
    def summ(g, col):
        x = g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    B["trend"] = np.where(B.ret60 > 0.1, "rising", np.where(B.ret60 < -0.1, "falling", "choppy"))
    B["agit"] = np.where(B.vpct > 0.5, "agit", "calm")
    G = B[B.grid].dropna(subset=["ret5", "fwd", "ret60", "vpct"]).copy()
    G["sgn"] = np.sign(G.ret5); G["cont"] = G.sgn * G.ex
    G["absq"] = G.groupby(["trend", "agit"])["ret5"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False, duplicates="drop"))
    out["continuation by profile x |ret5| tercile"] = G.groupby(["trend", "agit", "absq"]).apply(lambda g: summ(g, "cont")).round(3)
    # weekday by profile and year
    A = B.dropna(subset=["fwd1", "ret60", "vpct"]).copy()
    A["thfr"] = A.wd.isin([3, 4]).astype(int)
    out["Thu+Fri vs other next1d, by year"] = A.groupby(["yr", "thfr"]).apply(lambda g: summ(g, "fwd1")).round(3)
    out["Thu+Fri vs other next1d, by trend"] = A.groupby(["trend", "thfr"]).apply(lambda g: summ(g, "fwd1")).round(3)
    # book gain by side in profile
    Q = B[B.postRebalance_current_allocation.abs() > 0].dropna(subset=["fwd1"]).copy()
    Q["side"] = np.sign(Q.postRebalance_current_allocation)
    out["bar gain by side (held)"] = Q.groupby("side").apply(lambda g: summ(g, "gain")).round(4)
    out["bar gain by side x inprof"] = Q.groupby(["inprof", "side"]).apply(lambda g: summ(g, "gain")).round(4)
    return out
