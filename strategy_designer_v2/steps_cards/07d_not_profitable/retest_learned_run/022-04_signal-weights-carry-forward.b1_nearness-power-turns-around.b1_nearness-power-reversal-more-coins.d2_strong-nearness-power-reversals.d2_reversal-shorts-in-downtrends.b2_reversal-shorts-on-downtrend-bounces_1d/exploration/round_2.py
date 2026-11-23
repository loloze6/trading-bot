def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd1"] = c.shift(-1)/c - 1
            b["fwd5"] = c.shift(-5)/c - 1
            b["fwd10"] = c.shift(-10)/c - 1
            b["r20"] = c/c.shift(20) - 1
            b["r5"] = c/c.shift(5) - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["pos"]*b["fwd1"]
            # days since position opened
            held = (b["pos"] != 0).astype(int)
            start = (held.diff().fillna(held) == 1).cumsum()
            b["age"] = held.groupby(start).cumsum().where(held == 1, 0)
            b["fc_now"] = b["forecast"]
            b["vchg"] = b["postRebalance_total_value"]/b["total_portfolio_value"] - 1
            b["turn"] = (b["pos"] - b["previous_allocation"].fillna(0)).abs()
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % 5 == 0)
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    H = B[B["pos"] != 0].copy()
    H["ageb"] = pd.cut(H["age"], [0,5,10,20,1000], labels=["1-5","6-10","11-20","21+"])
    H["fczero"] = H["forecast"] == 0
    out["held by age"] = H.groupby("ageb").agg(n=("gain","size"), gain=("gain","mean"), sumgain=("gain","sum"),
        short1=("fwd1", lambda x: -x.mean()), abspos=("pos", lambda x: x.abs().mean()), share_fc0=("fczero","mean"))
    out["held by forecast zero"] = H.groupby("fczero").agg(n=("gain","size"), gain=("gain","mean"), sumgain=("gain","sum"),
        short1=("fwd1", lambda x: -x.mean()))
    out["costs"] = pd.Series({"sum gain before fees (alloc units)": B["gain"].sum(),
        "sum fee drag": B["vchg"].sum(), "sum turnover": B["turn"].sum(),
        "rebalances": (B["turn"] > 1e-9).sum(), "mean pos-target gap": (B["pos"]-B["forecast"]/10).abs()[B["pos"]!=0].mean()})
    G = B[B["grid"] & B["fwd5"].notna()].copy()
    G["gate"] = (G["r20"] < 0) & (G["r5"] > 0)
    G["sig"] = G["forecast"] < 0
    gg = G[G["gate"]].copy()
    gg["r5q"] = pd.qcut(gg["r5"], 3, labels=["small","mid","big"])
    out["gate: r5 bounce x signal, short5"] = gg.groupby(["r5q","sig"]).agg(n=("fwd5","size"), short5=("fwd5", lambda x: -x.mean()), short10=("fwd10", lambda x: -x.mean()))
    s = G[G["sig"]]
    out["signal horizons short"] = pd.Series({"short5": -s["fwd5"].mean(), "short10": -s["fwd10"].mean(),
        "t5": stats.ttest_1samp(-s["fwd5"].dropna(),0).statistic, "t10": stats.ttest_1samp(-s["fwd10"].dropna(),0).statistic, "n": len(s)})
    # forecast strength x pos: gain per unit
    s2 = s.copy()
    s2["fq"] = pd.qcut(s2["forecast"].abs().rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["signal by fq: short5 and t"] = s2.groupby("fq").agg(n=("fwd5","size"), short5=("fwd5", lambda x: -x.mean()),
        t=("fwd5", lambda x: -x.mean()/(x.std()/np.sqrt(len(x)))), short10=("fwd10", lambda x: -x.mean()))
    # trades: entry regime / age
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if t is not None and len(t)])
    T["dur"] = T["duration_minutes"]/1440
    T["db"] = pd.cut(T["dur"], [0,5.5,10,20,1000], labels=["<=5","6-10","11-20","21+"])
    out["trades by duration"] = T.groupby("db").agg(n=("dur","size"), net=("net_profit_loss_percent","mean"), pl=("profit_loss_percent","mean"))
    return out
