import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []; hrs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r24 = cl / cl.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(1440, min_periods=200).mean()
            z = r24 / mabs
            ret1 = cl.pct_change()
            vol = ret1.rolling(480, min_periods=100).std()
            vr = vol / vol.rolling(2400, min_periods=480).mean()
            ts = pd.to_datetime(b["timestamp"])
            yr = ts.dt.year.iloc[len(b)//2]
            for h in (6, 12, 24, 48):
                idx = np.arange(0, len(b) - h, h)
                fr = (cl.shift(-h) / cl - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": c, "w": w, "yr": yr, "h": h,
                    "z": z.iloc[idx].values, "vr": vr.iloc[idx].values, "fr": fr.values}))
            hrs.append(pd.DataFrame({"coin": c, "yr": ts.dt.year, "hour": ts.dt.hour,
                                     "wd": ts.dt.weekday, "r": ret1}))
    g = pd.concat(rows).dropna(subset=["z", "fr", "vr"])
    g["mu"] = g.groupby(["coin", "h"])["fr"].transform("mean")
    g["ex"] = g["fr"] - g["mu"]
    g["fade"] = -np.sign(g["z"]) * g["ex"]
    def summ(x, col="fade"):
        v = x[col]
        return pd.Series({"n": len(v), "mean": v.mean(),
                          "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    hv = g[g.vr >= 1.25]
    hv = hv.assign(az=pd.cut(hv.z.abs(), [0, 0.5, 1, 1.6, 2.5, np.inf]))
    out["highvol fade by |z| and h"] = hv.groupby(["h", "az"], observed=True).apply(summ)
    g["vrb"] = pd.cut(g["vr"], [0, 0.8, 1.0, 1.25, 1.5, np.inf])
    big = g[g.z.abs() >= 1.6]
    out["fade |z|>=1.6 by vr and h"] = big.groupby(["h", "vrb"], observed=True).apply(summ)
    b24 = big[(big.h == 24) & (big.vr >= 1.25)]
    out["hv big h24 by coin"] = b24.groupby("coin").apply(summ)
    out["hv big h24 by year"] = b24.groupby("yr").apply(summ)
    # regression slope of fade on |z|*vr within h24, all bars
    g24 = g[(g.h == 24)].copy()
    g24["x"] = g24.z.abs() * g24.vr
    s = stats.linregress(g24["x"], g24["fade"])
    out["h24 fade ~ |z|*vr slope"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(g24)})
    s2 = stats.linregress(g24[g24.vr >= 1.0]["z"].abs(), g24[g24.vr >= 1.0]["fade"])
    out["h24 fade ~ |z| vr>=1 slope"] = pd.Series({"slope": s2.slope, "t": s2.slope / s2.stderr})
    H = pd.concat(hrs).dropna()
    H["late"] = H.hour.isin([21, 22])
    def hs(x):
        return pd.Series({"n": len(x), "bp": x.r.mean() * 1e4, "t": x.r.mean() / (x.r.std() / np.sqrt(len(x)))})
    out["hours 21-22 by year"] = H[H.late].groupby("yr").apply(hs)
    out["hours 21-22 by coin"] = H[H.late].groupby("coin").apply(hs)
    out["hours 21-22 by weekday"] = H[H.late].groupby("wd").apply(hs)
    return out
