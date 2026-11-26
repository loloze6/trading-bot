def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data.get("bars", {})
    rows = []
    shape = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            shape.append((coin, w, len(d)))
            c = d["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            up = (r > 0).astype(float)
            prior_ups = up.shift(1).rolling(5).sum()
            prior_downs = (r < 0).astype(float).shift(1).rolling(5).sum()
            rng = (d["high"] - d["low"]).astype(float)
            pos = (c - d["low"]) / rng.replace(0, np.nan)
            vol20 = r.rolling(20).std()
            ts = pd.to_datetime(d["timestamp"])
            reg = d["regime"].astype(str) if "regime" in d else pd.Series("na", index=d.index)
            alloc = d["postRebalance_current_allocation"] if "postRebalance_current_allocation" in d else np.nan
            ret5 = c / c.shift(5) - 1
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "r": r, "nxt": nxt, "prior_ups": prior_ups,
                "prior_downs": prior_downs, "pos": pos, "rz": r / vol20, "ret5": ret5,
                "reg": reg, "alloc": alloc, "wd": ts.dt.dayofweek, "year": ts.dt.year}))
    out["windows"] = pd.DataFrame(shape, columns=["coin", "w", "n"]).groupby("w")["n"].agg(["count", "sum"])
    if not rows:
        return out
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["nxt", "r"])
    drift = A.groupby("coin")["nxt"].mean()
    A["ex"] = A["nxt"] - A["coin"].map(drift)
    out["regimes"] = A["reg"].value_counts()
    A["inprof"] = A["reg"].isin(["mean_reversion", "unknown"])

    def tab(sub, key):
        g = sub.groupby(key)["ex"]
        t = g.agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t

    upP = A[A.inprof & (A.r > 0)]
    out["inprof_up_by_prior_ups"] = tab(upP, "prior_ups")
    dnP = A[A.inprof & (A.r < 0)]
    out["inprof_down_by_prior_ups"] = tab(dnP, "prior_ups")
    out["outprof_up_by_prior_ups"] = tab(A[~A.inprof & (A.r > 0)], "prior_ups")
    # in profile, by size of today's move (rz quintile)
    P = A[A.inprof].copy()
    P["rzq"] = pd.qcut(P["rz"], 5, labels=False, duplicates="drop")
    out["inprof_by_rz_quintile"] = tab(P, "rzq")
    P["r5q"] = pd.qcut(P["ret5"], 5, labels=False, duplicates="drop")
    out["inprof_by_ret5_quintile"] = tab(P, "r5q")
    out["inprof_by_weekday"] = tab(P, "wd")
    O = A[~A.inprof].copy()
    O["rzq"] = pd.qcut(O["rz"], 5, labels=False, duplicates="drop")
    out["outprof_by_rz_quintile"] = tab(O, "rzq")
    out["inprof_up_by_year"] = tab(upP, "year")
    out["inprof_up_by_window"] = tab(upP, "w")
    out["inprof_up_by_coin"] = tab(upP, "coin")
    # book gain per held bar
    held = A[A["alloc"].fillna(0) != 0]
    if len(held):
        g = held["alloc"] * held["nxt"]
        out["book_bar_gain"] = pd.Series({"n": len(held), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(len(g)))})
    # correlation in profile up days
    s = upP.dropna(subset=["prior_ups"])
    if len(s) > 10:
        rho, p = stats.spearmanr(s["prior_ups"], s["ex"])
        out["spearman_priorups_ex_upP"] = pd.Series({"rho": rho, "p": p, "n": len(s)})
    return out
