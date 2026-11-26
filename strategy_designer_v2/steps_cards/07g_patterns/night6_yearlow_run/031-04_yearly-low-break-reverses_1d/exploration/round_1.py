def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    rows = []
    reg_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            reg_rows.append({"coin": coin, "w": w, "n": n,
                             "mr_bars": int((b["regime"] == "mean_reversion").sum()),
                             "inpos": int((b["postRebalance_current_allocation"].abs() > 1e-9).sum())})
            r1 = c.pct_change()
            past10 = c / c.shift(10) - 1
            past3 = c / c.shift(3) - 1
            vol20 = r1.rolling(20).std()
            low60 = c.shift(1).rolling(60).min()
            high60 = c.shift(1).rolling(60).max()
            d_low60 = c / low60 - 1
            rng = (c - low60) / (high60 - low60)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                fwd = c.iloc[i + H] / c.iloc[i] - 1
                rows.append({"coin": coin, "w": w, "fwd": fwd, "past10": past10.iloc[i], "past3": past3.iloc[i],
                             "vol20": vol20.iloc[i], "d_low60": d_low60.iloc[i], "rng60": rng.iloc[i],
                             "mr": b["regime"].iloc[i] == "mean_reversion", "wd": ts.iloc[i].dayofweek,
                             "year": ts.iloc[i].year})
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["unus"] = df["fwd"] - df["drift"]
    df["vol_rank"] = df.groupby("coin")["vol20"].rank(pct=True)
    out["n_cases"] = len(df)
    reg = pd.DataFrame(reg_rows)
    out["regime_by_coin"] = reg.groupby("coin")[["n", "mr_bars", "inpos"]].sum()

    def grp(col, q=5):
        d = df.dropna(subset=[col, "unus"]).copy()
        d["bin"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("bin")["unus"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        rho, p = stats.spearmanr(d[col], d["unus"])
        g.loc["spearman", "mean"] = rho
        g.loc["spearman", "t"] = p
        return g
    for col in ["past10", "past3", "vol20", "d_low60", "rng60"]:
        out["unus_by_" + col + "_quint"] = grp(col)
    g = df.groupby("wd")["unus"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["by_weekday"] = g
    g = df.groupby("year")["unus"].agg(["mean", "count"])
    out["by_year"] = g
    # vol-scaled fwd by past10 quintile in high vol vs low vol
    d = df.dropna(subset=["past10", "vol_rank"]).copy()
    d["z"] = d["unus"] / (d["vol20"] * np.sqrt(H))
    d["p10q"] = d.groupby("coin")["past10"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["vh"] = d["vol_rank"] > 0.5
    out["z_by_past10tercile_volhalf"] = d.groupby(["vh", "p10q"])["z"].agg(["mean", "count"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    if tr:
        T = pd.concat(tr)
        out["trades_summary"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "min", "max"])
    return out
