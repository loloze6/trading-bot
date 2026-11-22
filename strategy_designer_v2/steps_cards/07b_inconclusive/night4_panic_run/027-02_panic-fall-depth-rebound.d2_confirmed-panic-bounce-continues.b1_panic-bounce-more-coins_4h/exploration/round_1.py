def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 84
    bars = data["bars"]
    rows = []
    allgrid = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                g.append(c[i + H] / c[i] - 1)
        allgrid[coin] = (np.mean(g) if g else np.nan, np.std(g) if g else np.nan)
    for coin, wins in bars.items():
        mu, sd = allgrid[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            col = "debug_info.components.bounce.last_history_value"
            act = (df["regime"] == "mean_reversion").values
            bcol = df[col].values if col in df.columns else np.full(n, np.nan)
            seen = set()
            for t in np.where(act)[0]:
                cell = t // H
                if cell in seen: continue
                seen.add(cell)
                b = bcol[t]
                if t >= 6: b2 = c[t] / c[t - 6] - 1
                else: b2 = np.nan
                if not np.isfinite(b): b = b2
                fr = {}
                for h in [6, 18, 42, 84]:
                    fr[h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                fall = c[t - 6] / c[t - 12] - 1 if t >= 12 else np.nan
                prior = c[t - 12] / c[t - 12 - 180] - 1 if t >= 192 else np.nan
                yr = pd.Timestamp(df["timestamp"].iloc[t]).year
                rows.append(dict(coin=coin, win=w, year=yr, bounce=b, fall=fall, prior=prior,
                                 r6=fr[6], r18=fr[18], r42=fr[42], r84=fr[84],
                                 ex84=fr[84] - mu if np.isfinite(fr[84]) else np.nan, sd=sd))
    d = pd.DataFrame(rows)
    def slope(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 8: return pd.Series(dict(n=m.sum(), slope=np.nan, t=np.nan))
        r = stats.linregress(x[m], y[m])
        return pd.Series(dict(n=m.sum(), slope=r.slope, t=r.slope / r.stderr))
    out = {}
    out["overall"] = slope(d.bounce.values, d.ex84.values)
    hz = {}
    for h in ["r6", "r18", "r42", "r84"]:
        hz[h] = slope(d.bounce.values, d[h].values)
    out["slope by horizon (raw ret)"] = pd.DataFrame(hz).T
    out["by coin"] = d.groupby("coin").apply(lambda g: slope(g.bounce.values, g.ex84.values))
    out["by year"] = d.groupby("year").apply(lambda g: slope(g.bounce.values, g.ex84.values))
    d["bq"] = pd.qcut(d.bounce, 5, labels=False, duplicates="drop")
    out["by bounce quintile"] = d.groupby("bq").agg(n=("ex84", "count"), bounce=("bounce", "mean"),
        ex84=("ex84", "mean"), ex84_med=("ex84", "median"), r18=("r18", "mean"), r42=("r42", "mean"))
    d["pos"] = d.bounce > 0
    out["by bounce sign"] = d.groupby("pos").agg(n=("ex84", "count"), ex84=("ex84", "mean"),
        t=("ex84", lambda s: s.mean() / (s.std() / np.sqrt(s.count()))))
    d["fq"] = pd.qcut(d.fall, 3, labels=False)
    out["by fall tercile"] = d.groupby("fq").apply(lambda g: pd.concat([slope(g.bounce.values, g.ex84.values),
        pd.Series(dict(fall=g.fall.mean(), ex84=g.ex84.mean()))]))
    d["pq"] = pd.qcut(d.prior, 3, labels=False)
    out["by prior 30d tercile"] = d.groupby("pq").apply(lambda g: pd.concat([slope(g.bounce.values, g.ex84.values),
        pd.Series(dict(prior=g.prior.mean(), ex84=g.ex84.mean()))]))
    # robust: rank correlation and winsorised
    m = d[["bounce", "ex84"]].dropna()
    out["spearman"] = pd.Series(dict(zip(["rho", "p"], stats.spearmanr(m.bounce, m.ex84))))
    ql, qh = m.ex84.quantile([0.02, 0.98])
    out["winsorised slope"] = slope(m.bounce.values, m.ex84.clip(ql, qh).values)
    out["ex84 normalised by sd slope"] = slope(d.bounce.values, (d.ex84 / d.sd).values)
    return out
