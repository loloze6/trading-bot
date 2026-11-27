def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    H = [1, 2, 3, 5, 10]
    # drift per coin per horizon, from the grid of every window
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            o = df["open"].values
            hi = df["high"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            raw = df.get("debug_info.components.depth.last_history_value")
            for i in range(0, n - 5, 5):
                if df["regime"].iloc[i] != "unknown":
                    continue
                f = df["forecast"].iloc[i]
                if not (f < 0):
                    continue
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "f": f, "raw": raw.iloc[i] if raw is not None else np.nan,
                     "up": c[i] > o[i], "pos": i / n}
                for h in H:
                    if i + h < n:
                        r["ex%d" % h] = c[i + h] / c[i] - 1 - drift[(coin, h)]
                        r["tot%d" % h] = c[i + h] / c[i] - 1
                # recent 20-bar return before the bar (in-window)
                if i >= 20:
                    r["ret20"] = c[i] / c[i - 20] - 1
                if i >= 5:
                    r["ret5"] = c[i] / c[i - 5] - 1
                rows.append(r)
    d = pd.DataFrame(rows)
    d["absf"] = d["f"].abs()
    d["terc"] = pd.qcut(d["absf"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])

    def summ(g, col="ex5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_short": -x.mean(), "t_short": -x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["by_horizon"] = pd.DataFrame({h: summ(d, "ex%d" % h) for h in H}).T
    out["by_horizon_terc"] = pd.DataFrame({(h, t): summ(d[d.terc == t], "ex%d" % h) for h in H for t in ["shallow", "mid", "deep"]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    out["by_upday_terc"] = d.groupby(["up", "terc"]).apply(summ)
    d["r20s"] = np.sign(d["ret20"])
    out["by_ret20sign_terc"] = d.dropna(subset=["ret20"]).groupby(["r20s", "terc"]).apply(summ)
    d["r5s"] = np.sign(d["ret5"])
    out["by_ret5sign_terc"] = d.dropna(subset=["ret5"]).groupby(["r5s", "terc"]).apply(summ)
    out["absf_quintile"] = d.groupby(pd.qcut(d["absf"].rank(method="first"), 5, labels=False)).apply(summ)
    out["absf_stats"] = d["absf"].describe()
    out["share_f_at_cap"] = float((d["absf"] >= 19.9).mean())
    return out
