def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    drift = {}; usual = {}
    for c, ws in bars.items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            fc = b["forecast"].fillna(0).values
            n = len(cl)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            s = pd.Series(cl)
            r42 = s.pct_change(42).values
            r180 = s.pct_change(180).values
            r90 = s.pct_change(90).values
            above = (s / s.rolling(120, min_periods=60).mean() - 1).values
            lastmin = 0.0; prev = -1
            for t in range(n):
                cell = t // H
                if fc[t] - lastmin >= 2 and cell != prev:
                    prev = cell
                    if t + H < n:
                        u = cl[t + H] / cl[t] - 1 - drift[c]
                        u36 = cl[t + 36] / cl[t] - 1 if t + 36 < n else np.nan
                        rows.append(dict(coin=c, win=w, year=yr[t], fc=fc[t], r42=r42[t],
                                         r180=r180[t], r90=r90[t], above=above[t], u72=u, s72=u / usual[c]))
                    lastmin = fc[t]
                if fc[t] == 0:
                    lastmin = 0.0
                else:
                    lastmin = min(lastmin, fc[t])
    df = pd.DataFrame(rows)
    def summ(g, col="u72"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 5, labels=False)
    df["top"] = (df["fq"] >= 3).astype(int)
    out["year_x_top2fc"] = df.groupby(["year", "top"]).apply(summ)
    def slope(g):
        g = g.dropna(subset=["fc", "u72"])
        if len(g) < 10: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g["fc"], g["u72"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out["slope_by_year"] = df.groupby("year").apply(slope)
    out["slope_by_coin"] = df.groupby("coin").apply(slope)
    for col in ["r90", "r180", "above"]:
        d = df.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), 5, labels=False)
        out["by_%s_quint" % col] = d.groupby("q").apply(summ)
        out["slope_by_%s_quint" % col] = d.groupby("q").apply(slope)
    d = df.dropna(subset=["r180"]).copy()
    d["up"] = (d["r180"] > 0).astype(int)
    out["up30d_x_top2fc"] = d.groupby(["up", "top"]).apply(summ)
    out["strength_top2fc"] = summ(df[df.top == 1], "s72")
    out["corr_fc_r42"] = df[["fc", "r42"]].corr().iloc[0, 1]
    return out
