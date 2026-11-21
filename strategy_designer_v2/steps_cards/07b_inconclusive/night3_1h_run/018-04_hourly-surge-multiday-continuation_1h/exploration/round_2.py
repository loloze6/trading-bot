import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [48, 120, 240]
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
    ev = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float); n = len(c)
            r24 = pd.Series(c).pct_change(24)
            avg = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            m = (r24 / avg).values
            r168 = pd.Series(c).pct_change(168).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            last = -1
            for t in range(1, n - 120):
                if m[t] >= 2 and m[t - 1] < 2 and t // 120 != last:
                    last = t // 120
                    rec = dict(coin=coin, year=yr[t], mult=m[t], r168=r168[t])
                    for h in H:
                        if t + h < n:
                            d, s = drift[(coin, h)]
                            rec[f"u{h}"] = c[t + h] / c[t] - 1 - d
                            rec[f"s{h}"] = (c[t + h] / c[t] - 1 - d) / s
                            rec[f"tot{h}"] = c[t + h] / c[t] - 1
                    ev.append(rec)
    E = pd.DataFrame(ev)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            v = g[f"u{h}"].dropna()
            out[f"u{h}"] = v.mean()
            out[f"t{h}"] = v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan
        out["str120"] = g["s120"].mean()
        out["tot120"] = g["tot120"].mean()
        return pd.Series(out)
    E["mb"] = pd.cut(E["mult"], [2, 2.5, 3, 4, np.inf])
    E["r7b"] = pd.qcut(E["r168"], 4, labels=["q1", "q2", "q3", "q4"])
    v = E.dropna(subset=["u120"])
    sl = np.polyfit(np.minimum(v["mult"], 6), v["u120"], 1)[0]
    rho = v[["mult", "u120"]].corr(method="spearman").iloc[0, 1]
    return {
        "all": summ(E).to_frame().T,
        "by_mult": E.groupby("mb").apply(summ),
        "by_coin": E.groupby("coin").apply(summ),
        "by_year": E.groupby("year").apply(summ),
        "by_prior7d": E.groupby("r7b").apply(summ),
        "slope_u120_on_mult_capped6": sl,
        "spearman_mult_u120": rho,
    }
