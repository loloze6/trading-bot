def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            rng = b.high - b.low
            b["width"] = rng / rng.rolling(20, min_periods=20).mean()
            b["loc"] = (b.close - b.low) / rng.replace(0, np.nan)
            b["r1"] = b.close.pct_change()
            b["nxt"] = b.close.shift(-1) / b.close - 1
            b["r60"] = b.close / b.close.shift(60) - 1
            b["r5"] = b.close / b.close.shift(5) - 1
            b["r5p"] = b.close.shift(1) / b.close.shift(6) - 1  # 5d return before the up day
            b["r10"] = b.close / b.close.shift(10) - 1
            b["vol30"] = b.r1.rolling(30).std()
            b["vol90"] = b.r1.rolling(90, min_periods=60).std()
            b["case"] = b.forecast < 0
            b["alloc"] = b.postRebalance_current_allocation
            b["pnl"] = b.alloc * b.nxt
            b["coin"] = c; b["win"] = w; b["wn"] = int(w[1:])
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin").r1.mean()
    B["ex"] = -(B.nxt - B.coin.map(drift))
    B["tot"] = -B.nxt
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "ex_mean": g.ex.mean(), "tot_mean": g.tot.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "hit": (g.tot > 0).mean(), "pnl_sum": g.pnl.sum()})
    out = {}
    V = B[B.nxt.notna()]
    fall = V[V.r60 < -0.10].copy()
    fall["sig"] = (fall.r1 > 0) & (fall.width > 1) & (fall["loc"] >= .75)
    fall["r5neg"] = fall.r5 < 0
    out["falling: signal x 5d<0 (condition alone check)"] = fall.groupby(["sig", "r5neg"]).apply(summ)
    fall["r5pneg"] = fall.r5p < 0
    out["falling up days: signal x prior-5d<0"] = fall[fall.r1 > 0].groupby(["sig", "r5pneg"]).apply(summ)
    fall["agit"] = fall.vol30 > fall.vol90
    out["falling: signal x agitated"] = fall.groupby(["sig", "agit"]).apply(summ)
    cs = V[V.case].copy()
    cs["r5q"] = pd.qcut(cs.r5, 5, labels=False, duplicates="drop")
    out["cases by 5d return quintile"] = cs.groupby("r5q").apply(summ)
    cs["r5neg"] = cs.r5 < 0
    cs["wq"] = pd.qcut(cs.width, 3, labels=False, duplicates="drop")
    out["cases r5neg x width tercile"] = cs.groupby(["r5neg", "wq"]).apply(summ)
    out["cases r5neg by year"] = cs.assign(year=pd.to_datetime(cs.timestamp).dt.year).groupby(["year", "r5neg"]).apply(summ)
    # book restricted: keep pnl only on r5<0 case days (before fees, approx fee 0.22% * |alloc| *2 legs?)
    B["keep"] = B.case & (B.r5 < 0)
    B["pnl_k"] = np.where(B.keep, B.pnl - 0.0022 * B.alloc.abs(), 0.0)
    B["pnl_a"] = np.where(B.case, B.pnl - 0.0022 * B.alloc.abs(), 0.0)
    B["day"] = pd.to_datetime(B.timestamp).dt.floor("D")
    ncoin = B.groupby(["wn", "day"]).coin.transform("count")
    agg = B.groupby(["wn", "day"]).agg(a=("pnl_a", "mean"), k=("pnl_k", "mean")).reset_index().sort_values(["wn", "day"])
    res = {}
    for col in ["a", "k"]:
        r = agg[col]; v = (1 + r).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(r) / 365; yr = v.iloc[-1] ** (1 / yrs) - 1
        res[col] = {"mean": r.mean(), "sharpe": r.mean() / r.std() * np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr / -dd}
    out["approx book all cases vs r5<0 only"] = pd.DataFrame(res).T
    # worst case-days: r5 sign
    worst = V[V.case].nsmallest(15, "tot")
    out["15 worst cases: r5<0 share, mean r5, mean width"] = pd.Series({"r5neg_share": (worst.r5 < 0).mean(), "mean_r5": worst.r5.mean(), "mean_width": worst.width.mean(), "agit_share": (worst.vol30 > worst.vol90).mean()})
    w13 = V[V.case & (V.wn == 13)]
    out["w13 cases"] = summ(w13).append(pd.Series({"r5neg_share": (w13.r5 < 0).mean()})) if hasattr(pd.Series, "append") else pd.concat([summ(w13), pd.Series({"r5neg_share": (w13.r5 < 0).mean()})])
    return out
