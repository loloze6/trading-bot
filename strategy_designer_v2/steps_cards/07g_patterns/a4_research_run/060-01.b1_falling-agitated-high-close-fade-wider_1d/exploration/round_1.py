def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 3:
                continue
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": (c - l) / rng,
                "ret0": c / c.shift(1) - 1,
                "ret3": c / c.shift(3) - 1,
                "range_rel": (h - l) / c.shift(1),
                "body": (c - o) / rng,
                "next": c.shift(-1) / c - 1,
                "next2": c.shift(-2) / c - 1,
                "regime": b["regime"],
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            d["vol20"] = d["ret0"].rolling(20, min_periods=10).std()
            d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["next"])
    D["ret0z"] = D["ret0"] / D["vol20"]
    D["rngz"] = D["range_rel"] / D.groupby("coin")["range_rel"].transform("median")

    def summ(g, col="next"):
        x = g[col].dropna()
        n = len(x)
        m = x.mean()
        t = m / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t})

    out = {}
    out["regime counts"] = D.groupby(["coin", "regime"]).size().unstack(fill_value=0)
    D["locq"] = pd.cut(D["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["next by loc, in profile"] = D[D.inprof].groupby("locq", observed=True).apply(summ)
    out["next by loc, outside"] = D[~D.inprof].groupby("locq", observed=True).apply(summ)
    D["r0q"] = pd.qcut(D["ret0z"], 5, duplicates="drop")
    out["next by ret0z, all"] = D.groupby("r0q", observed=True).apply(summ)
    out["next by ret0z, in profile"] = D[D.inprof].groupby("r0q", observed=True).apply(summ)
    D["rgq"] = pd.qcut(D["rngz"], 5, duplicates="drop")
    out["next by range width, all"] = D.groupby("rgq", observed=True).apply(summ)
    out["next by weekday, all"] = D.groupby("wd").apply(summ)
    out["next by weekday, in profile"] = D[D.inprof].groupby("wd").apply(summ)
    D["r3q"] = pd.qcut(D["ret3"] / D["vol20"], 5, duplicates="drop")
    out["next by 3d ret z, all"] = D.groupby("r3q", observed=True).apply(summ)
    out["next2 by ret0z, all"] = D.groupby("r0q", observed=True).apply(lambda g: summ(g, "next2"))
    act = D[D["pos"].abs() > 1e-6].copy()
    act["gain"] = act["pos"] * act["next"]
    out["active by coin"] = act.groupby("coin").apply(lambda g: summ(g, "gain"))
    out["active by year"] = act.groupby("year").apply(lambda g: summ(g, "gain"))
    out["active gain by ret0z"] = act.groupby("r0q", observed=True).apply(lambda g: summ(g, "gain"))
    # book best/worst days context
    q = act["gain"].quantile([0.05, 0.95])
    out["worst 5% days ctx"] = act[act.gain <= q.iloc[0]][["loc", "ret0z", "rngz", "next"]].mean()
    out["best 5% days ctx"] = act[act.gain >= q.iloc[1]][["loc", "ret0z", "rngz", "next"]].mean()
    out["coin next-day mean all"] = D.groupby("coin").apply(summ)
    return out
