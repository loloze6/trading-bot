def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440.0
    out["trades_summary"] = pd.DataFrame({
        "n": [len(T)],
        "mean_days": [T["days"].mean()],
        "median_days": [T["days"].median()],
        "mean_gross_pct": [T["profit_loss_percent"].mean()],
        "mean_net_pct": [T["net_profit_loss_percent"].mean()],
        "mean_comm": [T["total_commission"].mean()],
        "win_gross": [(T["profit_loss_percent"] > 0).mean()],
        "share_long": [(T["side"] == "LONG").mean()],
    })
    T["fq"] = pd.cut(T["entry_forecast"], [-1, 1, 3, 5, 10, 21])
    out["trades_by_entry_fc"] = T.groupby("fq", observed=True).agg(
        n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), days=("days", "mean"))
    T["dq"] = pd.cut(T["days"], [0, 1.5, 3, 7, 20, 1000])
    out["trades_by_duration"] = T.groupby("dq", observed=True).agg(
        n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"))

    # bar-level non-overlapping 10-bar forward returns
    rows = []
    for c, ws in data["bars"].items():
        allc = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            fwd = pd.Series(cl).shift(-10) / pd.Series(cl) - 1
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20).std()
            vol60m = vol.rolling(200, min_periods=50).median()
            ma50 = pd.Series(cl).rolling(50).mean()
            ret20 = pd.Series(cl) / pd.Series(cl).shift(20) - 1
            dist = b["debug_info.components.below_sma200.last_history_value"] if "debug_info.components.below_sma200.last_history_value" in b else np.nan
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": c, "win": w, "i": np.arange(len(b)), "fc": b["forecast"].values,
                              "fwd": fwd.values, "hivol": (vol > vol60m).values,
                              "ret20": ret20.values, "dist": np.asarray(dist, dtype=float) if np.ndim(dist) else np.nan,
                              "above50": (pd.Series(cl) > ma50).values, "year": ts.dt.year.values})
            rows.append(d)
    B = pd.concat(rows, ignore_index=True)
    G = B[(B["i"] % 10 == 0) & B["fwd"].notna()].copy()
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    def st(x):
        x = x.dropna()
        n = len(x); m = x.mean(); s = x.std()
        return pd.Series({"n": n, "mean": m, "t": m / (s / np.sqrt(n)) if n > 1 and s > 0 else np.nan})
    G["fb"] = pd.cut(G["fc"], [-0.01, 0.0001, 1, 3, 5, 10, 21], include_lowest=True)
    out["fwd10_by_fc"] = G.groupby("fb", observed=True)["ex"].apply(st).unstack()
    A = G[G["fc"] > 0]
    out["active_by_vol"] = A.groupby("hivol")["ex"].apply(st).unstack()
    A2 = A.copy(); A2["mom"] = np.where(A2["ret20"] > 0, "ret20_up", "ret20_down")
    out["active_by_ret20"] = A2.groupby("mom")["ex"].apply(st).unstack()
    out["active_by_above50"] = A.groupby("above50")["ex"].apply(st).unstack()
    out["active_by_year"] = A.groupby("year")["ex"].apply(st).unstack()
    out["active_by_coin"] = A.groupby("coin")["ex"].apply(st).unstack()
    out["share_bars_active"] = float((B["fc"] > 0).mean())
    out["raw_dist_quant_active"] = A["dist"].describe()
    return out
