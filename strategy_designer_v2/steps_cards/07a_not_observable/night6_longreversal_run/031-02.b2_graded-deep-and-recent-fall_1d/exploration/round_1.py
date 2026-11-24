def explore(data):
    import pandas as pd, numpy as np
    H = 30
    rows = []
    wl = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            n = len(b)
            yr = pd.to_datetime(b["timestamp"].iloc[0]).year
            wl.append({"coin": coin, "window": w, "len": n, "year": yr,
                       "active_share": float((b["forecast"] > 0).mean())})
            for p in range(0, n - H, H):
                r = b["close"].iloc[p + H] / b["close"].iloc[p] - 1
                f = b["forecast"].iloc[p]
                rows.append({"coin": coin, "window": w, "year": yr, "pos": p,
                             "ts": str(b["timestamp"].iloc[p])[:10], "ret": r, "fc": f,
                             "act": f > 0})
    g = pd.DataFrame(rows)
    W = pd.DataFrame(wl)
    drift = g.groupby("coin")["ret"].mean()
    g["ex"] = g["ret"] - g["coin"].map(drift)
    c = g[g["act"]]
    out = {}
    out["window lengths"] = W["len"].describe()
    out["grid points per window"] = g.groupby(["coin", "window"]).size().describe()
    out["grid total / active / distinct days"] = pd.Series({"grid": len(g), "active": len(c), "distinct_days": c["ts"].nunique()})
    out["active bar share by coin"] = W.groupby("coin")["active_share"].mean()
    out["cases by coin"] = c.groupby("coin").size()
    out["cases by year"] = c.groupby("year").agg(n=("ex", "size"), days=("ts", "nunique"), mean_ex=("ex", "mean"))
    out["active bar share by year"] = W.groupby("year")["active_share"].mean()
    out["cases by grid position"] = c.groupby("pos").size()
    out["excess stats on cases"] = c["ex"].describe()
    out["forecast on cases"] = c["fc"].describe()
    # all-bar active forecast, distinct days with any coin active
    allb = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            a = b[b["forecast"] > 0]
            allb.append(pd.DataFrame({"coin": coin, "d": a["timestamp"].astype(str).str[:10]}))
    A = pd.concat(allb)
    out["active bars / distinct active days"] = pd.Series({"bars": len(A), "days": A["d"].nunique()})
    # correlation across coins of active cases: per day count
    out["cases per day distribution"] = c.groupby("ts").size().value_counts().sort_index()
    return out
