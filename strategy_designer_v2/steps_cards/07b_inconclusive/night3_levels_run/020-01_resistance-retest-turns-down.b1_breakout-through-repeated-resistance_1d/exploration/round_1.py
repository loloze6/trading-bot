import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20, 30]
    # normal drift per coin per horizon, non-overlapping grid
    drift, usual = {}, {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(list(cl[idx + h] / cl[idx] - 1))
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.break.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            cl = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            seen = set()
            for t in range(1, len(df)):
                if f[t] >= 2 and f[t - 1] < 2:
                    cell = t // 10
                    if cell in seen: continue
                    seen.add(cell)
                    r = {"coin": c, "window": w, "year": ts.iloc[t].year, "fc": f[t], "raw": raw[t]}
                    for h in H:
                        if t + h < len(cl):
                            r[f"ex{h}"] = cl[t + h] / cl[t] - 1 - drift[(c, h)]
                            r[f"tot{h}"] = cl[t + h] / cl[t] - 1
                    # past regime: 30-day and 90-day return before
                    r["past30"] = cl[t] / cl[t - 30] - 1 if t >= 30 else np.nan
                    r["sigbar"] = cl[t] / cl[t - 1] - 1
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="ex10"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"ex{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=False)
    out["by_fc_quart"] = d.groupby("fq").apply(summ)
    out["fc_range_by_q"] = d.groupby("fq")["fc"].agg(["min", "max"])
    d["pq"] = pd.qcut(d["past30"], 3, labels=False)
    out["by_past30_tercile"] = d.groupby("pq").apply(summ)
    out["past30_ranges"] = d.groupby("pq")["past30"].agg(["min", "max"])
    d["sq"] = pd.qcut(d["sigbar"], 3, labels=False)
    out["by_sigbar_tercile"] = d.groupby("sq").apply(summ)
    out["sigbar_ranges"] = d.groupby("sq")["sigbar"].agg(["min", "max", "mean"])
    out["raw_fc_corr"] = float(d[["raw", "fc"]].corr().iloc[0, 1]) if d["raw"].notna().any() else "na"
    out["spearman_fc_ex10"] = float(stats.spearmanr(d["fc"], d["ex10"], nan_policy="omit")[0])
    return out
