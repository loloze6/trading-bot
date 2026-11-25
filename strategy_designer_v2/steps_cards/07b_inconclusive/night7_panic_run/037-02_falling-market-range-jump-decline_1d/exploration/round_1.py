def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # normal drift per horizon over all windows (non-overlapping grid)
        dr = {}
        for h in (1, 3, 5, 10):
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            dr[h] = np.mean(vals)
        drift[coin] = dr
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values; op = df["open"].values
            n = len(df)
            rng = hi - lo
            rm = df.get("debug_info.components.range_mult.last_history_value")
            sit = (df["regime"] == "trending").values
            seen = set()
            for i in np.where(sit)[0]:
                cell = i // 3
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin, "window": w, "ts": df["timestamp"].iloc[i],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "rm": rm.iloc[i] if rm is not None else np.nan,
                     "clv": (c[i] - lo[i]) / rng[i] if rng[i] > 0 else np.nan,
                     "dayret": c[i] / op[i] - 1,
                     "ret5b": c[i] / c[i - 5] - 1 if i >= 5 else np.nan}
                for h in (1, 3, 5, 10):
                    if i + h < n:
                        r[f"ex{h}"] = -(c[i + h] / c[i] - 1 - drift[coin][h])  # short direction
                    else:
                        r[f"ex{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="ex3"):
        x = g[col].dropna()
        if len(x) < 2:
            return pd.Series({"n": len(x), "mean": x.mean(), "t": np.nan})
        gd = g.dropna(subset=[col]).groupby("ts")[col].sum()
        t = gd.sum() / (np.sqrt(len(gd)) * gd.std()) * 1 if gd.std() > 0 else np.nan
        return pd.Series({"n": len(x), "mean": x.mean(), "t": t})
    out = {}
    out["overall_by_h"] = pd.DataFrame({h: summ(d, f"ex{h}") for h in (1, 3, 5, 10)}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("window").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["rmq"] = pd.qcut(d["rm"], 4, duplicates="drop")
    out["by_rm_quartile"] = d.groupby("rmq").apply(summ)
    d["upclose"] = np.where(d["dayret"] > 0, "up day", "down day")
    out["by_close_dir"] = d.groupby("upclose").apply(summ)
    d["clvq"] = pd.cut(d["clv"], [0, 0.33, 0.67, 1.0001], include_lowest=True)
    out["by_clv"] = d.groupby("clvq").apply(summ)
    d["r5q"] = pd.qcut(d["ret5b"], 3, duplicates="drop")
    out["by_prior5d"] = d.groupby("r5q").apply(summ)
    out["by_close_dir_h10"] = d.groupby("upclose").apply(lambda g: summ(g, "ex10"))
    return out
