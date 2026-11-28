import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in (1, 3, 5)}
        for w, df in ws.items():
            c = df["close"].values
            n = len(c)
            for h in (1, 3, 5):
                idx = np.arange(0, n - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: (np.mean(allr[h]), np.std(allr[h])) for h in allr}
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            hi30 = c.rolling(30, min_periods=30).max()
            pbelow = (hi30 - c) / hi30 * 100
            prox = 1 / (1 + pbelow)
            reg = df["regime"].astype(str)
            inprof = reg != "chop"
            n = len(df)
            for t in range(0, n - 1):
                if not inprof.iloc[t] or pd.isna(r1.iloc[t]) or pd.isna(prox.iloc[t]):
                    continue
                rec = {"coin": coin, "w": w, "t": t, "r1": r1.iloc[t], "pbelow": pbelow.iloc[t],
                       "fc": df["forecast"].iloc[t], "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                for h in (1, 3, 5):
                    if t + h < n:
                        rec[f"f{h}"] = c.iloc[t + h] / c.iloc[t] - 1 - drift[coin][h][0]
                    else:
                        rec[f"f{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    out["profile_days_by_coin"] = d.groupby("coin").size()
    up = d[d.r1 > 0].copy()
    # one per 3-bar grid
    up3 = up[up.t % 3 == 0]
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_short": -x.mean(), "t_short": -x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    up["pq"] = pd.qcut(up.pbelow, 4, labels=["near_high", "q2", "q3", "deep"])
    up3 = up[up.t % 3 == 0]
    out["up_by_proximity_f3_grid"] = up3.groupby("pq").apply(lambda g: summ(g, "f3"))
    out["up_by_proximity_f1_all"] = up.groupby("pq").apply(lambda g: summ(g, "f1"))
    out["up_by_coin_f3_grid"] = up3.groupby("coin").apply(lambda g: summ(g, "f3"))
    out["up_by_year_f3_grid"] = up3.groupby("year").apply(lambda g: summ(g, "f3"))
    # brief's own: size of day's rise -> next day
    up["rq"] = pd.qcut(up.r1, 4, labels=["small", "r2", "r3", "large"])
    out["up_by_rise_f1_all"] = up.groupby("rq").apply(lambda g: summ(g, "f1"))
    out["up_by_rise_f3_grid"] = up[up.t % 3 == 0].groupby("rq").apply(lambda g: summ(g, "f3"))
    # regressions of fwd on proximity and on r1
    res = {}
    for col, g in (("f1", up), ("f3", up3), ("f5", up[up.t % 5 == 0])):
        x = g.dropna(subset=[col])
        s1 = stats.linregress(-x.pbelow, x[col]); s2 = stats.linregress(x.r1, x[col])
        res[col] = {"n": len(x), "slope_t_on_proximity(neg pbelow)": s1.slope / s1.stderr,
                    "slope_t_on_r1": s2.slope / s2.stderr}
    out["regressions_up"] = pd.DataFrame(res).T
    # all profile days: r1 -> f1 (two-way fade)
    x = d.dropna(subset=["f1"])
    s = stats.linregress(x.r1, x.f1)
    out["all_profile_r1_to_f1"] = pd.Series({"n": len(x), "slope": s.slope, "t": s.slope / s.stderr})
    out["drift"] = pd.DataFrame({c: {f"mean{h}": v[h][0] for h in v} | {f"sd{h}": v[h][1] for h in v} for c, v in drift.items()}).T
    return out
