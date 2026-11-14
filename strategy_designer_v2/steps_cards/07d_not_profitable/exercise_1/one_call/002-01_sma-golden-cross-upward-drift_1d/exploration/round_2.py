def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]; r = cl.pct_change()
            b["r1n"] = r.shift(-1)
            b["f10"] = cl.shift(-10) / cl - 1
            b["mom20"] = cl / cl.shift(20) - 1
            b["mom60"] = cl / cl.shift(60) - 1
            b["above50"] = cl > cl.rolling(50).mean()
            b["hi60"] = cl / cl.rolling(60).max() - 1
            b["bookr"] = b["postRebalance_total_value"].pct_change().shift(-1)
            b["coin"] = c; b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fd"] = np.sign(b["forecast"].diff().round(3))
            rows.append(b[["coin", "year", "forecast", "r1n", "f10", "mom20", "mom60", "above50", "hi60", "bookr", "fd"]])
    B = pd.concat(rows, ignore_index=True)
    act = B[B.forecast > 0].dropna(subset=["mom20", "mom60", "r1n"]).copy()
    act["aligned"] = (act.mom20 > 0) & (act.mom60 > 0)
    def tstat(x):
        x = x.dropna(); return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    out["aligned_by_coin"] = act.groupby(["coin", "aligned"]).agg(n=("r1n", "size"), r1n=("r1n", "mean"), bookr=("bookr", "mean")).unstack()
    act["era"] = np.where(act.year <= 2021, "2018-21", "2022-25")
    out["aligned_by_era"] = act.groupby(["era", "aligned"]).agg(n=("r1n", "size"), r1n=("r1n", "mean"), t=("r1n", tstat), f10=("f10", "mean"))
    out["active_by_above50"] = act.groupby("above50").agg(n=("r1n", "size"), r1n=("r1n", "mean"), t=("r1n", tstat), bookr=("bookr", "mean"))
    act["hiq"] = pd.cut(act.hi60, [-1, -0.3, -0.15, -0.05, -0.0001, 0.01])
    out["active_by_dist_from_60d_high"] = act.groupby("hiq", observed=True).agg(n=("r1n", "size"), r1n=("r1n", "mean"), t=("r1n", tstat), f10=("f10", "mean"))
    out["active_fd_by_aligned"] = act.groupby(["aligned", "fd"]).agg(n=("r1n", "size"), r1n=("r1n", "mean"))
    out["share_active_aligned"] = act.aligned.mean()
    # inactive bars with aligned momentum (missed by forecast)
    ina = B[B.forecast == 0].dropna(subset=["mom20", "mom60", "r1n"])
    al = (ina.mom20 > 0) & (ina.mom60 > 0)
    out["inactive_aligned"] = pd.DataFrame({"n": [al.sum(), (~al).sum()], "r1n": [ina.r1n[al].mean(), ina.r1n[~al].mean()], "t": [tstat(ina.r1n[al]), tstat(ina.r1n[~al])]}, index=["aligned", "not"])
    return out
