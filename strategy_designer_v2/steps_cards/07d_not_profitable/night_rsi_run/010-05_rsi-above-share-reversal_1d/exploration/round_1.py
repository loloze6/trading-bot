def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # pooled daily book, market part, timing
    rows = []
    for coin in data["bars"]:
        allmean = []
        for w, b in data["bars"][coin].items():
            r = b["close"].pct_change().shift(-1)
            allmean.append(r.dropna())
        mu = pd.concat(allmean).mean()
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["fwd1"] = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"]
            b["gain"] = pos*b["fwd1"]
            b["mkt"] = pos*mu
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            c = b["close"]
            b["ret30"] = c/c.shift(30)-1
            b["ret90"] = c/c.shift(90)-1
            b["fwd14"] = c.shift(-14)/c-1
            b["pos14"] = np.arange(len(b)) % 14 == 0
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B = B.dropna(subset=["fwd1"])
    out["coin_summary"] = B.groupby("coin").agg(gain=("gain","mean"), mkt=("mkt","mean"),
        meanpos=("postRebalance_current_allocation","mean"),
        shortshare=("postRebalance_current_allocation", lambda x:(x<0).mean()),
        n=("gain","size"))
    B["side"] = np.sign(B["postRebalance_current_allocation"])
    out["by_side"] = B.groupby("side").agg(gain=("gain","mean"), fwd1=("fwd1","mean"), n=("gain","size"))
    out["by_year"] = B.groupby("year").agg(gain=("gain","mean"), fwd1=("fwd1","mean"),
        meanpos=("postRebalance_current_allocation","mean"), n=("gain","size"))
    # by prior 90d trend tercile
    B["t90"] = pd.qcut(B["ret90"], 3, labels=["down","mid","up"])
    out["by_trend90"] = B.groupby("t90").agg(gain=("gain","mean"), fwd1=("fwd1","mean"),
        meanpos=("postRebalance_current_allocation","mean"), n=("gain","size"))
    # forecast quintile vs fwd14 on grid
    G = B[B["pos14"]].dropna(subset=["fwd14","forecast"])
    G["fq"] = pd.qcut(G["forecast"].rank(method="first"), 5, labels=False)
    out["fq_fwd14"] = G.groupby("fq").agg(fc=("forecast","mean"), fwd14=("fwd14","mean"), n=("fwd14","size"))
    # raw share vs fwd14 within trend tercile
    G["raw"] = G["debug_info.components.rsi_share.last_history_value"]
    res = {}
    for t, g in G.groupby("t90"):
        g = g.dropna(subset=["raw"])
        if len(g) > 10:
            s = stats.linregress(g["raw"], g["fwd14"])
            res[str(t)] = [s.slope, s.slope/s.stderr, len(g)]
    out["raw_slope_by_trend90"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # trades vs fees
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = T.groupby("side").agg(pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        n=("side","size"), dur_d=("duration_minutes", lambda x: x.mean()/1440))
    # daily book: worst/fees
    B["fee_drag"] = (B["total_portfolio_value"]-B["postRebalance_total_value"])/B["total_portfolio_value"]
    out["fee_mean_daily"] = float(B["fee_drag"].mean())
    return out
