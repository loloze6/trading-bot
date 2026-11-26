def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            z = r / sd
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 2, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "year": yr, "z": z, "r": r,
                               "regime": b["regime"].astype(str), "fc": b["forecast"].astype(float),
                               "f1": b["f1"], "f2": b["f2"], "f3": b["f3"], "f5": b["f5"],
                               "pos": np.arange(len(b)), "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["r"].mean()
    for h in (1, 2, 3, 5):
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(drift) * h
    out = {}
    out["regime counts"] = d["regime"].value_counts()
    up = d[(d["z"] > 0)].dropna(subset=["x1"])
    inp = up[up["regime"] == "unknown"].copy()
    outp = up[up["regime"] != "unknown"].copy()
    def tstat(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    # quintiles of z in profile
    inp["q"] = pd.qcut(inp["z"], 5, labels=False)
    out["in profile by z quintile"] = inp.groupby("q").agg(n=("x1", "size"), zmean=("z", "mean"),
        x1=("x1", "mean"), t1=("x1", tstat), x2=("x2", "mean"), x3=("x3", "mean"), x5=("x5", "mean"))
    outp["q"] = pd.qcut(outp["z"], 5, labels=False)
    out["outside profile by z quintile"] = outp.groupby("q").agg(n=("x1", "size"), zmean=("z", "mean"),
        x1=("x1", "mean"), t1=("x1", tstat), x2=("x2", "mean"))
    # all days in profile, down days included, for baseline
    allin = d[(d["regime"] == "unknown")].dropna(subset=["x1"])
    out["in profile: up vs down days next x1"] = pd.DataFrame({
        "up": [allin[allin.z > 0].x1.mean(), (allin.z > 0).sum(), tstat(allin[allin.z > 0].x1)],
        "down": [allin[allin.z <= 0].x1.mean(), (allin.z <= 0).sum(), tstat(allin[allin.z <= 0].x1)]},
        index=["mean", "n", "t"])
    out["in profile up by coin"] = inp.groupby("coin").agg(n=("x1", "size"), x1=("x1", "mean"), t=("x1", tstat),
        corr=("x1", lambda s: np.corrcoef(s, inp.loc[s.index, "z"])[0, 1]))
    out["in profile up by year"] = inp.groupby("year").agg(n=("x1", "size"), x1=("x1", "mean"), t=("x1", tstat),
        x2=("x2", "mean"))
    out["in profile up by window"] = inp.groupby("win").agg(n=("x1", "size"), x1=("x1", "mean"), t=("x1", tstat))
    # nonoverlapping 2,3 day
    for h in (2, 3):
        s = inp[inp["pos"] % h == 0]
        out[f"in profile up x{h} nonoverlap"] = f"n={len(s)} mean={s[f'x{h}'].mean():.4f} t={tstat(s[f'x{h}']):.2f}"
    # slope of x1 on z in profile
    s = inp.dropna(subset=["x1", "z"])
    sl = np.polyfit(s.z, s.x1, 1)[0]
    out["in profile slope x1 on z, corr"] = f"slope={sl:.5f} corr={np.corrcoef(s.z, s.x1)[0,1]:.3f} n={len(s)}"
    return out
