import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            dr = c.pct_change()
            sd = dr.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            sc = r7 / (sd * np.sqrt(7))
            r60 = c / c.shift(60) - 1
            fr = (c.shift(-5) / c - 1).values
            for i in np.arange(0, len(df) - 5, 5):
                rows.append(dict(coin=coin, w=w, day=str(df["timestamp"].iloc[i])[:10],
                                 regime=df["regime"].iloc[i], sc=sc.iloc[i], r60=r60.iloc[i],
                                 fc=df["forecast"].iloc[i], r=fr[i]))
    d = pd.DataFrame(rows).dropna(subset=["r"])
    d["drift"] = d.groupby("coin")["r"].transform("mean")
    d["u"] = d["r"] - d["drift"]
    d = d.dropna(subset=["sc"])
    d["calm"] = np.where(d["regime"] == "chop", "agit", "calm")
    d["side"] = np.where(d["sc"] < 0, "fall", "rise")
    d["cu"] = np.where(d["side"] == "fall", -d["u"], d["u"])
    d["trend"] = np.where(d["r60"] > 0.10, "rising", np.where(d["r60"] < -0.10, "falling", "choppy"))
    d.loc[d["r60"].isna(), "trend"] = "na"

    def tday(g, col="cu"):
        s = g.groupby("day")[col].sum()
        n = len(s)
        t = s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=len(g), days=n, mean=g[col].mean(), t=t))

    out = {}
    out["calm_by_trend_side"] = d[d.calm == "calm"].groupby(["trend", "side"]).apply(tday)
    out["agit_by_trend_side"] = d[d.calm == "agit"].groupby(["trend", "side"]).apply(tday)
    cf = d[(d.calm == "calm") & (d.side == "fall")]
    x = cf["sc"].abs(); y = cf["cu"]
    sl = np.polyfit(x, y, 1)
    out["calm_fall_slope_on_abs_sc"] = pd.Series(dict(slope=sl[0], intercept=sl[1], corr=np.corrcoef(x, y)[0, 1], n=len(x)))
    ca = d[d.calm == "calm"]
    sl2 = np.polyfit(ca["sc"].abs(), ca["cu"], 1)
    out["calm_both_sides_slope"] = pd.Series(dict(slope=sl2[0], corr=np.corrcoef(ca["sc"].abs(), ca["cu"])[0, 1], n=len(ca)))
    out["calm_both_sides"] = tday(ca)
    return out
