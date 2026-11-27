def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for H in (10, 20):
        for coin, ws in bars.items():
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(allr)
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            n = len(c)
            r60 = c.pct_change(60).values * 100
            r30 = c.pct_change(30).values * 100
            r5 = c.pct_change(5).values * 100
            dr = c.pct_change()
            vol30 = dr.rolling(30).std().values
            for i in range(0, n, 10):
                rec = dict(coin=coin, w=w, r60=r60[i], r30=r30[i], r5=r5[i], vol=vol30[i],
                           act=b["regime"].iloc[i] == "trending",
                           day=str(b["timestamp"].iloc[i])[:10], yr=str(b["timestamp"].iloc[i])[:4])
                for H in (10, 20):
                    if i + H < n:
                        rec[f"x{H}"] = c[i + H] / c[i] - 1 - drift[(coin, H)]
                rows.append(rec)
    df = pd.DataFrame(rows)
    def summ(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), days=np.nan, mean=np.nan, t_day=np.nan))
        dd = g.groupby("day")[col].sum()
        k = len(dd)
        t = (dd.sum() / len(g)) / (dd.std() * np.sqrt(k) / len(g)) if dd.std() > 0 else np.nan
        return pd.Series(dict(n=len(g), days=k, mean=g[col].mean(), t_day=t))
    ch = df[(df.r60.abs() <= 10) & df.r30.notna()].copy()
    out = {}
    # direction of 30-day move: unusual move in direction of r30 sign
    ch["sgn"] = np.sign(ch.r30)
    for H in (10, 20):
        ch[f"d{H}"] = ch[f"x{H}"] * ch["sgn"]
    out["choppy_dir30_side"] = pd.DataFrame({f"{s}_H{H}": summ(ch[ch.sgn == v], f"d{H}")
                                             for s, v in (("fall", -1), ("rise", 1)) for H in (10, 20)})
    ch["r30b"] = pd.cut(ch.r30, [-100, -20, -12, -6, 0, 6, 12, 20, 1000])
    out["choppy_by_r30bin_x10"] = ch.groupby("r30b").apply(lambda g: pd.concat([summ(g, "x10"), pd.Series({"r30m": g.r30.mean()})]))
    out["choppy_by_r30bin_x20"] = ch.groupby("r30b").apply(lambda g: summ(g, "x20"))
    sub = ch.dropna(subset=["x10"])
    out["spearman_r30_x10_all"] = float(stats.spearmanr(sub.r30, sub.x10)[0])
    f = sub[sub.r30 < 0]
    out["spearman_r30_x10_falls"] = float(stats.spearmanr(f.r30, f.x10)[0])
    out["spearman_r5_x10_falls"] = float(stats.spearmanr(f.r5, f.x10)[0])
    ri = sub[sub.r30 > 0]
    out["spearman_r30_x10_rises"] = float(stats.spearmanr(ri.r30, ri.x10)[0])
    # deep falls by window and year, short direction
    deep = ch[ch.r30 < -12].copy()
    deep["s10"] = -deep.x10
    out["deepfall_by_year"] = deep.groupby("yr").apply(lambda g: summ(g, "s10"))
    out["deepfall_by_window"] = deep.groupby("w").apply(lambda g: summ(g, "s10"))
    # standardised r30 (by vol) grading within falls
    f = f.copy()
    f["z30"] = f.r30 / (f.vol * 100 * np.sqrt(30))
    out["spearman_z30_x10_falls"] = float(stats.spearmanr(f.z30.dropna(), f.loc[f.z30.notna(), "x10"])[0])
    f["zq"] = pd.qcut(f.z30, 4, labels=False)
    f["s10"] = -f.x10
    out["falls_by_z30_quart_short"] = f.groupby("zq").apply(lambda g: pd.concat([summ(g, "s10"), pd.Series({"z30m": g.z30.mean()})]))
    return out
