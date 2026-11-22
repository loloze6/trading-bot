import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [6, 18, 42, 78, 84]
    # drift per coin per horizon on non-overlapping grid
    drift, usual = {}, {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs)
            drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].values
            cl = df["close"].values
            raw = df.get("debug_info.components.panic.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for s in range(0, n, 78):
                e = min(s + 78, n)
                q = np.where(f[s:e] <= -10)[0]
                if len(q) == 0: continue
                t = s + q[0]
                r = {"coin": c, "win": w, "year": yr[t], "fc": f[t], "raw": raw[t]}
                for h in H:
                    if t + h < n:
                        ret = cl[t + h] / cl[t] - 1
                        r[f"u{h}"] = -(ret - drift[(c, h)])
                        r[f"tot{h}"] = -ret
                    else:
                        r[f"u{h}"] = np.nan; r[f"tot{h}"] = np.nan
                # recovery window: from t+0 to t+6 vs t+6 to t+84 already via
                rows.append(r)
    d = pd.DataFrame(rows)
    def agg(g, col="u78"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: agg(d, f"u{h}") for h in H}).T
    out["by_horizon_total"] = pd.DataFrame({h: agg(d, f"tot{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    out["by_win"] = d.groupby("win").apply(agg)
    d["fcb"] = pd.cut(d["fc"], [-20.01, -19.99, -15, -10])
    out["by_fc"] = d.groupby("fcb").apply(agg)
    d["rawq"] = pd.qcut(d["raw"], 4, duplicates="drop")
    out["by_raw_q"] = d.groupby("rawq").apply(agg)
    # median of u78 and trimmed mean
    x = d["u78"].dropna()
    out["robust"] = pd.Series({"median": x.median(), "trim5_mean": stats.trim_mean(x, 0.05),
                               "skew": stats.skew(x)})
    return out
