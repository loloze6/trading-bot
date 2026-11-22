def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # the coin's mean return per horizon over all windows, on non-overlapping grids
        drift = {}
        for h in [1, 2, 3, 5, 10]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(20).std()
            vsr = r / vol
            ret90 = c / c.shift(90) - 1
            ret30 = c / c.shift(30) - 1
            f = b["forecast"]
            year = pd.to_datetime(b["timestamp"]).dt.year
            n = len(c)
            for i in range(n):
                if not (f.iloc[i] <= -2):
                    continue
                d = dict(coin=coin, window=w, year=year.iloc[i], fc=f.iloc[i],
                         vsr=vsr.iloc[i], r90=ret90.iloc[i], r30=ret30.iloc[i], pos=i)
                for h in [1, 2, 3, 5, 10]:
                    if i + h < n:
                        d[f"u{h}"] = -(c.iloc[i + h] / c.iloc[i] - 1 - drift[h])
                    else:
                        d[f"u{h}"] = np.nan
                rows.append(d)
    df = pd.DataFrame(rows)

    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})

    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: tstat(df[f"u{h}"]) for h in [1, 2, 3, 5, 10]}).T
    df["fcq"] = pd.qcut(df["fc"].abs().rank(method="first"), 5, labels=False)
    out["by_fc_quintile"] = df.groupby("fcq").apply(
        lambda g: pd.concat([tstat(g["u1"]), pd.Series({"fc_abs": g["fc"].abs().mean(),
                                                         "vsr": g["vsr"].mean(),
                                                         "u3": g["u3"].mean()})]))
    df["r90q"] = pd.qcut(df["r90"], 5, labels=False)
    out["by_r90_quintile"] = df.groupby("r90q").apply(
        lambda g: pd.concat([tstat(g["u1"]), pd.Series({"r90": g["r90"].mean(),
                                                        "u3": g["u3"].mean()})]))
    out["by_coin"] = df.groupby("coin").apply(lambda g: tstat(g["u1"]))
    out["by_year"] = df.groupby("year").apply(lambda g: tstat(g["u1"]))
    out["corr_u1"] = pd.Series({
        "spearman_fc_abs": stats.spearmanr(df["fc"].abs(), df["u1"], nan_policy="omit")[0],
        "spearman_vsr": stats.spearmanr(df["vsr"], df["u1"], nan_policy="omit")[0],
        "spearman_r90": stats.spearmanr(df["r90"], df["u1"], nan_policy="omit")[0],
        "fc_eq_-20_share": (df["fc"] <= -19.99).mean(),
    })
    return out
