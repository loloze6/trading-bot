def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l) / c
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "fwd1": c.shift(-1) / c - 1,
                "ret1": c / c.shift(1) - 1,
                "ret7": c / c.shift(7) - 1,
                "ret30": c / c.shift(30) - 1,
                "loc": (c - l) / (h - l).replace(0, np.nan),
                "rr": rng.rolling(30).mean() / rng.rolling(90).mean(),
                "rng_z": (rng - rng.rolling(30).mean()) / rng.rolling(30).std(),
                "newlow30": (l <= l.rolling(30).min()).astype(float),
                "dist_low30": c / l.rolling(30).min() - 1,
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "regime": b["regime"],
            })
            d["gain"] = d["alloc"] * d["fwd1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["fwd1"].mean()
    D["ab"] = D["fwd1"] - D["coin"].map(drift)
    D["wd"] = D["ts"].dt.dayofweek
    D["yr"] = D["ts"].dt.year
    D = D.dropna(subset=["ab"])
    def summ(g):
        x = g["ab"]
        return pd.Series({"n": len(x), "mean_ab%": 100*x.mean(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    D["inreg"] = D["regime"] == "mean_reversion"
    D["locq"] = pd.qcut(D["loc"], 5, labels=False, duplicates="drop")
    out["loc_quint_by_regime"] = D.groupby(["inreg", "locq"]).apply(summ)
    D["r1q"] = pd.qcut(D["ret1"], 5, labels=False)
    out["ret1_quint_by_regime"] = D.groupby(["inreg", "r1q"]).apply(summ)
    D["r7q"] = pd.qcut(D["ret7"], 5, labels=False)
    out["ret7_quint"] = D.groupby("r7q").apply(summ)
    D["r30q"] = pd.qcut(D["ret30"], 5, labels=False)
    out["ret30_quint"] = D.groupby("r30q").apply(summ)
    D["rrq"] = pd.qcut(D["rr"], 5, labels=False)
    out["rr_quint"] = D.groupby("rrq").apply(summ)
    D["rzq"] = pd.qcut(D["rng_z"], 5, labels=False)
    out["rangez_quint"] = D.groupby("rzq").apply(summ)
    D["dlq"] = pd.qcut(D["dist_low30"], 5, labels=False)
    out["dist_low30_quint"] = D.groupby("dlq").apply(summ)
    out["newlow30_x_falling"] = D[D["ret30"] < 0].groupby(["newlow30"]).apply(summ)
    out["weekday"] = D.groupby("wd").apply(summ)
    out["fc_sign"] = D.groupby(np.sign(D["fc"])).apply(summ)
    out["by_coin_gain"] = D.groupby("coin").agg(gain_mean=("gain", "mean"), alloc_mean=("alloc", "mean"))
    out["by_year_gain"] = D.groupby("yr").agg(gain=("gain", "mean"), ab=("ab", "mean"), n=("ab", "size"))
    out["by_win_gain"] = D.groupby("win")["gain"].mean()
    return out
