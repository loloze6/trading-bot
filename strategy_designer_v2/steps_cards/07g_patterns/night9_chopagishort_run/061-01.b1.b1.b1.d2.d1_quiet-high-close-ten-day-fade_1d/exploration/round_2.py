def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            z = r1 / sd20
            vr = b["volume"] / b["volume"].rolling(20).mean()
            lvr = np.log(vr)
            rng = (h - l).replace(0, np.nan)
            loc = (c - l) / rng
            ts = pd.to_datetime(b["timestamp"])
            for hz in (1, 2, 5, 10):
                fwd = c.shift(-hz) / c - 1
                for i in range(0, len(b), hz):
                    if np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, hz=hz, vr=vr.iloc[i], lvr=lvr.iloc[i], z=z.iloc[i],
                                     loc=loc.iloc[i], inprof=b["regime"].iloc[i] != "chop",
                                     wd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                                     day=ts.iloc[i].normalize(), fwd=fwd.iloc[i]))
    S = pd.DataFrame(rows)
    S["drift"] = S.groupby(["coin", "hz"])["fwd"].transform("mean")
    S["ex"] = S["fwd"] - S["drift"]
    S["usual"] = S.groupby(["coin", "hz"])["fwd"].transform("std")
    S["strength"] = S["ex"] / S["usual"]

    def summ(g):
        g = g.dropna(subset=["ex"])
        n = len(g)
        if n < 3:
            return pd.Series({"n": n, "mean_ex": g["ex"].mean(), "strength": np.nan, "t_day": np.nan, "days": np.nan})
        d = g.groupby("day")["ex"].sum()
        nd = len(d)
        m = g["ex"].mean()
        se = d.std() * np.sqrt(nd) / n
        return pd.Series({"n": n, "mean_ex": m, "strength": g["strength"].mean(),
                          "t_day": m / se if se > 0 else np.nan, "days": nd})

    out = {}
    S["sign"] = np.where(S["z"] > 0, "up", "down")
    for hz in (2, 5, 10):
        T = S[(S.hz == hz)].dropna(subset=["vr", "z"]).copy()
        T["vrq"] = pd.qcut(T["vr"], 5, labels=False)
        out[f"h{hz} vol quintile x day sign"] = T.groupby(["sign", "vrq"]).apply(summ)
        T5 = T[T.vrq == 4]
        out[f"h{hz} top vol quintile by year x sign"] = T5.groupby(["sign", "year"]).apply(summ)
        T5["inprof"] = T5["inprof"].astype(str)
        out[f"h{hz} top vol quintile x inprof"] = T5.groupby(["inprof", "sign"]).apply(summ)
    T = S[S.hz == 5].dropna(subset=["vr", "z"]).copy()
    T["vrq"] = pd.qcut(T["vr"], 5, labels=False)
    out["h5 top vol by coin x sign"] = T[T.vrq == 4].groupby(["coin", "sign"]).apply(summ)
    # weekday
    for hz in (1, 2):
        T = S[S.hz == hz]
        out[f"h{hz} weekday"] = T.groupby("wd").apply(summ)
    T = S[(S.hz == 2) & (S.wd == 6)]
    out["h2 sunday by year"] = T.groupby("year").apply(summ)
    out["h2 sunday by coin"] = T.groupby("coin").apply(summ)
    return out
