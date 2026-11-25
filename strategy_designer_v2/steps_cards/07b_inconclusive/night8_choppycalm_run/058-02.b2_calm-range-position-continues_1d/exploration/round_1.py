def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    drift = {h: {} for h in H}
    for coin, ws in bars.items():
        for h in H:
            allr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift[h][coin] = np.mean(allr) if allr else np.nan
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            hi = df["high"].rolling(20).max().values
            lo = df["low"].rolling(20).min().values
            pos = 2 * (c - lo) / (hi - lo) - 1
            reg = df["regime"].values
            fc = df["forecast"].values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            ret20 = df["close"].pct_change(20).values
            for i in range(0, len(c) - 5, 5):
                if reg[i] != "unknown" or fc[i] == 0:
                    continue
                r = {"coin": coin, "w": w, "day": day[i], "fc": fc[i], "pos": pos[i],
                     "ret20": ret20[i]}
                for h in H:
                    if i + h < len(c):
                        r["x%d" % h] = c[i + h] / c[i] - 1 - drift[h][coin]
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def slope_t(sub, col, xcol="fc"):
        s = sub.dropna(subset=[col, xcol])
        if len(s) < 10:
            return (np.nan, np.nan, len(s))
        x = s[xcol].values; y = s[col].values
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        g = pd.DataFrame({"d": s["day"].values, "u0": e, "u1": e * x}).groupby("d")[["u0", "u1"]].sum().values
        meat = g.T @ g
        V = XtXi @ meat @ XtXi
        return (b[1], b[1] / np.sqrt(V[1, 1]), len(s))
    out["by_horizon"] = pd.DataFrame({h: slope_t(d, "x%d" % h) for h in H}, index=["slope", "t", "n"]).T
    out["by_horizon_rawpos"] = pd.DataFrame({h: slope_t(d, "x%d" % h, "pos") for h in H}, index=["slope", "t", "n"]).T
    out["by_coin_5"] = pd.DataFrame({k: slope_t(g, "x5") for k, g in d.groupby("coin")}, index=["slope", "t", "n"]).T
    out["by_window_5"] = pd.DataFrame({k: slope_t(g, "x5") for k, g in d.groupby("w")}, index=["slope", "t", "n"]).T
    d["fq"] = pd.qcut(d["fc"], 5, labels=False, duplicates="drop")
    out["quintile"] = d.groupby("fq").agg(fc=("fc", "mean"), pos=("pos", "mean"), x1=("x1", "mean"),
        x3=("x3", "mean"), x5=("x5", "mean"), x10=("x10", "mean"), x20=("x20", "mean"), n=("x5", "count"))
    d["pq"] = pd.cut(d["pos"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["rawpos_bins"] = d.groupby("pq").agg(x1=("x1", "mean"), x3=("x3", "mean"), x5=("x5", "mean"),
        x10=("x10", "mean"), x20=("x20", "mean"), n=("x5", "count"))
    d["side"] = np.sign(d["fc"])
    out["side_signed5"] = d.assign(sx=d["side"] * d["x5"]).groupby("side").agg(
        m=("sx", "mean"), sd=("sx", "std"), n=("sx", "count"))
    d["year"] = pd.to_datetime(d["day"]).dt.year
    out["by_year_5"] = pd.DataFrame({k: slope_t(g, "x5") for k, g in d.groupby("year")}, index=["slope", "t", "n"]).T
    out["corr_fc_pos"] = float(d[["fc", "pos"]].corr().iloc[0, 1])
    return out
