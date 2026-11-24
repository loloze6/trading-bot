def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            dn = (r < 0).astype(int); up = (r > 0).astype(int)
            gd = (dn != dn.shift()).cumsum(); gu = (up != up.shift()).cumsum()
            ds = dn.groupby(gd).cumsum() * dn
            us = up.groupby(gu).cumsum() * up
            # run return of current streak (signed move accumulated during streak)
            lr = np.log(c).diff()
            runret_d = lr.where(dn == 1, 0).groupby(gd).cumsum() * dn
            runret_u = lr.where(up == 1, 0).groupby(gu).cumsum() * up
            vol60 = r.rolling(60, min_periods=30).std()
            fwd = c.shift(-H) / c - 1
            df = pd.DataFrame({"coin": coin, "ts": b["timestamp"].values, "fwd": fwd,
                               "ds": ds, "us": us, "rz": r / vol60,
                               "rund": runret_d / vol60, "runu": runret_u / vol60,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "pnl": b["postRebalance_current_allocation"].astype(float) * (c.shift(-1) / c - 1),
                               "r1n": c.shift(-1) / c - 1})
            rows.append(df.iloc[::H].assign(full=0))
            rows.append(df.assign(full=1))
    A = pd.concat(rows, ignore_index=True)
    F = A[A.full == 1]; D = A[A.full == 0].dropna(subset=["fwd"]).copy()
    g = D.groupby("coin")["fwd"]
    D["unus"] = D["fwd"] - g.transform("mean"); D["z"] = D["unus"] / g.transform("std")

    def pt(sub):
        sub = sub.dropna(subset=["unus"]); n = len(sub)
        if n < 10: return pd.Series({"n": n, "mean": np.nan, "z": np.nan, "t": np.nan, "days": 0})
        m = sub["unus"].mean(); S = (sub["unus"] - m).groupby(sub["ts"]).sum(); G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "z": sub["z"].mean(), "t": m / se, "days": G})
    out = {}
    out["by_rz_bin"] = D.groupby(pd.cut(D["rz"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])).apply(pt)
    dsub = D[D.ds >= 2].copy()
    dsub["q"] = pd.qcut(dsub["rund"].rank(method="first"), 4, labels=False)
    out["down_streak_runsize_q"] = dsub.groupby("q").apply(pt)
    usub = D[D.us >= 2].copy()
    usub["q"] = pd.qcut(usub["runu"].rank(method="first"), 4, labels=False)
    out["up_streak_runsize_q"] = usub.groupby("q").apply(pt)
    fsub = D[D.fc < 0].copy()
    fsub["q"] = pd.qcut(fsub["fc"].rank(method="first"), 4, labels=False)
    out["forecast_quartile_shortside"] = fsub.groupby("q").apply(pt)
    # book decomposition on bars
    md = F.groupby("coin")["r1n"].transform("mean")
    F = F.assign(mkt=F["alloc"] * md)
    out["book_bar_decomp"] = pd.Series({"mean_pnl": F["pnl"].mean(), "market_part": F["mkt"].mean(),
                                        "timing_part": F["pnl"].mean() - F["mkt"].mean(),
                                        "mean_alloc": F["alloc"].mean(), "share_short": (F["alloc"] < 0).mean()})
    return out
