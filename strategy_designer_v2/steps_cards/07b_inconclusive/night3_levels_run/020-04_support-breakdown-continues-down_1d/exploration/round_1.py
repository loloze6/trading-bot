import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    drift = {}
    sd = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); sd[(coin, h)] = np.std(rs)
    for coin, ws in bars.items():
        for wi, (w, df) in enumerate(ws.items()):
            c = df["close"].values; f = df["forecast"].values
            n = len(c)
            ma50 = pd.Series(c).rolling(50, min_periods=20).mean().values
            r30 = pd.Series(c).pct_change(30).values
            ref = None; last_cell = -1
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = None; continue
                if ref is None: ref = 0.0
                ref = max(ref, ft) if ref is not None else ft
                if ref - ft >= 2:
                    cell = t // 5
                    if cell != last_cell:
                        last_cell = cell
                        rec = {"coin": coin, "win": wi, "f": ft,
                               "trend": np.sign(c[t] / ma50[t] - 1) if np.isfinite(ma50[t]) else np.nan,
                               "r30": r30[t], "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                        for h in H:
                            if t + h < n:
                                rec[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[(coin, h)])
                                rec[f"s{h}"] = rec[f"u{h}"] / sd[(coin, h)]
                        rows.append(rec)
                    ref = ft
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=False, duplicates="drop")
    d["r30q"] = pd.qcut(d["r30"], 4, labels=False, duplicates="drop")
    return {
        "all": summ(d),
        "by_coin": d.groupby("coin").apply(summ),
        "by_year": d.groupby("year").apply(summ),
        "by_fq": d.groupby("fq").apply(summ),
        "by_trend_ma50": d.groupby("trend").apply(summ),
        "by_r30q": d.groupby("r30q").apply(summ),
        "strength5": d["s5"].mean(),
    }
