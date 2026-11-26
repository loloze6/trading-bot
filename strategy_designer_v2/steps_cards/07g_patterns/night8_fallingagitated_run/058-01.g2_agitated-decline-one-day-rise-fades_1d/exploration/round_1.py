def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            z1 = r1 / sd30
            z3 = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            z5 = (c / c.shift(5) - 1) / (sd30 * np.sqrt(5))
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            f5 = c.shift(-5) / c - 1
            n = len(b)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                               "inprof": (b["regime"] == "unknown").values,
                               "z1": z1, "z3": z3, "z5": z5, "rng": rng, "clo": clo,
                               "f1": f1, "f3": f3, "f5": f5,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {h: d.loc[d.pos % h == 0, "f%d" % h].mean() for h in (1, 3, 5)}
    out["drift"] = pd.Series(drift)
    out["share_in_profile"] = d["inprof"].mean()

    def tab(sub, key, h, bins):
        s = sub[sub.pos % h == 0].dropna(subset=[key, "f%d" % h]).copy()
        s["b"] = pd.cut(s[key], bins)
        s["u"] = s["f%d" % h] - drift[h]
        g = s.groupby(["inprof", "b"], observed=True)["u"]
        res = g.agg(["count", "mean", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res.round(4)

    zb = [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99]
    out["z1_f3"] = tab(d, "z1", 3, zb)
    out["z1_f1"] = tab(d, "z1", 1, zb)
    out["z3_f3"] = tab(d, "z3", 3, zb)
    out["z5_f5"] = tab(d, "z5", 5, zb)
    out["rng_f3"] = tab(d, "rng", 3, [0, 1, 1.5, 2, 3, 99])
    # close location in profile
    out["clo_f1"] = tab(d, "clo", 1, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    # weekday in profile, 1-day
    s = d[d.inprof].dropna(subset=["f1"])
    g = s.groupby("wd")["f1"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["wd_inprof_f1"] = g.round(4)
    s = d[~d.inprof].dropna(subset=["f1"])
    g = s.groupby("wd")["f1"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["wd_out_f1"] = g.round(4)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "sum"]).round(5)
    return out
