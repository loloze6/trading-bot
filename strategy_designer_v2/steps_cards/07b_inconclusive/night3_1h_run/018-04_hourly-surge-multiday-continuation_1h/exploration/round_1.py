import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [24, 48, 120, 240]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon: mean of non-overlapping returns over all windows
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].fillna(0).values
            r24 = pd.Series(c).pct_change(24)
            avg = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            mult = (r24 / avg).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # replicate cases
            base = 0.0
            last_cell = -1
            # prior 7-day return for regime
            r168 = pd.Series(c).pct_change(168).values
            for t in range(n):
                if f[t] <= 0:
                    base = 0.0
                    continue
                base = min(base, f[t])
                if f[t] - base >= 2:
                    base = f[t]
                    cell = t // 120
                    if cell != last_cell and t + 120 < n:
                        last_cell = cell
                        rec = dict(coin=coin, win=w, year=yr[t], mult=mult[t], f=f[t], r168=r168[t])
                        for h in H:
                            if t + h < n:
                                d, s = drift[(coin, h)]
                                rec[f"u{h}"] = c[t + h] / c[t] - 1 - d
                                rec[f"s{h}"] = (c[t + h] / c[t] - 1 - d) / s
                        rows.append(rec)
    X = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            v = g[f"u{h}"].dropna()
            out[f"u{h}"] = v.mean()
            out[f"t{h}"] = v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan
        return pd.Series(out)
    X["mb"] = pd.cut(X["mult"], [-np.inf, 0.5, 1, 1.5, 2, 3, np.inf])
    X["r7b"] = pd.qcut(X["r168"], 4, labels=["q1", "q2", "q3", "q4"])
    res = {
        "all": summ(X).to_frame().T,
        "by_mult": X.groupby("mb").apply(summ),
        "by_coin": X.groupby("coin").apply(summ),
        "by_year": X.groupby("year").apply(summ),
        "by_prior7d": X.groupby("r7b").apply(summ),
    }
    # first crossing events of multiple >= 2 and >= 3, non-overlapping 120 grid
    ev = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float); n = len(c)
            r24 = pd.Series(c).pct_change(24)
            avg = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            m = (r24 / avg).values
            for k in [2, 3]:
                last = -1
                for t in range(1, n - 240):
                    if m[t] >= k and m[t - 1] < k and t // 120 != last:
                        last = t // 120
                        rec = dict(k=k, mult=m[t])
                        for h in H:
                            d, s = drift[(coin, h)]
                            rec[f"u{h}"] = c[t + h] / c[t] - 1 - d
                        ev.append(rec)
    E = pd.DataFrame(ev)
    res["first_cross"] = E.groupby("k").apply(summ)
    return res
