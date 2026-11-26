import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20, 40]
    # coin drift per horizon: non-overlapping grid over all windows
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            m = df["debug_info.components.margin.last_history_value"].values.astype(float)
            n = len(cl)
            # range descriptors from prices (within window)
            s = pd.Series(cl)
            r60 = (s / s.shift(60) - 1).values
            hi = s.shift(1).rolling(60).max(); lo = s.shift(1).rolling(60).min()
            width = (hi / lo - 1).values
            r1 = (s / s.shift(1) - 1).values
            vol20 = pd.Series(r1).rolling(20).std().values
            for g in range(0, n, 20):
                idx = [i for i in range(g, min(g + 20, n)) if not np.isnan(m[i]) and m[i] > 0]
                if not idx:
                    continue
                t = idx[0]
                row = dict(coin=c, win=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                           margin=m[t], r60=r60[t], width=width[t], vol20=vol20[t],
                           mvol=m[t] / 100 / vol20[t] if vol20[t] and not np.isnan(vol20[t]) else np.nan)
                for h in H:
                    row[f"x{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                rows.append(row)
    d = pd.DataFrame(rows)
    out = {}
    out["n_cases"] = len(d)
    out["margin_desc"] = d["margin"].describe()
    def tt(a, b):
        a = a.dropna(); b = b.dropna()
        return stats.ttest_ind(a, b, equal_var=False).statistic
    med = d["margin"].median()
    sm = d["margin"] <= med
    rr = []
    for h in H:
        k = f"x{h}"
        rr.append(dict(h=h, n=d[k].notna().sum(), mean=d[k].mean(), t1=d[k].mean()/d[k].std()*np.sqrt(d[k].notna().sum()),
                       small=d.loc[sm, k].mean(), large=d.loc[~sm, k].mean(), welch=tt(d.loc[sm, k], d.loc[~sm, k]),
                       spear=stats.spearmanr(d["margin"], d[k], nan_policy="omit").correlation))
    out["by_horizon"] = pd.DataFrame(rr)
    d["mq"] = pd.qcut(d["margin"], 5, labels=False)
    out["x20_by_margin_q"] = d.groupby("mq").agg(n=("x20", "count"), m=("margin", "mean"), x20=("x20", "mean"), x10=("x10", "mean"), x40=("x40", "mean"))
    d["mvq"] = pd.qcut(d["mvol"], 5, labels=False)
    out["x20_by_margin_over_vol_q"] = d.groupby("mvq").agg(n=("x20", "count"), x20=("x20", "mean"), x40=("x40", "mean"))
    out["by_coin"] = d.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g), x20=g.x20.mean(), sp=stats.spearmanr(g.margin, g.x20, nan_policy="omit").correlation)))
    out["by_year"] = d.groupby("year").apply(lambda g: pd.Series(dict(n=len(g), x20=g.x20.mean(), sp=stats.spearmanr(g.margin, g.x20, nan_policy="omit").correlation)))
    # trendless vs trending: prior 60-day range width
    d["wq"] = pd.qcut(d["width"], 3, labels=["narrow", "mid", "wide"])
    out["by_width"] = d.groupby("wq").apply(lambda g: pd.Series(dict(n=len(g), width=g.width.mean(), x20=g.x20.mean(), x40=g.x40.mean(),
            sp20=stats.spearmanr(g.margin, g.x20, nan_policy="omit").correlation, sp40=stats.spearmanr(g.margin, g.x40, nan_policy="omit").correlation)))
    d["tq"] = pd.qcut(d["r60"], 3, labels=["low", "mid", "high"])
    out["by_r60"] = d.groupby("tq").apply(lambda g: pd.Series(dict(n=len(g), r60=g.r60.mean(), x20=g.x20.mean(), x40=g.x40.mean(),
            sp20=stats.spearmanr(g.r60, g.x20, nan_policy="omit").correlation)))
    out["spear_r60_x20"] = stats.spearmanr(d.r60, d.x20, nan_policy="omit").correlation
    out["spear_width_x20"] = stats.spearmanr(d.width, d.x20, nan_policy="omit").correlation
    return out
