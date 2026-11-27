def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 25:
                continue
            rng = (b["high"] - b["low"])
            base = rng.shift(1).rolling(20, min_periods=20).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "rm": rng / base,
                "loc": (b["close"] - b["low"]) / rng.replace(0, np.nan),
                "r0": b["close"] / b["close"].shift(1) - 1,
                "r5": b["close"] / b["close"].shift(5) - 1,
                "r20": b["close"] / b["close"].shift(20) - 1,
                "nxt": b["close"].shift(-1) / b["close"] - 1,
                "nxt3": b["close"].shift(-3) / b["close"] - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "pos": b["postRebalance_current_allocation"],
                "vol20": (b["close"].pct_change()).rolling(20).std(),
            })
            d["z0"] = d["r0"] / d["vol20"]
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["nxt"].mean()
    df["u"] = df["nxt"] - df["coin"].map(drift)
    df["day"] = df["ts"].dt.floor("D")
    df = df.dropna(subset=["u", "rm", "loc"])

    def tstat(g):
        s = g.groupby("day")["u"].sum()
        n = g["day"].nunique()
        m = g["u"].mean()
        se = np.sqrt((s - s.mean() * 0 - g.groupby("day")["u"].size() * m).pow(2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": n, "mean_u_%": 100 * m, "t": m / se if se > 0 else np.nan})

    df["rmq"] = pd.qcut(df["rm"], 4, labels=["rm1", "rm2", "rm3", "rm4"])
    df["locq"] = pd.cut(df["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["l0", "l1", "l2", "l3", "l4"])
    out = {}
    out["by_agit_rm_loc"] = df.groupby(["agit", "rmq", "locq"]).apply(tstat).round(3)
    df["z0q"] = pd.qcut(df["z0"], 5, labels=["z1", "z2", "z3", "z4", "z5"])
    out["by_agit_z0q"] = df.dropna(subset=["z0"]).groupby(["agit", "z0q"]).apply(tstat).round(3)
    df["r20s"] = np.sign(df["r20"].fillna(0)).map({1.0: "up20", -1.0: "dn20", 0.0: "na"})
    out["by_wd"] = df.groupby(df["ts"].dt.dayofweek).apply(tstat).round(3)
    df["volq"] = df.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["by_volq_z0q"] = df.dropna(subset=["z0", "volq"]).groupby(["volq", "z0q"]).apply(tstat).round(3)
    df["r5q"] = pd.qcut(df["r5"], 5, labels=False)
    out["by_agit_r5q"] = df.dropna(subset=["r5q"]).groupby(["agit", "r5q"]).apply(tstat).round(3)
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    daily = bd.groupby("day")["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean_%": 100 * daily.mean(), "sd_%": 100 * daily.std(), "n": len(daily),
                                   "share_of_total_from_top5pct_loss": daily[daily < daily.quantile(0.05)].sum() / daily.sum()})
    act = df[df["pos"] < 0]
    out["active_by_win"] = act.groupby("win").apply(tstat).round(3)
    return out
