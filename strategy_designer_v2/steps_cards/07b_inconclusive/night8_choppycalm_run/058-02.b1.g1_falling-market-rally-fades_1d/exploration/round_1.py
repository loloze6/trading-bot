def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allret = []
    for coin, wins in data["bars"].items():
        cr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            cr.append(r.dropna())
        mu = pd.concat(cr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            vol30 = r1.rolling(30).std()
            volrank = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            f = b["forecast"].astype(float).values
            for t in range(n):
                if not (f[t] < 0):
                    continue
                d = {"coin": coin, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                     "t": t, "absf": -f[t], "z": (r1.iloc[t] / vol20.iloc[t]) if vol20.iloc[t] > 0 else np.nan,
                     "agit": volrank.iloc[t], "r60": ret60.iloc[t],
                     "day": pd.Timestamp(b["timestamp"].iloc[t]).normalize()}
                for h in (1, 2, 3, 5):
                    d[f"u{h}"] = -(c[t + h] / c[t] - 1 - h * mu) if t + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u1"):
        x = g[col].dropna()
        if len(x) < 5:
            return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        dd = g.dropna(subset=[col]).groupby("day")[col].sum() - g.dropna(subset=[col]).groupby("day")[col].count() * x.mean()
        se = np.sqrt((dd ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean": x.mean(), "t": x.mean() / se if se > 0 else np.nan})
    out["all_by_h"] = pd.DataFrame({h: summ(df, f"u{h}") for h in ("u1", "u2", "u3", "u5")}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["absf"], 4, labels=False, duplicates="drop")
    out["by_forecast_quartile"] = df.groupby("fq").apply(summ)
    df["zq"] = pd.qcut(df["z"], 4, labels=False, duplicates="drop")
    out["by_z_quartile"] = df.groupby("zq").apply(summ)
    df["ag"] = np.where(df["agit"].isna(), "na", np.where(df["agit"] > 0.5, "agitated", "calm"))
    out["by_agitation"] = df.groupby("ag").apply(summ)
    out["by_agitation_u3"] = df.groupby("ag").apply(lambda g: summ(g, "u3"))
    df["r60q"] = pd.qcut(df["r60"], 3, labels=False, duplicates="drop")
    out["by_r60_tercile"] = df.groupby("r60q").apply(summ)
    out["corr_absf_u1"] = float(df[["absf", "u1"]].dropna().corr().iloc[0, 1])
    out["corr_z_u1"] = float(df[["z", "u1"]].dropna().corr().iloc[0, 1])
    return out
