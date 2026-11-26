def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        cr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cr.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(cr).mean()
        sd1 = pd.concat(cr).std()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cs = b["close"].astype(float)
            c = cs.values
            n = len(c)
            r1 = cs.pct_change()
            vol20 = r1.rolling(20).std()
            vol30 = r1.rolling(30).std()
            volexp = vol30.expanding(min_periods=10).median()
            reg = b["regime"].astype(str).values
            f = b["forecast"].astype(float).values
            for t in range(1, n - 1):
                if reg[t] != "unknown":
                    continue
                ts = pd.Timestamp(b["timestamp"].iloc[t])
                z = r1.iloc[t] / vol20.iloc[t] if vol20.iloc[t] > 0 else np.nan
                rows.append({"coin": coin, "year": ts.year, "day": ts.normalize(),
                             "z": z, "short": f[t] < 0,
                             "relvol": vol30.iloc[t] / volexp.iloc[t] if volexp.iloc[t] and volexp.iloc[t] > 0 else np.nan,
                             "u1_short": -(c[t + 1] / c[t] - 1 - mu),
                             "norm": -(c[t + 1] / c[t] - 1 - mu) / sd1})
    df = pd.DataFrame(rows)

    def summ(g, col="u1_short"):
        g = g.dropna(subset=[col]); x = g[col]
        if len(x) < 5:
            return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        dd = (x - x.mean()).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean": x.mean(), "t": x.mean() / se})

    out = {}
    out["falling_all_days"] = summ(df).to_frame().T
    df["sign"] = np.where(df["z"] > 0, "up_day", np.where(df["z"] < 0, "down_day", "flat"))
    out["falling_by_day_sign"] = df.groupby("sign").apply(summ)
    df["zbin"] = pd.cut(df["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["falling_by_z_bin"] = df.groupby("zbin").apply(summ)
    up = df[df["z"] > 0].copy()
    up["calm"] = np.where(up["relvol"].isna(), "na", np.where(up["relvol"] > 1, "agitated_rel", "calm_rel"))
    out["up_by_relvol"] = up.groupby("calm").apply(summ)
    out["up_by_year"] = up.groupby("year").apply(summ)
    out["share_short_in_falling"] = float(df["short"].mean())
    return out
