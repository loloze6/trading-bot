def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        # drift per horizon: mean of non-overlapping h returns over all windows
        for h in (1, 2, 3, 5):
            rr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rr), np.std(rr, ddof=1))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            zr = r1 / sd20
            f = b["forecast"]
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 2, 3, 5):
                for i in range(0, len(b) - h, h):
                    if f.iloc[i] <= -2:
                        ret = c.iloc[i + h] / c.iloc[i] - 1
                        d, s = drift[(coin, h)]
                        rows.append(dict(coin=coin, window=w, h=h, year=yr.iloc[i],
                                         day=str(b["timestamp"].iloc[i])[:10],
                                         f=-f.iloc[i], zr=zr.iloc[i],
                                         unusual=-(ret - d), total=-ret, strength=-(ret - d) / s))
    df = pd.DataFrame(rows)
    def tday(g):
        dd = g.groupby("day")["unusual"].sum()
        n = len(dd)
        m = g["unusual"].mean()
        se = dd.std(ddof=1) * np.sqrt(n) / len(g) if n > 1 else np.nan
        return pd.Series(dict(n=len(g), days=n, mean=m, t=m / se if se else np.nan,
                              strength=g["strength"].mean(), total=g["total"].mean()))
    out = {}
    out["by_h"] = df.groupby("h").apply(tday)
    d1 = df[df.h == 1].copy()
    out["by_coin_h1"] = d1.groupby("coin").apply(tday)
    out["by_year_h1"] = d1.groupby("year").apply(tday)
    out["by_window_h1"] = d1.groupby("window").apply(tday)
    d1["zbin"] = pd.cut(d1["zr"], [-np.inf, 1, 1.5, 2, 3, np.inf])
    out["by_zr_h1"] = d1.groupby("zbin").apply(tday)
    d1["fq"] = pd.qcut(d1["f"], 4, labels=False, duplicates="drop")
    out["by_fq_h1"] = d1.groupby("fq").apply(tday)
    for h in (2, 3, 5):
        dh = df[df.h == h].copy()
        dh["zbin"] = pd.cut(dh["zr"], [-np.inf, 1.5, 2, 3, np.inf])
        out[f"by_zr_h{h}"] = dh.groupby("zbin").apply(tday)
    return out
