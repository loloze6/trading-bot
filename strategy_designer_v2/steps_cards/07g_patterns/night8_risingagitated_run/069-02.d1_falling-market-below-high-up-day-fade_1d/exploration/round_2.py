def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            hh = b["high"].rolling(20, min_periods=20).max()
            ll = b["low"].rolling(20, min_periods=20).min()
            sd = r.rolling(20, min_periods=20).std()
            sd30 = r.rolling(30, min_periods=30).std()
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "nxt": nxt, "sd": sd, "sd30": sd30, "r60": r60,
                "depth": (c - hh) / hh / sd, "pos": (c - ll) / (hh - ll),
                "regime": b["regime"], "day": ts.dt.floor("D"),
                "clpos": (c - b["low"]) / (b["high"] - b["low"]),
                "rng": (b["high"] - b["low"]) / c,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(mu)
    d = d.dropna(subset=["ex", "sd", "sd30"])
    d["falling"] = d["regime"] != "chop"
    d["trend"] = np.where(d["falling"], "falling",
                  np.where(d["r60"] > 0.10, "rising", np.where(d["r60"].notna(), "choppy", "na")))
    med = d.groupby("coin")["sd30"].median()
    d["agit"] = np.where(d["sd30"] > d["coin"].map(med), "agitated", "calm")
    d["z"] = d["r"] / d["sd"]
    d["rngz"] = d["rng"] / d["sd"]

    def stat(g, sign=1.0):
        x = sign * g["ex"]
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "t_day": np.nan, "days": np.nan})
        dv = (x - 0).groupby(g["day"]).sum()
        tday = dv.sum() / np.sqrt((dv ** 2).sum()) if (dv ** 2).sum() > 0 else np.nan
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)),
                          "t_day": tday, "days": g["day"].nunique()})

    out = {}
    out["profile_x_up"] = d.groupby(["trend", "agit", d["r"] > 0]).apply(stat)
    up = d[d["r"] > 0].copy()
    up["zq"] = up.groupby(["trend", "agit"])["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["up_dayz_tercile_by_profile"] = up.groupby(["trend", "agit", "zq"]).apply(stat)
    up["cq"] = up.groupby(["trend", "agit"])["clpos"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["up_closepos_tercile_by_profile"] = up.groupby(["trend", "agit", "cq"]).apply(stat)
    # spearman of z vs ex, all days, per profile (reversal grading)
    def sp(g, col):
        from scipy.stats import spearmanr
        g = g.dropna(subset=[col])
        rho, p = spearmanr(g[col], g["ex"])
        return pd.Series({"n": len(g), "rho": rho, "p": p})
    out["spearman_dayz_vs_next_by_profile"] = d.groupby(["trend", "agit"]).apply(lambda g: sp(g, "z"))
    out["spearman_pos20_vs_next_up_by_profile"] = up.groupby(["trend", "agit"]).apply(lambda g: sp(g, "pos"))
    # by year for falling up days with high z
    fu = up[(up.trend == "falling")]
    out["falling_up_topz_by_year"] = fu[fu.zq == 2].groupby(fu["day"].dt.year).apply(stat)
    out["falling_up_topz_by_coin"] = fu[fu.zq == 2].groupby("coin").apply(stat)
    return out
