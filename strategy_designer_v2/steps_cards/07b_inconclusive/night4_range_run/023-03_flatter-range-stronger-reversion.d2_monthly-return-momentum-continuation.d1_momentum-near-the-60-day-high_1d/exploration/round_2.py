def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    pp = "debug_info.components.hpmom.post_pipeline_value"
    lh = "debug_info.components.hpmom.last_history_value"
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            s = pd.Series(c)
            r30 = s / s.shift(30) - 1
            hi60 = s.rolling(60, min_periods=60).max()
            D = (hi60 / s - 1) * 100
            prod = r30 * (1 / (1 + D)) ** 2
            r60 = s / s.shift(60) - 1
            year = pd.to_datetime(df["timestamp"]).dt.year
            for h in [3, 5]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=int(year.iloc[i]),
                                     f=df[pp].iloc[i], raw=df[lh].iloc[i],
                                     prod=prod.iloc[i], r30=r30.iloc[i], D=D.iloc[i],
                                     r60=r60.iloc[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]

    def st(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    out["h5_by_measure"] = pd.DataFrame({x: st(d[d.h == 5], x) for x in ["f", "raw", "prod", "r30"]}).T
    out["h3_by_measure"] = pd.DataFrame({x: st(d[d.h == 3], x) for x in ["f", "raw", "prod", "r30"]}).T
    d5 = d[d.h == 5].dropna(subset=["r30", "D"]).copy()
    d5["near"] = np.where(d5["D"] <= d5["D"].quantile(1 / 3), "near", "rest")
    d5["sgn"] = np.sign(d5["r30"])
    out["r30_by_near_and_sign_h5"] = d5.groupby(["near", "sgn"]).apply(lambda g: st(g, "r30"))
    d5["dir_ex"] = d5["ex"] * d5["sgn"]
    out["dir_excess_by_near_sign_h5"] = d5.groupby(["near", "sgn"])["dir_ex"].agg(
        n="size", mean="mean", t=lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["r30_near_by_coin_h5"] = d5[d5.near == "near"].groupby("coin").apply(lambda g: st(g, "r30"))
    out["f_corr_raw_prod"] = d[d.h == 5][["f", "raw", "prod", "r30"]].corr()
    return out
