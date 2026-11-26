def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; drift_rows = []
    H = [3, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            z = r / r.rolling(30, min_periods=20).std()
            calm = (df["regime"] != "chop")
            r60 = c / c.shift(60) - 1
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    drift_rows.append((coin, h, c[i + h] / c[i] - 1))
            for i in range(n):
                rows.append(dict(coin=coin, w=w, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                 year=str(df["timestamp"].iloc[i])[:4], z=z.iloc[i], calm=bool(calm.iloc[i]),
                                 r60=r60.iloc[i],
                                 **{f"f{h}": (c[i + h] / c[i] - 1 if i + h < n else np.nan) for h in H}))
    d = pd.DataFrame(rows)
    dr = pd.DataFrame(drift_rows, columns=["coin", "h", "ret"])
    drift = dr.groupby(["coin", "h"])["ret"].mean()
    for h in H:
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(lambda x: drift.get((x, h), np.nan))
    d["trend"] = np.where(d.r60 > 0.1, "rising", np.where(d.r60 < -0.1, "falling", np.where(d.r60.notna(), "choppy", "na")))

    def cases(mask, h, sign=1):
        x = d[mask].copy(); x["cell"] = x["i"] // h
        x = x.dropna(subset=[f"u{h}"]).groupby(["coin", "w", "cell"]).first().reset_index()
        x["v"] = sign * x[f"u{h}"]; return x

    def summ(x):
        if len(x) < 3:
            return pd.Series(dict(n=len(x), days=0, mean=np.nan, t=np.nan))
        m = x["v"].mean(); g = x.groupby("day")["v"].agg(["sum", "size"]); G = len(g)
        se = np.sqrt(((g["sum"] - m * g["size"]) ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series(dict(n=len(x), days=G, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    t = {}
    for h in H:
        for tr in ["rising", "choppy", "falling"]:
            t[f"calm_{tr}_up_h{h}"] = summ(cases(d.calm & (d.trend == tr) & (d.z >= 1), h))
            t[f"calm_{tr}_all_h{h}"] = summ(cases(d.calm & (d.trend == tr) & d.z.notna(), h))
            t[f"agit_{tr}_up_h{h}"] = summ(cases(~d.calm & (d.trend == tr) & (d.z >= 1), h))
    out["trend_horizon"] = pd.DataFrame(t).T
    x = cases(d.calm & (d.trend == "rising") & d.z.notna(), 5)
    x["zb"] = pd.cut(x["z"], [-99, -1, 0, 0.5, 1, 1.5, 2, 99])
    out["rising_calm_zbins_h5"] = x.groupby("zb").apply(summ)
    y = cases(d.calm & (d.trend == "rising") & (d.z >= 1), 5)
    out["rising_calm_up_by_year"] = y.groupby("year").apply(summ)
    out["rising_calm_up_by_coin"] = y.groupby("coin").apply(summ)
    out["rising_calm_up_by_w"] = y.groupby("w").apply(summ)
    y["hi"] = y["z"] > y["z"].median()
    out["rising_calm_up_hi_lo"] = y.groupby("hi").apply(summ)
    return out
