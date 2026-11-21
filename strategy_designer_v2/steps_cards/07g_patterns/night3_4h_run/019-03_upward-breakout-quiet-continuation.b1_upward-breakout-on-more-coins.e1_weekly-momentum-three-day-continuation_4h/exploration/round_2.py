def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < 250: continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol30 = pd.Series(r1).rolling(180, min_periods=120).std().values
            def back(k):
                return np.r_[np.full(k, np.nan), c[k:] / c[:-k] - 1]
            r1d, r2d, r7d, r30d = back(6), back(12), back(42), back(180)
            ts = pd.to_datetime(df["timestamp"])
            for h in [6, 18, 36]:
                idx = np.arange(0, n - h, h)
                fr = c[idx + h] / c[idx] - 1
                for j, t in enumerate(idx):
                    v = vol30[t]
                    if not v or np.isnan(v): continue
                    rows.append((coin, w, h, fr[j], r1d[t] / (v * np.sqrt(6)), r2d[t] / (v * np.sqrt(12)),
                                 r7d[t] / (v * np.sqrt(42)), r30d[t], ts[t].weekday(), ts[t].year))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "fr", "z1d", "z2d", "z7d", "r30", "wd", "year"])
    g = d.groupby(["coin", "h"])["fr"]
    d["un"] = d["fr"] - g.transform("mean"); d["st"] = d["un"] / g.transform("std")
    out = {}
    def tab(sub, col, q=10):
        sub = sub.dropna(subset=[col, "st"]).copy()
        sub["q"] = pd.qcut(sub[col].rank(method="first"), q, labels=False)
        a = sub.groupby("q").agg(mean=("st", "mean"), sd=("st", "std"), count=("st", "count"),
                                 un_pct=("un", "mean"), x=(col, "mean"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["count"])); a["un_pct"] *= 100
        return a.drop(columns="sd").round(4)
    for h in [6, 18, 36]:
        out[f"z1d deciles h{h}"] = tab(d[d.h == h], "z1d")
    s = d[d.h == 18].copy()
    out["z2d deciles h18"] = tab(s, "z2d")
    # fall rebound graded: correlation of -z1d with st among z1d<0
    neg = s[s.z1d < 0].dropna(subset=["z1d"])
    out["corr(-z1d, st | z1d<0) h18"] = round(float(np.corrcoef(-neg.z1d, neg.st)[0, 1]), 4)
    out["n neg"] = len(neg)
    # bottom quintile 1d by year, by coin
    s = s.dropna(subset=["z1d"])
    s["b"] = s.z1d <= s.z1d.quantile(0.2)
    b = s[s.b]
    out["low-1d q0 strength by year"] = b.groupby("year")["st"].agg(["mean", "count"]).round(4)
    bc = b.groupby("coin")["st"].agg(["mean", "count"])
    out["low-1d q0: coins positive / total"] = f"{(bc['mean']>0).sum()}/{len(bc)}"
    bw = b.groupby("w")["st"].mean()
    out["low-1d q0: windows positive / total"] = f"{(bw>0).sum()}/{len(bw)}"
    # within 7d momentum tercile
    s["m3"] = pd.qcut(s.z7d.rank(method="first"), 3, labels=["7d low", "7d mid", "7d high"])
    s["f5"] = pd.qcut(s.z1d.rank(method="first"), 5, labels=False)
    out["st by 7d tercile x 1d quintile h18"] = s.pivot_table(index="f5", columns="m3", values="st", aggfunc="mean").round(4)
    out["count 7d x 1d"] = s.pivot_table(index="f5", columns="m3", values="st", aggfunc="count")
    # 30d trend regime
    s["tr"] = np.where(s.r30 > 0, "30d up", "30d down")
    out["low-1d q0 by 30d trend"] = b.assign(tr=s.loc[b.index, "tr"]).groupby("tr")["st"].agg(["mean", "count"]).round(4)
    # weekday robustness: by year sign of sunday
    out["sunday strength by year h18"] = s[s.wd == 6].groupby("year")["st"].mean().round(4)
    out["thursday strength by year h18"] = s[s.wd == 3].groupby("year")["st"].mean().round(4)
    return out
