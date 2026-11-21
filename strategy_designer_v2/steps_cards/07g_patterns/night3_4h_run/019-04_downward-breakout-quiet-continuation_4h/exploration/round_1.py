def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < H + 2: continue
            fwd = c.shift(-H) / c - 1
            minlo = lo.shift(1).rolling(12).min(); maxhi = hi.shift(1).rolling(12).max()
            mbr = ((hi - lo) / c).rolling(180, min_periods=60).mean()
            width = ((maxhi - minlo) / c.shift(1)) / mbr
            r1 = np.log(c).diff()
            f = pd.DataFrame({
                "fwd": fwd,
                "brk_low": c / minlo - 1,
                "brk_high": c / maxhi - 1,
                "width": width,
                "ret1d": c / c.shift(6) - 1,
                "ret3d": c / c.shift(18) - 1,
                "ret7d": c / c.shift(42) - 1,
                "ret30d": c / c.shift(180) - 1,
                "volratio": r1.rolling(42).std() / r1.rolling(180, min_periods=60).std(),
                "vol7d": r1.rolling(42).std(),
                "barret": c / c.shift(1) - 1,
                "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            f = f.iloc[::H]
            f = f[f["fwd"].notna()]
            f["coin"] = coin; f["win"] = w
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df.groupby("coin")["fwd"]
    df["ex"] = df["fwd"] - g.transform("mean")
    df["z"] = df["ex"] / g.transform("std")
    out = {}
    out["n_cases_by_coin"] = df.groupby("coin")["fwd"].agg(["count", "mean", "std"])

    def q(col, k=5):
        d = df[df[col].notna()].copy()
        d["bin"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), k, labels=False))
        t = d.groupby("bin").agg(n=("ex", "size"), ex_mean=("ex", "mean"), strength=("z", "mean"),
                                 feat_med=(col, "median"))
        t["t"] = d.groupby("bin")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        sp = d.groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["z"])[0])
        t.loc["coin_rho_pos_share", "n"] = (sp > 0).mean()
        t.loc["coin_rho_mean", "n"] = sp.mean()
        return t
    for col in ["brk_low", "brk_high", "width", "ret1d", "ret3d", "ret7d", "ret30d", "volratio", "vol7d", "barret"]:
        out["q_" + col] = q(col)
    for col in ["hour", "wd"]:
        t = df.groupby(col).agg(n=("ex", "size"), ex_mean=("ex", "mean"), strength=("z", "mean"))
        t["t"] = df.groupby(col)["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        out["by_" + col] = t
    # breakdown below low: conditional on width tercile
    d = df[df["brk_low"] < 0].copy()
    d["wbin"] = pd.qcut(d["width"].rank(method="first"), 3, labels=False)
    t = d.groupby("wbin").agg(n=("ex", "size"), ex_mean=("ex", "mean"), strength=("z", "mean"))
    t["t"] = d.groupby("wbin")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["breakdown_by_width"] = t
    d = df[df["brk_high"] > 0].copy()
    d["wbin"] = pd.qcut(d["width"].rank(method="first"), 3, labels=False)
    t = d.groupby("wbin").agg(n=("ex", "size"), ex_mean=("ex", "mean"), strength=("z", "mean"))
    t["t"] = d.groupby("wbin")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["breakup_by_width"] = t
    # abs forward move vs width (does narrow -> larger moves?)
    d = df[df["width"].notna()].copy()
    d["wbin"] = d.groupby("coin")["width"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    d["absz"] = d["fwd"].abs() / d.groupby("coin")["fwd"].transform("std")
    out["absmove_by_width"] = d.groupby("wbin")["absz"].agg(["count", "mean"])
    return out
