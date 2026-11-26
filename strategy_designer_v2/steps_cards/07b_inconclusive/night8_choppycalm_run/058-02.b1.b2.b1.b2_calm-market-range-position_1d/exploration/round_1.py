def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            rp = df.get("debug_info.components.range_pos.last_history_value")
            for H in [1, 3, 5, 10, 20]:
                for i in range(0, n - H, H):
                    r = c[i + H] / c[i] - 1
                    ret60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    rows.append(dict(coin=coin, w=w, H=H, i=i, ts=df["timestamp"].iloc[i],
                                     reg=df["regime"].iloc[i], f=df["forecast"].iloc[i],
                                     raw=rp.iloc[i] if rp is not None else np.nan,
                                     r=r, ret60=ret60))
    d = pd.DataFrame(rows)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    drift = d.groupby(["coin", "H"])["r"].mean().rename("drift")
    d = d.join(drift, on=["coin", "H"])
    d["x"] = d["r"] - d["drift"]
    ip = d[d["reg"] == "unknown"].copy()

    def ct(g, xcol="f"):
        g = g.dropna(subset=[xcol, "x"])
        if len(g) < 20 or g[xcol].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = np.column_stack([np.ones(len(g)), g[xcol].values])
        y = g["x"].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        meat = np.zeros((2, 2))
        G = 0
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s); G += 1
        N = len(g)
        V = XtX @ meat @ XtX * G / (G - 1) * (N - 1) / (N - 2)
        return pd.Series(dict(n=N, days=G, slope=b[1], t=b[1] / np.sqrt(V[1, 1])))

    out = {}
    out["by_horizon"] = ip.groupby("H").apply(ct)
    h5 = ip[ip.H == 5].copy()
    out["by_window_h5"] = h5.groupby("w").apply(ct)
    out["by_year_h5"] = h5.groupby("year").apply(ct)
    out["by_coin_h5"] = h5.groupby("coin").apply(ct)
    h5["trend"] = pd.cut(h5["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["by_trend_h5"] = h5.groupby("trend").apply(ct)
    out["trend_missing_share"] = float(h5["ret60"].isna().mean())
    h5["side"] = np.where(h5["f"] > 0, "long", np.where(h5["f"] < 0, "short", "zero"))
    out["side_mean_x"] = h5.groupby("side")["x"].agg(["count", "mean"])
    h5["fq"] = pd.qcut(h5["f"], 5, duplicates="drop")
    out["forecast_quintile_mean_x"] = h5.groupby("fq")["x"].agg(["count", "mean", "std"])
    out["by_side_slope_h5"] = h5[h5.side != "zero"].groupby("side").apply(ct)
    out["raw_vs_x_h5"] = ct(h5, "raw")
    for H in [10, 20]:
        g = ip[ip.H == H].copy()
        g["trend"] = pd.cut(g["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
        out[f"by_trend_h{H}"] = g.groupby("trend").apply(ct)
    return out
