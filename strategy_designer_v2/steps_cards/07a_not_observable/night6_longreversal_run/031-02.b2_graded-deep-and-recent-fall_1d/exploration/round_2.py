def explore(data):
    import pandas as pd, numpy as np
    H = 30
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            n = len(b)
            for p in range(0, n - H, H):
                ts = pd.to_datetime(b["timestamp"].iloc[p])
                rows.append({"coin": coin, "window": w, "wnum": int(w[1:]), "year": ts.year,
                             "ts": str(ts)[:10], "pos": p,
                             "ret": b["close"].iloc[p + H] / b["close"].iloc[p] - 1,
                             "fc": b["forecast"].iloc[p]})
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["ret"].mean()
    g["ex"] = g["ret"] - g["coin"].map(drift)
    g["act"] = g["fc"] > 0
    g["fold"] = pd.cut(g["wnum"], [0, 6, 12, 18, 24], labels=["A", "B", "C", "D"])
    out = {}
    out["year range by window block"] = g.groupby("fold", observed=True)["year"].agg(["min", "max"])
    gd = g.groupby("fold", observed=True).agg(grid_dates=("ts", "nunique"), grid_cells=("ts", "size"))
    cd = g[g["act"]].groupby("fold", observed=True).agg(cases=("ts", "size"), case_days=("ts", "nunique"))
    out["grid dates vs case days by fold"] = gd.join(cd)
    out["grid dates per year"] = g.groupby("year").agg(grid_dates=("ts", "nunique"),
                                                       case_days=("ts", lambda s: s[g.loc[s.index, "act"]].nunique()))
    out["share of coin grid cells active by fold"] = g.groupby(["fold"], observed=True)["act"].mean()
    out["coins active per case-day"] = g[g["act"]].groupby("ts")["coin"].nunique().describe()
    # per-coin distinct days, and how many case-days are unique to one coin
    c = g[g["act"]]
    perday = c.groupby("ts")["coin"].nunique()
    out["case days with only one coin"] = int((perday == 1).sum())
    out["excess per case: mean, std, sem-like n"] = pd.Series({"mean": c["ex"].mean(), "std": c["ex"].std(),
                                                               "n": len(c)})
    return out
