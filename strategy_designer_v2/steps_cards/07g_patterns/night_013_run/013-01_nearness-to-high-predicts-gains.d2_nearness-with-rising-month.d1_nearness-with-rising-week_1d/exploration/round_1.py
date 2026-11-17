def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    days = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            b["coin"] = coin; b["win"] = w
            b["r1"] = r1
            b["f7"] = c.shift(-7) / c - 1
            b["f1"] = c.shift(-1) / c - 1
            b["m7"] = c / c.shift(7) - 1
            b["m30"] = c / c.shift(30) - 1
            vol = r1.rolling(30, min_periods=20).std()
            b["vol"] = vol
            b["z1"] = r1 / vol.shift(1)
            b["vr"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean().shift(1)
            b["hi20"] = c / c.rolling(20, min_periods=20).max().shift(1) - 1
            b["nh"] = b.get("debug_info.components.near_high.last_history_value")
            b["grid"] = (np.arange(len(b)) % 7) == 0
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["f1"]
            rows.append(b)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            days.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(days, ignore_index=True)
    cm = B[B.grid].groupby("coin")["f7"].mean()
    B["f7x"] = B["f7"] - B["coin"].map(cm)
    G = B[B.grid & B.f7x.notna()]
    out = {}
    def qtab(df, col, q=5):
        df = df[df[col].notna()].copy()
        df["q"] = pd.qcut(df[col].rank(method="first"), q, labels=False)
        t = df.groupby("q")["f7x"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["lo"] = df.groupby("q")[col].min(); t["hi"] = df.groupby("q")[col].max()
        return t.round(4)
    T = G[G.regime == "trending"]
    U = G[G.regime != "trending"]
    out["trend_nh_q"] = qtab(T, "nh")
    out["trend_m7_q"] = qtab(T, "m7")
    out["trend_m30_q"] = qtab(T, "m30")
    out["off_m7_q"] = qtab(U, "m7")
    out["off_m30_q"] = qtab(U, "m30")
    out["all_z1_q"] = qtab(G, "z1")
    out["all_vol_q"] = qtab(G, "vol")
    out["all_vr_q"] = qtab(G, "vr")
    out["all_hi20_q"] = qtab(G, "hi20")
    out["regime_counts"] = G.groupby("regime")["f7x"].agg(["count", "mean"]).round(4)
    # weekday of daily coin & book returns
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    wt = D.groupby("wd")[["coin_return", "book_return"]].agg(["mean", "count"])
    out["weekday_days"] = wt.round(5)
    # book by window-year
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_year"] = D.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    # book gain by regime and position sign
    B["insign"] = np.sign(B["pos"].fillna(0))
    out["gain_by_regime"] = B.groupby("regime")["gain"].agg(["count", "mean", "sum"]).round(5)
    out["gain_by_coin"] = B.groupby("coin")["gain"].agg(["count", "mean", "sum"]).round(5)
    return out
