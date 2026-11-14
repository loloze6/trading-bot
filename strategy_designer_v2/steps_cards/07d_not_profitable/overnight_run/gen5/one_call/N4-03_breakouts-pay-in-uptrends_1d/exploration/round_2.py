def explore(data):
    import pandas as pd, numpy as np
    out = {}
    def tstat(x):
        x = x.dropna()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]
            d = pd.DataFrame({"coin": c, "win": w, "fc": b["forecast"], "regime": b["regime"],
                "r10": cl.shift(-10) / cl - 1, "r20": cl.shift(-20) / cl - 1,
                "past20": cl / cl.shift(20) - 1, "past60": cl / cl.shift(60) - 1,
                "vol": cl.pct_change().rolling(20).std(), "i": np.arange(len(b))})
            rows.append(d)
    B = pd.concat(rows, ignore_index=True)
    B["hold10"] = B.groupby("coin")["r10"].transform("mean")
    B["hold20"] = B.groupby("coin")["r20"].transform("mean")
    B["ex10"] = B["r10"] - B["hold10"]; B["ex20"] = B["r20"] - B["hold20"]
    B["volt"] = B.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "vol"]))
    B["p60"] = np.where(B["past60"] > 0, "up60", "down60")
    G10 = B[(B["i"] % 10 == 0) & (B["fc"].abs() > 0)]
    G20 = B[(B["i"] % 20 == 0) & (B["fc"].abs() > 0)]
    for nm, G, col in [("ex10", G10, "ex10"), ("ex20", G20, "ex20")]:
        out[f"{nm}_by_regime_p60"] = G.groupby(["regime", "p60"])[col].agg(["size", "mean", tstat])
        out[f"{nm}_by_regime_vol"] = G.groupby(["regime", "volt"])[col].agg(["size", "mean", tstat])
    # all active-regime grid bars regardless of forecast: does being in MR regime itself predict?
    H = B[(B["i"] % 10 == 0)]
    out["ex10_all_by_regime"] = H.groupby("regime")["ex10"].agg(["size", "mean", tstat])
    # trades: long trades by duration bucket
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            tr.append(df.assign(coin=c))
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 2, 5, 10, 30, 1e4])
    out["trades_by_side_duration"] = T.groupby(["side", "db"]).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), median=("profit_loss_percent", "median"),
        comm=("total_commission", "mean"), gsum=("profit_loss_percent", "sum"))
    return out
