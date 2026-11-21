def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20, 40]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            # 30d return recomputed
            r30 = np.full(n, np.nan); r30[30:] = c[30:] / c[:-30] - 1
            r90hi = pd.Series(c).rolling(90, min_periods=30).max().values
            fp = np.r_[0, f[:-1]]
            sig = (f <= -2) & (fp > -2)
            seen = set()
            for t in np.where(sig)[0]:
                cell = t // 20
                if cell in seen: continue
                if t + 20 >= n: continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "year": yr[t], "absf": -f[t], "r30": r30[t],
                     "fall30c": df["debug_info.components.fall30.post_pipeline_value"].values[t] if "debug_info.components.fall30.post_pipeline_value" in df else np.nan,
                     "brk": df["debug_info.components.break.last_history_value"].values[t] if "debug_info.components.break.last_history_value" in df else np.nan}
                for h in H:
                    if t + h < n:
                        tot = -(c[t + h] / c[t] - 1)
                        d[f"tot{h}"] = tot; d[f"un{h}"] = tot + drift[(coin, h)]
                        d[f"str{h}"] = d[f"un{h}"] / usual[(coin, h)]
                    else:
                        d[f"un{h}"] = np.nan; d[f"tot{h}"] = np.nan; d[f"str{h}"] = np.nan
                # signal-bar move (same-day)
                d["sigbar"] = c[t] / c[t - 1] - 1 if t > 0 else np.nan
                rows.append(d)
    C = pd.DataFrame(rows)
    def summ(g, col="un20"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean(), "tot20": g["tot20"].mean()})
    out = {}
    out["overall_by_h"] = pd.DataFrame({h: summ(C, f"un{h}") for h in H}).T
    out["strength_by_h"] = pd.Series({h: C[f"str{h}"].mean() for h in H})
    out["by_coin"] = C.groupby("coin").apply(summ)
    out["by_year"] = C.groupby("year").apply(summ)
    C["q_absf"] = pd.qcut(C["absf"].rank(method="first"), 4, labels=False)
    out["by_absf_q"] = C.groupby("q_absf").apply(summ)
    C["q_r30"] = pd.qcut(C["r30"].rank(method="first"), 4, labels=False)
    out["by_r30_q(0=deepest)"] = C.groupby("q_r30").apply(summ)
    C["q_brk"] = pd.qcut(C["brk"].rank(method="first"), 4, labels=False)
    out["by_brk_q"] = C.groupby("q_brk").apply(summ)
    out["spearman"] = pd.Series({"absf": stats.spearmanr(C.absf, C.un20, nan_policy="omit")[0],
                                 "r30": stats.spearmanr(C.r30, C.un20, nan_policy="omit")[0],
                                 "brk": stats.spearmanr(C.brk, C.un20, nan_policy="omit")[0]})
    out["sigbar_mean"] = C["sigbar"].mean()
    out["median_un20"] = C["un20"].median()
    return out
