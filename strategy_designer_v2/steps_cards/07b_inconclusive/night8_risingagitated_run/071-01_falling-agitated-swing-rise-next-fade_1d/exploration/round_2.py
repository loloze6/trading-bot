def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "z": r / sd,
                "ret60": c / c.shift(60) - 1, "ret5": c.shift(1) / c.shift(6) - 1,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "rng": (h - l) / c.shift(1) / sd,
                "regime": b["regime"].astype(str), "f1": c.shift(-1) / c - 1,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["r"].mean()
    d["x1"] = d["f1"] - d["coin"].map(drift)
    def tday(s, days):
        g = s.groupby(days).sum(); n = len(g)
        return s.mean() / (np.sqrt(((g - s.groupby(days).size() * s.mean()) ** 2).sum()) / len(s)) if n > 2 else np.nan
    inp = d[(d.regime == "unknown")].dropna(subset=["x1", "z"]).copy()
    up = inp[inp.z > 0].copy()
    out = {}
    def by(col, frame, k=5):
        f = frame.dropna(subset=[col]).copy()
        f["q"] = pd.qcut(f[col], k, labels=False, duplicates="drop")
        return f.groupby("q").apply(lambda g: pd.Series({"n": len(g), "mean_col": g[col].mean(),
            "x1": g.x1.mean(), "t_day": tday(g.x1, g.day)}))
    out["up: by raw return r"] = by("r", up)
    out["up: by 60d return"] = by("ret60", up)
    out["up: by prior 5d return"] = by("ret5", up)
    out["up: by close location"] = by("clv", up)
    out["up: by range/swing"] = by("rng", up)
    out["all in-profile days: by z decile"] = by("z", inp, 10)
    s = inp
    out["all in-profile: slope x1 on z"] = f"slope={np.polyfit(s.z, s.x1, 1)[0]:.5f} corr={np.corrcoef(s.z, s.x1)[0,1]:.3f} n={len(s)}"
    dn = inp[inp.z < 0]
    out["down: slope x1 on |z|"] = f"slope={np.polyfit(-dn.z, dn.x1, 1)[0]:.5f} corr={np.corrcoef(-dn.z, dn.x1)[0,1]:.3f} n={len(dn)}"
    out["up mean x1, day t"] = f"mean={up.x1.mean():.4f} t={tday(up.x1, up.day):.2f} days={up.day.nunique()}"
    return out
