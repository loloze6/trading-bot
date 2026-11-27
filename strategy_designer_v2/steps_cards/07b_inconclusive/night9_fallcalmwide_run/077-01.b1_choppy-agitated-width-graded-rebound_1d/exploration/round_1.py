def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        rets = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            rets.append(pd.Series(c[1:] / c[:-1] - 1))
        drift[coin] = pd.concat(rets).mean() if rets else np.nan
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            h = b["high"].astype(float).values
            l = b["low"].astype(float).values
            o = b["open"].astype(float).values
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            mr = pd.Series(rng).rolling(30, min_periods=30).mean().values
            width = rng / mr
            r1 = pd.Series(c).pct_change().values
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ris = (rng / c) / sd30
            f = b["forecast"].astype(float).values
            reg = b["regime"].astype(str).values
            n = len(c)
            for t in range(n):
                fw = {}
                for k in (1, 2, 3, 5):
                    fw[k] = c[t + k] / c[t] - 1 if t + k < n else np.nan
                rows.append(dict(coin=coin, w=w, t=t, f=f[t], reg=reg[t], loc=loc[t], width=width[t],
                                 ris=ris[t], prev=r1[t], dayret=c[t]/o[t]-1,
                                 r1=fw[1], r2=fw[2], r3=fw[3], r5=fw[5],
                                 year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                                 day=pd.Timestamp(b["timestamp"].iloc[t]).floor("D")))
    df = pd.DataFrame(rows)
    df["d"] = df["coin"].map(drift)
    for k in (1, 2, 3, 5):
        df[f"x{k}"] = df[f"r{k}"] - k * df["d"]
    out = {}
    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), mean=np.nan, t=np.nan))
        s = g.groupby("day")[col].apply(lambda v: (v - g[col].mean()).sum())
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=D, mean=g[col].mean(), t=g[col].mean() / se if se > 0 else np.nan))
    cases = df[df.f > 0].copy()
    out["cases_all_horizons"] = pd.DataFrame({k: summ(cases, f"x{k}") for k in (1, 2, 3, 5)}).T
    out["by_coin"] = cases.groupby("coin").apply(summ).round(4)
    out["by_window"] = cases.groupby("w").apply(summ).round(4)
    out["by_year"] = cases.groupby("year").apply(summ).round(4)
    cases["locq"] = pd.cut(cases["loc"], [0, 0.1, 0.2, 0.3, 0.5], include_lowest=True)
    out["by_close_loc"] = cases.groupby("locq").apply(summ).round(4)
    cases["wq"] = pd.qcut(cases["ris"], 4, labels=False, duplicates="drop")
    out["by_width_vs_swing_q"] = cases.groupby("wq").apply(summ).round(4)
    cases["fq"] = pd.qcut(cases["f"], 4, labels=False, duplicates="drop")
    out["by_forecast_q"] = cases.groupby("fq").apply(summ).round(4)
    cases["dayside"] = np.where(cases["dayret"] < 0, "down_day", "up_day")
    out["by_day_direction"] = cases.groupby("dayside").apply(summ).round(4)
    # mirror side: high closes in same regime, wide
    hi = df[(df.reg == "unknown") | False]
    # regime unknown only when close<0.5, so recompute high-close wide days elsewhere: all wide high-close days
    wide = df[(df.width >= 1)]
    out["wide_low_close_all_profiles"] = summ(wide[wide["loc"] < 0.5])
    out["wide_high_close_all_profiles_neg"] = summ(wide[wide["loc"] >= 0.5].assign(x1=lambda z: -z.x1))
    out["regime_counts"] = df["reg"].value_counts()
    out["corr_ris_x1_spearman"] = float(stats.spearmanr(cases["ris"], cases["x1"], nan_policy="omit")[0])
    out["corr_loc_x1_spearman"] = float(stats.spearmanr(cases["loc"], cases["x1"], nan_policy="omit")[0])
    return out
