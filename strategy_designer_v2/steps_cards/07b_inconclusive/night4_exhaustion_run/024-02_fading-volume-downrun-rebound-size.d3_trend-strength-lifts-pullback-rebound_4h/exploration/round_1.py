def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 12, 18, 36]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(cl)
            d = np.diff(f, prepend=0.0)
            # down streak length
            down = np.r_[False, cl[1:] < cl[:-1]]
            streak = np.zeros(n, int)
            for i in range(n):
                streak[i] = streak[i-1] + 1 if down[i] and i > 0 else 0
            r180 = pd.Series(cl).pct_change(180).values
            r30 = pd.Series(cl).pct_change(6*7).values
            seen = set()
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(n):
                if d[i] >= 2:
                    cell = i // 18
                    if cell in seen: continue
                    seen.add(cell)
                    row = dict(coin=c, window=w, year=yr[i], f=f[i], streak=streak[i],
                               r180=r180[i], r7=r30[i])
                    for h in H:
                        if i + h < n:
                            row[f"u{h}"] = (cl[i+h]/cl[i]-1) - drift[(c, h)]
                            row[f"s{h}"] = row[f"u{h}"] / usual[(c, h)]
                    rows.append(row)
    cs = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["overall"] = summ(cs)
    out["by_horizon"] = pd.DataFrame({h: summ(cs, f"u{h}") for h in H}).T
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_window"] = cs.groupby("window").apply(summ)
    cs["fq"] = pd.qcut(cs["f"].rank(method="first"), 4, labels=False)
    out["by_forecast_q"] = cs.groupby("fq").apply(summ)
    out["by_streak"] = cs.groupby(cs["streak"].clip(upper=5)).apply(summ)
    cs["r180q"] = pd.qcut(cs["r180"].rank(method="first"), 4, labels=False)
    out["by_r180_q"] = cs.groupby("r180q").apply(summ)
    cs["r7q"] = pd.qcut(cs["r7"].rank(method="first"), 4, labels=False)
    out["by_7d_ret_q"] = cs.groupby("r7q").apply(summ)
    out["by_r180q_h36"] = cs.groupby("r180q").apply(lambda g: summ(g, "u36"))
    out["by_streak_h36"] = cs.groupby(cs["streak"].clip(upper=5)).apply(lambda g: summ(g, "u36"))
    out["r180q_ranges"] = cs.groupby("r180q")["r180"].agg(["min", "max"])
    out["r7q_ranges"] = cs.groupby("r7q")["r7"].agg(["min", "max"])
    return out
