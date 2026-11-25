def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r0 = c / c.shift(1) - 1
            vol30 = r0.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": ts, "year": ts.dt.year,
                "nextwd": (ts + pd.Timedelta(days=1)).dt.weekday,
                "r1": c.shift(-1) / c - 1, "r0": r0,
                "r3": c / c.shift(3) - 1,
                "r60": (c / c.shift(60) - 1) * 100,
                "vol30": vol30,
                "volpct": vol30.rolling(365, min_periods=120).apply(lambda s: (s <= s[-1]).mean(), raw=True),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["r1"].notna()].copy()
    D["ex"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    D["trend"] = np.where(D["r60"] > 10, "rising", np.where(D["r60"] < -10, "falling", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = "na"
    D["agit"] = np.where(D["volpct"] > 0.5, "agitated", "calm")
    D.loc[D["volpct"].isna(), "agit"] = "na"
    D["z0"] = D["r0"] / D["vol30"]
    D["z3"] = D["r3"] / (D["vol30"] * np.sqrt(3))

    def ct(g, col="ex", sign=None):
        x = g[col] if sign is None else g[col] * g[sign]
        x = x.dropna()
        s = x.groupby(g.loc[x.index, "ts"]).sum()
        n = len(s)
        return pd.Series({"cases": len(x), "days": n, "mean_%": x.mean() * 100,
                          "t_day": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    # reversal: signed by -z0 (bet against yesterday's move), by trend
    E = D[D.z0.notna() & (D.trend != "na")].copy()
    E["rev"] = -np.sign(E["r0"])
    E["exrev"] = E["ex"] * E["rev"]
    E["az"] = pd.qcut(E["z0"].abs(), 4, labels=False)
    out["reversal_by_trend_absz"] = E.groupby(["trend", "az"]).apply(lambda g: ct(g, "exrev")).round(3)
    E["az3"] = pd.qcut(E["z3"].abs(), 4, labels=False)
    E["rev3"] = -np.sign(E["r3"]) * E["ex"]
    out["rev3day_by_trend_absz"] = E.groupby(["trend", "az3"]).apply(lambda g: ct(g, "rev3")).round(3)
    F = E[E.trend == "falling"]
    out["falling_rev_by_agit_absz"] = F[F.agit != "na"].groupby(["agit", "az"]).apply(lambda g: ct(g, "exrev")).round(3)
    out["falling_rev_by_year"] = F[F.az >= 2].groupby("year").apply(lambda g: ct(g, "exrev")).round(3)
    out["falling_rev_by_coin"] = F[F.az >= 2].groupby("coin").apply(lambda g: ct(g, "exrev")).round(3)
    out["falling_rev_by_sign"] = F[F.az >= 2].groupby(np.sign(F.loc[F.az >= 2, "r0"])).apply(lambda g: ct(g, "exrev")).round(3)
    # weekday in falling, day-clustered
    out["falling_weekday"] = D[D.trend == "falling"].groupby("nextwd").apply(ct).round(3)
    out["rising_weekday"] = D[D.trend == "rising"].groupby("nextwd").apply(ct).round(3)
    # book: share of gain by weekday held
    return out
