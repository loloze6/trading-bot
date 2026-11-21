def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.beyond_high.post_pipeline_value"
    H = 20
    # coin mean H-bar return over all windows on grid
    drift = {}
    for c, ws in bars.items():
        r = []
        for w, df in ws.items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                r.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(r)
    grid = []
    ev = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df[col].fillna(0).values if col in df else df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            for i in range(0, n - H, H):
                if f[i] > 0:
                    a = cl[i + H] / cl[i] - 1 - drift[c]
                    grid.append((c, w, yr[i], f[i], a, f[i] * a))
            # entry events: forecast from 0 to >0
            for i in range(1, n):
                if f[i] > 0 and f[i - 1] <= 0:
                    row = {"coin": c, "yr": yr[i], "f": f[i]}
                    for h in (5, 10, 20, 40):
                        if i + h < n:
                            row[f"a{h}"] = cl[i + h] / cl[i] - 1 - drift[c] * h / H
                    # bars forecast stays positive
                    j = i
                    while j < n and f[j] > 0:
                        j += 1
                    row["run"] = j - i
                    ev.append(row)
    g = pd.DataFrame(grid, columns=["coin", "w", "yr", "f", "a", "p"])
    e = pd.DataFrame(ev)
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})
    out = {}
    out["grid_overall"] = pd.DataFrame({"a": tt(g.a), "p": tt(g.p)})
    out["grid_by_coin"] = g.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "mean_a": d.a.mean(), "mean_p": d.p.mean(), "mean_f": d.f.mean()}))
    g["fq"] = pd.qcut(g.f.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["grid_by_ftercile"] = g.groupby("fq").agg(n=("a", "size"), mean_a=("a", "mean"), med_a=("a", "median"), mean_p=("p", "mean"), mean_f=("f", "mean"))
    out["grid_p_top5_share"] = float(g.p.sort_values().head(5).sum() / g.p.sum()) if g.p.sum() != 0 else float(g.p.sort_values().head(5).sum())
    out["grid_by_year"] = g.groupby("yr").agg(n=("a", "size"), mean_a=("a", "mean"))
    out["events_overall"] = pd.DataFrame({h: tt(e[f"a{h}"]) for h in (5, 10, 20, 40)})
    out["events_by_coin_a20"] = e.groupby("coin")["a20"].apply(lambda x: tt(x)).unstack()
    out["events_by_year_a20"] = e.groupby("yr")["a20"].apply(lambda x: tt(x)).unstack()
    e["fq"] = pd.qcut(e.f.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["events_by_ftercile"] = e.groupby("fq").agg(n=("a20", "size"), a5=("a5", "mean"), a20=("a20", "mean"), a40=("a40", "mean"), f=("f", "mean"))
    out["event_run_len"] = e["run"].describe()
    out["events_corr_f_a20_spearman"] = float(stats.spearmanr(e.f, e.a20, nan_policy="omit")[0])
    return out
