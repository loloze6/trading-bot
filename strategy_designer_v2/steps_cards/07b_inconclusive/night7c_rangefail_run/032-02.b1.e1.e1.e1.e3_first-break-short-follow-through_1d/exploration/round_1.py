def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # coin mean h-bar returns on non-overlapping grid
    def grid_mean(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rs.extend(c[idx + h] / c[idx] - 1)
        return np.nanmean(rs), np.nanstd(rs)
    rows = []
    hs = [1, 3, 5, 10, 20]
    means = {(coin, h): grid_mean(coin, h) for coin in bars for h in hs}
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            prev_hi = pd.Series(c).shift(1).rolling(60, min_periods=60).max().values
            # range width of prior 60 closes
            prev_lo = pd.Series(c).shift(1).rolling(60, min_periods=60).min().values
            ret60 = pd.Series(c).pct_change(60).values
            trend = df["regime"].values == "trending"
            last = -10
            for i in range(len(df)):
                if not trend[i]:
                    continue
                if i - last <= 3:
                    continue
                last = i
                prox = df["debug_info.components.margin_prox.last_history_value"].iloc[i]
                r = {"coin": coin, "window": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                     "prox": prox,
                     "margin": (c[i] / prev_hi[i] - 1) * 100 if prev_hi[i] == prev_hi[i] else np.nan,
                     "width": (prev_hi[i] / prev_lo[i] - 1) * 100 if prev_lo[i] == prev_lo[i] else np.nan,
                     "ret60": ret60[i] * 100 if ret60[i] == ret60[i] else np.nan}
                for h in hs:
                    r[f"x{h}"] = (c[i + h] / c[i] - 1 - means[(coin, h)][0]) * 100 if i + h < len(c) else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    out["n"] = len(d)
    def summ(g):
        s = {}
        for h in hs:
            x = g[f"x{h}"].dropna()
            s[f"m{h}"] = x.mean()
            s[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        s["n"] = len(g)
        return pd.Series(s)
    d["mq"] = pd.qcut(d["margin"], 4, labels=["q1small", "q2", "q3", "q4big"])
    out["by_margin_q"] = d.groupby("mq").apply(summ).round(2)
    out["margin_q_edges"] = d.groupby("mq")["margin"].agg(["min", "median", "max"]).round(2)
    out["by_coin"] = d.groupby("coin").apply(summ).round(2)
    out["by_year"] = d.groupby("year").apply(summ).round(2)
    d["wq"] = pd.qcut(d["width"], 3, labels=["narrow", "mid", "wide"])
    out["by_width"] = d.groupby("wq").apply(summ).round(2)
    out["width_edges"] = d.groupby("wq")["width"].agg(["min", "median", "max"]).round(1)
    # correlations of margin with excess returns, overall and by width tercile
    cr = {}
    for h in hs:
        x = d[["margin", f"x{h}"]].dropna()
        r, p = stats.spearmanr(x["margin"], x[f"x{h}"])
        cr[f"h{h}"] = (round(r, 3), round(p, 3), len(x))
    out["spearman_margin_all"] = pd.Series({k: str(v) for k, v in cr.items()})
    cw = {}
    for q, g in d.groupby("wq"):
        for h in [3, 5, 10]:
            x = g[["margin", f"x{h}"]].dropna()
            r, p = stats.spearmanr(x["margin"], x[f"x{h}"])
            cw[f"{q}_h{h}"] = f"{r:.3f} p{p:.3f} n{len(x)}"
    out["spearman_by_width"] = pd.Series(cw)
    # margin x width
    out["margin_x_width_m3"] = d.pivot_table(index="mq", columns="wq", values="x3", aggfunc="mean").round(2)
    out["margin_x_width_m10"] = d.pivot_table(index="mq", columns="wq", values="x10", aggfunc="mean").round(2)
    return out
