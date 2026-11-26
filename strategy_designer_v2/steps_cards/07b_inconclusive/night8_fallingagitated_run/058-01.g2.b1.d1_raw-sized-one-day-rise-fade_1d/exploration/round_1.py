import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        # normal drift per horizon: non-overlapping returns over all windows
        for h in (1, 3, 5, 10):
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std().shift(1)
            z = r1 / sd
            inprof = (b["regime"] == "unknown")
            for i in range(0, len(b) - 10, 3):
                if not inprof.iloc[i] or not np.isfinite(z.iloc[i]):
                    continue
                d = {"coin": coin, "w": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": i, "z": z.iloc[i], "fc": b["forecast"].iloc[i],
                     "r1": r1.iloc[i]}
                for h in (1, 3, 5, 10):
                    d[f"u{h}"] = -(c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)])
                rows.append(d)
    df = pd.DataFrame(rows)
    df["zb"] = pd.cut(df["z"], [-99, -2, -1, 0, 0.5, 1, 1.5, 2, 99])
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "u1": g.u1.mean(), "u3": g.u3.mean(), "u5": g.u5.mean(),
                          "u10": g.u10.mean(), "t3": stats.ttest_1samp(g.u3, 0).statistic if len(g) > 2 else np.nan,
                          "t5": stats.ttest_1samp(g.u5, 0).statistic if len(g) > 2 else np.nan})
    out["by z bucket (short-direction unusual)"] = df.groupby("zb").apply(summ)
    up = df[df.z > 0]
    out["up days by coin"] = up.groupby("coin").apply(summ)
    out["up days by window"] = up.groupby("w").apply(summ)
    out["up days by year"] = up.groupby("year").apply(summ)
    sh = df[df.fc <= -2]
    out["forecast<=-2 cases"] = summ(sh)
    out["forecast<=-2 by fc bucket"] = sh.groupby(pd.cut(sh.fc, [-21, -15, -10, -5, -2])).apply(summ)
    out["corr z vs u3 (up days), spearman"] = float(stats.spearmanr(up.z, up.u3).correlation)
    out["all in-profile cases"] = summ(df)
    return out
