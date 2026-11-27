def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret1"] = c.pct_change()
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rng = (b["high"] - b["low"]) / c
            d["width"] = rng / rng.rolling(20, min_periods=20).mean()
            d["volr"] = b["volume"] / b["volume"].shift(1).rolling(20, min_periods=20).mean()
            d["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["vol30"] = d["ret1"].rolling(30, min_periods=20).std()
            d["regime"] = b["regime"]
            d["falling"] = b["regime"].isin(["mean_reversion", "unknown"])
            d["alloc"] = b["postRebalance_current_allocation"]
            d["pos"] = np.arange(len(d))
            rows.append(d)
    X = pd.concat(rows, ignore_index=True)
    X["day"] = X["ts"].dt.floor("D")
    X["wd"] = X["ts"].dt.dayofweek
    X["year"] = X["ts"].dt.year
    mu = X.groupby("coin")["f1"].mean()
    for h in (1, 2, 3, 5):
        X[f"u{h}"] = X[f"f{h}"] - X["coin"].map(mu) * h

    def stat(df, col, sign=1.0):
        df = df.dropna(subset=[col])
        if len(df) < 5:
            return pd.Series({"n": len(df), "mean%": np.nan, "t": np.nan, "days": 0})
        v = sign * df[col]
        n = len(v)
        m = v.mean()
        ds = (v - m).groupby(df["day"]).sum()
        se = np.sqrt((ds ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se if se > 0 else np.nan, "days": ds.size})

    out = {}
    F = X[X["falling"]]
    NF = X[~X["falling"]]
    # 1. falling up days by width quintile
    up = F[F["ret1"] > 0].dropna(subset=["width"]).copy()
    up["q"] = pd.qcut(up["width"], 5, labels=False)
    out["fall_up_by_width_q_u1"] = up.groupby("q").apply(lambda g: stat(g, "u1"))
    upn = NF[NF["ret1"] > 0].dropna(subset=["width"]).copy()
    upn["q"] = pd.qcut(upn["width"], 5, labels=False)
    out["notfall_up_by_width_q_u1"] = upn.groupby("q").apply(lambda g: stat(g, "u1"))
    # 2. falling: all days by ret1 quintile
    a = F.dropna(subset=["ret1"]).copy()
    a["q"] = pd.qcut(a["ret1"], 10, labels=False)
    out["fall_by_ret1_decile_u1"] = a.groupby("q").apply(lambda g: stat(g, "u1"))
    b2 = NF.dropna(subset=["ret1"]).copy()
    b2["q"] = pd.qcut(b2["ret1"], 10, labels=False)
    out["notfall_by_ret1_decile_u1"] = b2.groupby("q").apply(lambda g: stat(g, "u1"))
    # 3. situation days: horizons
    s = X[X["regime"] == "mean_reversion"]
    out["situation_horizons"] = pd.DataFrame({h: stat(s, f"u{h}") for h in (1, 2, 3, 5)}).T
    # 4. falling: close position in range, all days
    c2 = F.dropna(subset=["clpos"]).copy()
    c2["q"] = pd.qcut(c2["clpos"], 5, labels=False)
    out["fall_by_closepos_q_u1"] = c2.groupby("q").apply(lambda g: stat(g, "u1"))
    # 5. falling: volume ratio quintiles, all days
    v2 = F.dropna(subset=["volr"]).copy()
    v2["q"] = pd.qcut(v2["volr"], 5, labels=False)
    out["fall_by_volr_q_u1_alldays"] = v2.groupby("q").apply(lambda g: stat(g, "u1"))
    # 6. weekday of the next day, falling vs not
    X["wd_next"] = (X["wd"] + 1) % 7
    out["fall_by_nextweekday_u1"] = X[X["falling"]].groupby("wd_next").apply(lambda g: stat(g, "u1"))
    out["notfall_by_nextweekday_u1"] = X[~X["falling"]].groupby("wd_next").apply(lambda g: stat(g, "u1"))
    # 7. situation by year
    out["situation_by_year_short"] = s.groupby("year").apply(lambda g: stat(g, "u1", -1))
    out["regime_counts"] = X["regime"].value_counts()
    return out
