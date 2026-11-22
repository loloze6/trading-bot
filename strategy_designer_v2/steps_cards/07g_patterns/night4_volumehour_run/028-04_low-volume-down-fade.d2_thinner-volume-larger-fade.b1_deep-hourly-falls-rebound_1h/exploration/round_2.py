def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            ma = r1.abs().rolling(720, min_periods=120).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            d = pd.DataFrame({"coin": coin, "w": w, "r1": r1, "s": r1 / ma,
                              "vr": v / v.rolling(720, min_periods=120).mean(),
                              "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "pos": np.arange(len(b)),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float)})
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            # return over prior 12h / 24h, scaled
            d["p12"] = (c / c.shift(12) - 1) / (ma * np.sqrt(12))
            d["p20"] = (c / c.shift(20) - 1) / (ma * np.sqrt(20))
            d["gain"] = d["alloc"] * d["n1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def st(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # evening window: bar at hour 20, next 2 hours (21:00-23:00)
    E = D[D["hour"] == 20]
    out["eve2h_by_coin"] = E.groupby("coin")["n2"].apply(st).unstack().round(2)
    out["eve2h_by_year"] = E.groupby("year")["n2"].apply(st).unstack().round(2)
    wm = E.groupby(["coin", "w"])["n2"].mean()
    out["eve2h_window_share_pos"] = pd.Series({"share_pos": (wm > 0).mean(), "n_win": len(wm), "mean_bp": wm.mean() * 1e4})
    out["eve2h_by_weekday"] = E.groupby("wd")["n2"].apply(st).unstack().round(2)
    E = E.copy()
    E["p20q"] = pd.qcut(E["p20"], 5, labels=False, duplicates="drop")
    out["eve2h_by_prior20h_quint"] = E.groupby("p20q")["n2"].apply(st).unstack().round(2)
    out["eve2h_corr_prior20h"] = pd.Series({"corr": E[["p20", "n2"]].dropna().corr().iloc[0, 1], "n": E[["p20", "n2"]].dropna().shape[0]})
    # other hours, 2h returns from hour h, non-overlapping per day
    out["2h_from_hour"] = D[D["hour"] % 2 == 0].groupby("hour")["n2"].apply(st).unstack().round(2)
    # falls graded by volume: within s<-1.5, quintile of vr, 3h fwd, grid
    G = D[(D["pos"] % 3 == 0) & (D["s"] < -1.5)].copy()
    G["vq"] = pd.qcut(G["vr"], 5, labels=False, duplicates="drop")
    out["fall_fwd3_by_vol_quint"] = G.groupby("vq")["n3"].apply(st).unstack().round(2)
    out["fall_vq_vr_edges"] = G.groupby("vq")["vr"].median().round(2)
    G2 = D[(D["pos"] % 3 == 0) & (D["s"] > 1.5)].copy()
    G2["vq"] = pd.qcut(G2["vr"], 5, labels=False, duplicates="drop")
    out["rise_fwd3_by_vol_quint"] = G2.groupby("vq")["n3"].apply(st).unstack().round(2)
    # book gain by hour and by allocation level
    out["book_bar_gain_by_hour"] = D.groupby("hour")["gain"].apply(st).unstack().round(2)
    D["aq"] = pd.cut(D["alloc"], [-0.01, 0.001, 0.5, 1.0, 1.5, 2.01])
    out["bar_gain_by_alloc"] = D.groupby("aq", observed=True)["gain"].apply(st).unstack().round(2)
    return out
