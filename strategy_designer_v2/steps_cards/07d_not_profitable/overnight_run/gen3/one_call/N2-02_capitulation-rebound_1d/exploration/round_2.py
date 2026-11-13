def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # drawdown of the book per coin-window, located by year
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            v = d["book_value"].astype(float).values
            if len(v) < 2: continue
            peak = np.maximum.accumulate(v); ddv = v / peak - 1
            i = int(np.argmin(ddv))
            dd.append((c, w, ddv[i], pd.to_datetime(d["day"]).iloc[i].year, v[-1] / v[0] - 1))
    DD = pd.DataFrame(dd, columns=["coin", "win", "mdd", "year", "ret"])
    out["mdd_by_year"] = DD.groupby("year").agg(n=("mdd", "count"), mdd_mean=("mdd", "mean"), mdd_min=("mdd", "min"), ret_mean=("ret", "mean"))
    out["mdd_by_coin"] = DD.groupby("coin").agg(mdd_mean=("mdd", "mean"), mdd_min=("mdd", "min"), ret_mean=("ret", "mean"))
    # active-bar non-overlapping forward returns with conditioning
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values.astype(float); fc = b["forecast"].values.astype(float)
            raw = b["debug_info.components.depth.last_history_value"].values.astype(float) if "debug_info.components.depth.last_history_value" in b else np.full(len(b), np.nan)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (10, 20):
                for i in range(0, len(b) - h, h):
                    r1 = cl[i] / cl[i - 1] - 1 if i >= 1 else np.nan
                    r3 = cl[i] / cl[i - 3] - 1 if i >= 3 else np.nan
                    lo5 = cl[i] / cl[max(0, i - 5):i + 1].min() - 1
                    rows.append((c, h, fc[i], cl[i + h] / cl[i] - 1, r1, r3, lo5, raw[i], yr[i]))
    N = pd.DataFrame(rows, columns=["coin", "h", "fc", "fwd", "r1", "r3", "lo5", "raw", "year"])
    N["ex"] = N["fwd"] - N.groupby(["coin", "h"])["fwd"].transform("mean")
    tt = lambda g: pd.Series({"n": len(g), "mean": g["ex"].mean(), "t": g["ex"].mean() / g["ex"].std() * np.sqrt(len(g)) if len(g) > 2 else np.nan})
    A = N[(N["fc"] > 0.001)]
    out["h20_by_fc"] = N[N["h"] == 20].assign(fb=lambda x: pd.cut(x["fc"], [-0.01, 0.001, 5, 10, 20.01])).groupby("fb").apply(tt)
    A10 = A[A["h"] == 10].copy()
    A10["last_day"] = np.where(A10["r1"] > 0, "up", "down")
    out["h10_active_by_lastday"] = A10.groupby("last_day").apply(tt)
    A10["r3s"] = np.where(A10["r3"] > 0, "3d up", "3d down")
    out["h10_active_by_3d"] = A10.groupby("r3s").apply(tt)
    A10["bounce"] = pd.cut(A10["lo5"], [-0.01, 0.03, 0.08, 5])
    out["h10_active_by_off_5d_low"] = A10.groupby("bounce").apply(tt)
    A10["rawb"] = pd.cut(A10["raw"], [-5, -0.5, -0.35, -0.2, 0.5])
    out["h10_active_by_raw_depth"] = A10.groupby("rawb").apply(tt)
    out["h10_active_by_year"] = A10.groupby("year").apply(tt)
    out["raw_depth_quantiles"] = A10["raw"].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_frame()
    # trades gross by year and holding length
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            tr.append(t.assign(coin=c))
    T = pd.concat(tr, ignore_index=True)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    T["dur"] = pd.cut(T["duration_minutes"] / 1440, [0, 2, 5, 15, 40, 1000])
    g = lambda x: pd.Series({"n": len(x), "gross": x["profit_loss_percent"].mean(), "net": x["net_profit_loss_percent"].mean(), "win": (x["profit_loss_percent"] > 0).mean()})
    out["trades_by_year"] = T.groupby("year").apply(g)
    out["trades_by_dur"] = T.groupby("dur").apply(g)
    return out
