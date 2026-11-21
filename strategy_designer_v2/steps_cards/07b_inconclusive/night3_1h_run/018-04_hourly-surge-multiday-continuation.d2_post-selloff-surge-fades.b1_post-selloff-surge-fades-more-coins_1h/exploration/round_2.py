import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 120
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs.extend(c[idx + H] / c[idx] - 1)
        drift = np.mean(rs); sd = np.std(rs)
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.fall_depth.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            prevf = np.r_[0, f[:-1]]
            sig = (prevf - f) >= 2
            seen = set()
            for i in np.where(sig)[0]:
                cell = i // H
                if cell in seen or i + H >= n:
                    continue
                seen.add(cell)
                rows.append({"coin": coin, "year": ts.iloc[i].year, "f": f[i], "raw": raw[i],
                             "m": -(c[i + H] / c[i] - 1 - drift), "s": -(c[i + H] / c[i] - 1 - drift) / sd,
                             "wk": c[i - 24] / c[i - 192] - 1 if i >= 192 else np.nan,
                             "tr30": c[i] / c[i - 720] - 1 if i >= 720 else np.nan})
    d = pd.DataFrame(rows)
    def agg(g):
        x = g["m"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["s"].mean()})
    out = {}
    out["corr_f_m_spearman"] = pd.Series(stats.spearmanr(d["f"], d["m"], nan_policy="omit")[:2], index=["rho", "p"])
    out["corr_raw_m_spearman"] = pd.Series(stats.spearmanr(d["raw"], d["m"], nan_policy="omit")[:2], index=["rho", "p"])
    out["corr_wk_m_spearman"] = pd.Series(stats.spearmanr(d["wk"], d["m"], nan_policy="omit")[:2], index=["rho", "p"])
    d["rq"] = pd.qcut(d["raw"].rank(method="first"), 5, labels=False)
    out["by_raw_depth_q"] = d.groupby("rq").apply(agg)
    d["wq"] = pd.qcut(d["wk"].rank(method="first"), 5, labels=False)
    out["by_7d_return_q"] = d.groupby("wq").apply(agg)
    d["fh"] = d["f"] <= d["f"].median()
    yr = d.groupby(["year", "fh"])["m"].mean().unstack()
    yr["deep_minus_shallow"] = yr[True] - yr[False]
    out["depth_split_by_year"] = yr
    d["tr_up"] = d["tr30"] > 0
    out["depth_x_30d_trend"] = d.groupby(["tr_up", "fh"]).apply(agg)
    return out
