def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "r1": r1, "z1": r1 / vol20,
                "r5": pd.Series(c).pct_change(5),
                "r20": pd.Series(c).pct_change(20),
                "vol20": vol20,
                "fc": b["forecast"].astype(float),
                "dow": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["ma50gap"] = pd.Series(c) / pd.Series(c).rolling(50, min_periods=30).mean() - 1
            df["hi20"] = pd.Series(c) / pd.Series(c).rolling(20, min_periods=10).max() - 1
            fwd = pd.Series(c).shift(-H) / pd.Series(c) - 1
            df["fwd"] = fwd
            df = df.iloc[::H]
            df = df[df["fwd"].notna()]
            rows.append(df)
    g = pd.concat(rows, ignore_index=True)
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["exs"] = g["ex"] / g["coin"].map(sd)
    out = {"n_cells_drift_sd": pd.DataFrame({"n": g.groupby("coin").size(), "drift": drift, "sd": sd})}

    def by_q(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q")["ex"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        s = stats.linregress(d[col], d["exs"])
        t.loc["slope_t_std", "mean"] = s.slope / s.stderr
        return t
    for col in ["z1", "r5", "r20", "ma50gap", "hi20", "vol20"]:
        out["q_" + col] = by_q(col)
    t = g.groupby("dow")["ex"].agg(["count", "mean", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["dow"] = t
    t = g.groupby("year")["ex"].agg(["count", "mean"]); out["year"] = t
    # regime split: z1 effect above/below 50d mean
    d = g.dropna(subset=["z1", "ma50gap"])
    res = {}
    for name, m in [("above_ma50", d["ma50gap"] > 0), ("below_ma50", d["ma50gap"] <= 0)]:
        s = stats.linregress(d.loc[m, "z1"], d.loc[m, "exs"])
        res[name] = {"n": int(m.sum()), "slope": s.slope, "t": s.slope / s.stderr}
    out["z1_by_trend"] = pd.DataFrame(res).T
    # book: days by coin -> daily returns, gain from drift vs timing
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    D = pd.concat(dd)
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["days"] = tr["duration_minutes"] / 1440
    tr["dq"] = pd.qcut(tr["days"].rank(method="first"), 4, labels=False)
    out["trades_by_duration"] = tr.groupby("dq").agg(n=("days", "size"), days=("days", "mean"),
                                                     pnl=("net_profit_loss_percent", "mean"))
    return out
