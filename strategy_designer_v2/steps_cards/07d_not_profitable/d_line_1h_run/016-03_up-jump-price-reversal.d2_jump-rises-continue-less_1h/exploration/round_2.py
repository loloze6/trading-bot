def explore(data):
    import numpy as np, pandas as pd
    out = {}
    allb = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd72"] = b["close"].shift(-72) / b["close"] - 1
            b["past72"] = b["close"] / b["close"].shift(72) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["turn"] = (b["pos"] - b["previous_allocation"]).abs()
            b["raw"] = b["debug_info.components.grind.last_history_value"]
            b["raw_sm24"] = b["raw"].rolling(24, min_periods=24).mean()
            b["coin"] = coin; b["win"] = w
            b["idx"] = np.arange(len(b))
            allb.append(b[["coin","win","idx","ret1","fwd72","past72","pos","gross","fee","turn","raw","raw_sm24"]])
    A = pd.concat(allb, ignore_index=True)
    # totals per day across all coins
    out["totals_bp_per_day"] = pd.Series({
        "gross": A["gross"].mean()*24e4, "fee": A["fee"].mean()*24e4,
        "mkt_part": A["pos"].mean()*A["ret1"].mean()*24e4,
        "timing": (A["gross"].mean()-A["pos"].mean()*A["ret1"].mean())*24e4,
        "turn_per_day": A["turn"].mean()*24,
        "fee_per_unit_turn_bp": A["fee"].sum()/A["turn"].sum()*1e4})
    # trades
    T = pd.concat([t for c in data["trades"] for t in data["trades"][c].values()], ignore_index=True)
    T["hrs"] = T["duration_minutes"]/60
    T["dq"] = pd.cut(T["hrs"], [0,2,6,24,72,1e6])
    out["trades_by_dur"] = T.groupby("dq").agg(n=("hrs","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"), comm=("total_commission","mean"))
    # how often raw flips between 0 and positive
    A["on"] = (A["raw"] > 0).astype(int)
    flips = A.groupby(["coin","win"])["on"].apply(lambda s: s.diff().abs().sum()).sum()
    out["raw_on_off_flips_per_day"] = float(flips / len(A) * 24)
    # does raw add beyond past72 size? grid risen
    G = A[(A["idx"] % 72 == 0) & (A["past72"] > 0) & A["fwd72"].notna()].copy()
    G["pq"] = pd.qcut(G["past72"], 3, labels=["small","mid","big"])
    G["rhi"] = G.groupby("pq")["raw"].transform(lambda s: s > s.median())
    out["fwd72_by_size_and_raw"] = G.groupby(["pq","rhi"]).agg(n=("fwd72","size"), fwd=("fwd72","mean"), raw=("raw","mean"))
    # smoothed raw on all grid bars: graded?
    H = A[(A["idx"] % 72 == 0) & A["fwd72"].notna() & A["raw_sm24"].notna()].copy()
    H["sq"] = pd.qcut(H["raw_sm24"].rank(method="first"), 5, labels=False)
    out["fwd72_by_raw_sm24"] = H.groupby("sq").agg(n=("fwd72","size"), fwd=("fwd72","mean"), sm=("raw_sm24","mean"))
    # hourly gross when on vs fees
    A["state"] = np.where(A["pos"]>1e-6, "in", "out")
    out["by_state"] = A.groupby("state").agg(n=("ret1","size"), gross_bp=("gross", lambda s: s.mean()*1e4),
        fee_bp=("fee", lambda s: s.mean()*1e4), coin_bp=("ret1", lambda s: s.mean()*1e4), pos=("pos","mean"))
    return out
