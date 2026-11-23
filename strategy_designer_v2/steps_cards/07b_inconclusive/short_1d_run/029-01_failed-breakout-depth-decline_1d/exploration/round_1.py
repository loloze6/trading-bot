import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rawc = "debug_info.components.failed_breakout_depth.last_history_value"
    H = [1, 3, 5, 10, 20]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            raw = df[rawc].values.astype(float) if rawc in df else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for h in H:
                for t in range(0, n - h, h):
                    r = c[t + h] / c[t] - 1
                    r20 = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                    r1 = c[t] / c[t - 1] - 1 if t >= 1 else np.nan
                    rows.append((coin, w, h, int(ts[t].year), f[t], raw[t], r, r20, r1))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "year", "f", "raw", "r", "r20", "r1"])
    d["drift"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["ex"] = -(d["r"] - d["drift"])   # short direction
    d["tot"] = -d["r"]
    d["sit"] = d["f"] < 0

    def summ(g):
        x = g["ex"].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "mean_tot": g["tot"].mean()})
    out = {}
    out["by_horizon_sit"] = d[d.sit].groupby("h").apply(summ)
    # compare: down days not in situation
    dd = d[(~d.sit) & (d.r1 < 0)]
    out["by_horizon_other_downdays"] = dd.groupby("h").apply(summ)
    s5 = d[(d.h == 5) & d.sit].copy()
    out["h5_by_coin"] = s5.groupby("coin").apply(summ)
    out["h5_by_year"] = s5.groupby("year").apply(summ)
    s5["depthq"] = pd.qcut(s5["f"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h5_by_forecast_tercile"] = s5.groupby("depthq").apply(summ)
    s5["rawq"] = pd.qcut(s5["raw"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h5_by_rawdepth_tercile"] = s5.groupby("rawq").apply(summ)
    s5["trend"] = np.where(s5["r20"] > 0, "up20", np.where(s5["r20"] <= 0, "down20", "na"))
    out["h5_by_20d_trend"] = s5.groupby("trend").apply(summ)
    s10 = d[(d.h == 10) & d.sit].copy()
    s10["trend"] = np.where(s10["r20"] > 0, "up20", np.where(s10["r20"] <= 0, "down20", "na"))
    out["h10_by_20d_trend"] = s10.groupby("trend").apply(summ)
    for h in [5, 10]:
        x = d[(d.h == h) & d.sit].dropna(subset=["raw"])
        rho, p = stats.spearmanr(x["raw"].abs(), x["ex"])
        out[f"spearman_rawdepth_ex_h{h}"] = f"rho={rho:.3f} p={p:.3f} n={len(x)}"
    return out
