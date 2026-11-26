def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            sc = r7 / mabs
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            hi7 = c.rolling(7).max()
            lo7 = c.rolling(7).min()
            pos7 = (c - lo7) / (hi7 - lo7)
            rng = (b["high"] - b["low"]) / c
            vol30 = r1.rolling(30, min_periods=20).std()
            rngz = rng / rng.rolling(30, min_periods=20).mean()
            volz = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
            clv = (c - b["low"]) / (b["high"] - b["low"])
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)),
                               "regime": b["regime"], "sc": sc, "r7": r7, "r1": r1, "r1z": r1 / vol30,
                               "fwd": fwd, "fwd1": fwd1, "pos7": pos7, "rngz": rngz, "volz": volz,
                               "clv": clv, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.loc[A.i % H == 0, "fwd"].mean()
    G = A[(A.i % H == 0) & A.fwd.notna()].copy()
    G["ex"] = G.fwd - drift
    G["inprof"] = G.regime.isin(["trending", "unknown"])
    out = {"drift7": drift, "regime_counts_grid": G.regime.value_counts()}
    def summ(g):
        n = len(g)
        m = g.ex.mean()
        t = m / (g.ex.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_ex": m, "t": t})
    G["scq"] = pd.qcut(G.sc, 5, labels=False, duplicates="drop")
    out["by_prof_scq"] = G.groupby(["inprof", "scq"]).apply(summ)
    out["by_regime"] = G.groupby("regime").apply(summ)
    G["pq"] = pd.qcut(G.pos7, 4, labels=False, duplicates="drop")
    out["by_prof_pos7"] = G.groupby(["inprof", "pq"]).apply(summ)
    G["r1q"] = pd.qcut(G.r1z, 5, labels=False, duplicates="drop")
    out["by_prof_r1z"] = G.groupby(["inprof", "r1q"]).apply(summ)
    G["rq"] = pd.qcut(G.rngz, 4, labels=False, duplicates="drop")
    out["by_prof_rngz"] = G.groupby(["inprof", "rq"]).apply(summ)
    G["vq"] = pd.qcut(G.volz, 4, labels=False, duplicates="drop")
    out["by_prof_volz"] = G.groupby(["inprof", "vq"]).apply(summ)
    out["by_wd_1d"] = A[A.fwd1.notna()].assign(ex=lambda d: d.fwd1 - d.fwd1.mean()).groupby("wd").apply(summ)
    out["by_year_inprof"] = G[G.inprof].groupby("yr").apply(summ)
    # correlations
    for nm in ["sc", "pos7", "r1z", "rngz", "volz", "clv"]:
        for p in [True, False]:
            g = G[G.inprof == p][[nm, "ex"]].dropna()
            rr, pv = stats.spearmanr(g[nm], g.ex)
            out[f"spearman_{nm}_{'in' if p else 'out'}"] = f"rho {rr:.3f} p {pv:.3f} n {len(g)}"
    # book daily: largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    out["book_ret_by_win"] = D.groupby("win").book_return.agg(["mean", "std", "count"])
    return out
