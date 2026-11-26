def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        drift = pd.concat(allr).mean() if allr else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "regime": b["regime"],
                "srise": r1 / sd,
                "prior5": (c.shift(1) / c.shift(6) - 1) / (sd * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1 - drift,
                "f2": c.shift(-2) / c - 1 - 2 * drift,
                "f3": c.shift(-3) / c - 1 - 3 * drift,
                "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            rows.append(df)
    d = pd.concat(rows)
    a = d[(d.fc < 0)].dropna(subset=["f1", "srise"]).copy()
    out = {}
    def stat(g, col="f1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["all_h"] = pd.DataFrame({h: stat(a, h) for h in ["f1", "f2", "f3"]}).T
    a["q_fc"] = pd.qcut(-a.fc, 5, labels=False, duplicates="drop")
    a["q_rise"] = pd.qcut(a.srise, 5, labels=False, duplicates="drop")
    a["q_prior"] = pd.qcut(a.prior5, 5, labels=False, duplicates="drop")
    for q in ["q_fc", "q_rise", "q_prior"]:
        t = a.groupby(q).apply(lambda g: pd.concat([stat(g, "f1"), stat(g, "f3").rename(lambda s: s + "_3")]))
        out[q] = t
        out[q + "_mean_x"] = a.groupby(q)[{"q_fc": "fc", "q_rise": "srise", "q_prior": "prior5"}[q]].mean()
    out["by_year"] = a.groupby("year").apply(stat)
    out["by_coin"] = a.groupby("coin").apply(stat)
    from scipy import stats
    for x in ["srise", "prior5"]:
        s = a[[x, "f1"]].dropna()
        out["corr_" + x] = pd.Series(stats.spearmanr(s[x], s["f1"]), index=["rho", "p"])
    # prior up vs down
    a["prior_sign"] = np.where(a.prior5 < 0, "prior_down", "prior_up")
    out["by_prior_sign"] = a.groupby("prior_sign").apply(lambda g: pd.concat([stat(g, "f1"), stat(g, "f3").rename(lambda s: s + "_3")]))
    # all rise days in data vs active (check profile from fc)
    out["n_active_days"] = a.day.nunique()
    return out
