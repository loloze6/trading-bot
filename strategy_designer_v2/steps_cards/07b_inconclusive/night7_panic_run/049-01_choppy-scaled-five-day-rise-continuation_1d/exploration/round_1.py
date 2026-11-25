def explore(data):
    import numpy as np, pandas as pd
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            r5 = c / c.shift(5) - 1
            sc = r5 / sd30
            tr60 = (c / c.shift(60) - 1) * 100
            prof = np.where(tr60 > 10, "rising", np.where(tr60 < -10, "falling", "choppy"))
            prof = pd.Series(prof).where(tr60.notna())
            reg = b["regime"]
            fc = b["forecast"].astype(float)
            n = len(b)
            for h in H:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                for i in idx:
                    if pd.isna(fwd.iloc[i]) or pd.isna(sc.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], prof=prof.iloc[i],
                                     reg=reg.iloc[i], fc=fc.iloc[i], fwd=fwd.iloc[i],
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["ex"] = df["fwd"] - df["drift"]

    def tpool(g):
        d = g.groupby("day")["ex"].apply(lambda x: (x - g["ex"].mean()).sum())
        se = np.sqrt((d ** 2).sum()) / len(g)
        return g["ex"].mean() / se if se > 0 else np.nan

    def summ(g):
        return pd.Series({"n": len(g), "mean_ex%": 100 * g["ex"].mean(), "t": tpool(g)})

    out = {}
    df["side"] = np.where(df["sc"] > 0, "rise", "fall")
    sub = df[df["prof"].notna()]
    out["by_h_prof_side"] = sub.groupby(["h", "prof", "side"]).apply(summ)
    # magnitude quintiles of |sc| within side, h=3
    s3 = sub[sub.h == 3].copy()
    s3["q"] = s3.groupby("side")["sc"].transform(lambda x: pd.qcut(x.abs(), 5, labels=False))
    out["h3_prof_side_q"] = s3.groupby(["prof", "side", "q"]).apply(summ)
    # tested cases: forecast>0 in choppy regime 'unknown'
    tc = df[(df.h == 3) & (df.fc > 0)]
    out["tested_by_coin"] = tc.groupby("coin").apply(summ)
    out["tested_by_year"] = tc.groupby("year").apply(summ)
    tch = df[(df.fc > 0)]
    out["tested_by_h"] = tch.groupby("h").apply(summ)
    return out
