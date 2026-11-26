def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            hh = b["high"].rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c / hh - 1) / sd
            ll = b["low"].rolling(20, min_periods=20).min()
            pos = (c - ll) / (hh - ll)
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"])
            r5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "nxt": nxt, "depth": depth, "pos": pos, "tr60": tr60,
                               "rz": r / sd, "rng_z": rng / sd, "clv": clv, "r5z": r5 / (sd * np.sqrt(5)),
                               "regime": b["regime"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].mean()
    D["e"] = D["nxt"] - D["coin"].map(mu)
    D = D.dropna(subset=["e"])
    D["wd"] = D["ts"].dt.dayofweek
    D["yr"] = D["ts"].dt.year
    def summ(g):
        x = g["e"].dropna()
        return pd.Series({"n": len(x), "mean_e%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    up = D[D["r"] > 0].dropna(subset=["depth"])
    dn = D[D["r"] <= 0].dropna(subset=["depth"])
    up["dq"] = pd.qcut(up["depth"], 5, labels=False)
    dn["dq"] = pd.qcut(dn["depth"], 5, labels=False)
    out["up days by depth quintile (0 deepest)"] = up.groupby("dq").apply(summ)
    out["down days by depth quintile"] = dn.groupby("dq").apply(summ)
    D["trend"] = np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"].notna(), "choppy", "na")))
    D["side"] = np.where(D["r"] > 0, "up", "down")
    out["by trend x up/down"] = D.groupby(["trend", "side"]).apply(summ)
    out["in book (mean_reversion regime)"] = D[D["regime"] == "mean_reversion"].groupby(pd.qcut(D.loc[D["regime"] == "mean_reversion", "depth"], 4, labels=False)).apply(summ)
    D2 = D.dropna(subset=["rz"])
    D2["rzq"] = pd.qcut(D2["rz"], 10, labels=False)
    out["all days by today's z-return decile"] = D2.groupby("rzq").apply(summ)
    out["by weekday"] = D.groupby("wd").apply(summ)
    D3 = D.dropna(subset=["clv"])
    D3["cq"] = pd.qcut(D3["clv"], 5, labels=False)
    out["by close location in day (0 low) x side"] = D3.groupby(["side", "cq"]).apply(summ)
    D4 = D.dropna(subset=["r5z"])
    D4["q5"] = pd.qcut(D4["r5z"], 5, labels=False)
    out["by 5-day z-return quintile x trend"] = D4[D4.trend != "na"].groupby(["trend", "q5"]).apply(summ)
    out["by coin"] = D.groupby("coin").apply(summ)
    return out
