def explore(data):
    import pandas as pd, numpy as np
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            hi20 = hi.shift(1).rolling(20).max(); lo20 = lo.shift(1).rolling(20).min()
            vol20 = r1.rolling(20).std()
            tr60 = (c / c.shift(60) - 1) * 100
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(n), "cell": np.arange(n) // H,
                               "day": ts.dt.floor("D"), "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1, "r1": r1,
                               "dhi": c / hi20 - 1, "dlo": c / lo20 - 1, "vol20": vol20, "tr60": tr60,
                               "pos": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["i"] % H == 0) & A["fwd"].notna()]
    drift = grid.groupby("coin")["fwd"].mean(); sd = grid.groupby("coin")["fwd"].std()
    A["un"] = A["fwd"] - A["coin"].map(drift)
    A["str"] = A["un"] / A["coin"].map(sd)
    def ct(x, col="un"):
        x = x.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x), "days": x["day"].nunique() if len(x) else 0, "mean": np.nan, "t_day": np.nan, "strength": np.nan})
        m = x[col].mean(); dev = (x[col] - m).groupby(x["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_day": m / se, "strength": x["str"].mean() if "str" in x else np.nan})
    out = {}
    # upside break cases: first bar in each cell with close above prior 20d high
    up = A[(A["dhi"] > 0) & A["fwd"].notna()].sort_values("i").groupby(["coin", "win", "cell"]).head(1).copy()
    out["up_break_all"] = ct(up)
    up["z"] = up["dhi"] / up["vol20"]
    up["zq"] = pd.qcut(up["z"], 4, labels=False, duplicates="drop")
    out["up_break_by_depth_q"] = up.groupby("zq").apply(ct)
    up["trend"] = np.where(up["tr60"] > 10, "rising", np.where(up["tr60"] < -10, "falling", np.where(up["tr60"].isna(), "na", "choppy")))
    out["up_break_by_trend"] = up.groupby("trend").apply(ct)
    out["up_break_by_window"] = up.groupby("win").apply(ct)
    out["up_break_by_coin"] = up.groupby("coin").apply(ct)
    out["up_break_slope_z"] = float(np.polyfit(up["z"], up["un"], 1)[0])
    dn = A[(A["dlo"] < 0) & A["fwd"].notna()].sort_values("i").groupby(["coin", "win", "cell"]).head(1).copy()
    out["down_break_all"] = ct(dn)
    dn["z"] = dn["dlo"] / dn["vol20"]
    dn["zq"] = pd.qcut(dn["z"], 4, labels=False, duplicates="drop")
    out["down_break_by_depth_q"] = dn.groupby("zq").apply(ct)
    dn["trend"] = np.where(dn["tr60"] > 10, "rising", np.where(dn["tr60"] < -10, "falling", np.where(dn["tr60"].isna(), "na", "choppy")))
    out["down_break_by_trend"] = dn.groupby("trend").apply(ct)
    out["down_break_by_window"] = dn.groupby("win").apply(ct)
    # weekday of the bar's own return, day-clustered
    d = A.dropna(subset=["r1"]).copy()
    d["ra"] = d["r1"] - d["coin"].map(d.groupby("coin")["r1"].mean())
    out["weekday_own_return"] = d.groupby("wd").apply(lambda x: ct(x, "ra"))
    out["weekday_by_year_fri_sat"] = d[d["wd"].isin([4, 5])].groupby("yr").apply(lambda x: ct(x, "ra"))
    out["weekday_others_by_year"] = d[~d["wd"].isin([4, 5])].groupby("yr").apply(lambda x: ct(x, "ra"))
    # 1-day move grid quintile, day-clustered
    g = A[(A["i"] % H == 0) & A["fwd"].notna()].copy()
    g["z1"] = g["r1"] / g["vol20"]
    g["z1q"] = g.groupby("coin")["z1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["grid_by_1d_move_z_q"] = g.groupby("z1q").apply(ct)
    return out
