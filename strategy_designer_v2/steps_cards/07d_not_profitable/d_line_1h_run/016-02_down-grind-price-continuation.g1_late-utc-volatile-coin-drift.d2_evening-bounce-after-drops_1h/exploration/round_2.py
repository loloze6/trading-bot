def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    cm = {}
    for coin, ws in data["bars"].items():
        # coin mean h-bar return on non-overlapping grid, pooled over windows
        for h in [1, 2, 6, 12, 24]:
            vals = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            cm[(coin, h)] = np.concatenate(vals).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r24 = c / c.shift(24) - 1
            sd = (c / c.shift(1) - 1).rolling(168).std() * np.sqrt(24)
            z = r24 / sd
            d = pd.DataFrame({"hr": ts.dt.hour, "fc": b["forecast"], "z": z})
            for h in [1, 2, 6, 12, 24]:
                d[f"x{h}"] = c.shift(-h) / c - 1 - cm[(coin, h)]
            d["coin"] = coin
            recs.append(d[d["hr"] == 20])
    D = pd.concat(recs)
    D = D[D["fc"].notna()]
    pos = D[D["fc"] > 0].copy()
    pos["q"] = pd.qcut(pos["fc"].rank(method="first"), 5, labels=False)
    agg = {}
    for h in [1, 2, 6, 12, 24]:
        agg[f"x{h}"] = (f"x{h}", "mean")
    out["fwd_excess_by_fc_quintile"] = pos.groupby("q").agg(fc=("fc", "mean"), n=("fc", "count"), **agg)
    out["fwd_excess_fc0"] = D[D["fc"] == 0][[f"x{h}" for h in [1, 2, 6, 12, 24]]].mean()
    tt = {}
    for h in [1, 2, 6, 12, 24]:
        s = pos[f"x{h}"].dropna()
        tt[f"x{h}"] = s.mean() / (s.std() / np.sqrt(len(s)))
    out["t_fc_pos"] = pd.Series(tt)
    # z-score of 24h fall (raw) quintiles among falls
    f = D[D["z"] < 0].copy()
    f["zq"] = pd.qcut(f["z"].rank(method="first"), 5, labels=False)
    out["fwd_by_raw_fall_quintile"] = f.groupby("zq").agg(z=("z", "mean"), n=("z", "count"), x2=("x2", "mean"), x24=("x24", "mean"))
    # daily book stats per window share positive
    dr = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dr.append(pd.DataFrame({"w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    DR = pd.concat(dr)
    out["days_by_window"] = DR.groupby("w").agg(book=("br", "mean"), coin=("cr", "mean")).T
    return out
