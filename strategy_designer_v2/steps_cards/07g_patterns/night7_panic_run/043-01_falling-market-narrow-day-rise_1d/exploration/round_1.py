def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            ratio = rng / sd30
            nh = b.get("debug_info.components.narrow.last_history_value")
            if nh is not None:
                ratio = nh.where(nh.notna(), ratio)
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ret3p = c / c.shift(3) - 1
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "fwd3": fwd3, "fwd1": fwd1, "r1": r1, "ret3p": ret3p,
                "ratio": ratio, "rng": rng, "sd30": sd30, "clv": clv,
                "falling": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 3 == 0].groupby("coin")["fwd3"].mean()
    A["ex3"] = A["fwd3"] - A["coin"].map(drift)
    G = A[(A.pos % 3 == 0) & A.ex3.notna()].copy()
    out = {}
    def tab(df, key, val="ex3", q=5):
        d = df.dropna(subset=[key, val]).copy()
        d["bin"] = d.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("bin")[val].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.drop(columns="std")
    out["drift3_by_coin"] = drift
    out["share_falling_grid"] = G.falling.mean()
    out["ratio_q_falling"] = tab(G[G.falling == 1], "ratio")
    out["ratio_q_notfalling"] = tab(G[G.falling == 0], "ratio")
    out["r1_q_falling"] = tab(G[G.falling == 1], "r1")
    out["r1_q_notfalling"] = tab(G[G.falling == 0], "r1")
    out["ret3p_q_all"] = tab(G, "ret3p")
    out["clv_q_falling"] = tab(G[G.falling == 1], "clv")
    out["clv_q_all"] = tab(G, "clv")
    out["sd30_q_all"] = tab(G, "sd30")
    out["fc_sign"] = G[G.falling == 1].groupby(np.sign(G["fc"]))["ex3"].agg(["mean", "count"])
    # slopes
    def slope(df, x):
        d = df.dropna(subset=[x, "ex3"])
        s = stats.linregress(d[x], d["ex3"])
        return f"slope {s.slope:.4g} t {s.slope/s.stderr:.2f} n {len(d)}"
    out["slope_ratio_falling"] = slope(G[G.falling == 1], "ratio")
    out["slope_ratio_all"] = slope(G, "ratio")
    out["slope_r1_all"] = slope(G, "r1")
    out["slope_clv_all"] = slope(G, "clv")
    # weekday daily
    D = A.dropna(subset=["fwd1"])
    wd = D.groupby("wd")["fwd1"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday_next1"] = wd.drop(columns="std")
    # book long/short
    D["gain"] = D["alloc"] * D["fwd1"]
    D["side"] = np.sign(D["alloc"]).fillna(0)
    out["book_gain_by_side"] = D.groupby("side")["gain"].agg(["mean", "sum", "count"])
    out["by_year_falling_ex3"] = G[G.falling == 1].groupby("year")["ex3"].agg(["mean", "count"])
    return out
