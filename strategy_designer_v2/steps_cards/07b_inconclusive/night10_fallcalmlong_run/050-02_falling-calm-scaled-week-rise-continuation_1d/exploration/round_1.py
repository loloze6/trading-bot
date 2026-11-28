def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    H = [1, 3, 5, 7, 10]
    for coin, ws in bars.items():
        allr = {h: [] for h in H}
        for w, b in ws.items():
            c = b["close"].values
            n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    allr[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: np.mean(allr[h]) for h in H}
        usual[coin] = np.std(allr[3])
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            for g in range(0, n, 3):
                for i in range(g, min(g + 3, n)):
                    prev = f[i - 1] if i > 0 else 0
                    if f[i] >= 2 and (prev == 0 or f[i] - prev >= 2):
                        r = {"coin": coin, "window": w, "year": ts[i].year, "fc": f[i],
                             "day": ts[i].normalize(), "regime": b["regime"].iloc[i]}
                        for h in H:
                            r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[coin][h]) if i + h < n else np.nan
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    out = {}
    def summ(gr):
        x = gr["u3"].dropna()
        return pd.Series({"n": len(x), "mean_u3": x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean()})
    out["overall_by_horizon"] = pd.DataFrame({h: [d["u%d" % h].dropna().mean(), 
        d["u%d" % h].dropna().mean() / (d["u%d" % h].dropna().std() / np.sqrt(d["u%d" % h].notna().sum())),
        d["u%d" % h].notna().sum()] for h in H}, index=["mean", "t", "n"]).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("window").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_quartile"] = d.groupby("fq").apply(summ)
    out["fc_quartile_means"] = d.groupby("fq")["fc"].mean()
    out["by_regime"] = d.groupby("regime").apply(summ)
    out["usual_3"] = pd.Series(usual)
    out["corr_fc_u3_spearman"] = float(stats.spearmanr(d["fc"], d["u3"], nan_policy="omit")[0])
    return out
