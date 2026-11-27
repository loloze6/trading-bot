import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3, 7, 14]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            r14 = c / c.shift(14) - 1
            z = r14 / (sd * np.sqrt(14))
            inprof = (df["regime"] == "unknown").values
            fc = df["forecast"].astype(float).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=day[i],
                                     ret=c.iloc[i + h] / c.iloc[i] - 1,
                                     z=z.iloc[i], prof=inprof[i], fc=fc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    d = d.dropna(subset=["z"])
    d["sgn"] = np.sign(d["z"])
    d["direx"] = d["ex"] * d["sgn"]
    out = {}

    def summ(g):
        x = g["direx"]
        return pd.Series({"n": len(x), "mean_direx": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    def slope(g):
        if len(g) < 10:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g["z"], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})

    p = d[d.prof]
    out["slope_ex_on_z_by_h_profile"] = p.groupby("h").apply(slope)
    out["slope_ex_on_z_by_h_all"] = d.groupby("h").apply(slope)
    p7 = p[p.h == 7].copy()
    p7["absq"] = pd.qcut(p7["z"].abs(), 4, labels=False)
    out["prof7_by_absz_quartile_side"] = p7.groupby(["absq", "sgn"]).apply(summ)
    out["prof7_by_side"] = p7.groupby("sgn").apply(summ)
    out["prof7_by_coin"] = p7.groupby("coin").apply(summ)
    out["prof7_by_window"] = p7.groupby("w").apply(summ)
    p7["yr"] = pd.to_datetime(p7["day"]).dt.year
    out["prof7_by_year"] = p7.groupby("yr").apply(summ)
    for h in [3, 14]:
        ph = p[p.h == h].copy()
        ph["absq"] = pd.qcut(ph["z"].abs(), 4, labels=False)
        out[f"prof{h}_by_absz_quartile"] = ph.groupby("absq").apply(summ)
    a7 = d[(d.h == 7) & (~d.prof)].copy()
    a7["absq"] = pd.qcut(a7["z"].abs(), 4, labels=False)
    out["outside_prof7_by_absz_quartile"] = a7.groupby("absq").apply(summ)
    return out
