def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            vol = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            mult = r24 / vol
            r7 = c / c.shift(168) - 1
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            for h in (24, 72, 168):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).values[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "fr": fr,
                    "mult": mult.values[idx], "vol": vol.values[idx], "r7": r7.values[idx] / vol.values[idx],
                    "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx]}))
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["fr"] - d.groupby(["coin", "h"])["fr"].transform("mean")
    d["usual"] = d.groupby(["coin", "h"])["fr"].transform("std")
    d = d.dropna(subset=["mult", "ex"])
    def summ(g):
        x = g["ex"]
        n = len(x)
        return pd.Series({"n": n, "mean_bps": 1e4 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": (x / g["usual"]).mean()})
    out = {}
    d["mbin"] = pd.cut(d["mult"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    for h in (24, 72, 168):
        out[f"by_drop_multiple_h{h}"] = d[d.h == h].groupby("mbin", observed=True).apply(summ)
    d["r7bin"] = pd.cut(d["r7"], [-np.inf, -6, -3, -1, 1, 3, 6, np.inf])
    for h in (72, 168):
        out[f"by_7d_multiple_h{h}"] = d[d.h == h].groupby("r7bin", observed=True).apply(summ)
    d["volrel"] = d["vol"] / d.groupby("coin")["vol"].transform("median")
    d["vbin"] = pd.cut(d["volrel"], [0, 0.7, 1.0, 1.4, 2.0, np.inf])
    for h in (24, 168):
        out[f"by_vol_level_h{h}"] = d[d.h == h].groupby("vbin", observed=True).apply(summ)
    dd = d[(d.h == 24) & (d.mult < -1)]
    out["drop_gt1_by_vol_h24"] = dd.groupby("vbin", observed=True).apply(summ)
    out["by_weekday_h24"] = d[d.h == 24].groupby("wd").apply(summ)
    out["drop_gt2_by_coin_h72"] = d[(d.h == 72) & (d.mult < -2)].groupby("coin").apply(summ)
    # book days
    bk = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["book_return", "coin_return"]].astype(float).copy()
            x["next_coin"] = x["coin_return"].shift(-1)
            x["coin"] = coin
            bk.append(x)
    b = pd.concat(bk).dropna()
    b["bq"] = pd.qcut(b["book_return"].rank(method="first"), 10, labels=False)
    out["book_decile_vs_coin"] = b.groupby("bq")[["book_return", "coin_return", "next_coin"]].mean() * 1e4
    return out
