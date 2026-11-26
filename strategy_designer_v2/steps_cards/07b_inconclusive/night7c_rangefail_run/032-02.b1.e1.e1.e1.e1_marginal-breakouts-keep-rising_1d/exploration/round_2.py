import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20, 40]
    col = "debug_info.components.margin.last_history_value"
    drift = {}
    usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs) if rs else np.nan
    rows = []
    colinfo = {"windows_with_col": 0, "windows_total": 0}
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            colinfo["windows_total"] += 1
            cl = df["close"].values.astype(float)
            n = len(cl)
            s = pd.Series(cl)
            hi = s.shift(1).rolling(60, min_periods=20).max()
            lo = s.shift(1).rolling(60, min_periods=20).min()
            mcomp = ((s / hi - 1) * 100).values
            if col in df.columns:
                colinfo["windows_with_col"] += 1
                mrec = pd.to_numeric(df[col], errors="coerce").values
            else:
                mrec = np.full(n, np.nan)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0).values
            fprev = np.r_[0, f[:-1]]
            width = (hi / lo - 1).values
            r60 = (s / s.shift(min(60, n - 1)) - 1).values
            r1 = s.pct_change()
            vol20 = r1.rolling(20).std().values
            for g in range(0, n, 20):
                idx = [i for i in range(g, min(g + 20, n)) if f[i] - fprev[i] >= 2 and f[i] > 0]
                if not idx:
                    continue
                t = idx[0]
                m = mrec[t] if not np.isnan(mrec[t]) else mcomp[t]
                row = dict(coin=c, win=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                           margin=m, mrec=mrec[t], mcomp=mcomp[t], fc=f[t], width=width[t], r60=r60[t],
                           mvol=(m / 100 / vol20[t]) if (vol20[t] and not np.isnan(vol20[t])) else np.nan)
                for h in H:
                    row[f"x{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                    row[f"z{h}"] = row[f"x{h}"] / usual[(c, h)]
                rows.append(row)
    d = pd.DataFrame(rows)
    out = {"colinfo": pd.Series(colinfo), "n_cases": len(d)}
    out["margin_desc"] = d[["margin", "mrec", "mcomp", "fc"]].describe()
    def tt(a, b):
        a = a.dropna(); b = b.dropna()
        return stats.ttest_ind(a, b, equal_var=False).statistic
    d20 = d[d.x20.notna()].copy()
    med = d20["margin"].median()
    sm = d20["margin"] <= med
    rr = []
    for h in H:
        k = f"x{h}"
        x = d[k].dropna()
        smh = d["margin"] <= d.loc[d[k].notna(), "margin"].median()
        rr.append(dict(h=h, n=len(x), mean=x.mean(), t1=x.mean() / x.std() * np.sqrt(len(x)),
                       small=d.loc[smh, k].mean(), large=d.loc[~smh, k].mean(),
                       welch=tt(d.loc[smh, k], d.loc[~smh, k]),
                       spear=stats.spearmanr(d["margin"], d[k], nan_policy="omit").correlation))
    out["by_horizon"] = pd.DataFrame(rr)
    d["mq"] = pd.qcut(d["margin"].rank(method="first"), 5, labels=False)
    out["by_margin_q"] = d.groupby("mq").agg(n=("x20", "count"), m=("margin", "mean"), x10=("x10", "mean"),
                                            x20=("x20", "mean"), sd20=("x20", "std"), x40=("x40", "mean"))
    def grp(g):
        return pd.Series(dict(n=g.x20.notna().sum(), x20=g.x20.mean(),
                              t=g.x20.mean() / g.x20.std() * np.sqrt(max(g.x20.notna().sum(), 1)),
                              sp=stats.spearmanr(g.margin, g.x20, nan_policy="omit").correlation))
    out["by_coin"] = d.groupby("coin").apply(grp)
    out["by_year"] = d.groupby("year").apply(grp)
    out["by_window"] = d.groupby("win").apply(grp)
    dw = d.dropna(subset=["width"]).copy()
    dw["wq"] = pd.qcut(dw["width"].rank(method="first"), 3, labels=["narrow", "mid", "wide"])
    out["by_width"] = dw.groupby("wq").apply(lambda g: pd.Series(dict(n=g.x20.notna().sum(), width=g.width.mean(),
            x20=g.x20.mean(), t=g.x20.mean() / g.x20.std() * np.sqrt(g.x20.notna().sum()), x40=g.x40.mean(),
            sp20=stats.spearmanr(g.margin, g.x20, nan_policy="omit").correlation)))
    out["spear_width_x20"] = stats.spearmanr(dw.width, dw.x20, nan_policy="omit").correlation
    out["spear_mvol_x20"] = stats.spearmanr(d.mvol, d.x20, nan_policy="omit").correlation
    return out
