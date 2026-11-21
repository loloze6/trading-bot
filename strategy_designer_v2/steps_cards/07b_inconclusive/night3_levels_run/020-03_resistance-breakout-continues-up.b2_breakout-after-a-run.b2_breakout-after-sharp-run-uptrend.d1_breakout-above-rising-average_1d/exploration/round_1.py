import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    # drift per coin per horizon, on non-overlapping grid
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
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            brk = df.get("debug_info.components.break.last_history_value", pd.Series(np.nan, index=df.index)).values
            mad = df.get("debug_info.components.ma_dist.last_history_value", pd.Series(np.nan, index=df.index)).values
            n = len(df)
            # 60-bar return and 20-bar return
            seen = set()
            for t in range(n):
                if fc[t] <= 0:
                    continue
                cell = t // 5
                if cell in seen:
                    continue
                if t + 5 >= n:
                    continue
                seen.add(cell)
                r = {"coin": c, "window": w, "year": yr[t], "fc": fc[t], "brk": brk[t], "mad": mad[t],
                     "new": fc[t - 1] <= 0 if t > 0 else True,
                     "ret20": cl[t] / cl[t - 20] - 1 if t >= 20 else np.nan}
                for h in H:
                    if t + h < n:
                        r[f"u{h}"] = cl[t + h] / cl[t] - 1 - drift[(c, h)][0]
                        r[f"s{h}"] = r[f"u{h}"] / drift[(c, h)][1]
                    else:
                        r[f"u{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def summ(g):
        x = g["u5"].dropna()
        return pd.Series({"n": len(x), "mean_u5": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "median_u5": x.median(), "hit": (x > 0).mean()})

    out = {}
    out["all"] = summ(d)
    hz = {}
    for h in H:
        x = d[f"u{h}"].dropna()
        hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "strength": d[f"s{h}"].mean()}
    out["by_horizon"] = pd.DataFrame(hz).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fc_q"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_q"] = d.groupby("fc_q").apply(summ)
    d["mad_q"] = pd.qcut(d["mad"].rank(method="first"), 5, labels=False)
    out["by_mad_q"] = d.groupby("mad_q").apply(summ)
    out["mad_q_range"] = d.groupby("mad_q")["mad"].agg(["min", "max"])
    d["brk_q"] = pd.qcut(d["brk"].rank(method="first"), 5, labels=False)
    out["by_brk_q"] = d.groupby("brk_q").apply(summ)
    out["by_new"] = d.groupby("new").apply(summ)
    d["r20_q"] = pd.qcut(d["ret20"].rank(method="first"), 5, labels=False)
    out["by_ret20_q"] = d.groupby("r20_q").apply(summ)
    out["spearman_mad_u5"] = stats.spearmanr(d["mad"], d["u5"], nan_policy="omit")[0]
    out["spearman_brk_u5"] = stats.spearmanr(d["brk"], d["u5"], nan_policy="omit")[0]
    out["spearman_mad_u20"] = stats.spearmanr(d["mad"], d["u20"], nan_policy="omit")[0]
    out["u5_skew_kurt"] = pd.Series({"skew": d["u5"].skew(), "kurt": d["u5"].kurt(), "std": d["u5"].std(),
                                     "trim5_mean": stats.trim_mean(d["u5"].dropna(), 0.05)})
    return out
