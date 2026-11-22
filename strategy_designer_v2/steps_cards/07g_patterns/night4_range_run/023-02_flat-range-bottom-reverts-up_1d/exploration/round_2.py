def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min(); rng = hh - ll
            pos = (c - (hh + ll) / 2) / rng
            nmr = (c - c.shift(30)).abs() / rng
            r1 = c.pct_change(); vol30 = r1.rolling(30).std()
            past30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nmr": nmr,
                                      "p30z": past30 / (vol30 * np.sqrt(30)), "fwd": fwd,
                                      "yr": ts.dt.year, "grid": (np.arange(len(b)) % H == 0)}))
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean(); sd = G.groupby("coin").fwd.std()
    G["ex"] = G.fwd - G.coin.map(drift); G["z"] = G.ex / G.coin.map(sd)
    def summ(df, key):
        g = df.groupby(key, observed=True)["ex"]
        o = g.agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["strength"] = df.groupby(key, observed=True)["z"].mean()
        return o.drop(columns="std").round(4)
    res = {}
    M = G.dropna(subset=["p30z", "nmr"]).copy()
    M["q"] = pd.qcut(M.p30z, 5, labels=False)
    M["flat"] = np.where(M.nmr <= 0.3, "flat", "trend")
    res["p30z_q_x_flat"] = summ(M, ["flat", "q"])
    # signed momentum: excess return in direction of past 30d move
    M["sgn"] = np.sign(M.p30z); M["mz"] = M.z * M.sgn; M["mex"] = M.ex * M.sgn
    def msum(df, key):
        g = df.groupby(key, observed=True)
        o = g.mex.agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["strength"] = g.mz.mean(); return o.drop(columns="std").round(4)
    M["absq"] = pd.qcut(M.p30z.abs(), 4, labels=False)
    res["signed_mom_by_absq"] = msum(M, "absq")
    res["signed_mom_by_coin"] = msum(M, "coin")
    res["signed_mom_by_year"] = msum(M, "yr")
    res["slope_corr_p30z_z"] = pd.Series({"corr": M.p30z.corr(M.z), "n": len(M),
                                          "t": M.p30z.corr(M.z) * np.sqrt((len(M) - 2) / (1 - M.p30z.corr(M.z) ** 2))}).round(4)
    # weekday robustness
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd, ignore_index=True)
    dt = pd.to_datetime(D["day"]); D["wd"] = dt.dt.dayofweek; D["yr"] = dt.dt.year
    D = D.dropna(subset=["coin_return"])
    D["wk"] = np.where(D.wd.isin([4, 5]), "FriSat", "other")
    # average across coins per day first (independent days)
    P = D.groupby(["w", "day"]).agg(r=("coin_return", "mean"), wk=("wk", "first"), yr=("yr", "first")).reset_index()
    o = P.groupby("wk").r.agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    res["FriSat_pooled_days"] = o.round(5)
    piv = D.groupby(["coin", "wk"]).coin_return.mean().unstack()
    piv["diff"] = piv.FriSat - piv.other
    res["FriSat_by_coin"] = piv.round(5)
    py = P.groupby(["yr", "wk"]).r.mean().unstack(); py["diff"] = py.FriSat - py.other
    res["FriSat_by_year"] = py.round(5)
    return res
