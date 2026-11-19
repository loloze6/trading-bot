def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; hz = []; bins = []; ac = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r1 = b.close.shift(-1) / b.close - 1
            pos = b.postRebalance_current_allocation
            gross = pos * r1
            ts = pd.to_datetime(b.timestamp)
            day = ts.dt.floor("D")
            fee = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            turn = (b.postRebalance_current_allocation - b.previous_allocation).abs()
            g = pd.DataFrame({"day": day, "gross": gross, "fee": fee, "turn": turn, "abspos": pos.abs()}).groupby("day").agg(
                {"gross": "sum", "fee": "sum", "turn": "sum", "abspos": "mean"})
            d = data["days"][c][w]
            g["net"] = d.set_index(pd.to_datetime(d.day).dt.floor("D")).book_return.reindex(g.index).values
            g["coin"] = c
            rows.append(g)
            f = b.forecast
            for h in [1, 6, 24, 72]:
                idx = np.arange(0, len(b) - h, h)
                fr = (b.close.shift(-h) / b.close - 1).iloc[idx]
                hz.append(pd.DataFrame({"h": h, "f": f.iloc[idx].values, "r": fr.values, "c": c}))
            bins.append(pd.DataFrame({"f": f, "g": gross}))
            ac.append([f.autocorr(1), f.autocorr(6), f.autocorr(24)])
    D = pd.concat(rows)
    out = {}
    out["daily means gross fee net turn abspos"] = D[["gross", "fee", "net", "turn", "abspos"]].mean()
    out["per coin daily"] = D.groupby("coin")[["gross", "fee", "net", "turn"]].mean()
    H = pd.concat(hz).dropna()
    res = []
    for h, gp in H.groupby("h"):
        gp = gp.copy()
        gp["r"] = gp.r - gp.groupby("c").r.transform("mean")
        s = stats.linregress(gp.f, gp.r)
        res.append({"h": h, "n": len(gp), "slope": s.slope, "t": s.slope / s.stderr, "slope_per_hour": s.slope / h})
    out["slope by horizon (hours)"] = pd.DataFrame(res)
    B = pd.concat(bins).dropna()
    B["q"] = pd.qcut(B.f, 10, labels=False, duplicates="drop")
    out["gross per bar by forecast decile"] = B.groupby("q").agg(fmean=("f", "mean"), g=("g", "mean"), n=("g", "size"))
    out["forecast autocorr lag1,6,24"] = pd.Series(np.nanmean(ac, axis=0), index=["lag1", "lag6", "lag24"])
    return out
