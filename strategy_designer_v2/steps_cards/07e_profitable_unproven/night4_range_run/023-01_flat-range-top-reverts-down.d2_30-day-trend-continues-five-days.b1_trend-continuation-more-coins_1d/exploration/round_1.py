def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # per-bar gains
    rows = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            r = b["close"].shift(-1) / b["close"] - 1
            allr.append(r.dropna())
        mu = pd.concat(allr).mean()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            b["rn"] = b["close"].shift(-1) / b["close"] - 1
            b["al"] = b["postRebalance_current_allocation"]
            b["gain"] = b["al"] * b["rn"]
            b["drift"] = b["al"] * mu
            b["timing"] = b["gain"] - b["drift"]
            b["coin"] = c; b["window"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["side"] = np.where(b["al"] > 0, "long", np.where(b["al"] < 0, "short", "flat"))
            ret30 = b["close"] / b["close"].shift(30) - 1
            b["ret30"] = ret30
            rows.append(b[["coin","window","year","side","al","rn","gain","drift","timing","forecast","regime","ret30","close"]])
    B = pd.concat(rows).dropna(subset=["rn","al"])
    tot = B[["gain","drift","timing"]].sum()
    out["share gain drift vs timing (sum of bar gains)"] = (tot / tot["gain"]).round(3)
    out["by side"] = B.groupby("side")[["gain","drift","timing"]].agg(["sum","count"]).round(3)
    out["by coin"] = B.groupby("coin")[["gain","timing"]].sum().round(3).sort_values("gain")
    out["by year"] = B.groupby("year")[["gain","drift","timing"]].sum().round(3)
    out["by window"] = B.groupby("window")[["gain","timing"]].sum().round(3).sort_values("gain")
    # book daily returns
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["window","day"])[["book_return","coin_return"]].mean().dropna()
    s = bk["book_return"]
    out["book daily mean/sharpe/n"] = pd.Series({"mean": s.mean(), "sharpe": s.mean()/s.std()*np.sqrt(365), "n": len(s),
        "top10days_share_of_sum": s.nlargest(10).sum()/s.sum(), "top1pct_share": s.nlargest(int(len(s)*0.01)).sum()/s.sum()})
    # book by market state: coin-average daily return sign/quintile
    q = pd.qcut(bk["coin_return"], 5, labels=False)
    out["book mean by market-day quintile"] = bk.groupby(q)["book_return"].agg(["mean","count"])
    # horizons: unusual move in forecast direction, regime bars with forecast nonzero, plus out-of-regime ret30 sign
    res = []
    for h in [1,3,5,10,20]:
        cases = []
        for c in bars:
            fr = []
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                fr.append((b["close"].shift(-h)/b["close"]-1).iloc[::h].dropna())
            mu = pd.concat(fr).mean(); sd = pd.concat(fr).std()
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                f = b["close"].shift(-h)/b["close"]-1
                r30 = b["close"]/b["close"].shift(30)-1
                g = pd.DataFrame({"f": f, "fc": b["forecast"], "r30": r30, "reg": b["regime"]}).iloc[::h].dropna()
                g["u"] = (g["f"]-mu); g["sd"] = sd
                cases.append(g)
        G = pd.concat(cases)
        for name, m in [("in-regime fc!=0", G["fc"]!=0), ("out-regime", G["reg"]!="trending")]:
            gg = G[m]
            sg = np.sign(gg["fc"]) if name.startswith("in") else np.sign(gg["r30"])
            dm = gg["u"]*sg
            for side in [1,-1]:
                x = dm[sg==side]
                res.append({"h":h,"set":name,"side":"long" if side>0 else "short","n":len(x),
                            "mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                            "strength":(x/gg["sd"][sg==side]).mean()})
    out["horizons"] = pd.DataFrame(res).round(4)
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    p = T["net_profit_loss_percent"]
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10 share": p.nlargest(10).sum()/p.sum(),
                               "win rate": (p>0).mean(), "long sum": p[T.side=="LONG"].sum(), "short sum": p[T.side=="SHORT"].sum()})
    return out
