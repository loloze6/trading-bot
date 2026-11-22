import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 18
    rows = []
    bars = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < H + 200:
                continue
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(r1)
            sd = s.rolling(180, min_periods=90).std().values
            r6 = pd.Series(c).pct_change(6).values
            z6 = r6 / (sd * np.sqrt(6))
            vol30 = s.rolling(30, min_periods=20).std()
            vr = (vol30 / vol30.rolling(180, min_periods=90).mean()).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, fwd=c[i + H] / c[i] - 1,
                                 z6=z6[i], vr=vr[i]))
            # next 4h bar return keyed by its start hour
            bars.append(pd.DataFrame(dict(coin=coin, w=w, year=ts.dt.year.values[:-1],
                                          hour=ts.dt.hour.values[:-1], wd=ts.dt.dayofweek.values[:-1],
                                          r=np.r_[c[1:] / c[:-1] - 1],
                                          oc=(b["close"] / b["open"] - 1).values[:-1])))
    g = pd.DataFrame(rows).dropna(subset=["z6", "fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["str_"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    def summ(df, key):
        o = df.groupby(key)["ex"].agg(["mean", "std", "count"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["strength"] = df.groupby(key)["str_"].mean()
        return o.drop(columns="std").round(5)
    out = {}
    g["az"] = g["z6"].abs()
    g["azq"] = pd.qcut(g["az"], 5, labels=False)
    g["side"] = np.sign(g["z6"]).astype(int)
    out["fwd3d by |1d z| quintile and side"] = summ(g, ["azq", "side"])
    lo = g[g["z6"] <= g["z6"].quantile(0.1)]
    out["1d-fall decile10: by coin"] = summ(lo, "coin")
    out["1d-fall decile10: by year"] = summ(lo, "year")
    lo = lo.dropna(subset=["vr"]).copy()
    lo["vrh"] = (lo["vr"] > lo["vr"].median()).astype(int)
    out["1d-fall decile10: by vol ratio half"] = summ(lo, "vrh")
    # graded: corr of -z6 with ex in down side
    dn = g[g["z6"] < 0]
    rho, p = stats.spearmanr(-dn["z6"], dn["ex"])
    out["down side spearman(-z6, ex), p"] = f"{rho:.4f}, {p:.4g}, n={len(dn)}"
    hi = g[g["z6"] >= g["z6"].quantile(0.9)]
    out["1d-rise decile10: by year"] = summ(hi, "year")
    bb = pd.concat(bars).dropna(subset=["r"])
    bb["ex"] = bb["r"] - bb.groupby("coin")["r"].transform("mean")
    bb["str_"] = bb["ex"] / bb.groupby("coin")["r"].transform("std")
    h = bb[bb["hour"].isin([16, 20])]
    out["hour16/20 by coin"] = summ(h, ["hour", "coin"])
    out["hour16/20 by year"] = summ(h, ["hour", "year"])
    f = bb[bb["wd"] == 4]
    out["Friday by year"] = summ(f, "year")
    out["Friday by hour"] = summ(f, "hour")
    return out
