def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = {"1d": 6, "3d": 18, "7d": 42, "14d": 84}
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            hi6 = b["high"].rolling(6).max(); lo6 = b["low"].rolling(6).min()
            rng = (hi6 - lo6) / c
            rngm = rng / rng.rolling(180, min_periods=60).mean()
            r24 = c / c.shift(6) - 1
            vol = r1.rolling(180, min_periods=60).std()
            r7d = c / c.shift(42) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "r24": r24, "rngm": rngm, "vol": vol, "r7d": r7d,
                               "z24": r24 / (vol * np.sqrt(6)), "z7d": r7d / (vol * np.sqrt(42)),
                               "raw": b.get("debug_info.components.panic.last_history_value"),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1n": r1.shift(-1)})
            for k, h in H.items():
                df["f" + k] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def graded(feat, hk, q=5, cond=None):
        h = H[hk]; g = A[A["pos"] % h == 0].dropna(subset=[feat, "f" + hk]).copy()
        drift = g.groupby("coin")["f" + hk].transform("mean")
        usual = g.groupby("coin")["f" + hk].transform("std")
        g["ex"] = (g["f" + hk] - drift) / usual
        if cond is not None: g = g[cond(g)]
        g["bk"] = g.groupby("coin")[feat].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = g.groupby("bk")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
        t.columns = ["mean_strength", "n", "t"]
        rho, p = stats.spearmanr(g[feat], g["ex"])
        t.loc["spearman"] = [rho, len(g), p]
        return t
    for hk in ["1d", "3d", "14d"]:
        out[f"z24 quintiles -> {hk}"] = graded("z24", hk)
    out["z7d quintiles -> 7d"] = graded("z7d", "7d")
    out["z7d quintiles -> 14d"] = graded("z7d", "14d")
    out["rngm quintiles -> 3d"] = graded("rngm", "3d")
    out["rngm quintiles -> 14d"] = graded("rngm", "14d")
    out["vol quintiles -> 14d"] = graded("vol", "14d")
    out["z24 in falls only -> 14d"] = graded("z24", "14d", cond=lambda g: g["r24"] < 0)
    out["z24 in rises only -> 3d"] = graded("z24", "3d", cond=lambda g: g["r24"] > 0)
    # hour / weekday of next 4h bar return, normalised
    A["r1z"] = A["r1n"] / A["vol"]
    out["by hour"] = A.groupby("hour")["r1z"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["by weekday"] = A.groupby("wd")["r1z"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book: gain split by in-position
    A["gain"] = A["alloc"] * A["r1n"]
    out["position share / gain by in-pos"] = A.assign(inpos=A["alloc"].abs() > 1e-6).groupby("inpos").agg(
        share=("pos", "count"), gain=("gain", "mean"), coin=("r1n", "mean"))
    # book days: largest losses
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in days.items() for w, d in ws.items()])
    D = D.dropna(subset=["book_return"])
    out["book day ret quantiles"] = D["book_return"].quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["book by window (mean, sum)"] = D.groupby("w")["book_return"].agg(["mean", "sum"]).T
    return out
