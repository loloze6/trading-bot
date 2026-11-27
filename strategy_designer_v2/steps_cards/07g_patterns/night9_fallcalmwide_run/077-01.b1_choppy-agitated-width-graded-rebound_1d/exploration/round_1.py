def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            rng = (h - l)
            width = rng / rng.rolling(30, min_periods=30).mean()
            loc = (c - l) / rng.replace(0, np.nan)
            sd30 = r.rolling(30, min_periods=30).std()
            rstd = (rng / c) / sd30
            tr60 = c / c.shift(60) - 1
            vol_rel = sd30 / sd30.rolling(90, min_periods=60).median()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": nxt, "r": r, "width": width, "loc": loc, "rstd": rstd,
                "tr60": tr60, "volrel": vol_rel, "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"],
                "body": (c - o) / rng.replace(0, np.nan),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df = df.dropna(subset=["nxt"])
    drift = df.groupby("coin")["nxt"].mean()
    df["ex"] = df["nxt"] - df["coin"].map(drift)
    df["day"] = df["ts"].dt.floor("D")

    def ct(sub, col="ex", sign=1):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t": np.nan})
        v = sign * s[col]
        m = v.mean()
        dev = (v - m).groupby(s["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(v)
        return pd.Series({"n": len(v), "days": D, "mean%": 100 * m, "t": m / se})

    out = {}
    out["regime counts"] = df["regime"].value_counts()
    # all bars: width x loc
    s = df.dropna(subset=["width", "loc"]).copy()
    s["wq"] = pd.qcut(s["width"], 4, labels=["w1", "w2", "w3", "w4"])
    s["lq"] = pd.cut(s["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["l0-20", "l20-40", "l40-60", "l60-80", "l80-100"])
    out["all bars width q x loc"] = s.groupby(["wq", "lq"], observed=True).apply(ct).unstack(0) if False else s.groupby(["wq", "lq"], observed=True).apply(ct)
    # by trend bucket (60d within window)
    s2 = s.dropna(subset=["tr60"]).copy()
    s2["trend"] = np.where(s2["tr60"] > 0.1, "rising", np.where(s2["tr60"] < -0.1, "falling", "choppy"))
    s2["agit"] = np.where(s2["volrel"] > 1, "agit", "calm")
    wide = s2[s2["width"] >= 1.3]
    out["wide days, trend x agit x low/high close"] = wide.assign(side=np.where(wide["loc"] < 0.3, "lowclose", np.where(wide["loc"] > 0.7, "highclose", "mid"))).groupby(["trend", "agit", "side"]).apply(ct)
    # in-position (regime unknown) cases
    u = df[df["regime"] == "unknown"]
    out["unknown regime cases"] = ct(u)
    uu = u.dropna(subset=["loc", "rstd"]).copy()
    uu["lb"] = pd.cut(uu["loc"], [-0.01, 0.15, 0.3, 0.5], labels=["0-15", "15-30", "30-50"])
    out["cases by close loc"] = uu.groupby("lb", observed=True).apply(ct)
    uu["rq"] = pd.qcut(uu["rstd"], 3, labels=["lo", "mid", "hi"])
    out["cases by range/std tercile"] = uu.groupby("rq", observed=True).apply(ct)
    # after large moves: return z
    s3 = df.dropna(subset=["r"]).copy()
    sd = s3.groupby("coin")["r"].transform("std")
    s3["z"] = s3["r"] / sd
    s3["zb"] = pd.cut(s3["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["next day by today's z"] = s3.groupby("zb", observed=True).apply(ct)
    df["wd"] = df["ts"].dt.dayofweek
    out["next day by weekday of signal bar"] = df.groupby("wd").apply(ct)
    return out
