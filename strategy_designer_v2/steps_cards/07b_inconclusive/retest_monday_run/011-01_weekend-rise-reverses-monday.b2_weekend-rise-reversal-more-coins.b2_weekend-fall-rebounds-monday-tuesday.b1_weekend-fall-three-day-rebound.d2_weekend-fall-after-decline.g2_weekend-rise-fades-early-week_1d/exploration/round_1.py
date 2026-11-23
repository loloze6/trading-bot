import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon: non-overlapping grid per window, pooled
        drift = {}
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.nanmean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            r = pd.Series(c).pct_change()
            vol = r.rolling(20).std()
            sc = (r / vol).values
            fc = df["forecast"].values
            wd = ts.dt.weekday.values
            yr = ts.dt.year.values
            n = len(c)
            for t in range(n):
                if t + 3 >= n or np.isnan(sc[t]):
                    continue
                rec = {"coin": coin, "w": w, "yr": yr[t], "wd": wd[t], "sc": sc[t], "fc": fc[t]}
                for h in H:
                    rec[f"f{h}"] = (c[t + h] / c[t] - 1 - drift[h]) if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def summ(g, col="f3", sign=-1):
        x = sign * g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    sun = d[(d.wd == 6) & (d.fc < 0)].copy()
    sun["af"] = -sun.fc
    sun["q"] = pd.qcut(sun.af.rank(method="first"), 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out = {}
    out["sun_rise_by_forecast_quintile"] = sun.groupby("q").apply(summ)
    out["sun_rise_af_mean_by_q"] = sun.groupby("q")["af"].mean()
    out["sun_rise_by_year"] = sun.groupby("yr").apply(summ)
    out["sun_rise_by_coin"] = sun.groupby("coin").apply(summ)
    out["sun_rise_by_horizon"] = pd.DataFrame({f"h{h}": summ(sun, f"f{h}") for h in H}).T
    # rises on each weekday (scaled return > 0), 3-day shortfall, short direction
    rises = d[d.sc > 0].copy()
    out["rise_by_weekday_f3"] = rises.groupby("wd").apply(summ)
    falls = d[d.sc < 0].copy()
    out["fall_by_weekday_f3_long"] = falls.groupby("wd").apply(lambda g: summ(g, "f3", 1))
    # within Sunday rises: by raw scaled-return bins
    sun["scb"] = pd.cut(sun.sc, [0, 0.5, 1, 1.5, 2, 3, 100])
    out["sun_rise_by_scaled_bin"] = sun.groupby("scb").apply(summ)
    # share of mean carried by top 5% outliers
    x = -sun.f3
    out["sun_trimmed_mean%_5pct"] = 100 * stats.trim_mean(x.dropna(), 0.05)
    out["sun_median%"] = 100 * x.median()
    out["sun_share_positive"] = (x > 0).mean()
    return out
