def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "year": ts.dt.year,
                "nextwd": (ts + pd.Timedelta(days=1)).dt.weekday,
                "r1": c.shift(-1) / c - 1,
                "r0": c / c.shift(1) - 1,
                "r3p": c / c.shift(3) - 1,
                "r60": (c / c.shift(60) - 1) * 100,
                "vol30": (c / c.shift(1) - 1).rolling(30).std(),
                "rng": (b["high"] - b["low"]) / c,
                "vz": np.log(b["volume"].astype(float) + 1) - np.log(b["volume"].astype(float) + 1).rolling(30).mean(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["r1"].notna()]
    D["ex"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    D["trend"] = np.where(D["r60"] > 10, "rising", np.where(D["r60"] < -10, "falling", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = "na"

    def summ(g):
        x = g["ex"].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_ex_%": x.mean() * 100,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    out["weekday_x_trend"] = D.groupby(["trend", "nextwd"]).apply(summ).round(3)
    R = D[D["trend"] == "rising"].copy()
    R["fs"] = R["nextwd"].isin([4, 5])
    R["q60"] = pd.qcut(R["r60"], 4, labels=False)
    out["rising_r60q_x_FriSat"] = R.groupby(["fs", "q60"]).apply(summ).round(3)
    D["q0"] = D.groupby("coin")["r0"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["prevday_q_x_trend"] = D[D.trend != "na"].groupby(["trend", "q0"]).apply(summ).round(3)
    D["qv"] = D.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["vol30_q"] = D.groupby("qv").apply(summ).round(3)
    D["qvz"] = D.groupby("coin")["vz"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["volume_shock_q"] = D.groupby("qvz").apply(summ).round(3)
    out["FriSat_rising_by_year"] = R[R.fs].groupby("year").apply(summ).round(3)
    out["FriSat_rising_by_coin"] = R[R.fs].groupby("coin").apply(summ).round(3)
    return out
