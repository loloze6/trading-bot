def explore(data):
    import numpy as np, pandas as pd
    rec = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30).std()
            z = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            tr60 = (c / c.shift(60) - 1) * 100
            sd_prev = r.shift(14).rolling(30).std()
            reg = b["regime"].astype(str)
            df = pd.DataFrame({"z": z, "tr60": tr60, "sdratio": sd / sd_prev,
                               "unk": reg.eq("unknown")})
            df["coin"] = coin
            df["window"] = w
            rec.append(df)
    D = pd.concat(rec).dropna(subset=["z"])
    out = {}
    low = D[D.z <= -2]
    out["z<=-2 bars: n"] = int(len(low))
    out["z<=-2: 60d return quantiles"] = low["tr60"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
    out["z<=-2: share 60d return in [-10,10]"] = float(low["tr60"].between(-10, 10).mean())
    out["z<=-2: share 60d return < -10"] = float((low["tr60"] < -10).mean())
    out["z<=-2: 30d swing vs swing 14d earlier, median"] = float(low["sdratio"].median())
    ch = D[D["tr60"].between(-10, 10)]
    out["choppy bars: share z<=-2"] = float((ch.z <= -2).mean())
    out["choppy bars: z quantiles"] = ch["z"].quantile([0.005, 0.01, 0.05, 0.5])
    out["profile (unknown) bars: z quantiles"] = D.loc[D.unk, "z"].quantile([0.001, 0.01, 0.05, 0.5])
    out["profile bars: z min"] = float(D.loc[D.unk, "z"].min())
    out["z<=-2 bars by coin"] = low.groupby("coin").size()
    out["z<=-2 grid-cell days by coin"] = low.assign(cell=low.index // 7).groupby(["coin", "window", "cell"]).size().groupby("coin").size()
    return out
