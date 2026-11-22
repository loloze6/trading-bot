def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 18, 42, 84, 126]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs)
            usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            ret30 = pd.Series(c).pct_change(180).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for s in range(0, n, 84):
                e = min(s + 84, n)
                idx = np.where(f[s:e] >= 2)[0]
                if len(idx) == 0:
                    continue
                t = s + idx[0]
                r = {"coin": coin, "win": w, "year": yr[t], "fc": f[t], "prior30": ret30[t]}
                for h in H:
                    if t + h < n:
                        r["u%d" % h] = c[t + h] / c[t] - 1 - drift[(coin, h)]
                        r["z%d" % h] = r["u%d" % h] / usual[(coin, h)]
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u84"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, "u%d" % h) for h in H}).T
    out["strength_by_horizon"] = pd.Series({h: d["z%d" % h].mean() for h in H})
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_quintile"] = d.groupby("fq").apply(summ)
    out["fc_quintile_h18"] = d.groupby("fq").apply(lambda g: summ(g, "u18"))
    out["fc_quintile_mean_fc"] = d.groupby("fq")["fc"].mean()
    d["prior_up"] = np.where(d["prior30"] > 0, "up", "down")
    out["by_prior30"] = d.groupby("prior_up").apply(summ)
    out["by_prior30_h18"] = d.groupby("prior_up").apply(lambda g: summ(g, "u18"))
    return out
