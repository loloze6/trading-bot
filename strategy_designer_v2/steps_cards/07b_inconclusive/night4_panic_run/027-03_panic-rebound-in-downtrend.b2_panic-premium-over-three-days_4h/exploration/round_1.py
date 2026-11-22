def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 12, 18, 42, 84]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        # coin mean returns per horizon over non-overlapping grids
        cm = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            cm[h] = (np.mean(rs), np.std(rs))
        coin_mean[coin] = cm
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            rng = (df["high"] - df["low"]) / c
            ratio = rng.rolling(6).mean() / rng.rolling(180, min_periods=30).mean()
            r6 = c / c.shift(6) - 1
            fallz = r6 / r6.abs().rolling(180, min_periods=30).mean()
            r30 = c / c.shift(180) - 1
            r7 = c / c.shift(42) - 1
            f = df["forecast"].fillna(0).values
            n = len(df)
            for start in range(0, n, 18):
                end = min(start + 18, n)
                sel = np.where(f[start:end] >= 2)[0]
                if len(sel) == 0:
                    continue
                t = start + sel[0]
                year = pd.Timestamp(df["timestamp"].iloc[t]).year
                rec = dict(coin=coin, window=w, year=year, fc=f[t],
                           ratio=ratio.iloc[t], fallz=fallz.iloc[t],
                           r30=r30.iloc[t], r7=r7.iloc[t])
                for h in H:
                    if t + h < n:
                        rec[f"x{h}"] = c.iloc[t + h] / c.iloc[t] - 1 - cm[h][0]
                    else:
                        rec[f"x{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def summ(g, col="x18"):
        v = g[col].dropna()
        return pd.Series({"n": len(v), "mean": v.mean(),
                          "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan,
                          "share_pos": (v > 0).mean()})
    out = {}
    out["horizons_all"] = pd.DataFrame({h: summ(d, f"x{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["ratio_q"] = pd.qcut(d["ratio"], 4, labels=False, duplicates="drop")
    d["fall_q"] = pd.qcut(d["fallz"], 4, labels=False, duplicates="drop")
    d["fc_q"] = pd.qcut(d["fc"], 4, labels=False, duplicates="drop")
    out["by_ratio_q"] = d.groupby("ratio_q").apply(summ).join(d.groupby("ratio_q")["ratio"].median())
    out["by_fall_q (0=deepest)"] = d.groupby("fall_q").apply(summ).join(d.groupby("fall_q")["fallz"].median())
    out["by_fc_q"] = d.groupby("fc_q").apply(summ).join(d.groupby("fc_q")["fc"].median())
    out["by_prior30_sign"] = d.groupby(d["r30"] > 0).apply(summ)
    for h in [6, 42, 84]:
        out[f"by_fall_q_x{h}"] = d.groupby("fall_q").apply(lambda g: summ(g, f"x{h}"))
        out[f"by_ratio_q_x{h}"] = d.groupby("ratio_q").apply(lambda g: summ(g, f"x{h}"))
    sp = d[["fc", "ratio", "fallz", "r30", "x18", "x42"]].corr(method="spearman")
    out["spearman"] = sp
    return out
