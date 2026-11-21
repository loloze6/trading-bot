import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20, 30]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(list(cl[idx + h] / cl[idx] - 1))
            rs = np.array(rs)
            drift[(c, h)] = (np.nanmean(rs), np.nanstd(rs))
    out = {}
    hz = {}
    per = {}
    for h in H:
        rows = []
        for c, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                fc = df["forecast"].fillna(0).values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                mad = df.get("debug_info.components.ma_dist.last_history_value", pd.Series(np.nan, index=df.index)).values
                brk = df.get("debug_info.components.break.last_history_value", pd.Series(np.nan, index=df.index)).values
                n = len(df)
                seen = set()
                for t in range(n):
                    if fc[t] <= 0 or t + h >= n:
                        continue
                    cell = t // h
                    if cell in seen:
                        continue
                    seen.add(cell)
                    u = cl[t + h] / cl[t] - 1 - drift[(c, h)][0]
                    rows.append({"coin": c, "year": yr[t], "u": u, "s": u / drift[(c, h)][1],
                                 "mad": mad[t], "brk": brk[t], "fc": fc[t]})
        d = pd.DataFrame(rows)
        x = d["u"]
        lo, hi = x.quantile(0.01), x.quantile(0.99)
        xw = x.clip(lo, hi)
        hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                 "median": x.median(), "hit": (x > 0).mean(), "strength": d["s"].mean(),
                 "wins_mean": xw.mean(), "wins_t": xw.mean() / (xw.std() / np.sqrt(len(xw))),
                 "trim5": stats.trim_mean(x, 0.05),
                 "sp_fc": stats.spearmanr(d["fc"], d["u"])[0],
                 "sp_mad": stats.spearmanr(d["mad"], d["u"], nan_policy="omit")[0],
                 "sp_brk": stats.spearmanr(d["brk"], d["u"], nan_policy="omit")[0]}
        if h in (10, 20):
            def summ(g):
                y = g["u"]
                return pd.Series({"n": len(y), "mean": y.mean(),
                                  "t": y.mean() / (y.std() / np.sqrt(len(y))) if len(y) > 2 else np.nan,
                                  "median": y.median(), "strength": g["s"].mean()})
            out[f"coin_h{h}"] = d.groupby("coin").apply(summ)
            out[f"year_h{h}"] = d.groupby("year").apply(summ)
            # positive coins and years count
    out["horizon_own_grid"] = pd.DataFrame(hz).T
    return out
