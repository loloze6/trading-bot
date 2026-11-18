def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["alloc"] = b.postRebalance_current_allocation.fillna(0)
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["r3"] = b.close.shift(-3) / b.close - 1
            b["gain"] = b.alloc * b.r1
            b["ret60"] = b.close / b.close.shift(60) - 1
            b["ret5"] = b.close / b.close.shift(5) - 1
            b["act"] = b.forecast > 0
            b["prevact"] = b.act.shift(1, fill_value=False)
            b["nact5"] = b.act.rolling(5, min_periods=1).sum().shift(1).fillna(0)
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["w"] = w; b["wn"] = int(w[1:])
            recs.append(b)
    B = pd.concat(recs, ignore_index=True)
    mu3 = B[B.pos % 3 == 0].groupby("coin").r3.mean()
    B["x3"] = B.r3 - B.coin.map(mu3)
    G = B[(B.pos % 3 == 0) & B.act].dropna(subset=["x3"]).copy()
    def tt(s): return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    G["fq"] = pd.qcut(G.forecast.rank(method="first"), 4, labels=False)
    out["x3_by_forecast_q"] = G.groupby("fq").x3.apply(tt).unstack()
    out["x3_by_prior_flush5"] = G.groupby(G.nact5.clip(upper=2)).x3.apply(tt).unstack()
    G["r60q"] = pd.qcut(G.ret60, 3, labels=False)
    out["x3_by_ret60_tercile"] = G.dropna(subset=["ret60"]).groupby("r60q").x3.apply(tt).unstack()
    G["r5q"] = pd.qcut(G.ret5, 3, labels=False)
    out["x3_by_ret5_tercile"] = G.dropna(subset=["ret5"]).groupby("r5q").x3.apply(tt).unstack()
    # held gain by consecutive flush days and ret5
    H = B[B.alloc.abs() > 1e-9].dropna(subset=["gain"]).copy()
    out["held_gain_by_prior_flush5"] = H.groupby(H.nact5.clip(upper=3)).agg(n=("gain", "size"), gain=("gain", "mean"), sd=("gain", "std"))
    H["r5q"] = pd.qcut(H.ret5, 4, labels=False)
    out["held_gain_by_ret5_q"] = H.groupby("r5q").agg(n=("gain", "size"), gain=("gain", "mean"), ret5=("ret5", "median"))
    # worst windows: what held
    out["held_by_window_worst"] = H.groupby("wn").agg(gain_sum=("gain", "sum"), n=("gain", "size"), nact5=("nact5", "mean"), ret60=("ret60", "median")).sort_values("gain_sum").head(6)
    return out
