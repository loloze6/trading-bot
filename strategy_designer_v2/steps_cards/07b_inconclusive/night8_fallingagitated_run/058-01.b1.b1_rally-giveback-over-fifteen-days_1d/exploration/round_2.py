import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    HS = [5, 10, 15, 20, 30]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in HS:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rr.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std().values
            r3 = pd.Series(c).pct_change(3).values
            r60 = pd.Series(c).pct_change(60).values
            for i in range(0, len(c), 15):
                if not (f[i] < 0):
                    continue
                d = dict(coin=coin, win=w, year=ts.iloc[i].year, f=f[i],
                         s=r3[i] / sd30[i] if sd30[i] > 0 else np.nan, r3=r3[i], r60=r60[i])
                for H in HS:
                    if i + H < len(c):
                        d["x%d" % H] = c[i + H] / c[i] - 1 - drift[(coin, H)]
                        d["raw%d" % H] = c[i + H] / c[i] - 1
                rows.append(d)
    t = pd.DataFrame(rows)
    out = {}
    idx = ["n", "slope", "t", "short_mean", "t_mean"]

    def slope(sub, col="x15", xcol="f"):
        s = sub.dropna(subset=[col, xcol])
        if len(s) < 5:
            return pd.Series([len(s), np.nan, np.nan, np.nan, np.nan], index=idx)
        res = stats.linregress(s[xcol], s[col])
        m = s[col].mean()
        tm = m / (s[col].std() / np.sqrt(len(s)))
        return pd.Series([len(s), res.slope, res.slope / res.stderr, -m, -tm], index=idx)

    out["by horizon"] = pd.DataFrame({"H%d" % H: slope(t, "x%d" % H) for H in HS}).T
    out["by horizon raw (with drift)"] = pd.DataFrame({"H%d" % H: slope(t, "raw%d" % H) for H in HS}).T
    out["by coin x15"] = pd.DataFrame({c: slope(g) for c, g in t.groupby("coin")}).T
    out["by year x15"] = pd.DataFrame({y: slope(g) for y, g in t.groupby("year")}).T
    out["by window x15"] = pd.DataFrame({w: slope(g) for w, g in t.groupby("win")}).T
    t["q"] = pd.qcut(t["f"].rank(method="first"), 4, labels=["q1_largest", "q2", "q3", "q4_smallest"])
    g = t.groupby("q", observed=True)
    out["by forecast quartile, mean unusual short move (-x)"] = pd.DataFrame(
        {"n": g["x15"].count(), "f": g["f"].mean(), "s": g["s"].mean(),
         "-x5": -g["x5"].mean(), "-x10": -g["x10"].mean(), "-x15": -g["x15"].mean(),
         "-x20": -g["x20"].mean(), "-x30": -g["x30"].mean(),
         "t15": -g["x15"].mean() / (g["x15"].std() / np.sqrt(g["x15"].count()))})
    t["sq"] = pd.qcut(t["s"].rank(method="first"), 4, labels=["s1_small", "s2", "s3", "s4_large"])
    g = t.groupby("sq", observed=True)
    out["by scaled rise quartile"] = pd.DataFrame(
        {"n": g["x15"].count(), "s": g["s"].mean(), "-x5": -g["x5"].mean(),
         "-x15": -g["x15"].mean(), "-x30": -g["x30"].mean(),
         "t15": -g["x15"].mean() / (g["x15"].std() / np.sqrt(g["x15"].count()))})
    out["slope x15 on s"] = slope(t, "x15", "s")
    out["slope x15 on s, r3>0 only"] = slope(t[t["r3"] > 0], "x15", "s")
    out["share r3>0"] = float((t["r3"] > 0).mean())
    t["deep"] = np.where(t["r60"] < t["r60"].median(), "deeper_fall", "shallower_fall")
    out["by depth of 60d fall"] = pd.DataFrame({k: slope(g) for k, g in t.groupby("deep")}).T
    out["forecast desc"] = t["f"].describe()
    return out
