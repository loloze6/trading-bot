def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].shift(-1) / b["close"] - 1)
        drift = pd.concat(allr).mean()
        allr2 = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r2 = b["close"].shift(-2) / b["close"] - 1
            allr2.append(r2.iloc[::2])
        drift2 = pd.concat(allr2).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["ex"] = b["nxt"] - drift
            b["ex2"] = b["close"].shift(-2) / b["close"] - 1 - drift2
            rng = b["high"] - b["low"]
            b["clv"] = np.where(rng > 0, 2 * (b["close"] - b["low"]) / rng - 1, np.nan)
            b["wide"] = rng / rng.rolling(20, min_periods=20).mean()
            b["ret1"] = b["close"].pct_change()
            b["vol20"] = b["ret1"].rolling(20, min_periods=15).std()
            b["z1"] = b["ret1"] / b["vol20"].shift(1)
            b["inprof"] = b["regime"] != "chop"
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["ex", "z1", "clv"])

    def stat(g, col="ex"):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t_day": np.nan, "days": np.nan})
        m = g[col].mean(); s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum() * len(s) / max(len(s) - 1, 1)) / n
        return pd.Series({"n": n, "mean": m, "t_day": m / se if se > 0 else np.nan, "days": len(s)})

    out = {}
    ip = d[d["inprof"]].copy()
    up = ip[ip["z1"] > 0].copy()
    up["z1q"] = pd.qcut(up["z1"], 4, labels=False)
    out["inprof_up_by_z1q"] = up.groupby("z1q").apply(stat).round(4)
    out["inprof_up_by_z1q_meanz"] = up.groupby("z1q")["z1"].mean().round(2)
    up["clvh"] = np.where(up["clv"] > 0.2, "highclose", "lowmidclose")
    out["inprof_up_by_clv"] = up.groupby("clvh").apply(stat).round(4)
    out["inprof_up_by_year"] = up.groupby("yr").apply(stat).round(4)
    out["inprof_up_by_coin"] = up.groupby("coin").apply(stat).round(4)
    # 2 day horizon on grid
    up2 = up[up["pos"] % 2 == 0]
    out["inprof_up_2day_grid"] = up2.groupby("z1q").apply(lambda g: stat(g, "ex2")).round(4)
    # joint regression in profile
    X = np.column_stack([np.ones(len(ip)), ip["z1"].clip(-4, 4), ip["clv"]])
    y = ip["ex"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    XtX = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(XtX) * res.var(ddof=3))
    out["inprof_ols_ex_on_z1_clv"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z1", "clv"]).round(5)
    # other profiles for up days (excluding in profile)
    op = d[~d["inprof"]].copy()
    op["z1q"] = pd.qcut(op["z1"], 5, labels=False)
    out["outprof_z1q_count_check"] = op.groupby("z1q").apply(stat).round(4)
    # spearman in up days
    from scipy.stats import spearmanr
    rho, p = spearmanr(up["z1"], up["ex"])
    out["inprof_up_spearman_z1_ex"] = f"rho={rho:.3f} p={p:.4f} n={len(up)}"
    return out
