def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float)
            n = len(b)
            if n < 30: continue
            ts = pd.to_datetime(b["timestamp"])
            hh20 = c.rolling(20).max().shift(1)
            hh20h = hi.rolling(20).max().shift(1)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            brk_size = c / hh20 - 1
            dist20 = c / hh20 - 1
            exc = b.get("debug_info.components.fail_exc.last_history_value")
            exc = exc.astype(float) if exc is not None else pd.Series(np.nan, index=b.index)
            for H in (3, 5, 10):
                fwd = c.shift(-H) / c - 1
                df = pd.DataFrame({"coin": coin, "w": w, "H": H, "fwd": fwd, "dist20": dist20,
                                   "brk_z": brk_size / vol20, "exc": exc, "yr": ts.dt.year,
                                   "pos": np.arange(n)})
                recs.append(df[(df.pos % H == 0) & df.fwd.notna()])
    G = pd.concat(recs)
    G["drift"] = G.groupby(["coin", "H"]).fwd.transform("mean")
    G["sd"] = G.groupby(["coin", "H"]).fwd.transform("std")
    G["u"] = G.fwd - G.drift
    G["z"] = G.u / G.sd
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x)))
    # breakout vs not at each horizon
    G["brk"] = (G.dist20 > 0).astype(int)
    out["brk_by_H"] = G.dropna(subset=["dist20"]).groupby(["H", "brk"]).agg(mean_u=("u", "mean"), mean_z=("z", "mean"), n=("u", "size"), t=("u", tt))
    # graded: distance to prior 20-day high, all bars, deciles within coin, H=5
    g5 = G[(G.H == 5)].dropna(subset=["dist20", "brk_z"]).copy()
    g5["q"] = g5.groupby("coin").dist20.transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    out["dist20_dec_H5"] = g5.groupby("q").agg(mean_u=("u", "mean"), n=("u", "size"), t=("u", tt), feat=("dist20", "mean"))
    # among breakouts, size graded
    bb = g5[g5.dist20 > 0].copy()
    s = stats.linregress(bb.brk_z, bb.z)
    out["brk_size_slope_H5"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(bb)})
    bb["q"] = pd.qcut(bb.brk_z.rank(method="first"), 3, labels=False)
    out["brk_size_terc_H5"] = bb.groupby("q").agg(mean_u=("u", "mean"), n=("u", "size"), t=("u", tt), bz=("brk_z", "mean"))
    out["brk_by_coin_H5"] = bb.groupby("coin").agg(mean_u=("u", "mean"), n=("u", "size"), t=("u", tt))
    out["brk_by_year_H5"] = bb.groupby("yr").agg(mean_u=("u", "mean"), n=("u", "size"), t=("u", tt))
    # failed-breakout excursion slope at H=5 and 10
    for H in (5, 10):
        e = G[(G.H == H) & (G.exc > 0)]
        if len(e) > 20:
            s = stats.linregress(e.exc, e.z)
            out[f"exc_slope_H{H}"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(e), "mean_u": e.u.mean(), "t_mean": tt(e.u)})
    return out
