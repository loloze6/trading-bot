def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift_rows = []
    H = [1, 3, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            rec = df.get("debug_info.components.rise.last_history_value")
            calm = (df["regime"] != "chop")
            ret60 = c / c.shift(60) - 1
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    drift_rows.append((coin, h, c[i + h] / c[i] - 1))
            for i in range(n):
                fw = {}
                for h in H:
                    fw[h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, w=w, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                 year=str(df["timestamp"].iloc[i])[:4],
                                 z=z.iloc[i], calm=bool(calm.iloc[i]), regime=df["regime"].iloc[i],
                                 bet=float(df["postRebalance_current_allocation"].iloc[i] or 0) > 0 and df["regime"].iloc[i] == "trending",
                                 r60=ret60.iloc[i], **{f"f{h}": fw[h] for h in H}))
    d = pd.DataFrame(rows)
    dr = pd.DataFrame(drift_rows, columns=["coin", "h", "ret"])
    drift = dr.groupby(["coin", "h"])["ret"].mean()
    for h in H:
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(lambda x: drift.get((x, h), np.nan))

    def cases(mask, h, sign=1):
        x = d[mask].copy()
        x["cell"] = x["i"] // h
        x = x.dropna(subset=[f"u{h}"]).groupby(["coin", "w", "cell"]).first().reset_index()
        x["v"] = sign * x[f"u{h}"]
        return x

    def summ(x):
        if len(x) < 3:
            return pd.Series(dict(n=len(x), days=0, mean=np.nan, t=np.nan))
        g = x.groupby("day")["v"].sum()
        m = x["v"].mean()
        G = len(g)
        se = np.sqrt((g - g.mean() * 0 - m * x.groupby("day").size()).pow(2).sum() * G / (G - 1)) / len(x)
        return pd.Series(dict(n=len(x), days=G, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    # tested situation: calm & z>=1, by horizon, long
    t1 = {}
    for h in H:
        t1[f"calm_up_h{h}"] = summ(cases(d.calm & (d.z >= 1), h))
        t1[f"agit_up_h{h}"] = summ(cases(~d.calm & (d.z >= 1), h))
        t1[f"calm_dn_short_h{h}"] = summ(cases(d.calm & (d.z <= -1), h, -1))
        t1[f"agit_dn_short_h{h}"] = summ(cases(~d.calm & (d.z <= -1), h, -1))
        t1[f"calm_all_long_h{h}"] = summ(cases(d.calm & d.z.notna(), h))
    out["by_situation_horizon"] = pd.DataFrame(t1).T
    # grading: calm, bins of z, h=5 (long)
    x = cases(d.calm & d.z.notna(), 5)
    x["zb"] = pd.cut(x["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    out["calm_zbins_h5_long"] = x.groupby("zb").apply(summ)
    x = cases(~d.calm & d.z.notna(), 5)
    x["zb"] = pd.cut(x["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    out["agit_zbins_h5_long"] = x.groupby("zb").apply(summ)
    # tested cases by coin, year, trend
    x = cases(d.calm & (d.z >= 1), 5)
    out["calm_up_by_coin"] = x.groupby("coin").apply(summ)
    out["calm_up_by_year"] = x.groupby("year").apply(summ)
    x["trend"] = np.where(x.r60 > 0.1, "rising", np.where(x.r60 < -0.1, "falling", "choppy"))
    out["calm_up_by_trend"] = x.groupby("trend").apply(summ)
    x2 = cases(d.calm & (d.z <= -1), 5, -1)
    x2["trend"] = np.where(x2.r60 > 0.1, "rising", np.where(x2.r60 < -0.1, "falling", "choppy"))
    out["calm_dn_short_by_trend"] = x2.groupby("trend").apply(summ)
    # actual bet cases
    out["bet_cases_h5"] = summ(cases(d.bet, 5))
    return out
