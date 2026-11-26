def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}
        for h in (3, 7, 14):
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[h] = (np.mean(rs), np.std(rs, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (3, 7, 14):
                m, s = drift[h]
                low = 0.0
                taken = set()
                for i in range(n):
                    if f[i] > low:
                        low = f[i]
                    low = min(low, f[i])
                    if f[i] >= 0:
                        low = 0.0
                    cell = i // h
                    if f[i] <= -2 and (f[i] - (f[i-1] if i > 0 else 0)) <= -2 or (f[i] < 0 and (i == 0 or f[i-1] >= 0) and f[i] <= -2):
                        if cell in taken or i + h >= n:
                            continue
                        taken.add(cell)
                        fwd = c[i + h] / c[i] - 1
                        rows.append(dict(coin=coin, win=w, h=h, year=yr[i], f=abs(f[i]),
                                         short_unus=-(fwd - m), short_total=-fwd, strength=-(fwd - m) / s))
    df = pd.DataFrame(rows)
    out = {}
    def summ(g):
        x = g["short_unus"]
        t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series({"n": len(x), "short_unus": x.mean(), "t": t,
                          "short_total": g["short_total"].mean(), "strength": g["strength"].mean()})
    out["cases_by_h"] = df.groupby("h").apply(summ)
    d7 = df[df.h == 7]
    out["h7_by_window"] = d7.groupby("win").apply(summ)
    out["h7_by_year"] = d7.groupby("year").apply(summ)
    out["h7_by_coin"] = d7.groupby("coin").apply(summ)
    for h in (3, 7, 14):
        q = df[df.h == h]
        med = q["f"].median()
        out[f"h{h}_large_minus_small"] = float(q[q.f > med]["short_unus"].mean() - q[q.f <= med]["short_unus"].mean())
    return out
