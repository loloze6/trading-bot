def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1, 3, 5, 10, 20)}
        for w, b in wins.items():
            c = b["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            s = np.maximum(0, -f)
            v = b["volume"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            ret1 = pd.Series(c).pct_change().values
            for start in range(0, n, 5):
                for t in range(start, min(start + 5, n)):
                    lo = s[max(0, t - 5):t].min() if t > 0 else 0
                    if s[t] >= 2 and s[t] - lo >= 2:
                        r = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(), "s": s[t]}
                        for h in (1, 3, 5, 10, 20):
                            r[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                        r["fall20"] = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                        r["dry"] = b["debug_info.components.dryup_moderation.last_history_value"].iloc[t]
                        r["vol20"] = np.nanstd(ret1[max(1, t - 19):t + 1]) if t >= 5 else np.nan
                        r["ret5past"] = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                        rows.append(r)
                        break
    df = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g.dropna(subset=[col])
        d = x.groupby("day")[col].agg(["sum", "count"])
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        D = len(d)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x) if D > 1 else np.nan
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(df, f"u{h}") for h in (1, 3, 5, 10, 20)}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_window"] = df.groupby("win").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    for col in ["s", "fall20", "dry", "vol20", "ret5past"]:
        q = pd.qcut(df[col], 3, labels=["low", "mid", "high"], duplicates="drop")
        out[f"by_{col}_tercile"] = df.groupby(q).apply(summ)
        out[f"{col}_tercile_ranges"] = df.groupby(q)[col].agg(["min", "max"])
    return out
