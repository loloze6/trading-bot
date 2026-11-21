def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            vol = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            mult = r24 / vol
            r7 = (c / c.shift(168) - 1) / vol
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            for h in (24, 72, 168):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).values[idx]
                f6 = (c.shift(-6) / c - 1).values[idx] if h == 24 else np.full(len(idx), np.nan)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "fr": fr, "f6": f6,
                    "mult": mult.values[idx], "vol": vol.values[idx], "r7": r7.values[idx],
                    "year": ts.dt.year.values[idx], "wd": ts.dt.weekday.values[idx],
                    "hour": ts.dt.hour.values[idx]}))
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["fr"] - d.groupby(["coin", "h"])["fr"].transform("mean")
    d["usual"] = d.groupby(["coin", "h"])["fr"].transform("std")
    d = d.dropna(subset=["mult", "ex"])
    d["volrel"] = d["vol"] / d.groupby("coin")["vol"].transform("median")
    def summ(g):
        x = g["ex"]; n = len(x)
        return pd.Series({"n": n, "mean_bps": 1e4 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": (x / g["usual"]).mean()})
    out = {}
    d24 = d[d.h == 24].copy()
    deep = d24[d24.mult < -3]
    out["deep3_by_coin"] = deep.groupby("coin").apply(summ)
    out["deep3_by_year"] = deep.groupby("year").apply(summ)
    out["deep3_first6h_bps"] = pd.Series({"mean_f6_bps": 1e4 * deep["f6"].mean(), "mean_f24_bps": 1e4 * deep["fr"].mean()})
    dr = d24[d24.mult < -1].copy()
    dr["vbin"] = pd.cut(dr["volrel"], [0, 1.0, 1.4, np.inf])
    dr["mb"] = pd.cut(dr["mult"], [-np.inf, -3, -2, -1])
    out["drop_by_mult_and_vol"] = dr.groupby(["mb", "vbin"], observed=True).apply(summ)
    dr["hv"] = dr["volrel"] > 1.4
    out["drop_highvol_by_coin"] = dr[dr.hv].groupby("coin").apply(summ)
    out["drop_highvol_by_year"] = dr[dr.hv].groupby("year").apply(summ)
    # graded: product of depth and vol
    dr["score"] = (-dr["mult"]) * dr["volrel"]
    dr["sq"] = pd.qcut(dr["score"], 5, labels=False)
    out["drop_score_quintile"] = dr.groupby("sq").apply(summ)
    # weekday robustness
    fri = d24[d24.wd == 4]
    out["friday_by_coin"] = fri.groupby("coin").apply(summ)
    out["friday_by_year"] = fri.groupby("year").apply(summ)
    out["grid_hour_counts"] = d24.groupby("hour").size()
    # 7d rise continuation
    up = d[(d.h == 72) & (d.r7 > 6)]
    out["r7up6_h72_by_coin"] = up.groupby("coin").apply(summ)
    out["r7up6_h72_by_year"] = up.groupby("year").apply(summ)
    return out
