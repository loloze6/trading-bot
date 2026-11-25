import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 20
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = (np.mean(rets), np.std(rets, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            wt = df["debug_info.components.brk_runup.last_history_value"].values
            n = len(c)
            seen = set()
            for t in range(60, n):
                if c[t] > c[t - 60:t].max():
                    cell = t // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    R = c[t - 1] / c[t - 61] - 1 if t >= 61 else np.nan
                    rec = dict(coin=coin, w=w, t=t, day=str(df["timestamp"].iloc[t])[:10],
                               year=str(df["timestamp"].iloc[t])[:4], wt=wt[t], R=R,
                               brk=c[t] / c[t - 60:t].max() - 1)
                    for h in (5, 10, 20, 40):
                        rec[f"f{h}"] = c[t + h] / c[t] - 1 - drift[coin][0] * h / 20 if t + h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    out["n_cases"] = len(d)
    out["n_with_f20"] = int(d["f20"].notna().sum())
    dd = d.dropna(subset=["f20"])
    # slope of f20 on weight
    def slope_t(x, y):
        m = pd.notna(x) & pd.notna(y)
        if m.sum() < 5: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m])
        return (r.slope, r.slope / r.stderr, int(m.sum()))
    res = {}
    for h in (5, 10, 20, 40):
        s = slope_t(d["wt"], d[f"f{h}"])
        s2 = slope_t(d["R"], d[f"f{h}"])
        s3 = slope_t(d["brk"], d[f"f{h}"])
        y = d[f"f{h}"].dropna()
        res[h] = dict(slope_wt=s[0], t_wt=s[1], slope_R=s2[0], t_R=s2[1],
                      slope_brk=s3[0], t_brk=s3[1], mean_excess=y.mean(),
                      t_mean=y.mean() / (y.std(ddof=1) / np.sqrt(len(y))), n=len(y))
    out["by_horizon"] = pd.DataFrame(res).T
    dd = dd.copy()
    dd["wgrp"] = np.where(dd["wt"] > 0, "wt>0", "wt=0")
    try:
        dd["Rq"] = pd.qcut(dd["R"], 4, labels=["q1low", "q2", "q3", "q4high"])
    except Exception:
        dd["Rq"] = "na"
    agg = lambda g: pd.Series(dict(n=len(g), mean20=g["f20"].mean(),
                                    t=g["f20"].mean() / (g["f20"].std(ddof=1) / np.sqrt(len(g))) if len(g) > 1 else np.nan,
                                    hit=(g["f20"] > 0).mean(), meanR=g["R"].mean(), mean_wt=g["wt"].mean()))
    out["by_wgrp"] = dd.groupby("wgrp").apply(agg)
    out["by_Rquart"] = dd.groupby("Rq").apply(agg)
    out["by_coin"] = dd.groupby(["coin", "wgrp"]).apply(agg)
    out["by_year"] = dd.groupby(["year", "wgrp"]).apply(agg)
    dd["bq"] = pd.qcut(dd["brk"], 3, labels=["small", "mid", "large"])
    out["by_breaksize"] = dd.groupby("bq").apply(agg)
    out["wt_stats"] = dd["wt"].describe()
    out["corr_wt_R"] = float(dd[["wt", "R"]].corr().iloc[0, 1])
    return out
