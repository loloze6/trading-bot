def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 240
    hs = [24, 72, 120, 240, 480]
    rows = []
    base = []
    drift = {}
    for coin, wins in bars.items():
        # normal drift per horizon
        d = {}
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(list(c[idx + h] / c[idx] - 1))
            d[h] = (np.mean(rr), np.std(rr))
        drift[coin] = d
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            r720 = np.full(n, np.nan); r720[720:] = c[720:] / c[:-720] - 1
            raw = df.get("debug_info.components.surge.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            for start in range(0, n - H, H):
                seg = np.where(f[start:start + H] >= 2)[0]
                if len(seg) == 0:
                    # base: trending-regime, no surge cell start bar
                    t = start
                    if df["regime"].iloc[t] == "trending":
                        base.append({"coin": coin, "ex240": c[t + H] / c[t] - 1 - d[H][0]})
                    continue
                t = start + seg[0]
                rec = {"coin": coin, "win": w, "year": yr[t], "fc": f[t], "r24": r24[t],
                       "r720": r720[t], "raw": raw[t], "hour": ts.iloc[t].hour}
                for h in hs:
                    if t + h < n:
                        rec[f"ex{h}"] = c[t + h] / c[t] - 1 - d[h][0]
                        rec[f"st{h}"] = rec[f"ex{h}"] / d[h][1]
                rows.append(rec)
    R = pd.DataFrame(rows)
    B = pd.DataFrame(base)
    def summ(g, col="ex240"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(R, f"ex{h}") for h in hs}).T
    out["strength_by_h"] = pd.Series({h: R[f"st{h}"].mean() for h in hs})
    out["by_coin"] = R.groupby("coin").apply(summ)
    out["by_year"] = R.groupby("year").apply(summ)
    R["fcq"] = pd.qcut(R["fc"].rank(method="first"), 4, labels=False)
    out["by_fc_quartile"] = R.groupby("fcq").apply(lambda g: pd.concat([summ(g), pd.Series({"fc_mid": g.fc.median()})]))
    R["r720q"] = pd.qcut(R["r720"].rank(method="first"), 4, labels=False)
    out["by_r720_quartile"] = R.groupby("r720q").apply(lambda g: pd.concat([summ(g), pd.Series({"r720_mid": g.r720.median()})]))
    R["r24q"] = pd.qcut(R["r24"].rank(method="first"), 4, labels=False)
    out["by_r24_quartile"] = R.groupby("r24q").apply(lambda g: pd.concat([summ(g), pd.Series({"r24_mid": g.r24.median()})]))
    out["base_trending_nosurge"] = summ(B)
    out["base_by_coin"] = B.groupby("coin").apply(summ)
    out["fc_desc"] = R["fc"].describe()
    return out
