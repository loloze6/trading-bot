def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # per-bar decomposition: gain = alloc * next-bar return; market part = alloc * coin mean hourly return
    recs = []
    for c, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            cl = b["close"].values
            rets.append(cl[1:] / cl[:-1] - 1)
        mu = np.concatenate(rets).mean()
        for w, b in ws.items():
            cl = b["close"].values
            al = b["postRebalance_current_allocation"].fillna(0).values
            fc = b["forecast"].fillna(0).values
            n = len(cl)
            if n < 800: continue
            r1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            p720 = np.full(n, np.nan); p720[720:] = cl[720:] / cl[:-720] - 1
            p168 = np.full(n, np.nan); p168[168:] = cl[168:] / cl[:-168] - 1
            tv = b["total_portfolio_value"].values; pv = b["postRebalance_total_value"].values
            fee = np.r_[(tv - pv) / tv]
            recs.append(pd.DataFrame({"coin": c, "al": al, "fc": fc, "r1": r1, "mu": mu,
                                      "p720": p720, "p168": p168, "fee": fee}))
    B = pd.concat(recs).dropna(subset=["r1"])
    B["gain"] = B.al * B.r1
    B["mkt"] = B.al * B.mu
    B["timing"] = B.gain - B.mkt
    out["decomp_per_bar_x1e4"] = (B[["gain", "mkt", "timing", "fee"]].mean() * 1e4)
    # forecast-level bars
    B["fcb"] = pd.cut(B.fc, [-0.01, 0.0, 0.5, 2, 8, 20.01], labels=["0", "0-0.5", "0.5-2", "2-8", "8-20"])
    g = B.groupby("fcb")
    out["by_forecast_level"] = pd.DataFrame({"share_bars": g.size() / len(B), "alloc": g.al.mean(),
                                            "gain_sum_share": g.gain.sum() / B.gain.sum(),
                                            "timing_x1e4": g.timing.mean() * 1e4,
                                            "fee_sum_share": g.fee.sum() / B.fee.sum()})
    # 30-day trend state
    Bq = B.dropna(subset=["p720"]).copy()
    Bq["s30"] = pd.qcut(Bq.p720.rank(method="first"), 5, labels=False)
    g = Bq.groupby("s30")
    out["by_30d_state"] = pd.DataFrame({"alloc": g.al.mean(), "gain_x1e4": g.gain.mean() * 1e4,
                                       "timing_x1e4": g.timing.mean() * 1e4, "coin_r1_x1e4": g.r1.mean() * 1e4,
                                       "fee_x1e4": g.fee.mean() * 1e4, "p720_med": g.p720.median()})
    # graded: in falling 30d state, do larger forecasts still rebound? next-48h on grid
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; fc = b["forecast"].fillna(0).values; n = len(cl)
            for k in range(720, n - 48, 48):
                cases.append((cl[k] / cl[k - 720] - 1, cl[k] / cl[k - 168] - 1, fc[k], cl[k + 48] / cl[k] - 1))
    C = pd.DataFrame(cases, columns=["p720", "p168", "fc", "r48"])
    C["s30"] = np.where(C.p720 > 0, "up30", "down30")
    C["fcb"] = pd.cut(C.fc, [-0.01, 0.0, 2, 20.01], labels=["0", "0-2", "2-20"])
    def summ(x):
        return pd.Series({"n": len(x), "r48": x.r48.mean(), "t": x.r48.mean() / x.r48.std() * np.sqrt(len(x))})
    out["grid_48h_by_30d_and_fc"] = C.groupby(["s30", "fcb"]).apply(summ)
    return out
