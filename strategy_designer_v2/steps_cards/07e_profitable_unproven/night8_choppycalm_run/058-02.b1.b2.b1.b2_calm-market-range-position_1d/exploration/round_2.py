def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    def cl_t(x, y, g):
        x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
        X = np.column_stack([np.ones(len(x)), x])
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        df = pd.DataFrame({"g": g, "a": e, "bx": e * x}).groupby("g")[["a", "bx"]].sum().values
        G = len(df); N = len(x)
        V = XtX @ (df.T @ df) @ XtX * G / (G - 1) * (N - 1) / (N - 2)
        return b[1], b[1] / np.sqrt(V[1, 1]), G
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = ((b["close"] - lo) / (hi - lo) * 2 - 1).values
            tr = (b["close"] / b["close"].shift(60) - 1).values
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    recs.append((c, w, h, ts[i], b["regime"].iloc[i], b["forecast"].iloc[i], pos[i], tr[i], cl[i + h] / cl[i] - 1))
    G = pd.DataFrame(recs, columns=["coin", "window", "h", "day", "regime", "fc", "pos", "trend", "fwd"])
    G = G.join(G.groupby(["coin", "h"])["fwd"].mean().rename("drift"), on=["coin", "h"]); G["ex"] = G["fwd"] - G["drift"]
    G["trendp"] = pd.cut(G["trend"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"]).astype(str)
    G["calm"] = G["regime"] == "unknown"
    res = []
    for h in [5, 10]:
        for calm in [True, False]:
            for tp in ["all", "falling", "choppy", "rising"]:
                g = G[(G.h == h) & (G.calm == calm)]
                if tp != "all": g = g[g.trendp == tp]
                for var in ["pos", "fc"]:
                    gg = g.dropna(subset=[var, "ex"])
                    if len(gg) > 40:
                        s, t, nd = cl_t(gg[var], gg["ex"], gg["day"])
                        res.append((h, calm, tp, var, len(gg), nd, s, t))
    out["clustered_slopes"] = pd.DataFrame(res, columns=["h", "calm", "trend", "var", "n", "days", "slope", "t"])
    g = G[(G.h == 5) & G.calm].dropna(subset=["pos"]).copy()
    g["side"] = np.where(g.pos > 0, "upper", "lower")
    g["edge"] = pd.cut(g["pos"].abs(), [0, 0.5, 0.8, 1.01], labels=["mid", "near", "edge"]).astype(str)
    out["h5_calm_side_edge"] = g.groupby(["side", "edge"]).agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["h5_calm_choppy_side_edge"] = g[g.trendp == "choppy"].groupby(["side", "edge"]).agg(n=("ex", "size"), ex=("ex", "mean"))
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])], ignore_index=True)
    T = T.sort_values("net_profit_loss_percent", ascending=False)
    tot = T["net_profit_loss_percent"].sum()
    out["trades"] = pd.Series({"n": len(T), "sum_net": tot, "top10_share": T["net_profit_loss_percent"].head(10).sum() / tot,
        "top5pct_share": T["net_profit_loss_percent"].head(int(len(T) * 0.05)).sum() / tot,
        "long_sum": T.loc[T.side == "LONG", "net_profit_loss_percent"].sum(), "short_sum": T.loc[T.side == "SHORT", "net_profit_loss_percent"].sum(),
        "win_rate": (T["net_profit_loss_percent"] > 0).mean()})
    return out
