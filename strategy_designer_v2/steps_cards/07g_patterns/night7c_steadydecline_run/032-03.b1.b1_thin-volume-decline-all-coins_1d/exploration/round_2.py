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
            rng = (hi - lo) / c
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(df["timestamp"]),
                "fwd": c.shift(-H) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "r28": c / c.shift(28) - 1,
                "vr": np.log(v.rolling(28).mean() / v.rolling(60).mean().shift(28)),
                "rngratio": np.log(rng.rolling(28).mean() / rng.rolling(60).mean().shift(28)),
                "rngratio14": np.log(rng.rolling(14).mean() / rng.rolling(42).mean().shift(14)),
                "vr14": np.log(v.rolling(14).mean() / v.rolling(42).mean().shift(14)),
            })
            f = f.iloc[::H]
            rows.append(f)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    drift = A.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    d10 = A.groupby("coin")["fwd10"].mean()
    A["ex10"] = A["fwd10"] - A["coin"].map(d10)
    A["day"] = A["ts"].dt.floor("D")

    def tday(s, d):
        g = pd.DataFrame({"x": s - s.mean(), "d": d}).groupby("d")["x"].sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return s.mean() / se if se > 0 else np.nan

    def bucket(col, sub, y="ex", q=5):
        s = sub.dropna(subset=[col, y]).copy()
        s["b"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        out = s.groupby("b").apply(lambda g: pd.Series({
            "mid": g[col].median(), "n": len(g), "mean": g[y].mean(), "median": g[y].median(),
            "share_pos": (g[y] > 0).mean(), "t_day": tday(g[y], g["day"])}))
        sp = stats.spearmanr(s[col], s[y])
        out.loc["rho"] = [np.nan, len(s), sp.correlation, sp.pvalue, np.nan, np.nan]
        return out

    res = {}
    res["rngratio14_all"] = bucket("rngratio14", A)
    res["rngratio14_ex10"] = bucket("rngratio14", A, "ex10")
    res["vr14_all"] = bucket("vr14", A)
    res["rngratio14_up"] = bucket("rngratio14", A[A["r28"] >= 0])
    res["rngratio14_dec"] = bucket("rngratio14", A[A["r28"] < 0])
    # per coin rho for rngratio14
    pc = []
    for coin, g in A.dropna(subset=["rngratio14"]).groupby("coin"):
        if len(g) > 30:
            sp = stats.spearmanr(g["rngratio14"], g["ex"])
            pc.append([coin, len(g), sp.correlation])
    res["rng14_per_coin"] = pd.DataFrame(pc, columns=["coin", "n", "rho"]).set_index("coin")
    pw = []
    for w, g in A.dropna(subset=["rngratio14"]).groupby("win"):
        if len(g) > 20:
            sp = stats.spearmanr(g["rngratio14"], g["ex"])
            pw.append([w, len(g), sp.correlation])
    res["rng14_per_window"] = pd.DataFrame(pw, columns=["win", "n", "rho"]).set_index("win")
    # 28-day version per window to check concentration
    pw2 = []
    for w, g in A.dropna(subset=["rngratio"]).groupby("win"):
        sp = stats.spearmanr(g["rngratio"], g["ex"]) if len(g) > 10 else None
        pw2.append([w, len(g), sp.correlation if sp else np.nan])
    res["rng28_per_window"] = pd.DataFrame(pw2, columns=["win", "n", "rho"]).set_index("win")
    # book: daily returns by forecast sign
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d[["book_return", "coin_return"]].assign(coin=coin, win=w))
    B = pd.concat(bk).dropna()
    res["book_by_window"] = B.groupby("win")[["book_return", "coin_return"]].mean()
    return res
