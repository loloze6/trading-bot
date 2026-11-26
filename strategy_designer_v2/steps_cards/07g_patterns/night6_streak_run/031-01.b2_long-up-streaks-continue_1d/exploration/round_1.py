def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(int); dn = (r1 < 0).astype(int)
            us = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            ds = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "r3p": c / c.shift(3) - 1, "r7p": c / c.shift(7) - 1,
                "r30p": c / c.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "us": us, "ds": ds,
                "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    drift = g.groupby("coin")["fwd3"].mean()
    g["ex"] = g["fwd3"] - g["coin"].map(drift)
    g["vnorm"] = g["vol20"] / g.groupby("coin")["vol20"].transform("median")
    g["wd"] = g["ts"].dt.weekday
    g["yr"] = g["ts"].dt.year

    def summ(key, df=None):
        df = g if df is None else df
        out = {}
        for k, s in df.groupby(key):
            day = s.groupby("ts")["ex"].sum()
            n = len(s); m = s["ex"].mean()
            se = day.std(ddof=1) * np.sqrt(len(day)) / n if len(day) > 1 else np.nan
            out[k] = {"n": n, "mean_ex_%": 100 * m, "t_day": m / se if se else np.nan,
                      "hit": (s["ex"] > 0).mean()}
        return pd.DataFrame(out).T

    g["us_b"] = g["us"].clip(upper=6)
    g["ds_b"] = g["ds"].clip(upper=6)
    g["r3q"] = g.groupby("coin")["r3p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g["r7q"] = g.groupby("coin")["r7p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g["r30q"] = g.groupby("coin")["r30p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g["r1q"] = g.groupby("coin")["r1"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g["vq"] = g.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g["fcq"] = pd.cut(g["fc"], [-0.1, 0.01, 5, 10, 15, 20.1])
    # standardized r3 by vol
    g["z3"] = g["r3p"] / (g["vol20"] * np.sqrt(3))
    g["z3q"] = g.groupby("coin")["z3"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    # abs move in prior 3d vs abs future
    res = {
        "up_streak": summ("us_b"), "down_streak": summ("ds_b"),
        "prior1d_quint": summ("r1q"), "prior3d_quint": summ("r3q"),
        "prior7d_quint": summ("r7q"), "prior30d_quint": summ("r30q"),
        "z3_quint": summ("z3q"), "vol_quint": summ("vq"),
        "weekday": summ("wd"), "year": summ("yr"), "fc_bucket": summ("fcq"),
        "coin": summ("coin"),
    }
    # down streak by coin (>=3)
    res["ds_ge3_by_coin"] = summ("coin", g[g["ds"] >= 3])
    res["r30_top_by_coin"] = summ("coin", g[g["r30q"] == 4])
    # vol in bars after streaks: abs fwd3 relative
    g["absf"] = g["fwd3"].abs() / (g["vol20"] * np.sqrt(3))
    res["abs_fwd_by_upstreak"] = g.groupby("us_b")["absf"].agg(["count", "mean"])
    res["abs_fwd_by_downstreak"] = g.groupby("ds_b")["absf"].agg(["count", "mean"])
    return res
