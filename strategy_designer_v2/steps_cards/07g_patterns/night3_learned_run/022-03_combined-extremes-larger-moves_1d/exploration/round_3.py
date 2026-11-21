def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=15).std()
            fwd = c.shift(-H) / c - 1
            comb = b["debug_info.components.combined.last_history_value"]
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], r1=r1[i], vol30=vol30[i],
                                 comb=comb[i], yr=ts[i].year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["usual"] = d.groupby("coin")["fwd"].transform("std")
    d["un"] = d["fwd"] - d["drift"]
    d["z"] = d["un"] / d["usual"]
    d["sr"] = d["r1"] / d["vol30"]
    d["ar"] = d["sr"].abs()
    x = d.dropna(subset=["ar", "z"]).copy()
    x["q"] = x.groupby("coin")["ar"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    x["side"] = np.where(x["r1"] > 0, "up", "down")
    out = {}
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "z": g["z"].mean(), "t": g["z"].mean() / (g["z"].std() / np.sqrt(n)),
                          "un_pct": g["un"].mean() * 100, "total_pct": g["fwd"].mean() * 100})
    out["absmove_q_by_side"] = x.groupby(["side", "q"]).apply(summ).round(4)
    out["absmove_rho_by_side"] = x.groupby("side").apply(lambda g: pd.Series({"rho": stats.spearmanr(g["ar"], g["z"]).correlation, "n": len(g), "t": stats.spearmanr(g["ar"], g["z"]).correlation * np.sqrt(len(g))})).round(4)
    x["half"] = np.where(x["yr"] <= 2021, "early", "late")
    out["absmove_rho_by_half"] = x.groupby("half").apply(lambda g: pd.Series({"rho": stats.spearmanr(g["ar"], g["z"]).correlation, "n": len(g), "t": stats.spearmanr(g["ar"], g["z"]).correlation * np.sqrt(len(g))})).round(4)
    out["absmove_rho_by_year"] = x.groupby("yr").apply(lambda g: stats.spearmanr(g["ar"], g["z"]).correlation).round(3)
    out["absmove_top_q_strength"] = summ(x[x["q"] == 4]).round(4)
    # signed move: rho of sr with z (reversal vs continuation)
    out["signed_rho"] = pd.Series({"rho": stats.spearmanr(x["sr"], x["z"]).correlation, "n": len(x)}).round(4)
    # combined score inverted: top decile abs, sign flipped
    y = d.dropna(subset=["comb", "z"]).copy()
    thr = y["comb"].abs().quantile(0.9)
    t10 = y[y["comb"].abs() >= thr]
    s = -np.sign(t10["comb"]) * t10["z"]
    out["comb_top10_inverted"] = pd.Series({"n": len(s), "mean_z": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))}).round(4)
    return out
