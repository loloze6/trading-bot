import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 26
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        drift[coin] = (np.mean(rs), np.std(rs))
    rows = []
    for coin, wins in bars.items():
        dr, sd = drift[coin]
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            lo = df["low"].values; hi = df["high"].values
            cf = df.get("debug_info.components.cloud_fall.post_pipeline_value")
            cfr = df.get("debug_info.components.cloud_fall.last_history_value")
            cv = df.get("debug_info.components.calm.post_pipeline_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for i in range(0, n - H, H):
                if not (f[i] < 0):
                    continue
                past26 = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                rows.append(dict(coin=coin, year=yr[i], f=f[i],
                                 g26=-(c[i + H] / c[i] - 1 - dr), raw=-(c[i + H] / c[i] - 1),
                                 cf=cf.values[i] if cf is not None else np.nan,
                                 cfr=cfr.values[i] if cfr is not None else np.nan,
                                 cv=cv.values[i] if cv is not None else np.nan,
                                 past26=past26))
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["g26"]
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "raw": g["raw"].mean()})
    d["cfq"] = pd.qcut(d["cf"], 3, labels=["gentle", "mid", "steep"])
    d["bear"] = np.where(d["year"].isin([2018, 2019, 2022, 2025]), "y18_19_22_25", "other")
    d["p26"] = pd.qcut(d["past26"], 3, labels=["p_lo", "p_mid", "p_hi"])
    out = {
        "spearman_cf_gain": pd.Series({"rho": stats.spearmanr(d["cf"], d["g26"], nan_policy="omit").correlation,
                                       "rho_cv": stats.spearmanr(d["cv"], d["g26"], nan_policy="omit").correlation,
                                       "rho_absf": stats.spearmanr(d["f"].abs(), d["g26"]).correlation}),
        "cf_by_coin": d.groupby(["coin", "cfq"]).apply(summ).unstack()["mean"],
        "cf_by_yeargroup": d.groupby(["bear", "cfq"]).apply(summ),
        "cf_rawslope_by_q": d.groupby("cfq")["cfr"].describe()[["mean", "min", "max"]],
        "by_past26": d.groupby("p26").apply(summ),
        "cf_x_cv": d.groupby(["cfq", pd.qcut(d["cv"], 2, labels=["cv_lo", "cv_hi"])]).apply(summ),
    }
    return out
