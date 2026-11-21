def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    for H in [120, 240]:
        rows = []
        for coin, wins in data["bars"].items():
            recs = []
            for w, b in wins.items():
                c = b["close"].astype(float).reset_index(drop=True)
                ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
                prox = c / c.rolling(720, min_periods=500).max() - 1
                r1 = c.pct_change()
                vol = r1.rolling(720, min_periods=500).std() * np.sqrt(24)
                proxv = prox / vol
                r168 = c / c.shift(168) - 1
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(c), H)
                d = pd.DataFrame({"prox": prox, "proxv": proxv, "r168": r168, "fwd": fwd,
                                  "yr": ts.dt.year}).iloc[idx]
                d["w"] = int(w[1:])
                recs.append(d)
            dd = pd.concat(recs)
            g = dd["fwd"].dropna()
            dd["u"] = (dd["fwd"] - g.mean()) / g.std()
            dd["ub"] = dd["fwd"] - g.mean()
            dd["coin"] = coin
            dd["pq"] = dd["prox"].rank(pct=True)
            rows.append(dd)
        D = pd.concat(rows).dropna(subset=["u", "prox", "proxv"])
        D["b"] = pd.qcut(D["proxv"], 5, labels=False)
        r = D.groupby("b").agg(lo=("proxv", "min"), hi=("proxv", "max"), n=("u", "size"),
                               strength=("u", "mean"), unusual=("ub", "mean"), sd=("u", "std"))
        r["t"] = r["strength"] / (r["sd"] / np.sqrt(r["n"]))
        out[f"H{H} fwd by prox in daily vols"] = r.drop(columns="sd")
        D["b2"] = pd.qcut(D["prox"], 5, labels=False)
        r = D.groupby("b2").agg(n=("u", "size"), strength=("u", "mean"), unusual=("ub", "mean"), sd=("u", "std"))
        r["t"] = r["strength"] / (r["sd"] / np.sqrt(r["n"]))
        out[f"H{H} fwd by prox quintile"] = r.drop(columns="sd")
        # rank correlation per coin
        out[f"H{H} spearman prox vs fwd per coin"] = D.groupby("coin").apply(
            lambda y: pd.Series(stats.spearmanr(y["pq"], y["u"])[:2], index=["rho", "p"]))
        # top minus bottom quintile per half of windows and per year
        D["half"] = np.where(D["w"] <= 12, "w1-12", "w13-24")
        def tb(y):
            hi = y.loc[y.b2 == 4, "u"]; lo = y.loc[y.b2 == 0, "u"]
            t = stats.ttest_ind(hi, lo, equal_var=False)[0] if len(hi) > 5 and len(lo) > 5 else np.nan
            return pd.Series({"top": hi.mean(), "bottom": lo.mean(), "diff": hi.mean() - lo.mean(), "t": t, "n_top": len(hi)})
        out[f"H{H} top-bottom by window half"] = D.groupby("half").apply(tb)
        out[f"H{H} top-bottom by year"] = D.groupby("yr").apply(tb)
        # within near-high, does r168 grade?
        N = D[D.b2 >= 3].copy()
        N["rb"] = pd.qcut(N["r168"], 3, labels=False)
        out[f"H{H} near-high: by r168 tercile"] = N.groupby("rb")["u"].agg(["mean", "size"])
    return out
