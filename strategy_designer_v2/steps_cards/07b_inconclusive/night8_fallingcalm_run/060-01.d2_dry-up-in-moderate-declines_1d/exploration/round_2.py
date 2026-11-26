def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    H = (1, 3, 5, 10, 20)
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, b in wins.items():
            c = b["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values
            s = np.maximum(0, -f)
            v = b["volume"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            ret1 = pd.Series(c).pct_change().values
            dcol = "debug_info.components.dryup_moderation.last_history_value"
            for start in range(0, n, 5):
                for t in range(start, min(start + 5, n)):
                    lo = s[max(0, t - 5):t].min() if t > 0 else 0
                    if s[t] >= 2 and s[t] - lo >= 2:
                        r = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(), "s": s[t]}
                        for h in H:
                            r[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                        r["fall20"] = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                        r["trend60"] = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                        r["dry"] = b[dcol].iloc[t] if dcol in b else np.nan
                        r["volratio"] = (v[t-29:t+1].mean() / v[t-59:t-29].mean()) if t >= 59 else np.nan
                        r["vol20"] = np.nanstd(ret1[max(1, t - 19):t + 1]) if t >= 5 else np.nan
                        r["ret5past"] = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                        rows.append(r)
                        break
    df = pd.DataFrame(rows)
    def summ(x, col="u5"):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return pd.Series({"n": len(x), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(df, f"u{h}") for h in H}).T
    out["by_coin"] = pd.DataFrame({k: summ(g) for k, g in df.groupby("coin")}).T
    out["by_window"] = pd.DataFrame({k: summ(g) for k, g in df.groupby("win")}).T
    out["by_year"] = pd.DataFrame({k: summ(g) for k, g in df.groupby("year")}).T
    for col in ["s", "fall20", "trend60", "dry", "volratio", "vol20", "ret5past"]:
        x = df.dropna(subset=[col])
        if len(x) < 9:
            continue
        q = pd.qcut(x[col].rank(method="first"), 3, labels=["low", "mid", "high"])
        res = {}
        for lab in ["low", "mid", "high"]:
            g = x[q == lab]
            sr = summ(g)
            sr["min"] = g[col].min(); sr["max"] = g[col].max()
            sr["u10"] = g["u10"].mean()
            res[lab] = sr
        out[f"by_{col}"] = pd.DataFrame(res).T
    out["n_cases"] = len(df)
    return out
