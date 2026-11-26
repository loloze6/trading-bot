def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
            usual[(coin, h)] = np.std(rs, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            prev = np.r_[0, f[:-1]]
            rise = f - prev
            seen = set()
            for i in range(len(df)):
                if rise[i] >= 2 and f[i] > 0:
                    cell = i // 3
                    if cell in seen:
                        continue
                    seen.add(cell)
                    r = {"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                         "fc": f[i], "pos": i}
                    for h in H:
                        if i + h < len(c):
                            r[f"u{h}"] = c[i + h] / c[i] - 1 - drift[(coin, h)]
                            r[f"s{h}"] = r[f"u{h}"] / usual[(coin, h)]
                        else:
                            r[f"u{h}"] = np.nan
                    rows.append(r)
    cs = pd.DataFrame(rows)

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 3:
            return pd.Series({"n": len(s), "days": s["day"].nunique() if len(s) else 0, "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(s) if D > 1 else np.nan
        return pd.Series({"n": len(s), "days": D, "mean": m, "t": m / se})

    out = {}
    out["horizons"] = pd.DataFrame({f"h{h}": tday(cs, f"u{h}") for h in H}).T
    out["by_coin_h3"] = cs.groupby("coin").apply(lambda s: tday(s, "u3"))
    out["by_year_h3"] = cs.groupby("year").apply(lambda s: tday(s, "u3"))
    out["by_window_h3"] = cs.groupby("win").apply(lambda s: tday(s, "u3"))
    cs["fcq"] = pd.qcut(cs["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_fc_tercile"] = pd.concat({h: cs.groupby("fcq").apply(lambda s: tday(s, f"u{h}")) for h in [3, 5]})
    out["strength_h3"] = cs["s3"].mean()
    out["share_pos_h3"] = (cs["u3"] > 0).mean()
    out["median_u3"] = cs["u3"].median()
    return out
