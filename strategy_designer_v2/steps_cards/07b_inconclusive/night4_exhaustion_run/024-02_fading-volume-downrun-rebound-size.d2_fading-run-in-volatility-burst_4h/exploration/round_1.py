def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 18
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in (6, 12, 18, 36)}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in rets:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        usual[coin] = np.std(rets[18])
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].fillna(0).values
            df_ = np.diff(np.r_[0, f])
            sig = np.where(df_ >= 2)[0]
            seen = set()
            vr = df.get("debug_info.components.vol_ratio.last_history_value")
            sl = df.get("debug_info.components.streak_loss.last_history_value")
            r30 = pd.Series(c).pct_change(180).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in sig:
                cell = t // H
                if cell in seen or t + H >= n:
                    continue
                seen.add(cell)
                rec = {"coin": coin, "win": w, "year": year[t], "fc": f[t],
                       "vr": vr.values[t] if vr is not None else np.nan,
                       "sl": sl.values[t] if sl is not None else np.nan,
                       "r30": r30[t]}
                for h in (6, 12, 18, 36):
                    rec["ex%d" % h] = (c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="ex18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: summ(d, "ex%d" % h) for h in (6, 12, 18, 36)}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    for col in ("fc", "vr", "sl", "r30"):
        q = pd.qcut(d[col].rank(method="first"), 5, labels=False)
        out["by_%s_quintile" % col] = d.groupby(q).apply(summ)
    d["trend"] = np.where(d["r30"] > 0, "up30d", "down30d")
    out["by_trend"] = d.groupby("trend").apply(summ)
    out["by_trend_h6"] = d.groupby("trend").apply(lambda g: summ(g, "ex6"))
    out["usual18_pct"] = pd.Series({k: 100 * v for k, v in usual.items()})
    return out
