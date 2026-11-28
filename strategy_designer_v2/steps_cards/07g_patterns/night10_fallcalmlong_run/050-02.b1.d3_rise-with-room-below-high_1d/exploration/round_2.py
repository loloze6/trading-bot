def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "inprof": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "s7": c.pct_change(7) / (vol20 * np.sqrt(7)),
                "s3": c.pct_change(3) / (vol20 * np.sqrt(3)),
                "s14": c.pct_change(14) / (vol20 * np.sqrt(14)),
                "rng": (b["high"] - b["low"]) / c / vol20,
                "vrel": b["volume"] / b["volume"].rolling(20).mean(),
                "pnl": b["postRebalance_total_value"].pct_change(),
                "cr": r1,
            })
            for h in (3, 7, 14):
                f[f"fwd{h}"] = c.shift(-h) / c - 1
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    def clus_t(d, ycol):
        g = d.groupby("day")[ycol].sum()
        n = len(g)
        m = d[ycol].mean()
        dev = d.groupby("day")[ycol].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum()) / len(d)
        return m / se if se > 0 else np.nan, n
    res = []
    for h, col in [(3, "s3"), (7, "s7"), (14, "s14"), (7, "s14"), (14, "s7"), (3, "rng"), (3, "vrel")]:
        for off in range(min(h, 3)):
            grid = ((df.pos - off) % h == 0) & (df.pos >= off)
            mh = df.loc[(df.pos % h == 0), f"fwd{h}"].mean()
            P = df[grid & (df.inprof == 1)].dropna(subset=[f"fwd{h}", col]).copy()
            P["u"] = P[f"fwd{h}"] - mh
            rho = stats.spearmanr(P[col], P["u"])
            top = P[P[col] >= P[col].quantile(0.8)]
            t, nd = clus_t(top, "u")
            res.append({"h": h, "x": col, "off": off, "n": len(P), "rho": rho.correlation,
                        "p": rho.pvalue, "top20 u": top.u.mean(), "top20 t": t, "top days": nd})
    out["grading robustness over grid offsets"] = pd.DataFrame(res)
    # positive scaled 7d rise in profile, by coin, at 7d
    m7 = df.loc[df.pos % 7 == 0, "fwd7"].mean()
    P = df[(df.pos % 7 == 0) & (df.inprof == 1)].dropna(subset=["fwd7", "s7"]).copy()
    P["u"] = P.fwd7 - m7
    out["s7>0 vs s7<=0, 7d u"] = P.groupby(P.s7 > 0)["u"].agg(["count", "mean", "std"])
    out["s7 top half by coin"] = P[P.s7 > P.s7.median()].groupby("coin")["u"].agg(["count", "mean"])
    # book: largest days
    D = df.dropna(subset=["pnl"])
    D = D[D.alloc.shift(1).fillna(0) != 0] if False else D
    big = D[D.pnl.abs() > 0]
    q = big.pnl.quantile([0.05, 0.95])
    out["book days: worst5% / best5% count, mean cr, mean s7"] = pd.DataFrame({
        "worst": [ (big.pnl <= q[0.05]).sum(), big[big.pnl <= q[0.05]].cr.mean(), big[big.pnl <= q[0.05]].s7.mean()],
        "best": [ (big.pnl >= q[0.95]).sum(), big[big.pnl >= q[0.95]].cr.mean(), big[big.pnl >= q[0.95]].s7.mean()]},
        index=["n", "coin ret", "s7"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr, ignore_index=True)
    T["fb"] = pd.qcut(T.entry_forecast, 3, labels=False, duplicates="drop")
    out["trades by entry forecast tercile"] = T.groupby("fb")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
