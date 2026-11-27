def explore(data):
    import numpy as np, pandas as pd
    out = {}
    feats = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]
            b["loc"] = (c - l) / (h - l)
            b["r5"] = c / c.shift(5) - 1
            b["r20"] = c / c.shift(20) - 1
            b["r60"] = c / c.shift(60) - 1
            b["rng"] = (h - l) / c
            b["rngrel"] = b["rng"] / b["rng"].rolling(20, min_periods=10).mean()
            b["f5"] = c.shift(-5) / c - 1
            b["f1"] = c.shift(-1) / c - 1
            b["f1to5"] = c.shift(-5) / c.shift(-1) - 1
            b["pos"] = b.index; b["grid"] = b["pos"] % 5 == 0
            b["n"] = len(b)
            b["coin"] = coin; b["w"] = w
            b["alloc"] = b["postRebalance_current_allocation"]
            b["prev"] = b["previous_allocation"]
            b["regnext"] = b["regime"].shift(-1)
            feats.append(b)
    F = pd.concat(feats, ignore_index=True)
    G = F[F.grid].dropna(subset=["f5"]).copy()
    drift = G.groupby("coin")["f5"].mean()
    G["u"] = -(G["f5"] - G["coin"].map(drift))
    def summ(x):
        return pd.Series({"n": len(x), "u_mean": x["u"].mean(), "tot_short": (-x["f5"]).mean(),
                          "t": x["u"].mean()/(x["u"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    sig = (G.regime == "mean_reversion")
    nos = ~sig
    # condition alone checks (no signal), all regimes
    out["nosig r5 deep (<-0.05) vs not"] = G[nos].groupby(G[nos]["r5"] < -0.05).apply(summ)
    out["nosig r20 < -0.17 vs not"] = G[nos].groupby(G[nos]["r20"] < -0.17).apply(summ)
    out["nosig rngrel>1.08 vs not"] = G[nos].groupby(G[nos]["rngrel"] > 1.08).apply(summ)
    # signal-like situation everywhere (r5<0, loc>0.5), any profile, by regime
    sit = G[(G.r5 < 0) & (G["loc"] > 0.5)]
    out["situation any profile, by regime"] = sit.groupby("regime").apply(summ)
    out["situation chop-regime by r5 deep"] = sit[sit.regime=="chop"].groupby(sit[sit.regime=="chop"]["r5"] < -0.05).apply(summ)
    S = G[sig]
    out["signal r5<-0.05 & r20<-0.17"] = S.groupby((S.r5 < -0.05)).apply(summ)
    # all signal bars (not just grid), split by r5 depth
    A = F[(F.regime=="mean_reversion")].dropna(subset=["f5"]).copy()
    A["u"] = -(A["f5"] - A["coin"].map(drift))
    out["all signal bars by r5 quartile"] = A.groupby(pd.qcut(A["r5"], 4)).apply(summ)
    out["all signal bars: first day vs rest"] = pd.Series({
        "n": len(A), "short_f1": (-A.f1).mean(), "short_f1to5": (-A.f1to5).mean(),
        "rest_if_day1_up": (-A.f1to5[A.f1 > 0]).mean(), "n_up": (A.f1 > 0).sum(),
        "rest_if_day1_down": (-A.f1to5[A.f1 <= 0]).mean()})
    # trades: why early exits
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T["duration_minutes"]/1440
    T["early"] = T["days"] < 4.5
    out["trades early by exit_forecast==0"] = T.groupby(["early", T.exit_forecast == 0]).agg(
        n=("side","size"), net=("net_profit_loss_percent","mean"))
    out["trades by entry r5 sign (forecast mag)"] = T.groupby(pd.qcut(T.entry_forecast.abs(), 3, duplicates="drop")).agg(
        n=("side","size"), net=("net_profit_loss_percent","mean"))
    # regime on exits of early trades: look up bar regime at exit
    F["ts"] = pd.to_datetime(F["timestamp"])
    key = F.set_index(["coin","w","ts"])[["regime","r60","rngrel"]]
    T["xt"] = pd.to_datetime(T["exit_time"]); T["et"] = pd.to_datetime(T["entry_time"])
    def look(r, col, tcol):
        try: return key.loc[(r.coin, r.w, r[tcol]), col]
        except Exception: return np.nan
    T["exit_reg"] = T.apply(lambda r: look(r, "regime", "xt"), axis=1)
    T["entry_r60"] = T.apply(lambda r: look(r, "r60", "et"), axis=1)
    out["trades by exit regime"] = T.groupby(["early","exit_reg"]).agg(n=("side","size"), net=("net_profit_loss_percent","mean"))
    out["trades by entry r60"] = T.groupby(pd.cut(T.entry_r60, [-1,-0.05,0,0.05,1])).agg(n=("side","size"), net=("net_profit_loss_percent","mean"), worst=("net_profit_loss_percent","min"))
    out["worst 8 trades"] = T.nsmallest(8, "net_profit_loss_percent")[["coin","w","days","entry_forecast","exit_reg","entry_r60","net_profit_loss_percent"]].reset_index(drop=True)
    # in-position days: pnl by days since entry
    P = F[F.alloc.abs() > 0].copy()
    P["pnl"] = P.alloc * P.f1
    P["entry"] = (P.prev.abs() == 0) | P.prev.isna()
    out["pos pnl by regime held"] = P.groupby("regime").agg(n=("pnl","size"), pnl_bp=("pnl", lambda x: x.mean()*1e4))
    return out
