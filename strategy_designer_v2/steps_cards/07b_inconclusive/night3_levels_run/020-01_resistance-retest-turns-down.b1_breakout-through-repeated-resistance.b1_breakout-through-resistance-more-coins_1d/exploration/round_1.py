def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    Hs = [1, 3, 5, 10, 20]
    for coin, wins in bars.items():
        rets = {h: [] for h in Hs}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in Hs:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(rets[h]) for h in Hs}
        usual[coin] = {h: np.std(rets[h]) for h in Hs}
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df["debug_info.components.res_break.last_history_value"].fillna(0).values
            n = len(c)
            floor = 0.0
            taken = set()
            for t in range(n):
                if f[t] <= 0:
                    floor = 0.0
                cell = t // 10
                if f[t] - floor >= 2 and cell not in taken:
                    taken.add(cell)
                    floor = f[t]
                    r = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                         "fc": f[t], "raw": raw[t]}
                    for h in Hs:
                        if t + h < n:
                            r["u%d" % h] = c[t + h] / c[t] - 1 - drift[coin][h]
                            r["s%d" % h] = r["u%d" % h] / usual[coin][h]
                    r["bar0"] = c[t] / c[t - 1] - 1 if t > 0 else np.nan
                    r["past30"] = c[t] / c[t - 30] - 1 if t >= 30 else np.nan
                    r["past90"] = c[t] / c[t - 90] - 1 if t >= 90 else np.nan
                    # recent vol
                    if t >= 30:
                        lr = np.diff(np.log(c[t - 30:t + 1]))
                        r["vol30"] = lr.std()
                    else:
                        r["vol30"] = np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u10"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(d, "u%d" % h) for h in Hs}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fcq"] = pd.qcut(d["fc"], 4, labels=False, duplicates="drop")
    out["by_fc_q"] = d.groupby("fcq").apply(summ)
    d["p90q"] = pd.qcut(d["past90"], 4, labels=False)
    out["by_past90_q"] = d.groupby("p90q").apply(summ)
    d["p30q"] = pd.qcut(d["past30"], 4, labels=False)
    out["by_past30_q"] = d.groupby("p30q").apply(summ)
    d["volq"] = pd.qcut(d["vol30"], 4, labels=False)
    out["by_vol_q"] = d.groupby("volq").apply(summ)
    d["b0q"] = pd.qcut(d["bar0"], 4, labels=False)
    out["by_bar0_q"] = d.groupby("b0q").apply(summ)
    out["by_bar0_q_u20"] = d.groupby("b0q").apply(lambda g: summ(g, "u20"))
    out["by_past90_u20"] = d.groupby("p90q").apply(lambda g: summ(g, "u20"))
    out["q_edges"] = pd.DataFrame({"past90": d["past90"].quantile([.25, .5, .75]).values,
                                   "past30": d["past30"].quantile([.25, .5, .75]).values,
                                   "bar0": d["bar0"].quantile([.25, .5, .75]).values,
                                   "vol30": d["vol30"].quantile([.25, .5, .75]).values})
    out["mean_strength10"] = d["s10"].mean()
    return out
