import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in [1, 3]:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.nanmean(rr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            r = pd.Series(c).pct_change()
            vol = r.rolling(20).std()
            sc = (r / vol).values
            r2 = pd.Series(c).pct_change(2)
            sc2 = (r2 / (vol * np.sqrt(2))).values
            v = df["volume"].astype(float)
            vrel = (v / v.shift(1).rolling(20).mean()).values
            vrel2 = ((v + v.shift(1)) / 2 / v.shift(2).rolling(20).mean()).values
            wd = ts.dt.weekday.values
            yr = ts.dt.year.values
            n = len(c)
            for t in range(n):
                if t + 3 >= n or np.isnan(sc[t]):
                    continue
                rows.append({"coin": coin, "w": w, "yr": yr[t], "wd": wd[t], "sc": sc[t],
                             "sc2": sc2[t], "vrel": vrel[t], "vrel2": vrel2[t],
                             "f1": c[t+1]/c[t]-1-drift[1], "f3": c[t+3]/c[t]-1-drift[3]})
    d = pd.DataFrame(rows)

    def summ(g, col="f3"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(),
                          "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    sun = d[d.wd == 6].copy()
    # reversal in move direction: -sign(sc)*f3
    sun["rev3"] = -np.sign(sun.sc) * sun.f3
    sun["rev3_2d"] = -np.sign(sun.sc2) * sun.f3
    sun["absq"] = pd.qcut(sun.sc.abs().rank(method="first"), 5, labels=list("12345"))
    out["sun_rev3_by_abs_sc_quintile"] = sun.groupby("absq").apply(lambda g: summ(g, "rev3"))
    sun["abs2q"] = pd.qcut(sun.sc2.abs().rank(method="first"), 5, labels=list("12345"))
    out["sun_rev3_2day_by_abs_sc2_quintile"] = sun.groupby("abs2q").apply(lambda g: summ(g, "rev3_2d"))
    s = sun.dropna(subset=["vrel"])
    s["vq"] = pd.qcut(s.vrel.rank(method="first"), 5, labels=list("12345"))
    out["sun_rev3_by_sunday_volume_quintile(1=low)"] = s.groupby("vq").apply(lambda g: summ(g, "rev3"))
    s2 = sun.dropna(subset=["vrel2"])
    s2["vq2"] = pd.qcut(s2.vrel2.rank(method="first"), 5, labels=list("12345"))
    out["sun_rev3_2d_by_weekend_volume_quintile(1=low)"] = s2.groupby("vq2").apply(lambda g: summ(g, "rev3_2d"))
    # all Sundays unconditional f3 (is Monday-Tuesday just a Sunday-close drift?)
    out["sun_all_f3_unsigned"] = summ(sun, "f3")
    out["sun_rise_vs_fall_f3_raw"] = sun.groupby(np.sign(sun.sc)).apply(lambda g: summ(g, "f3"))
    # correlations
    out["corr_sc_f3_sun"] = stats.pearsonr(sun.sc, sun.f3)[0]
    out["corr_sc2_f3_sun"] = stats.pearsonr(sun.dropna(subset=["sc2"]).sc2, sun.dropna(subset=["sc2"]).f3)[0]
    out["corr_sc_f3_otherdays"] = stats.pearsonr(d[d.wd != 6].sc, d[d.wd != 6].f3)[0]
    # rev by sign of 2-day weekend move by year
    out["sun_rev3_2d_by_year"] = sun.groupby("yr").apply(lambda g: summ(g, "rev3_2d"))
    out["sun_rev3_by_year"] = sun.groupby("yr").apply(lambda g: summ(g, "rev3"))
    return out
