def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df):
                d = df.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    T["efb"] = pd.cut(T["entry_forecast"], [-0.01, 0.5, 2, 8, 15, 21])
    out["trades_by_entry_forecast"] = T.groupby("efb").agg(n=("side", "size"), days=("days", "mean"),
        gross=("profit_loss_percent", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()))
    T["long_hold"] = T["days"] > 15
    out["trades_by_year_hold"] = T.groupby(["year", "long_hold"]).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean")).unstack()
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values); n = len(cl)
            d = pd.DataFrame({"coin": c, "win": w, "i": np.arange(n), "f": b["forecast"].values})
            for h in (5, 10, 20):
                d[f"fwd{h}"] = cl.shift(-h) / cl - 1
            d["past100"] = cl / cl.shift(100) - 1
            d["past5"] = cl / cl.shift(5) - 1
            d["past20"] = cl / cl.shift(20) - 1
            r = cl.pct_change()
            d["vol20"] = r.rolling(20).std()
            d["dd60"] = cl / cl.rolling(60, min_periods=30).max() - 1
            rows.append(d)
    B = pd.concat(rows, ignore_index=True)
    for h in (5, 10, 20):
        B[f"ex{h}"] = B[f"fwd{h}"] - B.groupby("coin")[f"fwd{h}"].transform("mean")
    B["vq"] = B.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "vol"]))
    def tstat(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    deep = B["f"] >= 5
    small = (B["f"] > 0) & (B["f"] < 2)
    res = {}
    for h in (5, 10, 20):
        nb = B[B["i"] % h == 0]
        res[f"deep_h{h}"] = tstat(nb.loc[deep.loc[nb.index], f"ex{h}"])
        res[f"small_h{h}"] = tstat(nb.loc[small.loc[nb.index], f"ex{h}"])
    out["horizon_deep_vs_small"] = pd.DataFrame(res).T
    nb = B[B["i"] % 10 == 0].copy()
    nd = nb[deep.loc[nb.index]].copy()
    nd["trend100"] = np.where(nd["past100"] > 0, "up100", "down100")
    out["deep_by_trend100_h10"] = nd.groupby("trend100")["ex10"].apply(tstat).unstack()
    out["deep_by_vol_h10"] = nd.groupby("vq")["ex10"].apply(tstat).unstack()
    nd["bounce5"] = np.where(nd["past5"] > 0, "last5_up", "last5_down")
    out["deep_by_last5_h10"] = nd.groupby("bounce5")["ex10"].apply(tstat).unstack()
    nd["ddq"] = pd.cut(nd["dd60"], [-1, -0.4, -0.25, -0.15, 0])
    out["deep_by_dd60_h10"] = nd.groupby("ddq")["ex10"].apply(tstat).unstack()
    ns = nb[small.loc[nb.index]].copy()
    ns["trend100"] = np.where(ns["past100"] > 0, "up100", "down100")
    out["small_by_trend100_h10"] = ns.groupby("trend100")["ex10"].apply(tstat).unstack()
    return out
