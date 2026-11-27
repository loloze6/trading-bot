def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / sd,
                "rng": (b["high"] - b["low"]) / c / sd,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1,
                "fc": (b["regime"] == "unknown"),
                "alloc": b["postRebalance_current_allocation"],
                "gain": b["postRebalance_current_allocation"] * (c.shift(-1) / c - 1),
            })
            df["r5z"] = df["r5"] / (sd * np.sqrt(5))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    drift = A.groupby("coin")["f1"].mean()
    A["u1"] = A["f1"] - A["coin"].map(drift)

    def tstat(s, d):
        x = pd.DataFrame({"v": s, "d": d}).dropna()
        if len(x) < 10: return (len(x), np.nan, np.nan)
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return (len(x), m, m / se)

    def table(mask, col, bins, val="u1"):
        out = []
        sub = A[mask & A[col].notna()]
        cut = pd.cut(sub[col], bins)
        for k, g in sub.groupby(cut, observed=True):
            n, m, t = tstat(g[val], g["day"])
            out.append({"bin": str(k), "n": n, "mean": m, "t": t, "days": g["day"].nunique()})
        return pd.DataFrame(out)

    zb = [-20, -2, -1, -0.3, 0.3, 1, 2, 20]
    res = {}
    res["z_next_fallcalm"] = table(A["fc"], "z", zb)
    res["z_next_other"] = table(~A["fc"], "z", zb)
    A["u2"] = A["f2"] - 2 * A["coin"].map(drift)
    res["z_next2_fallcalm"] = table(A["fc"], "z", zb, "u2")
    res["z_next2_other"] = table(~A["fc"], "z", zb, "u2")
    res["r5z_next_all"] = table(A["r5z"].notna(), "r5z", [-20, -1.5, -0.5, 0.5, 1.5, 20])
    res["clpos_next_all"] = table(A["clpos"].notna(), "clpos", [0, 0.2, 0.4, 0.6, 0.8, 1.0001])
    res["rng_next_all"] = table(A["rng"].notna(), "rng", [0, 1, 1.5, 2, 3, 50])
    wd = []
    A["wd"] = A["ts"].dt.weekday
    for k, g in A.groupby("wd"):
        n, m, t = tstat(g["u1"], g["day"]); wd.append({"wd": k, "n": n, "mean": m, "t": t})
    res["weekday_next"] = pd.DataFrame(wd)
    res["share_fallcalm"] = float(A["fc"].mean())
    # book gains by window, by coin
    held = A[A["alloc"].abs() > 0]
    res["book_gain_by_win"] = held.groupby("win")["gain"].agg(["count", "mean", "sum"])
    res["book_gain_by_coin"] = held.groupby("coin")["gain"].agg(["count", "mean", "sum"])
    return res
