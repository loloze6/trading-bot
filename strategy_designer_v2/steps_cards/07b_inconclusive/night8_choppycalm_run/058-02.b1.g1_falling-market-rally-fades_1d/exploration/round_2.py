def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        cr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cr.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(cr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cs = b["close"].astype(float)
            c = cs.values
            n = len(c)
            r1 = cs.pct_change()
            vol20 = r1.rolling(20).std()
            vol30 = r1.rolling(30).std()
            volrank = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret60 = cs / cs.shift(60) - 1
            f = b["forecast"].astype(float).values
            for t in range(n):
                if not (f[t] < 0):
                    continue
                ts = pd.Timestamp(b["timestamp"].iloc[t])
                d = {"coin": coin, "win": w, "year": ts.year, "t": t, "absf": -f[t],
                     "z": (r1.iloc[t] / vol20.iloc[t]) if vol20.iloc[t] > 0 else np.nan,
                     "agit": volrank.iloc[t], "r60": ret60.iloc[t], "day": ts.normalize()}
                for h in (1, 2, 3, 5):
                    ok = (t + h < n) and (t % h == 0)
                    d[f"u{h}"] = -(c[t + h] / c[t] - 1 - h * mu) if ok else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)

    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        x = g[col]
        if len(x) < 5:
            return pd.Series({"n": len(x), "days": np.nan, "mean": np.nan, "t": np.nan})
        dd = (x - x.mean()).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean": x.mean(),
                          "t": x.mean() / se if se > 0 else np.nan})

    def wsumm(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series({"n": len(g), "wmean": np.nan, "t": np.nan})
        wv = g["absf"]; x = g[col]
        m = (wv * x).sum() / wv.sum()
        dd = (wv * (x - m)).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / wv.sum()
        return pd.Series({"n": len(g), "wmean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    out["all_by_h"] = pd.DataFrame({col: summ(df, col) for col in ("u1", "u2", "u3", "u5")}).T
    out["weighted_by_h"] = pd.DataFrame({col: wsumm(df, col) for col in ("u1", "u2", "u3", "u5")}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    out["by_year_u3"] = df.groupby("year").apply(lambda g: summ(g, "u3"))
    df["fq"] = pd.qcut(df["absf"], 4, labels=False, duplicates="drop")
    out["by_forecast_quartile"] = df.groupby("fq").apply(summ)
    out["by_forecast_quartile_u3"] = df.groupby("fq").apply(lambda g: summ(g, "u3"))
    df["zq"] = pd.qcut(df["z"], 4, labels=False, duplicates="drop")
    out["by_z_quartile"] = df.groupby("zq").apply(summ)
    df["ag"] = np.where(df["agit"].isna(), "na", np.where(df["agit"] > 0.5, "agitated", "calm"))
    out["by_agitation"] = df.groupby("ag").apply(summ)
    out["by_agitation_u3"] = df.groupby("ag").apply(lambda g: summ(g, "u3"))
    df["r60q"] = pd.qcut(df["r60"], 3, labels=False, duplicates="drop")
    out["by_r60_tercile"] = df.groupby("r60q").apply(summ)
    out["by_r60_tercile_u3"] = df.groupby("r60q").apply(lambda g: summ(g, "u3"))
    out["corr_absf_u1"] = float(df[["absf", "u1"]].dropna().corr().iloc[0, 1])
    out["corr_z_u1"] = float(df[["z", "u1"]].dropna().corr().iloc[0, 1])
    return out
