def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    H = [1, 3, 5, 10]
    # normal drift per coin and horizon, non-overlapping across all windows
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            r = cl.pct_change()
            sd = r.rolling(30).std()
            z = r / sd
            tr = (cl / cl.shift(60) - 1) * 100
            falling = np.where(tr.notna(), tr < -10, df["regime"] == "unknown")
            rising = np.where(tr.notna(), tr > 10, False)
            sdmed = sd.rolling(90, min_periods=30).median()
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    if not (z.iloc[i] > 0): continue
                    fr = cl.iloc[i + h] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, win=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     z=z.iloc[i], fall=bool(falling[i]), rise=bool(rising[i]),
                                     trend=tr.iloc[i], agit=bool(sd.iloc[i] > sdmed.iloc[i]) if pd.notna(sdmed.iloc[i]) else np.nan,
                                     short_unusual=-(fr - drift[(c, h)]),
                                     short_total=-fr, strength=-(fr - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)

    def ct(g, col="short_unusual"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series(dict(n=len(g), days=0, mean=np.nan, t=np.nan))
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    out["fall_by_h"] = d[d.fall].groupby("h").apply(ct)
    out["rise_by_h"] = d[d.rise].groupby("h").apply(ct)
    f3 = d[(d.fall) & (d.h == 3)].copy()
    f3["zq"] = pd.qcut(f3.z, 4, labels=False)
    out["fall3_by_zquart"] = f3.groupby("zq").apply(ct)
    out["fall3_zq_meanz"] = f3.groupby("zq").z.mean()
    out["fall3_by_coin"] = f3.groupby("coin").apply(ct)
    out["fall3_by_win"] = f3.groupby("win").apply(ct)
    out["fall3_by_agit"] = f3.groupby("agit").apply(ct)
    f3["tq"] = pd.qcut(f3.trend, 3, labels=False)
    out["fall3_by_trendtercile"] = f3.groupby("tq").apply(ct)
    for h in [1, 5, 10]:
        fh = d[(d.fall) & (d.h == h)].copy()
        fh["zq"] = pd.qcut(fh.z, 4, labels=False)
        out[f"fall{h}_by_zquart"] = fh.groupby("zq").apply(ct)
    r3 = d[(d.rise) & (d.h == 3)].copy()
    r3["zq"] = pd.qcut(r3.z, 4, labels=False)
    out["rise3_by_zquart"] = r3.groupby("zq").apply(ct)
    out["fall3_total"] = ct(f3, "short_total")
    out["fall3_strength_mean"] = f3.strength.mean()
    return out
