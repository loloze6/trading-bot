def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            hi = df["high"].astype(float); lo = df["low"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(df["timestamp"]),
                "fwd": c.shift(-H) / c - 1,
                "r28": c / c.shift(28) - 1,
                "r5": c / c.shift(5) - 1,
                "r1": r1,
                "vol20": r1.rolling(20).std(),
                "vol60": r1.rolling(60).std(),
                "rng28": ((hi - lo) / c).rolling(28).mean(),
                "rng90p": ((hi - lo) / c).rolling(60).mean().shift(28),
                "vr": np.log(v.rolling(28).mean() / v.rolling(60).mean().shift(28)),
                "maxdd28": (c / c.rolling(28).max() - 1),
                "worst1_28": r1.rolling(28).min(),
                "pos": df["postRebalance_current_allocation"].astype(float),
                "fc": df["forecast"].astype(float),
            })
            f["volratio"] = f["vol20"] / f["vol60"]
            f["rngratio"] = np.log(f["rng28"] / f["rng90p"])
            f["calm"] = f["worst1_28"] / f["vol60"]
            f = f.iloc[::H]
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["fwd"])
    drift = A.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A["day"] = A["ts"].dt.floor("D")

    def tday(s, d):
        g = pd.DataFrame({"x": s - s.mean(), "d": d}).groupby("d")["x"].sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return s.mean() / se if se > 0 else np.nan

    def bucket(col, sub, q=5):
        s = sub.dropna(subset=[col, "ex"]).copy()
        s["b"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        out = s.groupby("b").apply(lambda g: pd.Series({
            "mid": g[col].median(), "n": len(g), "mean_ex": g["ex"].mean(),
            "t_day": tday(g["ex"], g["day"])}))
        sp = stats.spearmanr(s[col], s["ex"])
        out.loc["rho"] = [np.nan, len(s), sp.correlation, sp.pvalue]
        return out

    res = {}
    res["all_r28"] = bucket("r28", A)
    res["all_r5"] = bucket("r5", A)
    res["all_r1"] = bucket("r1", A)
    res["all_volratio"] = bucket("volratio", A)
    res["all_vr"] = bucket("vr", A)
    res["all_rngratio"] = bucket("rngratio", A)
    D = A[A["r28"] < 0]
    res["dec_r28"] = bucket("r28", D)
    res["dec_vr"] = bucket("vr", D)
    res["dec_calm"] = bucket("calm", D)
    res["dec_maxdd28"] = bucket("maxdd28", D)
    res["dec_rngratio"] = bucket("rngratio", D)
    U = A[A["r28"] >= 0]
    res["up_vr"] = bucket("vr", U)
    A["wd"] = A["ts"].dt.dayofweek
    res["weekday"] = A.groupby("wd")["ex"].agg(["count", "mean"])
    res["year_dec_vs_up"] = A.assign(y=A["ts"].dt.year, dec=A["r28"] < 0).groupby(["y", "dec"])["ex"].agg(["count", "mean"])
    return res
