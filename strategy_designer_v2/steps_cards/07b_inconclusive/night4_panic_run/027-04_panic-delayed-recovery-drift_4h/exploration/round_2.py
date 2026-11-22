def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = {"1d":6, "2d":12, "3d":18, "7d":42, "13d":78}
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for hn, h in H.items():
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, hn)] = np.mean(rs)
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            lr = np.log(c[1:] / c[:-1])
            runmin = 0.0
            taken = set()
            for i in range(n):
                if f[i] <= 0:
                    runmin = 0.0
                    continue
                runmin = min(runmin, f[i])
                cell = i // 78
                if f[i] - runmin >= 2 and cell not in taken:
                    taken.add(cell)
                    runmin = f[i]
                    r = {"coin": coin, "year": ts.iloc[i].year, "f": f[i]}
                    for hn, h in H.items():
                        if i + h < n:
                            r["u_" + hn] = c[i + h] / c[i] - 1 - drift[(coin, hn)]
                    r["prior180d"] = c[i] / c[i - 1080] - 1 if i >= 1080 else np.nan
                    r["prior90d"] = c[i] / c[i - 540] - 1 if i >= 540 else np.nan
                    # fall of the 24h stretch ending 24h ago, and the 24h since
                    r["stretch_fall"] = c[i - 6] / c[i - 12] - 1 if i >= 12 else np.nan
                    r["since"] = c[i] / c[i - 6] - 1 if i >= 6 else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows).dropna(subset=["u_13d"])
    def summ(g):
        o = {"n": len(g)}
        for hn in H:
            x = g["u_" + hn].dropna()
            o["m_" + hn] = x.mean()
            o["t_" + hn] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(o)
    out = {}
    out["f_eq_20_vs_rest"] = d.groupby(d["f"] >= 19.99).apply(summ)
    d["t180"] = pd.qcut(d["prior180d"], 3, labels=["down", "mid", "up"])
    out["by_prior180d"] = d.groupby("t180").apply(summ)
    d["t90"] = pd.qcut(d["prior90d"], 3, labels=["down", "mid", "up"])
    out["by_prior90d"] = d.groupby("t90").apply(summ)
    d["sf"] = pd.qcut(d["stretch_fall"], 3, labels=["deep", "mid", "mild"])
    out["by_stretch_fall"] = d.groupby("sf").apply(summ)
    d["sn"] = pd.qcut(d["since"], 3, labels=["kept_falling", "mid", "bounced"])
    out["by_since"] = d.groupby("sn").apply(summ)
    top = d[d["f"] >= 19.99]
    out["top_by_prior180d"] = top.groupby("t180").apply(summ)
    out["corr_f_u13_spearman"] = d["f"].corr(d["u_13d"], method="spearman")
    out["corr_stretchfall_u13_spearman"] = d["stretch_fall"].corr(d["u_13d"], method="spearman")
    return out
