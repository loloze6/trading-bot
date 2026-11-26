import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(df)
            vs = pd.Series(v)
            m30 = vs.rolling(30).mean()
            vr = np.log(m30 / m30.shift(30)).values
            cs = pd.Series(c)
            r60 = (cs / cs.shift(60) - 1).values
            r5p = (cs / cs.shift(5) - 1).values
            lr = np.log(cs).diff()
            sd30 = lr.rolling(30).std()
            agit = (sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True) > 0.5).values
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n, 5):
                rec = dict(coin=coin, w=w, i=i, yr=yr[i], f=f[i], vr=vr[i], r60=r60[i], r5p=r5p[i], ag=agit[i], dayk=f"{w}_{i}")
                for h in (1, 3, 5, 10, 20):
                    rec[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    d["day"] = d["w"] + "_" + d["i"].astype(str)
    mean5 = d.groupby("coin")["r5"].mean()
    d["ex5"] = -(d["r5"] - d["coin"].map(mean5))
    def tday(s, keys):
        x = pd.DataFrame({"x": s, "k": keys}).dropna()
        g = x.groupby("k")["x"].sum()
        n = len(x)
        if len(g) < 3: return np.nan
        return x["x"].mean() / (g.std(ddof=1) * np.sqrt(len(g)) / n)
    def summ(sub, col="ex5"):
        return pd.Series({"n": sub[col].notna().sum(), "mean": sub[col].mean(), "t": tday(sub[col], sub["day"])})
    cases = d[d["f"] < 0]
    out = {}
    out["all_cases"] = summ(cases)
    out["by_coin"] = cases.groupby("coin").apply(summ)
    out["by_window"] = cases.groupby("w").apply(summ)
    out["by_year"] = cases.groupby("yr").apply(summ)
    out["by_agit"] = cases.groupby("ag").apply(summ)
    cases = cases.copy()
    cases["fq"] = pd.qcut(cases["f"].abs(), 3, labels=["lo", "mid", "hi"])
    out["by_fstrength"] = cases.groupby("fq").apply(summ)
    hz = {}
    for h in (1, 3, 5, 10, 20):
        mh = d.groupby("coin")[f"r{h}"].mean()
        d[f"ex{h}"] = -(d[f"r{h}"] - d["coin"].map(mh))
        sub = d[d["f"] < 0]
        hz[h] = summ(sub, f"ex{h}")
    out["horizons_cases"] = pd.DataFrame(hz).T
    fall = d[d["r60"] < -0.10].copy()
    fall["vgrp"] = np.where(fall["vr"] < 0, "shrink", "grow")
    fall["sgrp"] = np.where(fall["r5p"] < 0, "slide", "bounce")
    out["falling_vol_x_slide"] = fall.groupby(["vgrp", "sgrp"]).apply(summ)
    fs = fall[fall["vr"] < 0].copy()
    fs["vq"] = pd.qcut(fs["vr"], 3, labels=["deep", "mid", "light"])
    out["falling_shrink_by_depth"] = fs.groupby("vq").apply(summ)
    out["falling_by_agit"] = fall.groupby(["ag", "vgrp"]).apply(summ)
    hz2 = {}
    for h in (1, 3, 5, 10, 20):
        hz2[h] = summ(fall[fall["vr"] < 0], f"ex{h}")
    out["horizons_fall_shrink"] = pd.DataFrame(hz2).T
    return out
