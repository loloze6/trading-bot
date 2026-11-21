def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20]
    drift = {}; usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            r30 = np.full(n, np.nan); r30[30:] = c[30:] / c[:-30] - 1
            r90 = np.full(n, np.nan); r90[90:] = c[90:] / c[:-90] - 1
            ma = pd.Series(c).rolling(120, min_periods=60).mean().values
            fp = np.r_[0, f[:-1]]
            sig = (f <= -2) & (fp > -2)
            for h in H:
                seen = set()
                for t in np.where(sig)[0]:
                    cell = t // h
                    if cell in seen or t + h >= n: continue
                    seen.add(cell)
                    tot = -(c[t + h] / c[t] - 1)
                    rows.append({"h": h, "coin": coin, "win": w, "year": yr[t], "r30": r30[t], "r90": r90[t],
                                 "belowma": c[t] < ma[t] if not np.isnan(ma[t]) else np.nan,
                                 "tot": tot, "un": tot + drift[(coin, h)], "str": (tot + drift[(coin, h)]) / usual[(coin, h)]})
    C = pd.DataFrame(rows)
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "un": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "tot": g["tot"].mean(), "str": g["str"].mean()})
    out = {}
    out["by_h_gridded_per_h"] = C.groupby("h").apply(summ)
    C10 = C[C.h == 10].copy()
    out["h10_by_coin"] = C10.groupby("coin").apply(summ)
    out["h10_by_year"] = C10.groupby("year").apply(summ)
    C10["q_r30"] = pd.qcut(C10["r30"].rank(method="first"), 4, labels=False)
    out["h10_by_r30_q(0=deepest)"] = C10.groupby("q_r30").apply(summ)
    out["h10_spearman_r30_un"] = stats.spearmanr(C10.r30, C10.un, nan_policy="omit")[0]
    out["h10_by_r90_sign(True=neg)"] = C10.groupby(C10.r90 < 0).apply(summ)
    out["h10_by_belowma120"] = C10.dropna(subset=["belowma"]).groupby("belowma").apply(summ)
    loyo = {}
    for y in sorted(C10.year.unique()):
        x = C10[C10.year != y]["un"]
        loyo[y] = x.mean() / (x.std() / np.sqrt(len(x)))
    out["h10_t_leave_one_year_out"] = pd.Series(loyo)
    C20 = C[C.h == 20]
    out["h20_by_r90_sign(True=neg)"] = C20.groupby(C20.r90 < 0).apply(summ)
    return out
