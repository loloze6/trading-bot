import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 26
    rows = []
    allret = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        allret[coin] = (np.mean(rs), np.std(rs), len(rs))
    for coin, wins in bars.items():
        drift, sd, _ = allret[coin]
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            cf = df.get("debug_info.components.cloud_fall.post_pipeline_value")
            cv = df.get("debug_info.components.calm.post_pipeline_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for i in range(0, n, H):
                if not (f[i] < 0):
                    continue
                r = {}
                for h in (5, 10, 26, 40):
                    r[h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                # past 60-day return within window
                past = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                rows.append(dict(coin=coin, window=w, year=yr[i], f=f[i],
                                 g26=-(r[26] - drift) if not np.isnan(r[26]) else np.nan,
                                 g5=-r[5], g10=-r[10], g26raw=-r[26], g40=-r[40],
                                 str26=-(r[26] - drift) / sd if not np.isnan(r[26]) else np.nan,
                                 cf=cf.values[i] if cf is not None else np.nan,
                                 cv=cv.values[i] if cv is not None else np.nan,
                                 past60=past))
    d = pd.DataFrame(rows).dropna(subset=["g26"])
    def summ(g):
        x = g["g26"]
        return pd.Series({"n": len(x), "mean_gain": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean(), "raw_gain": g["g26raw"].mean()})
    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=["q1small", "q2", "q3", "q4large"])
    d["cfq"] = pd.qcut(d["cf"], 3, labels=["cf_lo", "cf_mid", "cf_hi"], duplicates="drop")
    d["cvq"] = pd.qcut(d["cv"], 3, labels=["cv_lo", "cv_mid", "cv_hi"], duplicates="drop")
    d["p60"] = pd.qcut(d["past60"], 3, labels=["p_lo", "p_mid", "p_hi"])
    hz = pd.DataFrame({h: [d[h].mean(), d[h].mean() / (d[h].std() / np.sqrt(d[h].notna().sum())), d[h].notna().sum()]
                       for h in ["g5", "g10", "g26raw", "g40"]}, index=["mean", "t", "n"]).T
    return {
        "all": summ(d),
        "by_coin": d.groupby("coin").apply(summ),
        "by_year": d.groupby("year").apply(summ),
        "by_fq": d.groupby("fq").apply(summ),
        "by_cloudfall_post": d.groupby("cfq").apply(summ),
        "by_calm_post": d.groupby("cvq").apply(summ),
        "by_past60": d.groupby("p60").apply(summ),
        "horizons_raw_short_gain": hz,
        "corr_absf_gain": stats.spearmanr(d["f"].abs(), d["g26"]).correlation,
        "coin_drift_sd": pd.DataFrame(allret, index=["drift26", "sd26", "n"]).T,
    }
