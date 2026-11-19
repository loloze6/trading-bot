def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # daily book & coin returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["book_return", "coin_return"]].copy(); dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    out["daily"] = pd.DataFrame({"book_mean": [D.book_return.mean()], "coin_mean": [D.coin_return.mean()],
                                 "book_t": [stats.ttest_1samp(D.book_return.dropna(), 0).statistic],
                                 "n": [D.book_return.notna().sum()]})
    # bar-level: gross gain, drift part, fees
    g = []; grid = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            r = b.close.shift(-1) / b.close - 1
            allr.append(r)
        mu_h = pd.concat(allr).mean()
        for w, b in ws.items():
            r = b.close.shift(-1) / b.close - 1
            pos = b.postRebalance_current_allocation
            fee = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            g.append(pd.DataFrame({"coin": c, "gross": pos * r, "drift": pos * mu_h, "fee": fee, "pos": pos}))
            # grid features
            cl = b.close.values; n = len(cl)
            lr = np.log(b.close).diff()
            ret72 = b.close / b.close.shift(72) - 1
            ret720 = b.close / b.close.shift(720) - 1
            vol72 = lr.rolling(72).std()
            vol720 = lr.rolling(720).std()
            fwd = b.close.shift(-72) / b.close - 1
            idx = np.arange(0, n, 72)
            sub = pd.DataFrame({"coin": c, "w": w, "f": b.forecast.values[idx], "ret72": ret72.values[idx],
                                "ret720": ret720.values[idx], "volr": (vol72 / vol720).values[idx],
                                "fwd": fwd.values[idx], "pos": pos.values[idx]})
            grid.append(sub)
    G = pd.concat(g)
    out["bar_parts_per_bar"] = pd.DataFrame({"gross": [G.gross.mean()], "drift": [G.drift.mean()],
                                             "timing": [G.gross.mean() - G.drift.mean()],
                                             "fee": [G.fee.mean()], "mean_pos": [G.pos.mean()],
                                             "share_bars_short": [(G.pos < 0).mean()]})
    out["by_coin"] = G.groupby("coin").agg(gross=("gross", "mean"), drift=("drift", "mean"), fee=("fee", "mean"))
    X = pd.concat(grid).dropna(subset=["fwd"])
    mu = X.groupby("coin").fwd.transform("mean")
    X["ex"] = X.fwd - mu
    A = X[X.f < 0].copy()
    out["active_vs_flat_excess"] = pd.DataFrame({
        "active_mean_ex": [A.ex.mean()], "active_n": [len(A)], "active_t": [stats.ttest_1samp(A.ex, 0).statistic],
        "flat_mean_ex": [X[X.f == 0].ex.mean()], "flat_n": [(X.f == 0).sum()]})
    A["fq"] = pd.qcut(A.f, 4, labels=False, duplicates="drop")
    out["by_forecast_q"] = A.groupby("fq").agg(f=("f", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    A["rq"] = pd.qcut(A.ret72, 4, labels=False)
    out["by_fall_size_q"] = A.groupby("rq").agg(ret72=("ret72", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    B = A.dropna(subset=["ret720"]).copy()
    B["tq"] = pd.qcut(B.ret720, 4, labels=False)
    out["by_30d_trend_q"] = B.groupby("tq").agg(ret720=("ret720", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                                t=("ex", lambda s: stats.ttest_1samp(s, 0).statistic))
    V = A.dropna(subset=["volr"]).copy()
    V["vq"] = pd.qcut(V.volr, 4, labels=False)
    out["by_volratio_q"] = V.groupby("vq").agg(volr=("volr", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                               t=("ex", lambda s: stats.ttest_1samp(s, 0).statistic))
    # grind within fall-size buckets, residual
    A["gq"] = A.groupby("rq").f.transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    out["grind_within_size"] = A.groupby(["rq", "gq"]).ex.agg(["mean", "size"])
    return out
