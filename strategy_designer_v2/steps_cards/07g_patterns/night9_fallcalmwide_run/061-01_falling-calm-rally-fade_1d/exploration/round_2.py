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
                "z": r / sd,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c / sd,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "fc": (b["regime"] == "unknown"),
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["year"] = A["ts"].dt.year
    drift = A.groupby("coin")["f1"].mean()
    A["u1"] = A["f1"] - A["coin"].map(drift)
    A["u3"] = A["f3"] - 3 * A["coin"].map(drift)
    A["trend"] = np.where(A["tr60"] > 0.1, "rising", np.where(A["tr60"] < -0.1, "falling", np.where(A["tr60"].notna(), "choppy", "na")))
    A.loc[A["fc"], "trend"] = "fallcalm"

    def tstat(s, d):
        x = pd.DataFrame({"v": s, "d": d}).dropna()
        if len(x) < 10: return (len(x), np.nan, np.nan)
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return (len(x), m, m / se)

    def grp(sub, keys, val):
        out = []
        for k, g in sub.groupby(keys, observed=True):
            n, m, t = tstat(g[val], g["day"])
            out.append({"key": str(k), "n": n, "mean": m, "t": t, "days": g["day"].nunique()})
        return pd.DataFrame(out)

    res = {}
    big = A[A["z"] <= -2]
    res["bigdown_by_trend_u1"] = grp(big, "trend", "u1")
    res["bigdown_by_trend_u3"] = grp(big, "trend", "u3")
    res["bigdown_by_year_u1"] = grp(big[~big["fc"]], "year", "u1")
    res["bigdown_by_coin_u1"] = grp(big[~big["fc"]], "coin", "u1")
    A["cpb"] = pd.cut(A["clpos"], [0, 0.2, 0.8, 1.0001])
    res["clpos_by_trend"] = grp(A[A["clpos"].notna()], ["trend", "cpb"], "u1")
    # graded: down z and low close in non-fallcalm
    nf = A[~A["fc"] & A["z"].notna()]
    res["corr_z_u1_nonfc"] = float(nf[["z", "u1"]].corr().iloc[0, 1])
    res["corr_z_u1_fc"] = float(A[A["fc"]][["z", "u1"]].corr().iloc[0, 1])
    down = nf[nf["z"] < 0].copy()
    down["zb"] = pd.qcut(down["z"], 5)
    res["nonfc_down_quintile_u1"] = grp(down, "zb", "u1")
    res["bigdown_by_year_fc_excl_wide"] = grp(big[~big["fc"] & (big["rng"] > 3)], "year", "u1")
    return res
