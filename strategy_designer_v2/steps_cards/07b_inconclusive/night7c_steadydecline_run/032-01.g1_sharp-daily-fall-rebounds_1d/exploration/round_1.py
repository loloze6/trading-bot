def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        g = {h: [] for h in (1, 2, 3, 5)}
        for w, b in wins.items():
            c = b["close"].astype(float).values
            for h in g:
                idx = np.arange(0, len(c) - h, h)
                g[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in g.items()}
        usual = {h: np.std(v, ddof=1) for h, v in g.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            z = r / sd
            r20 = c / c.shift(20) - 1
            rng = (b["high"] - b["low"]) / b["close"]
            rngz = rng / rng.rolling(20).mean()
            volz = b["volume"] / b["volume"].rolling(20).mean()
            year = pd.to_datetime(b["timestamp"]).dt.year
            seen = set()
            for t in range(len(b)):
                if not (z.iloc[t] <= -2):
                    continue
                cell = t // 2
                if cell in seen:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "year": int(year.iloc[t]), "z": z.iloc[t],
                     "r20": r20.iloc[t], "rngz": rngz.iloc[t], "volz": volz.iloc[t],
                     "day": str(b["timestamp"].iloc[t])[:10]}
                for h in (1, 2, 3, 5):
                    if t + h < len(b):
                        d[f"x{h}"] = c.iloc[t + h] / c.iloc[t] - 1 - drift[coin][h]
                        d[f"s{h}"] = d[f"x{h}"] / usual[h]
                rows.append(d)
    df = pd.DataFrame(rows)

    def summ(s):
        s = s.dropna()
        n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    out["by_horizon"] = pd.DataFrame({h: summ(df[f"x{h}"]) for h in (1, 2, 3, 5)}).T
    out["by_coin_x2"] = df.groupby("coin")["x2"].apply(summ).unstack()
    out["by_year_x2"] = df.groupby("year")["x2"].apply(summ).unstack()
    df["zb"] = pd.cut(df["z"], [-99, -3.5, -3, -2.5, -2])
    out["by_z_x1x2"] = pd.concat([df.groupby("zb")["x1"].apply(summ).unstack().add_prefix("h1_"),
                                  df.groupby("zb")["x2"].apply(summ).unstack().add_prefix("h2_")], axis=1)
    df["r20b"] = pd.qcut(df["r20"], 3, labels=["low", "mid", "high"])
    out["by_prior20d_x2"] = df.groupby("r20b")["x2"].apply(summ).unstack()
    df["volb"] = pd.qcut(df["volz"], 3, labels=["low", "mid", "high"])
    out["by_volume_x2"] = df.groupby("volb")["x2"].apply(summ).unstack()
    df["rngb"] = pd.qcut(df["rngz"], 3, labels=["low", "mid", "high"])
    out["by_range_x2"] = df.groupby("rngb")["x2"].apply(summ).unstack()
    d2 = df.dropna(subset=["x2", "z"])
    sl = stats.linregress(-d2["z"], d2["x2"])
    out["slope_x2_on_negz"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(d2)})
    d2 = df.dropna(subset=["x2", "r20"])
    sl = stats.linregress(d2["r20"], d2["x2"])
    out["slope_x2_on_r20"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr})
    return out
