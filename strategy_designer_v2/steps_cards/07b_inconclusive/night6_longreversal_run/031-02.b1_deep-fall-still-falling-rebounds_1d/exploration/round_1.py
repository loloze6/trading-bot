import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 30
    drift = {}; usual = {}
    for c, ws in bars.items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                rs.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs, ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            s90 = b.get("debug_info.components.fall90.last_history_value")
            s90 = s90.values if s90 is not None else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            ref = 0.0; used = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    ref = 0.0; continue
                if f[t] - ref >= 2:
                    ref = f[t]
                    cell = t // H
                    if cell in used or t + H >= len(b):
                        continue
                    used.add(cell)
                    r = {"coin": c, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                         "fc": f[t], "s90": s90[t],
                         "r30": cl[t] / cl[t - 30] - 1 if t >= 30 else np.nan}
                    for h in (5, 10, 20, 30):
                        r[f"x{h}"] = cl[t + h] / cl[t] - 1 - drift[c] * h / 30
                    r["tot30"] = cl[t + H] / cl[t] - 1
                    r["str"] = r["x30"] / usual[c]
                    rows.append(r)
            # horizons 45/60 where possible
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["x30"].sum()
        n = len(dd)
        t = dd.mean() / (dd.std(ddof=1) / np.sqrt(n)) if n > 1 else np.nan
        return pd.Series({"n": len(g), "days": n, "mean": g["x30"].mean(),
                          "median": g["x30"].median(), "hit": (g["x30"] > 0).mean(), "t_day": t})
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fc_q"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_fc_tercile"] = d.groupby("fc_q").apply(summ)
    d["s90_q"] = pd.qcut(d["s90"].rank(method="first"), 3, labels=["deepest", "mid", "shallow"])
    out["by_s90_tercile"] = d.groupby("s90_q").apply(summ)
    d["r30_q"] = pd.qcut(d["r30"].rank(method="first"), 3, labels=["r30_deep", "mid", "r30_small"])
    out["by_r30_tercile"] = d.groupby("r30_q").apply(summ)
    hz = {}
    for h in (5, 10, 20, 30):
        dd = d.groupby("day")[f"x{h}"].sum()
        hz[h] = {"mean": d[f"x{h}"].mean(), "t_day": dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd)))}
    out["by_horizon"] = pd.DataFrame(hz).T
    out["top5_share_of_sum"] = d["x30"].nlargest(5).sum() / d["x30"].sum()
    out["mean_without_top5"] = d["x30"].drop(d["x30"].nlargest(5).index).mean()
    out["spearman_fc_x30"] = stats.spearmanr(d["fc"], d["x30"]).correlation
    out["spearman_s90_x30"] = stats.spearmanr(d["s90"], d["x30"], nan_policy="omit").correlation
    out["spearman_r30_x30"] = stats.spearmanr(d["r30"], d["x30"], nan_policy="omit").correlation
    out["mean_strength"] = d["str"].mean()
    return out
