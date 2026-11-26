def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            sc = (c / c.shift(5) - 1) / sd30
            tr60 = (c / c.shift(60) - 1) * 100
            for h in [3, 5]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(sc.iloc[i]) or pd.isna(tr60.iloc[i]):
                        continue
                    t = tr60.iloc[i]
                    prof = "rising" if t > 10 else ("falling" if t < -10 else "choppy")
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], prof=prof, fwd=fwd.iloc[i],
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]

    def tpool(g):
        m = g["ex"].mean()
        d = g.groupby("day")["ex"].apply(lambda x: (x - m).sum())
        se = np.sqrt((d ** 2).sum()) / len(g)
        return m / se if se > 0 else np.nan

    def summ(g):
        rho, p = stats.spearmanr(g["sc"].abs(), g["ex"]) if len(g) > 5 else (np.nan, np.nan)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean_ex%": 100 * g["ex"].mean(),
                          "t": tpool(g), "rho_|sc|_ex": rho})

    out = {}
    fall = df[df.sc < 0]
    rise = df[df.sc > 0]
    out["fall_by_h_prof"] = fall.groupby(["h", "prof"]).apply(summ)
    cf = fall[(fall.h == 3) & (fall.prof == "choppy")]
    out["choppy_fall_h3_by_coin"] = cf.groupby("coin").apply(summ)
    out["choppy_fall_h3_by_year"] = cf.groupby("year").apply(summ)
    cf["half"] = np.where(cf["sc"].abs() > cf["sc"].abs().median(), "top", "bottom")
    out["choppy_fall_h3_half"] = cf.groupby("half").apply(summ)
    nr = fall[(fall.h == 3) & (fall.prof != "rising")].copy()
    nr["half"] = np.where(nr["sc"].abs() > nr["sc"].abs().median(), "top", "bottom")
    out["notrising_fall_h3_half"] = nr.groupby("half").apply(summ)
    out["notrising_fall_h3_by_year"] = nr.groupby("year").apply(summ)
    cr = rise[(rise.h == 3) & (rise.prof == "choppy")]
    out["choppy_rise_h3_by_year"] = cr.groupby("year").apply(summ)
    return out
