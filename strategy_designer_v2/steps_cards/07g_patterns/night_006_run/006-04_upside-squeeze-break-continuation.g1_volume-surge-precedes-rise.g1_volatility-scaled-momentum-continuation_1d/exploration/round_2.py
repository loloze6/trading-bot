def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vsr = (c / c.shift(10) - 1) / (r1.rolling(20).std() * np.sqrt(10))
            r10 = c / c.shift(10) - 1
            rng = (b["high"] - b["low"]) / c
            comp = rng.rolling(10).mean() / rng.rolling(60, min_periods=30).mean()
            volr = b["volume"].rolling(10).mean() / b["volume"].rolling(60, min_periods=30).mean()
            volr3 = b["volume"].rolling(3).mean() / b["volume"].rolling(60, min_periods=30).mean()
            fwd3 = c.shift(-3) / c - 1
            fwd10 = c.shift(-10) / c - 1
            idx = np.arange(0, len(b), 3)
            idx10 = np.arange(0, len(b), 10)
            g = pd.DataFrame({"coin": coin, "win": w, "fc": b["forecast"].values[idx],
                "vsr": vsr.values[idx], "r10": r10.values[idx], "comp": comp.values[idx],
                "volr": volr.values[idx], "volr3": volr3.values[idx], "fwd3": fwd3.values[idx],
                "absfwd3": np.abs(fwd3.values[idx]),
                "year": pd.to_datetime(b["timestamp"]).dt.year.values[idx]})
            rows.append(g)
            g10 = pd.DataFrame({"coin": coin, "volr": volr.values[idx10], "vsr": vsr.values[idx10], "fwd10": fwd10.values[idx10]})
            rows.append(g10.assign(kind=10))
    A = pd.concat(rows)
    G = A[A.get("kind").isna()].dropna(subset=["fwd3"]).copy()
    H = A[A.get("kind") == 10].dropna(subset=["fwd10"]).copy()
    G["ex"] = G["fwd3"] - G.groupby("coin")["fwd3"].transform("mean")
    H["ex"] = H["fwd10"] - H.groupby("coin")["fwd10"].transform("mean")
    def st(s):
        return pd.Series({"mean": s.mean(), "n": s.count(), "t": s.mean() / (s.std() / np.sqrt(s.count()))})
    d = G.dropna(subset=["volr", "vsr"]).copy()
    d["vq"] = pd.qcut(d["volr"], 3, labels=False)
    d["sq"] = pd.qcut(d["vsr"], 3, labels=False)
    out["volr_x_vsr_ex"] = d.groupby(["sq", "vq"])["ex"].apply(st).unstack().round(4)
    d["vq5"] = pd.qcut(d["volr"], 5, labels=False)
    out["volr_top_by_coin"] = d[d.vq5 == 4].groupby("coin")["ex"].apply(st).unstack().round(4)
    out["volr_bot_by_coin"] = d[d.vq5 == 0].groupby("coin")["ex"].apply(st).unstack().round(4)
    out["volr_top_by_year"] = d[d.vq5 == 4].groupby("year")["ex"].apply(st).unstack().round(4)
    # per-coin rank within coin
    d["vrank"] = d.groupby("coin")["volr"].rank(pct=True)
    out["spearman_volr_ex"] = float(stats.spearmanr(d["volr"], d["ex"]).correlation)
    out["spearman_volr_ex_p"] = float(stats.spearmanr(d["volr"], d["ex"]).pvalue)
    # residual regression of ex on volr and vsr
    X = np.column_stack([np.ones(len(d)), np.log(d["volr"]), d["vsr"].clip(-3, 3)])
    beta, *_ = np.linalg.lstsq(X, d["ex"].values, rcond=None)
    res = d["ex"].values - X @ beta
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * res.var())
    out["reg_logvolr_vsr"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "logvolr", "vsr"]).round(4)
    d3 = G.dropna(subset=["volr3"]).copy(); d3["q"] = pd.qcut(d3["volr3"], 5, labels=False)
    out["volr3_quint_ex"] = d3.groupby("q")["ex"].apply(st).unstack().round(4)
    h = H.dropna(subset=["volr"]).copy(); h["q"] = pd.qcut(h["volr"], 5, labels=False)
    out["volr_quint_ex10"] = h.groupby("q")["ex"].apply(st).unstack().round(4)
    # comp with direction
    c2 = G.dropna(subset=["comp", "r10"]).copy(); c2["q"] = pd.qcut(c2["comp"], 3, labels=False)
    c2["up"] = (c2["r10"] > 0).astype(int)
    out["comp_x_up_ex"] = c2.groupby(["q", "up"])["ex"].apply(st).unstack().round(4)
    return out
