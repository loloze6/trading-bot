def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["f12x"] = b["f12"] - b["f12"].mean()
            b["p12"] = lc - lc.shift(12)
            b["p24"] = lc - lc.shift(24)
            b["vol24"] = b["r1"].rolling(24).std()
            b["rsi"] = b["debug_info.components.rsi_high.last_history_value"]
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            pv = b["postRebalance_total_value"].astype(float)
            b["bookr"] = np.log(pv).diff()
            b["coin"] = coin; b["w"] = w
            b["hour"] = b["ts"].dt.hour; b["wd"] = b["ts"].dt.weekday
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["fcbin"] = pd.cut(B["forecast"], [-21, -10, -4, -1, -0.25, -1e-9, 1e-9, 21],
                        labels=["<=-10", "-10..-4", "-4..-1", "-1..-.25", "-.25..0", "0", ">0"])
    out["fwd12x_by_forecast_bin"] = B.groupby(["fcbin"], observed=True).agg(
        n=("f12x", "size"), mean=("f12x", "mean"), alloc=("alloc", "mean"),
        rawrsi=("rsi", "mean"), vol=("vol24", "mean"))
    out["alloc_desc"] = B["alloc"].describe()
    out["corr_alloc_forecast"] = float(B[["alloc", "forecast"]].corr().iloc[0, 1])
    out["rsi_raw_desc"] = B["rsi"].describe()
    # past 12h move quintiles -> forward
    B["p12q"] = B.groupby("coin")["p12"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    g = B.groupby("p12q")["f12x"]
    out["fwd12x_by_past12_decile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size() / 12))})
    B["volq"] = B.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    g = B.groupby("volq")
    out["by_vol_quintile"] = pd.DataFrame({"fwd12x": g["f12x"].mean(), "book_r_mean": g["bookr"].mean(),
        "abs_alloc": g["alloc"].apply(lambda s: s.abs().mean())})
    g = B.groupby("hour")
    out["by_hour"] = pd.DataFrame({"r1_mean_bp": g["r1"].mean() * 1e4,
        "t": g["r1"].mean() / (g["r1"].std() / np.sqrt(g["r1"].count())),
        "book_bp": g["bookr"].mean() * 1e4})
    g = B.groupby("wd")
    out["by_weekday"] = pd.DataFrame({"r1_mean_bp": g["r1"].mean() * 1e4,
        "t": g["r1"].mean() / (g["r1"].std() / np.sqrt(g["r1"].count())),
        "book_bp": g["bookr"].mean() * 1e4})
    g = B.groupby(["coin", "w"])
    out["by_coin_window"] = pd.DataFrame({"coin_ret": g["r1"].sum(), "book_ret": g["bookr"].sum(),
        "short_share": g["alloc"].apply(lambda s: (s < -1e-6).mean())})
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades_summary"] = T.groupby(["coin", "side"]).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        comm=("total_commission", "mean"), dur_h=("duration_minutes", lambda s: s.mean() / 60),
        win=("profit_loss_percent", lambda s: (s > 0).mean()))
    T["durq"] = pd.qcut(T["duration_minutes"], 5, duplicates="drop")
    out["trades_by_duration"] = T.groupby("durq", observed=True).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
