def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:] / c[:-1] - 1)
        drift1 = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = h - l
            mr = rng.rolling(20, min_periods=20).mean()
            width = rng / mr
            loc = (c - l) / rng.replace(0, np.nan)
            body = (c - o) / mr
            ret1 = c / c.shift(1) - 1
            ret5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "day": ts.dt.floor("D"), "year": ts.dt.year,
                               "regime": b["regime"], "fc": b["forecast"], "width": width, "loc": loc,
                               "body": body, "ret1": ret1, "ret5": ret5,
                               "u1": -(c.shift(-1) / c - 1 - drift1),
                               "prod": (c - (h + l) / 2) / mr})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    def ct(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean(); g = (s - m).groupby(dd).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"mean": m, "t": m / se if se > 0 else np.nan, "n": len(s), "days": dd.nunique()})

    def summ(sub): return ct(sub["u1"], sub["day"])
    cases = D[(D["regime"] == "mean_reversion") & (D["fc"] < 0)].copy()
    out = {}
    cases["bq"] = pd.qcut(cases["body"], 4, labels=["b1_low", "b2", "b3", "b4_high"])
    out["by_body_quartile"] = cases.groupby("bq").apply(summ)
    cases["r1q"] = pd.qcut(cases["ret1"], 3, labels=["r_low", "r_mid", "r_high"])
    out["by_dayreturn_tercile"] = cases.groupby("r1q").apply(summ)
    cases["r5q"] = pd.qcut(cases["ret5"], 3, labels=["r5_low", "r5_mid", "r5_high"])
    out["by_5day_return_tercile"] = cases.groupby("r5q").apply(summ)
    up = cases[cases["body"] > 0].copy()
    up["bpq"] = pd.qcut(up["body"], 3, labels=["low", "mid", "high"])
    out["upday_by_body_tercile"] = up.groupby("bpq").apply(summ)
    out["upday_by_year"] = up.groupby("year").apply(summ)
    out["upday_by_coin"] = up.groupby("coin").apply(summ)
    # correlation of u1 with gradings, in cases
    out["spearman_u1"] = pd.Series({k: cases[[k, "u1"]].dropna().corr(method="spearman").iloc[0, 1]
                                    for k in ["prod", "body", "width", "loc", "ret1"]})
    return out
