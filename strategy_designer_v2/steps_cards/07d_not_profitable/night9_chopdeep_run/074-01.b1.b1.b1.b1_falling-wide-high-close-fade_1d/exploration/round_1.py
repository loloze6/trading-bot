def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
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
            b["vol30"] = b.r1.rolling(30).std()
            b["vol90"] = b.r1.rolling(90, min_periods=60).std()
            b["case"] = b.forecast < 0
            b["alloc"] = b.postRebalance_current_allocation
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b.timestamp).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin").r1.mean()
    B["ex"] = -(B.nxt - B.coin.map(drift))  # short-direction excess
    B["tot"] = -B.nxt
    cs = B[B.case & B.nxt.notna()].copy()
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "ex_mean": g.ex.mean(), "tot_mean": g.tot.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "hit": (g.tot > 0).mean(), "abs_alloc": g.alloc.abs().mean()})
    out["all cases"] = summ(cs)
    cs["wq"] = pd.qcut(cs.width, 4, labels=False, duplicates="drop")
    out["by width quartile"] = cs.groupby("wq").apply(summ)
    cs["r1q"] = pd.qcut(cs.r1, 4, labels=False, duplicates="drop")
    out["by day return quartile"] = cs.groupby("r1q").apply(summ)
    cs["r60q"] = pd.qcut(cs.r60, 3, labels=False, duplicates="drop")
    out["by 60d return tercile"] = cs.groupby("r60q").apply(summ)
    cs["agit"] = (cs.vol30 > cs.vol90)
    out["by vol30>vol90"] = cs.groupby("agit").apply(summ)
    cs["r5neg"] = cs.r5 < 0
    out["by 5d return<0"] = cs.groupby("r5neg").apply(summ)
    out["by year"] = cs.groupby("year").apply(summ)
    out["by coin"] = cs.groupby("coin").apply(summ)
    # tail: worst cases share of losses
    out["tot quantiles"] = cs.tot.quantile([.02, .05, .1, .25, .5, .75, .9, .95, .98])
    # book daily chain
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["wn"] = D.win.str[1:].astype(int)
    agg = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    agg = agg.dropna()
    v = (1 + agg.br).cumprod(); dd = v / v.cummax() - 1
    out["book chain"] = pd.Series({"days": len(agg), "mean": agg.br.mean(), "std": agg.br.std(),
                                   "sharpe": agg.br.mean() / agg.br.std() * np.sqrt(365),
                                   "hold_sharpe": agg.cr.mean() / agg.cr.std() * np.sqrt(365),
                                   "maxdd": dd.min(), "final": v.iloc[-1]})
    i = dd.values.argmin(); pk = v.values[:i + 1].argmax()
    seg = agg.iloc[pk:i + 1]
    out["deepest fall"] = pd.Series({"length_days": len(seg), "windows": str(sorted(seg.wn.unique())),
                                     "coin_ret_sum": seg.cr.sum(), "worst_book_day": seg.br.min(),
                                     "n_neg_days": (seg.br < 0).sum()})
    out["worst 10 book days"] = agg.nsmallest(10, "br")[["wn", "br", "cr"]].reset_index(drop=True)
    # condition-alone: falling market up days not cases
    fall = B[(B.r60 < -0.10) & B.nxt.notna()]
    out["falling, up days, wide&highclose (recomputed) vs other"] = fall.assign(
        sig=(fall.r1 > 0) & (fall.width > 1) & (fall["loc"] >= .75)).groupby("sig").apply(summ)
    return out
