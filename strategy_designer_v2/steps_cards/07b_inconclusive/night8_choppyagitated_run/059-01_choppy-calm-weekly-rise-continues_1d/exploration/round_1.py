def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 7, 14]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            raw = df.get("debug_info.components.scaled_week_rise.last_history_value")
            for i in range(0, n, 7):
                reg = df["regime"].iloc[i]
                if reg != "unknown":
                    continue
                r7 = c[i] / c[i - 7] - 1 if i >= 7 else np.nan
                rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                           day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                           fc=df["forecast"].iloc[i],
                           raw=raw.iloc[i] if raw is not None else np.nan, r7=r7)
                for h in H:
                    if i + h < n:
                        rec[f"ex{h}"] = c[i + h] / c[i] - 1 - drift[(coin, h)][0]
                        rec[f"tot{h}"] = c[i + h] / c[i] - 1
                    else:
                        rec[f"ex{h}"] = np.nan
                        rec[f"tot{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    pos = d[d.fc > 0].dropna(subset=["ex7"])
    def slope_t(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        if m.sum() < 5: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m])
        return (r.slope, r.slope / r.stderr, int(m.sum()))
    res = {}
    for h in H:
        p = d[d.fc > 0].dropna(subset=[f"ex{h}"])
        s, t, n = slope_t(p.fc.values, p[f"ex{h}"].values)
        res[f"h{h}"] = dict(slope=s, t=t, n=n, mean_ex=p[f"ex{h}"].mean(),
                            t_mean=p[f"ex{h}"].mean() / (p[f"ex{h}"].std() / np.sqrt(len(p))),
                            mean_tot=p[f"tot{h}"].mean())
    out["pos cases by horizon"] = pd.DataFrame(res).T
    # by coin
    g = {}
    for k, p in pos.groupby("coin"):
        s, t, n = slope_t(p.fc.values, p.ex7.values)
        g[k] = dict(n=n, slope_t=t, mean_ex=p.ex7.mean(), mean_tot=p.tot7.mean())
    out["by coin h7"] = pd.DataFrame(g).T
    g = {}
    for k, p in pos.groupby("year"):
        s, t, n = slope_t(p.fc.values, p.ex7.values)
        g[k] = dict(n=n, slope_t=t, mean_ex=p.ex7.mean())
    out["by year h7"] = pd.DataFrame(g).T
    pos = pos.copy()
    pos["q"] = pd.qcut(pos.fc.rank(method="first"), 4, labels=False)
    out["by forecast quartile h7"] = pos.groupby("q").agg(n=("ex7", "size"), fc=("fc", "mean"),
        ex7=("ex7", "mean"), ex3=("ex3", "mean"), ex14=("ex14", "mean"))
    # all profile grid cases, including falls, graded by raw scaled return
    a = d.dropna(subset=["ex7", "raw"]).copy()
    a["q"] = pd.qcut(a.raw.rank(method="first"), 5, labels=False)
    out["all profile cases by raw quintile"] = a.groupby("q").agg(n=("ex7", "size"), raw=("raw", "mean"),
        ex3=("ex3", "mean"), ex7=("ex7", "mean"), ex14=("ex14", "mean"))
    s, t, n = slope_t(a.raw.values, a.ex7.values)
    out["all profile slope raw->ex7"] = f"slope {s:.4g} t {t:.2f} n {n}"
    out["raw>0 vs fc>0 counts"] = f"raw>0 {int((a.raw>0).sum())}, fc>0 {int((d.fc>0).sum())}, grid profile {len(d)}"
    return out
