def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns: per window, per day mean over coins
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["br"])
    B["v"] = (1 + B["br"]).cumprod()
    B["dd"] = B["v"] / B["v"].cummax() - 1
    out["book by window"] = B.groupby("w").agg(n=("br", "size"), mean_bp=("br", lambda x: x.mean()*1e4),
        tot=("br", lambda x: (1+x).prod()-1), coin_tot=("cr", lambda x: (1+x).prod()-1),
        worst_dd=("dd", "min")).sort_index()
    i = B["dd"].idxmin()
    trough = B.loc[i]
    peak_v = B.loc[:i, "v"].max()
    out["deepest dd"] = f"{trough['dd']:.4f} in {trough['w']}"
    # per-bar features and cases
    feats = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]
            b["loc"] = (c - l) / (h - l)
            b["r5"] = c / c.shift(5) - 1
            b["r1"] = c / c.shift(1) - 1
            b["rng"] = (h - l) / c
            b["rngrel"] = b["rng"] / b["rng"].rolling(20, min_periods=10).mean()
            b["r20"] = c / c.shift(20) - 1
            b["f5"] = c.shift(-5) / c - 1
            b["pos"] = b.index
            b["grid"] = b["pos"] % 5 == 0
            b["coin"] = coin; b["w"] = w
            b["dayret_next"] = c.shift(-1)/c - 1
            feats.append(b[["coin","w","pos","grid","regime","loc","r5","r1","rng","rngrel","r20","f5","forecast",
                            "postRebalance_current_allocation","dayret_next"]])
    F = pd.concat(feats)
    drift = F[F.grid].groupby("coin")["f5"].mean()
    F["u"] = -(F["f5"] - F["coin"].map(drift))  # short-direction unusual
    G = F[F.grid].dropna(subset=["f5"])
    def summ(x):
        return pd.Series({"n": len(x), "u_mean": x["u"].mean(), "tot_short": (-x["f5"]).mean(),
                          "t": x["u"].mean()/(x["u"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["grid by regime"] = G.groupby("regime").apply(summ)
    S = G[G.regime == "mean_reversion"].copy()
    out["signal by loc bin"] = S.groupby(pd.cut(S["loc"], [0.5,0.7,0.85,0.95,1.0])).apply(summ)
    out["signal by r5 bin"] = S.groupby(pd.qcut(S["r5"], 4)).apply(summ)
    out["signal by rngrel"] = S.groupby(pd.qcut(S["rngrel"], 3)).apply(summ)
    out["signal by r1"] = S.groupby(pd.qcut(S["r1"], 3)).apply(summ)
    out["signal by r20"] = S.groupby(pd.qcut(S["r20"], 3)).apply(summ)
    out["signal by window"] = S.groupby("w").apply(summ)
    out["signal by coin"] = S.groupby("coin").apply(summ)
    # in-profile no signal (unknown), split by loc
    U = G[G.regime == "unknown"]
    out["unknown by loc>0.5"] = U.groupby(U["loc"] > 0.5).apply(summ)
    out["unknown by r5<0"] = U.groupby(U["r5"] < 0).apply(summ)
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    T = pd.concat(T)
    T["days"] = T["duration_minutes"]/1440
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
        "win": (T["net_profit_loss_percent"]>0).mean(), "mean_days": T["days"].mean(),
        "comm_mean": T["total_commission"].mean()})
    out["trades by dur"] = T.groupby(pd.cut(T["days"], [0,4.5,5.5,8,15,100])).agg(n=("side","size"),
        net=("net_profit_loss_percent","mean"))
    out["trades by window"] = T.groupby("w").agg(n=("side","size"), net=("net_profit_loss_percent","mean"),
        worst=("net_profit_loss_percent","min"))
    # position-day returns: mean daily pnl when in position by window
    P = F[F["postRebalance_current_allocation"].abs()>0].copy()
    P["pnl"] = P["postRebalance_current_allocation"]*P["dayret_next"]
    out["pos bars"] = pd.Series({"n": len(P), "mean_alloc": P["postRebalance_current_allocation"].mean(),
        "mean_pnl_bp": P["pnl"].mean()*1e4})
    return out
