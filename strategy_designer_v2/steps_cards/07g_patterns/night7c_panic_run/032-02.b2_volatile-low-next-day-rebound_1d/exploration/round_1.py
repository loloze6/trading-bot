def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["pos"] = np.arange(len(b))
            d["r1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["ret30"] = c / c.shift(30) - 1
            low30 = l.shift(1).rolling(30).min()
            d["below"] = c / low30 - 1
            high30 = h.shift(1).rolling(30).max()
            d["above"] = c / high30 - 1
            rng = (h - l) / c
            d["rng30"] = rng.rolling(30).mean()
            d["rng90"] = rng.rolling(90, min_periods=60).mean()
            d["rngratio"] = d["rng30"] / d["rng90"]
            d["rng1"] = rng
            d["vol20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["vol20"].shift(1)
            d["alloc"] = b["postRebalance_current_allocation"]
            d["regime"] = b["regime"]
            d["fc"] = b["forecast"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["year"] = D["ts"].dt.year

    def ct(sub, col="x1"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 5: return pd.Series({"n": len(sub), "days": 0, "mean": np.nan, "t": np.nan})
        m = sub[col].mean()
        g = (sub[col] - m).groupby(sub["day"]).sum()
        D_ = len(g)
        se = np.sqrt((g**2).sum() * D_ / max(D_-1, 1)) / len(sub)
        return pd.Series({"n": len(sub), "days": D_, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    # new 30d low, by 30d return sign
    nl = D[D["below"] < 0].copy()
    nl["fall"] = nl["ret30"] < 0
    nl["deep"] = pd.qcut(nl["below"], 3, labels=["deep", "mid", "shallow"])
    out["newlow_by_deep"] = nl.groupby("deep").apply(ct)
    out["newlow_by_rngratio_tercile"] = nl.groupby(pd.qcut(nl["rngratio"], 3, labels=["calm", "mid", "wide"])).apply(ct)
    nh = D[D["above"] > 0].copy()
    out["newhigh_by_height"] = nh.groupby(pd.qcut(nh["above"], 3, labels=["small", "mid", "big"])).apply(ct)
    # large moves
    D["z1q"] = pd.qcut(D["z1"], 10, labels=False)
    out["next_by_prev_zret_decile"] = D.groupby("z1q").apply(ct)
    D["rngq"] = pd.qcut(D["rng1"] / D["rng30"].shift(0), 5, labels=False)
    out["next_by_todays_range_vs_month_q"] = D.groupby("rngq").apply(ct)
    out["by_weekday"] = D.groupby("wd").apply(ct)
    out["by_volregime_q"] = D.groupby(pd.qcut(D["rngratio"], 5, labels=False)).apply(ct)
    out["by_ret30_q"] = D.groupby(pd.qcut(D["ret30"], 5, labels=False)).apply(ct)
    # book
    act = D[D["alloc"].abs() > 0]
    out["active_summary"] = pd.Series({"bars_in_pos": len(act), "mean_alloc": act["alloc"].mean(), "mean_f1": act["f1"].mean(), "mr_bars": (D["regime"] == "mean_reversion").sum()})
    out["regime_counts"] = D["regime"].value_counts()
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    out["trades"] = tr.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), mean_dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
