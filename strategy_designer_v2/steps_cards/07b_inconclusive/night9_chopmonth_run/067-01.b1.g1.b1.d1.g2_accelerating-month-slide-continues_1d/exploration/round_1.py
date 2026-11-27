def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for H in (5, 10, 20):
        for coin, ws in bars.items():
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(allr)
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r5 = pd.Series(c).pct_change(5).values * 100
            r30 = pd.Series(c).pct_change(30).values * 100
            act = (b["regime"] == "trending").values
            fc = b["forecast"].values
            for i in range(0, n, 10):
                rec = dict(coin=coin, w=w, act=act[i], fc=fc[i], r5=r5[i], r30=r30[i],
                           day=str(b["timestamp"].iloc[i])[:10], yr=str(b["timestamp"].iloc[i])[:4])
                for H in (5, 10, 20):
                    if i + H < n:
                        rec[f"u{H}"] = -(c[i + H] / c[i] - 1 - drift[(coin, H)])
                rows.append(rec)
    df = pd.DataFrame(rows)
    def summ(g, col="u10"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), mean=np.nan, t_day=np.nan))
        dd = g.groupby("day")[col].sum()
        m = g[col].mean()
        k = len(dd)
        t = (dd.sum() / len(g)) / (dd.std() * np.sqrt(k) / len(g)) if dd.std() > 0 else np.nan
        return pd.Series(dict(n=len(g), days=k, mean=m, t_day=t))
    a = df[df.act].copy()
    out = {}
    out["active_by_H"] = pd.DataFrame({H: summ(a, f"u{H}") for H in (5, 10, 20)})
    out["short_fc_by_H"] = pd.DataFrame({H: summ(a[a.fc < 0], f"u{H}") for H in (5, 10, 20)})
    a["r5q"] = pd.qcut(a["r5"], 5, labels=False)
    out["by_r5_quint"] = a.groupby("r5q").apply(lambda g: pd.concat([summ(g), pd.Series({"r5mean": g.r5.mean()})]))
    a["r30q"] = pd.qcut(a["r30"], 5, labels=False)
    out["by_r30_quint"] = a.groupby("r30q").apply(lambda g: pd.concat([summ(g), pd.Series({"r30mean": g.r30.mean()})]))
    out["by_r30_quint_u20"] = a.groupby("r30q").apply(lambda g: summ(g, "u20"))
    out["by_coin"] = a.groupby("coin").apply(summ)
    out["by_window"] = a.groupby("w").apply(summ)
    out["by_year"] = a.groupby("yr").apply(summ)
    out["corr_r5_u10"] = float(a[["r5", "u10"]].dropna().corr().iloc[0, 1])
    out["corr_r30_u10"] = float(a[["r30", "u10"]].dropna().corr().iloc[0, 1])
    return out
